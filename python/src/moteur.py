# Les 8 combinaisons gagnantes : 3 lignes, 3 colonnes, 2 diagonales
LIGNES_GAGNANTES = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]


def verifier_victoire(plateau: list[str], joueur: str) -> bool:
    return any(all(plateau[i] == joueur for i in c) for c in LIGNES_GAGNANTES)


class MoteurMorpion:
    def __init__(self) -> None:
        self.plateau: list[str] = [" "] * 9
        self.joueur_actuel: str = "X"
        self.gagnant: str | None = None

    def jouer_coup(self, pos: int) -> bool:
        """Valide et exécute un coup (0-8). Retourne True si réussi."""
        if 0 <= pos <= 8 and self.plateau[pos] == " " and not self.gagnant:
            self.plateau[pos] = self.joueur_actuel
            if verifier_victoire(self.plateau, self.joueur_actuel):
                self.gagnant = self.joueur_actuel
            else:
                self.joueur_actuel = "O" if self.joueur_actuel == "X" else "X"
            return True
        return False

    def reinitialiser(self) -> None:
        self.plateau = [" "] * 9
        self.joueur_actuel = "X"
        self.gagnant = None

    def formater_plateau(self) -> str:
        p = self.plateau
        return f" {p[0]} | {p[1]} | {p[2]} \n-----------\n {p[3]} | {p[4]} | {p[5]} \n-----------\n {p[6]} | {p[7]} | {p[8]} "
