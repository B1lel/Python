# e = 0

# a = float( input("Entrer la valeur de a:"))
# while a == 0 :
#     e = e + 1
#     print(e)
#     if e < 3 :
#         print('La valeur de "a" doit être différente de 0')
#         a = float(input('Entrer la valeur de "a":'))
#     elif e == 3 : 
#         print ('met pas 0 zebi')
#         a = float(input('Entre la valeur de "a" enculé: '))
#     else:
#         a = 1
#         print('"a" vaut 1 et va te faire')

# b = float( input("Entrer la valeur de b:"))
# c = float( input("Entrer la valeur de c:"))

# delta = b**2 -4*a*c
# if delta > 0: 
#     print("L'équation a deux solutions réelles distinctes.")
# elif delta == 0:
#     print("L'équation a une solution réelle double.")
# else:
#     print("L'équation n'a pas de solution réelle.")
# print("fin")


# i = 0
# tous_paires = True 

# while i < 5 :
#     n = int(input("Entrer un nombre:"))
#     tous_paires = tous_paires and n % 2 == 0
#     i = i + 1

# if tous_paires:
#    print("tous les entier sont paires")
# else:
#    print("un entier n'etait pas paire")



# n = int(input("Entrer la taille du carrée : "))
# num_lig = 0

# while num_lig < n :
#     num_col = 0 
#     while num_col < n :
#         print("*",end="")
#         num_col = num_col + 1
#     print()
#     num_lig = num_lig + 1

# import turtle

# def carre (longueur_cote):
#     i = 1 
#     while i <= 4 :
#         turtle.forward (longueur_cote)
#         turtle.right(90)
#         i = i + 1 

# def deplacer_sans_tracer (espacement):
#     turtle.penup()
#     turtle.forward(espacement)
#     turtle.pendown()

# def ligne_de_carre (nb_carre, longueur_cote, espacement):
#     i = 0 
#     while i < nb_carre :
#         valeur = longueur_cote*(0.9**i)
#         print(valeur) 
#         carre(valeur)
#         deplacer_sans_tracer(espacement)
#         i = i + 1 
        

# if __name__ == "__main__":
#     ligne_de_carre(4, 100, 150)

# def decalage(s):
#     # renvoie la chaîne s préfixée de n tirets
#     espaces = "-" * n
#     resultat = espaces + s
#     return resultat

# if __name__ == "__main__":
#     n = 5
#     test = decalage("toto")
#     print(test)
#     n = 10
#     test = decalage("maison")
#     print(test)


# def cherche(elem, l) :
#     if elem in l:
#         return True
#     else: 
#         return False

# trouver = cherche(2, Chiffre)
# print(trouver)

# trouver = cherche(85, Chiffre)
# print(trouver)

# Chiffre = [0, 1, 2, 3, 4, 6]
# print(Chiffre)
# Chiffre.insert(5,5)
# print(Chiffre)
# Chiffre.extend([7,8])
# print(Chiffre)

# Multiple3 = [3, 6, 9, 15, 21, 24, 27]
# print(Multiple3)

# Multiple3.insert(3, 12)
# Multiple3.insert(5,18)
# print(Multiple3)

# Multiple3.extend([30, 33])
# print(Multiple3)

# Multiple3.append(36)
# print(Multiple3)

Chiffre0 = [0, 1, 2, 3, 4, 6]
Chiffre1 = list(Chiffre0)
Chiffre1.append("bip")
print(Chiffre0)
print(Chiffre1)

