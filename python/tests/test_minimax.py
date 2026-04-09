import minimax


def test_victoire_immediate():
    # X | X |
    # O | O |
    #   |   |
    plateau = ["X", "X", " ", "O", "O", " ", " ", " ", " "]
    conseil = minimax.obtenir_meilleur_coup(plateau, "X")
    assert conseil.position == 2
    assert conseil.score > 0


def test_blocage_obligatoire():
    # X | X |      O doit jouer en 2 pour bloquer
    # O |   |
    #   |   |
    plateau = ["X", "X", " ", "O", " ", " ", " ", " ", " "]
    conseil = minimax.obtenir_meilleur_coup(plateau, "O")
    assert conseil.position == 2
    assert conseil.score < 0  # O ne peut pas gagner, au mieux perdre moins vite


def test_prefere_victoire_au_nul():
    # X | O | X
    # X | O |      X joue 5 (victoire) plutôt que 7 (nul)
    # O |   | X
    plateau = ["X", "O", "X", "X", "O", " ", "O", " ", "X"]
    conseil = minimax.obtenir_meilleur_coup(plateau, "X")
    assert conseil.position == 5
    assert conseil.score > 0


def test_plateau_vide_retourne_position_valide():
    plateau = [" "] * 9
    conseil = minimax.obtenir_meilleur_coup(plateau, "X")
    assert 0 <= conseil.position <= 8
    assert conseil.score == 0  # jeu parfait des deux côtés → nul


def test_explication_contient_toutes_les_positions_disponibles():
    plateau = ["X", "O", "X", "X", "O", " ", "O", " ", "X"]
    conseil = minimax.obtenir_meilleur_coup(plateau, "X")
    assert conseil.score > 0
    assert "5" in conseil.explication
    assert "7" in conseil.explication
    assert "optimal" in conseil.explication


def test_explication_mentionne_victoire_et_nul():
    plateau = ["X", "O", "X", "X", "O", " ", "O", " ", "X"]
    conseil = minimax.obtenir_meilleur_coup(plateau, "X")
    assert conseil.score > 0
    assert "victoire" in conseil.explication
    assert "nul" in conseil.explication
