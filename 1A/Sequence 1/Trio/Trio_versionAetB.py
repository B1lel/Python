import random

def creation_jeux(nombre_joueur):
        # Creation du Jeu
    Carte = [] # Jeu de carte à distribuer 
    Jeu_Centre = []
    Jeu = [[] for i in range(nombre_joueur) ] # Jeu des joueurs 


    for j in range (3) :
        for i in range(1,13) :
            Carte.append(i)

    random.shuffle(Carte)

    for x in range (nombre_joueur): # nbr Joueur
        for i in range(36//(nombre_joueur + 1)): # nbr de carte pour chaque joeur
            Jeu[x].append(Carte.pop(0))
    
    Jeu_Centre = list(Carte) # le reste des cartes c'est le centre
    Jeu.insert(0,Jeu_Centre)   
    return Jeu 


def creation_score(nombre_joueur): 
    return [0 for i in range(nombre_joueur)]
    
def premier_joueur(nombre_joueur):
    st = random.randint(1,nombre_joueur)
    print("C'est au joueur", st, "de commencé")
    return st

def un_tour(numero_joueur, nombre_joueur, Jeu, Score):
    
    # initialisation
    Carte_selected = []
    Carte_selected_valeur = []
    cartes_identique = True # aussi une initialisation
    
    print("C'est au tour de", numero_joueur)
    print("Voici votre main:", Jeu[numero_joueur])
    
    while cartes_identique :
        
        carte_choisi_result = carte_choisi(nombre_joueur, Jeu)
        Carte_selected.append(carte_choisi_result)
        
        Carte_selected_valeur = [triplet[0] for triplet in Carte_selected ]
        print("Carte pioché: ", Carte_selected_valeur)
        
        cartes_identique = check_trio(Carte_selected, numero_joueur, Score)
    
    redistribution(Carte_selected, Jeu)
    print("Fin du tour")
    print("Le score est: ",Score)
    return check_victoire(numero_joueur, Score)

def carte_choisi(nombre_joueur, Jeu):
    
    stop = False
    while not stop  : 

        numero_jeu_choisi = input(f"Choissisez un jeu à reveler (1 à {nombre_joueur}), ou 'centre' : ")
            
        if numero_jeu_choisi == "centre" : # on regarde si on a pris le centre 
            numero_jeu_choisi = 0
            stop = True

        if not numero_jeu_choisi.isdigit():
            print(f"Veuillez entrez une valeur valide (1 à {nombre_joueur}) ")
            continue

        numero_jeu_choisi = int(numero_jeu_choisi)
        if numero_jeu_choisi < 1 or numero_jeu_choisi > nombre_joueur :
            print(f"Veuillez entrez une valeur valide (1 à {nombre_joueur}) ")
            continue

        else : 
            stop = True




    carte_choisi = choix_carte(numero_jeu_choisi, Jeu) # {"valeur carte", "index jeu ", "index carte dans jeu"}
    
    return carte_choisi

def choix_carte(numero_jeu_choisi, Jeu):  
    if numero_jeu_choisi == 0 :
        return choix_carte_centre(Jeu)
    else:
        return choix_carte_joueur(numero_jeu_choisi, Jeu)

def choix_carte_centre(Jeu) :

    Centre = Jeu.pop(0)

    while True :
            stop = False
            while not stop :
                
                index_max = len(Jeu[1])
                index_carte = input("Entrez la position de la carte que vous souhaitez révéler :"  )
                
                if not index_carte.isdigit  :
                    print(f"Veuillez entrez une valeur valide (1 à {index_max}) ")
                    continue
              
                if index_carte < 1 or index_carte > index_max :
                    print(f"Veuillez entrez une valeur valide (1 à {index_max}) ")
                    continue
                
                else : 
                    stop = True
                    

            if Centre[index_carte] == None :
                print("Cette carte à déjà était tirée")

            else:
                carte_choisi = Centre.pop(index_carte)
                Centre.insert(index_carte,None)
                Jeu.insert(0,Centre)
                
                return carte_choisi, 0, index_carte

def choix_carte_joueur(numero_jeu_choisi, Jeu) :
 
    # on extrait le jeu choisi
    jeu_choisi = Jeu.pop(numero_jeu_choisi)
    
    # on attribut les max / min
    max_carte, min_carte = max(jeu_choisi), min(jeu_choisi)

    stop = False
    while not stop  :
        choix = input("Quelle Carte voulez vous revelez ? (max/min)")
        if choix != "min" and choix != "max" :
            print('Réponse invalide, entrez "max" ou "min"')
        else :
            stop = True
    
    if choix == "max":
        carte_choisi = max_carte    
        index_carte = jeu_choisi.index(max_carte)
        jeu_choisi.remove(max_carte)
        Jeu.insert(numero_jeu_choisi,jeu_choisi)
        
        return carte_choisi, numero_jeu_choisi, index_carte
    
    else :
        carte_choisi = min_carte
        index_carte = jeu_choisi.index(min_carte)
        jeu_choisi.remove(min_carte)
        Jeu.insert(numero_jeu_choisi,jeu_choisi)

        return carte_choisi, numero_jeu_choisi, index_carte

def redistribution(Carte_selected, Jeu_selected, Jeu):
    
    if len(Carte_selected) >= 2 and not check_identique(Carte_selected): # quand c'est pas un trio 

        while len(Carte_selected) != 0:

            if Carte_selected[0][1] == 0 : # si carte du centre
                
                jeu_a_remplir = Jeu.pop(0)                
                jeu_a_remplir.pop(Carte_selected[0][2])
                jeu_a_remplir.insert(Carte_selected[0][2],Carte_selected[0][0])
                
                Jeu.insert(Carte_selected[0][1], jeu_a_remplir)
                Carte_selected.pop(0)
           
            else:

                jeu_a_remplir = Jeu.pop(Carte_selected[0][1])
                jeu_a_remplir.insert(Carte_selected[0][2],Carte_selected[0][0])
                Jeu.insert(Carte_selected[0][1], jeu_a_remplir)
                Carte_selected.pop(0)
                          
    else : # quand c'est un trio 

        Carte_selected = []

def ajout_point(numero_joueur, type_trio, Score):

    print("score:" , Score)

    if type_trio == 7 :

        Score[numero_joueur - 1] = 3

    else :

        Score[numero_joueur - 1] += 1

def check_victoire(numero_joueur, Score) :

    if Score[numero_joueur - 1] == 3 :

        print("Le Joueur", numero_joueur, "a gagné !!")

        return True
    
    else :
        return False

def check_trio(Carte_selected, numero_joueur, Score ) :

    if len(Carte_selected) == 2 :
         
         cartes_identique = check_identique(Carte_selected)

         return cartes_identique
    
    elif len(Carte_selected) == 3 :

        cartes_identique = check_identique(Carte_selected)
        
        if cartes_identique :
                
                ajout_point(numero_joueur, Carte_selected[0][0], Score)
                print("Vous avez un trio de", Carte_selected[0][0])
                cartes_identique = False

                return cartes_identique  # permet d'arreter la bloucle du tour 
        else :

            cartes_identique = False

            return cartes_identique
    
    else:

        cartes_identique = True

        return cartes_identique

def check_identique(Carte_selected):

    Carte_valeur = [triplet[0] for triplet in Carte_selected]
    Set_Carte_valeur = set(Carte_valeur)

    if len(Set_Carte_valeur) == 1:

        print("la carte choisi est identique")
        return True
    
    else :

        print("la carte choisi est differente")
        return False
    
def imprimer(Jeu):
    for indice_jeu, jeu in enumerate(Jeu):
        print("Jeux",indice_jeu, jeu)

def compteur(numero_joueur, nombre_joueur):
    max_joueur = nombre_joueur
    i = numero_joueur
    if i == max_joueur :
        i = 1
    else :
        i = i + 1
    return(i)

def main():
    stop = False
    while not stop :
            nombre_joueur = input("Quel est le nombre de joueurs ? ")
            
            if not nombre_joueur.isdigit():
                print("Veuillez entrez une valeur valide (3 à 6) ")
                continue
            
            nombre_joueur = int(nombre_joueur)
            
            if  nombre_joueur < 3 or nombre_joueur > 6 :
                print("Veuillez entrez une valeur valide (3 à 6) ")
                continue
            else:
                stop = True

    Score = creation_score(nombre_joueur)
    Jeu = creation_jeux(nombre_joueur)

    print("Les cartes ont été distribuées")

    victoire = False
    premier_tour = True

    while not victoire:
        imprimer(Jeu)
        if premier_tour:
            numero_joueur = premier_joueur(nombre_joueur)
            victoire = un_tour(numero_joueur, nombre_joueur, Jeu, Score)
            premier_tour = False
        else:
            numero_joueur = compteur(numero_joueur, nombre_joueur)
            victoire = un_tour(numero_joueur, nombre_joueur, Jeu, Score)

if __name__ == "__main__":
    main()
    



