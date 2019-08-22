liste_arme = ["épée", "fusil", "baton", "knif", "lame", "styleto", "canon", "pistolet", "revolver", "fusil-a-pompe"]
inventaire = ["épée", "bananas"]
equiper = 0
dommage = 10
key = input("?>")
if key == "attaquer":
    if (inventaire[equiper] in liste_arme):
        print("Vous frapper avec", inventaire[equiper]+",", dommage, "point de dommage.")
    else:
        print("Vous n'est pas armé!")
