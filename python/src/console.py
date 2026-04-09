import sys

import minimax
import moteur


def lancer_partie():
    jeu = moteur.MoteurMorpion()
    print("--- Morpion : Humain vs Minimax ---")

    while not jeu.gagnant and " " in jeu.plateau:
        print("\n" + jeu.formater_plateau())
        if jeu.joueur_actuel == "O":
            conseil = minimax.obtenir_meilleur_coup(jeu.plateau, "O", True)
            jeu.jouer_coup(conseil.position)
            print(f"Minimax a choisi la position {conseil.position}")
        else:
            try:
                saisie = input(
                    f"Joueur {jeu.joueur_actuel} (0-8) ou 'q' pour quitter : "
                )
                if saisie.lower() == "q":
                    sys.exit()
                pos = int(saisie)
                if not jeu.jouer_coup(pos):
                    print("Coup invalide.")
            except ValueError:
                print("Veuillez entrer un chiffre entre 0 et 8.")

    print("\n" + jeu.formater_plateau())
    if jeu.gagnant == "X":
        print("Félicitations, vous avez battu Minimax !")
    elif jeu.gagnant == "O":
        print("Minimax a gagné !")
    else:
        print("Match nul !")


if __name__ == "__main__":
    lancer_partie()
