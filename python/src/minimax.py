import dataclasses

import moteur


@dataclasses.dataclass
class NoeudMinimax:
    plateau: list[str]
    position_jouee: int | None  # None = racine
    score: int
    est_max: bool  # True = c'est au joueur maximisant de jouer depuis ce noeud
    enfants: list["NoeudMinimax"] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class ConseilMinimax:
    position: int
    score: int
    explication: str
    arbre: NoeudMinimax


def obtenir_meilleur_coup(plateau: list[str], joueur: str) -> ConseilMinimax:
    racine = construire_arbre(plateau, joueur)
    meilleur_enfant = max(racine.enfants, key=lambda n: n.score)

    lignes = ["Positions analysées :"]
    for enfant in sorted(racine.enfants, key=lambda n: -n.score):
        label = "victoire" if enfant.score > 0 else ("nul" if enfant.score == 0 else "défaite")
        marqueur = " ← optimal" if enfant is meilleur_enfant else ""
        assert enfant.position_jouee is not None
        lignes.append(f"  {enfant.position_jouee} → {label}{marqueur}")

    return ConseilMinimax(
        position=meilleur_enfant.position_jouee,  # type: ignore[arg-type]
        score=meilleur_enfant.score,
        explication="\n".join(lignes),
        arbre=racine,
    )


def construire_arbre(plateau: list[str], joueur: str) -> NoeudMinimax:
    racine = NoeudMinimax(plateau=plateau[:], position_jouee=None, score=0, est_max=True)
    racine.score = _construire_sous_arbre(racine, plateau[:], True, joueur)
    return racine


def _construire_sous_arbre(
    noeud: NoeudMinimax,
    p: list[str],
    est_max: bool,
    joueur: str,
) -> int:
    adv = "O" if joueur == "X" else "X"
    if moteur.verifier_victoire(p, joueur):
        return 1
    if moteur.verifier_victoire(p, adv):
        return -1
    if " " not in p:
        return 0

    joueur_courant = joueur if est_max else adv
    scores = []
    for i in range(9):
        if p[i] == " ":
            p[i] = joueur_courant
            enfant = NoeudMinimax(plateau=p[:], position_jouee=i, score=0, est_max=not est_max)
            noeud.enfants.append(enfant)
            score = _construire_sous_arbre(enfant, p[:], not est_max, joueur)
            enfant.score = score
            scores.append(score)
            p[i] = " "
    return max(scores) if est_max else min(scores)
