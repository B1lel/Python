# ##- Exercices : instruction If ... else
# a = int(input("Entier a= ?"))
# b = int(input ("Entier b= ?"))

# s = a + b 

# if s >= 100 :
#     print("La somme depasse 100")
# else :
#     print("La somme vaut", s)

# #### - Exercices : boucle whilePage
# Moi
# arreter = False
# x = "non"

# while arreter == False :
#     n = int(input("Choissisez un nombre"))
#     carre_n = n**2
#     print("Le carré de", n, "est", carre_n)
    
#     x = input("Voulez vous choisir un autre nombre ? (oui/non)")
#     if x == "oui" :
#         arreter = False
#     else:
#         arreter = True

# Apres Chat GPT
# boucle = True
# reponse = "non"

# while boucle  :
#     n = int(input("Choissisez un nombre"))
#     carre_n = n**2
#     print("Le carré de", n, "est", carre_n)
    
#    reponse  = input("Voulez vous choisir un autre nombre ? (oui/non)")
#     if reponse != "oui":
#         boucle = False

# print("Fin")
# Exercie A
# import math
# def perimetre_cercle(rayon):
#     pi = 3.1416
#     p = 2*math.pi*rayon
#     return p 

# print(perimetre_cercle(1))

# # Exercice B
# def aire_triangle(cote1, cote2, cote3):   
#     s = (cote1 + cote2 + cote3)/2
#     a = math.sqrt(s*(s-cote1)*(s-cote2)*(s-cote2))
#     return a

# print(aire_triangle(1,3,3))

# # Excercice C
# g = 9.81
# def chuteLibre_v1(hauteur):
#     T1 = math.sqrt(2*hauteur/g)
#     return T1
# print(chuteLibre_v1(50))

# def chuteLibre_v2(hauteur) :
#     T2 = math.sqrt(2*hauteur/g)
#     print("Le temps mis à l'objet pour tomber de", hauteur, "est de", round(T2,1), "secondes")
# chuteLibre_v2(50)

# # Exercice D
# import random

# def doubleDe():
#     x = random.randint(1,6)
#     y = random.randint(1,6)
#     s = x + y
#     print(s)

# for i in range(10):
#     doubleDe()


def compteur(st):
    i = st
    if i == 3 :
        i = 1
    else :
        i = i + 1
    return(i)     
st = 2
while True:
    st = compteur(st)
    print(st)





