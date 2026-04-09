import argparse
import functools
import sys

import mcp.server.fastmcp as fastmcp
import pydantic.networks as networks
import structlog

import moteur
import minimax

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
)
log = structlog.get_logger()


def mcp_logger(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            result_str = str(result)
            log.info(
                "mcp_call",
                operation=func.__name__,
                result=result_str[:300] + "..." if len(result_str) > 300 else result,
            )
            return result
        except Exception as e:
            log.error(
                "mcp_call_failed", operation=func.__name__, error=str(e), exc_info=True
            )
            raise e

    return wrapper


server = fastmcp.FastMCP("Morpion-MCP")
jeu = moteur.MoteurMorpion()


@server.resource("game://plateau")
@mcp_logger
async def voir_plateau() -> str:
    """Affiche l'état actuel du jeu pour l'IA."""
    return f"Tour du joueur : {jeu.joueur_actuel}\n{jeu.formater_plateau()}"


@server.resource("game://plateau-nonce/{nonce}")
@mcp_logger
async def voir_plateau_nonce(_nonce: str) -> str:
    """Affiche l'état actuel du jeu pour l'IA."""
    return f"Tour du joueur : {jeu.joueur_actuel}\n{jeu.formater_plateau()}"


@server.tool()
@mcp_logger
async def jouer_position(pos: int, ctx: fastmcp.Context) -> str:
    """Permet à l'IA de placer son symbole sur le plateau (0-8)."""
    j = jeu.joueur_actuel
    await ctx.info(f"Le joueur {j} joue en position {pos}")

    if jeu.jouer_coup(pos):
        await ctx.session.send_resource_updated(networks.AnyUrl("game://plateau"))
        if jeu.gagnant:
            await ctx.info(f"Le joueur {j} a gagné la partie !")
            return f"Le joueur {j} a gagné la partie !"
        return f"Coup accepté. C'est maintenant au tour de {jeu.joueur_actuel}."
    await ctx.error(
        f"Coup rejeté pour joueur {j} en position {pos}: case occupée ou index invalide."
    )
    return f"Coup rejeté pour joueur {j} en position {pos}: case occupée ou index invalide."


@server.tool()
@mcp_logger
async def conseil_minimax() -> str:
    """Demande à l'algorithme Minimax le coup mathématiquement parfait."""
    conseil = minimax.obtenir_meilleur_coup(jeu.plateau, jeu.joueur_actuel)
    return f"Position suggérée : {conseil.position}\n\n{conseil.explication}"


@server.tool()
@mcp_logger
async def recommencer_partie(ctx: fastmcp.Context) -> str:
    """Réinitialise le plateau pour une nouvelle partie."""
    jeu.reinitialiser()
    j = jeu.joueur_actuel
    await ctx.info(f"Le joueur {j} a décidé de recommencer la partie")
    await ctx.session.send_resource_updated(networks.AnyUrl("game://plateau"))

    return "La partie a été réinitialisée. X commence."


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sse", action="store_true", help="Use SSE transport instead of stdio"
    )
    args = parser.parse_args()

    transport = "sse" if args.sse else "stdio"
    log.info("Starting mcp server", transport=transport)
    server.run(transport=transport)  # type: ignore[arg-type]
