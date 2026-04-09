import flask

import minimax
import moteur

app = flask.Flask(__name__)
jeu = moteur.MoteurMorpion()
dernier_arbre: minimax.NoeudMinimax | None = None
avec_profondeur = False


def bfs_niveaux(racine: minimax.NoeudMinimax) -> list[list[minimax.NoeudMinimax]]:
    niveaux = []
    courant = [racine]
    while courant:
        niveaux.append(courant)
        courant = [enfant for noeud in courant for enfant in noeud.enfants]
    return niveaux


@app.get("/")
def index() -> str:
    niveaux = bfs_niveaux(dernier_arbre) if dernier_arbre else []
    return flask.render_template(
        "index.html",
        jeu=jeu,
        arbre=dernier_arbre,
        arbre_niveaux=niveaux,
        avec_profondeur=avec_profondeur,
    )


@app.post("/jouer/<int:pos>")
def jouer(pos: int) -> flask.Response:
    global dernier_arbre
    if jeu.jouer_coup(pos) and not jeu.gagnant and " " in jeu.plateau:
        conseil = minimax.obtenir_meilleur_coup(jeu.plateau, "O", avec_profondeur)
        dernier_arbre = conseil.arbre
        jeu.jouer_coup(conseil.position)
    return flask.redirect("/")


@app.post("/recommencer")
def recommencer() -> flask.Response:
    global dernier_arbre, avec_profondeur
    jeu.reinitialiser()
    dernier_arbre = None
    avec_profondeur = flask.request.form.get("avec_profondeur") == "1"
    return flask.redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
