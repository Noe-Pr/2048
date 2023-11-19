# Importation des bibliothèques nécessaires
import pygame
import random

# Initialisation de Pygame
pygame.init()

# Fonction principale du jeu
def principal():
    pygame.display.set_caption("Jeu 2048")  # Titre
    icone = pygame.image.load("2048_logo.png")  # Icône
    pygame.display.set_icon(icone)  # Définition de l'icône de la fenêtre

    écran = pygame.display.set_mode((size * (taille_case + marge) + 3 * marge,
                                     size * (taille_case + marge) + 8 * marge))  # Création de la fenêtre du jeu

    grille = initialiser_grille()
    score = 0
    fin_de_partie = False

    horloge = pygame.time.Clock()  # Horloge pour limiter le nombre d'images par seconde

    while True:
        for événement in pygame.event.get():
            if événement.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif événement.type == pygame.KEYDOWN:
                if not fin_de_partie:
                    if événement.key == pygame.K_LEFT:
                        delta_score = fusionner_gauche(grille)
                        ajouter_nouvelle_case(grille)
                        score += delta_score
                    elif événement.key == pygame.K_RIGHT:
                        delta_score = déplacer_droite(grille)
                        ajouter_nouvelle_case(grille)
                        score += delta_score
                    elif événement.key == pygame.K_UP:
                        delta_score = déplacer_haut(grille)
                        ajouter_nouvelle_case(grille)
                        score += delta_score
                    elif événement.key == pygame.K_DOWN:
                        delta_score = déplacer_bas(grille)
                        ajouter_nouvelle_case(grille)
                        score += delta_score
                if est_fin_de_partie(grille):
                    fin_de_partie = True
            elif événement.type == pygame.MOUSEBUTTONDOWN and fin_de_partie:
                souris_x, souris_y = événement.pos
                bouton_recommencer = pygame.Rect(size * (taille_case + marge) // 1.6 - 122,
                                                 size * (taille_case + marge) // 1.6 + 20, 157, 40)
                if bouton_recommencer.collidepoint(souris_x, souris_y):
                    grille = initialiser_grille()
                    score = 0
                    fin_de_partie = False
                    pygame.event.get()  # Vider la file d'attente des événements

        dessiner_grille(écran, grille, score, fin_de_partie)
        pygame.display.flip()
        horloge.tick(10)  # Limite le nombre d'images par seconde


# Configuration de la boite du jeu
size = 4  # Taille de la boite (4x4)
taille_case = 106
marge = 15
gris_semifoncé = (238, 228, 218, 125)

# Couleurs des cases
bg_color = (250, 248, 239, 255) 
couleurs_cases = {
    2: (238, 228, 218, 255),
    4: (237, 224, 200, 255),
    8: (242, 177, 121, 255),
    16: (245, 149, 99, 255),
    32: (246, 124, 95, 255),
    64: (246, 94, 59, 255),
    128: (237, 207, 114, 255),
    256: (237, 204, 97, 255),
    512: (237, 200, 80, 255),
    1024: (237, 197, 63, 255),
    2048: (237, 194, 46, 255)
}

# Fonction pour initialiser la grille du jeu
def initialiser_grille():
    grille = [[0] * size for _ in range(size)]  # Création de la grille vide
    ajouter_nouvelle_case(grille)
    ajouter_nouvelle_case(grille)
    return grille

# Ajouter une nouvelle case, 2 ou 4, aléatoirement
def ajouter_nouvelle_case(grille):
    # Création d'une liste représentant les coordonnées des blocs vides
    cellules_vides = [(i, j) for i in range(size) for j in range(size) if grille[i][j] == 0]
    if cellules_vides:
        i, j = random.choice(cellules_vides)
        grille[i][j] = 2 if random.random() < 0.9 else 4


def dessiner_grille(écran, grille, score, fin_de_partie):
    # Remplissage avec la couleur de fond
    écran.fill((250, 248, 239, 255))

    # Boîte de jeu avec des bords arrondis
    boite_left = marge
    boite_top = marge * 2 + 55
    boite_width = marge + size * (taille_case + marge)
    boite_height = marge + size * (taille_case + marge)
    pygame.draw.rect(écran, (187, 173, 160, 255), (boite_left, boite_top, boite_width, boite_height), border_radius = 4)
    
    # Parcours de la grille pour dessiner chaque case
    for i in range(size):
        for j in range(size):
            # Couleur du texte de la case
            valeur_case = grille[i][j]
            if valeur_case in [2, 4]:
                couleur_chiffre = (119, 110, 101, 255)
            else:
                couleur_chiffre = (255, 255, 255)

            couleur_case = couleurs_cases.get(valeur_case, (205, 193, 180, 255))

            # Calcul des coordonnées des cases
            rect_x = j * (taille_case + marge) + marge * 2
            rect_y = i * (taille_case + marge) + marge * 3 + 55
            rect_width = taille_case
            rect_height = taille_case
            # Case avec les bords arrondis
            pygame.draw.rect(écran, couleur_case, (rect_x, rect_y, rect_width, rect_height), border_radius = 3)

            # Si la case n'est pas vide, valeur au centre de la case
            if valeur_case != 0:
                # Police plus grande pour les chiffres
                fonte_case = pygame.font.Font(None, 80)
                # Choix de la couleur pour le chiffre
                texte_case = fonte_case.render(str(valeur_case), True, couleur_chiffre)
                # Calcul de la position du texte pour le centrer dans le rectangle
                rect_texte = texte_case.get_rect(center=(rect_x + rect_width // 2, rect_y + rect_height // 2))
                écran.blit(texte_case, rect_texte)

    # Boîte grise pour le score avec des bords arrondis
    score_box_left = marge + 409
    score_box_top = marge  # ajustez la valeur en conséquence pour le positionnement vertical
    score_box_width = 90
    score_box_height = 55
    pygame.draw.rect(écran, (187, 173, 160, 255), (score_box_left, score_box_top, score_box_width, score_box_height), border_radius = 3)

    # Score
    fonte_score_label = pygame.font.Font(None, 21)
    texte_score_label = fonte_score_label.render("SCORE", True, (236, 224, 210, 255))
    fonte_score = pygame.font.Font(None, 40)
    texte_score = fonte_score.render(str(score), True, (255, 255, 255))
    # Ajustez la position du texte_score_label dans la boîte grise
    rect_texte_score = texte_score.get_rect() # Obtenir la surface rectangulaire du texte_score
    # Ajustez la position des scores dans la boîte grise
    rect_texte_score_label = texte_score_label.get_rect()
    écran.blit(texte_score_label, (score_box_left + (score_box_width - rect_texte_score_label.width) // 2, score_box_top + 10))
    écran.blit(texte_score, (score_box_left + (score_box_width - rect_texte_score.width) // 2, score_box_top + 27))
    
    # Game Over
    if fin_de_partie:
        # Dessiner un rectangle semi-transparent sur toute la surface
        overlay = pygame.Surface((écran.get_width(), écran.get_height()), pygame.SRCALPHA)
        pygame.draw.rect(overlay, gris_semifoncé, (0, 0, écran.get_width(), écran.get_height()))
        écran.blit(overlay, (0, 0))
        
        # Texte "Jeu terminé !"
        fonte_fin_de_partie = pygame.font.Font(None, 90)
        texte_fin_de_partie = fonte_fin_de_partie.render("Jeu terminé !", True, (119, 110, 101, 255))
        écran.blit(texte_fin_de_partie, (size * (taille_case + marge) // 3 - 85, size * (taille_case + marge) // 1.7 - 30)) # Position en hauteur puis en largeur
    
        # Bouton "Recommencer"
        fonte_recommencer = pygame.font.Font(None, 25)
        bouton_recommencer = pygame.Rect(size * (taille_case + marge) // 1.6 - 122, size * (taille_case + marge) // 1.6 + 20, 157, 40)
        pygame.draw.rect(écran, (119, 110, 101, 255), bouton_recommencer, border_radius=3)
        texte_recommencer = fonte_recommencer.render("Recommencer", True, (255, 255, 255))
        écran.blit(texte_recommencer, texte_recommencer.get_rect(center=bouton_recommencer.center))


    # Rafraîchissement de l'affichage
    pygame.display.flip()

# Fusionner les cases d'une ligne vers la gauche
def fusionner_gauche(grille):
    delta_score = 0
    for i in range(size):
        ligne = grille[i]
        ligne_fusionnee, delta_ligne = fusionner(ligne)
        grille[i] = ligne_fusionnee
        delta_score += delta_ligne
    return delta_score

# Fusionner les cases d'une ligne vers la droite
def déplacer_droite(grille):
    delta_score = 0
    for i in range(size):
        ligne = grille[i][::-1]
        ligne_fusionnee, delta_ligne = fusionner(ligne)
        grille[i] = ligne_fusionnee[::-1]
        delta_score += delta_ligne
    return delta_score

# Fusionner les cases d'une colonne vers le haut
def déplacer_haut(grille):
    delta_score = 0
    for j in range(size):
        colonne = [grille[i][j] for i in range(size)]
        colonne_fusionnee, delta_colonne = fusionner(colonne)
        for i in range(size):
            grille[i][j] = colonne_fusionnee[i]
        delta_score += delta_colonne
    return delta_score

# Fusionner les cases d'une colonne vers le bas
def déplacer_bas(grille):
    delta_score = 0
    for j in range(size):
        colonne = [grille[i][j] for i in range(size)][::-1]
        colonne_fusionnee, delta_colonne = fusionner(colonne)
        for i in range(size):
            grille[i][j] = colonne_fusionnee[::-1][i]
        delta_score += delta_colonne
    return delta_score

# Vérifier si la partie est terminée
def est_fin_de_partie(grille):
    for i in range(size):
        for j in range(size):
            if grille[i][j] == 0:
                return False
            if i < size - 1 and grille[i][j] == grille[i + 1][j]:
                return False
            if j < size - 1 and grille[i][j] == grille[i][j + 1]:
                return False
    return True

# Fusion des cases d'une ligne ou d'une colonne
def fusionner(ligne_ou_colonne):
    ligne_fusionnée = [0] * size
    index = 0
    delta_score = 0
    for valeur in ligne_ou_colonne:
        if valeur != 0:
            if ligne_fusionnée[index] == 0:
                ligne_fusionnée[index] = valeur
            elif ligne_fusionnée[index] == valeur:
                ligne_fusionnée[index] *= 2
                delta_score += ligne_fusionnée[index]
                index += 1
            else:
                index += 1
                ligne_fusionnée[index] = valeur
    return ligne_fusionnée, delta_score

if __name__ == "__main__":
    principal()