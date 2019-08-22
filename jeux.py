#Il y a une fonction de chargement nouveau scénario automatique 'map.txt' 
#Vous avez acces au mode edition interactife, jouer et créer en même temps.
#Tout les objets son classer dans une fichier externe au jeux: [Ennemi, Arme, Soin]

#La map 3d fait 5x5x3 avec des listes Objet, Description, Lieux, etc.
#Déplacé les objets attend que vous le voulez la description suivra.
#Vous avez un pouvoir de vision, se sont vos actions sur la ligne du temps.
#Vous pouvez maintenant voyager partout dans le temps sans problème.
#Vous pouvez même vous croisez a de multiple reprise dans space temps.
#Vous pouvez également volé des objets a vos homologs et les dupliquer.
#L'espace limite est supprimé de la simulation et refermer sur elle-même.
#LE MONDE A L'ENVER: temps recule au ralentie, texte inversé, map transposer

#Il y a un max item variable début 10. Vous ne pouvez pas prendre tout.
#Si l'objet commence par une lettre Majuscule elle est Surdimensionnée.
#Par contre les objets Maj sont toujours accessibles pour regarder.
#Les séquences de Quête sont fonctionnelles avec drop Objet en List/Lieux.
#Vous devez éditer par liste Lieux zyx [Lieux, act1, act2...n, objet 'x'].
#Ne pas oublier faire pareille dans liste DespL['Descrip', '',''...n, '?']
#J'ai dus ajouté la possibilité de chercher un mot de direction dans Objet
#Pour contourné le problème des portes et monte-charge non accéssible clé
#Créer une soluce linéaire pour terminé la quête.

#Il rest surement des bugs non découvert.
#Les sauvegarde peuvent crasher si la partie dure trop longtemps.

#Bugs
#1)'tout prendre' avec pile objet dupliqué
#2)'tout jeté','tout prendre' 2x
#3) Pourquoi un seul objet par destination sur la ligne nord?

import copy
import os
import os.path
from pathlib import Path
import glob
from datetime import datetime
from time import localtime
import random
import re
import json
from math import *

sourcefile = "jeu-save.txt"
#Rep = 'E:/PERSONNEL/python_2/python/histoires/AventureText/'
Rep = str(os.path.dirname(os.path.realpath(__file__)))
Rep = Rep + "/"
dash = str(Rep[2])
Rep = Rep.replace(dash,"/")
#print(Rep)
repertoir = os.listdir(Rep)

soin = 0
game = 1
key = ""
x = 2
y = 2
z = 1
temps = 1
speed = 1
score = 0
move = 0
inventaire = ["nécronomicon", "dés"]
DespI = []
DespI.append("Vous ouvrez le livre a n'importe quel page. UN PLAN DES SOUS-TERRAINS SE DESSINE AVEC DU SANG... C'EST ÉCRIT EN HIEROGLYPHES SIRRIAQUE DES COLLINES DU L'EST...'II,x,III,_,x';'x,_,I,x,II';'II,III,x,_,x';'^,_,x,II,II';'x,_,III,x,II'")
DespI.append("Un petit dés en bois a six face.")
roll = 6
timeline = []
spaceline = []
log = []
ok = 0
maxitem = 10
upsidedown = 0
mem = upsidedown
HP = 100
liste_soin = ['bouteille-eau', 'eau', 'bouteille-vin', 'vin', 'jus', 'contenant-jus', 'bouteille-alcool', 'alcool', 'sandwich', 'conserve', 'fruit', 'fruit-sec', 'pain', 'pain-sec', 'viande', 'viande-sec', 'viande-en-boite', 'ration', 'salade', 'restant', 'légume', 'légume-sec', 'chocolat', 'cannette', 'pop-corn', 'boisson-gazeuse', 'bonbons', 'potion', 'elixir', 'soin', 'premier-soin', 'trousse-médical', 'life-spray', 'médicament', 'médecine', 'anti-biotique', 'pilule', 'résurrection', 'nourriture']
liste_arme = ["robot-combat", "limié", "jare-abeille", "venin", "dare-empoisoné", "fronde", "dare", "ache-de-jet", "ache", "rateau", "pèle", "arme-improvisé", "explosif-improvisé", "bombe-improvisé", "corde", "oreiller", "soulier-de-fer", "chapeau-jet", "ligne-électrique", "cable-à-booster", "défibrilateur", "électro-chock", "verre", "tesson-bouteille", "chaine", "bouteille-cassé", "esscence", "explosif", "pétard", "crow-bare", "pied-de-biche", "clé-anglaise", "démonte-pneu", "bare-à-clou", "bare", "débrousailleur", "feux-artifice", "tnt", "sciseau", "poison", "acide", "matraque", "gourdin", "planche-clouter",".50", "tazer", "couteau", "arme", "sword", "épée", "fusil", "baton", "knif", "lame", "styleto", "canon", "pistolet", "revolver", "fusil-a-pompe", "blade-gun", "sniper", "mitraillette", "uzy", "gun", "blade", "laser", "lance-flamme", "lance-rokette", "canif", "crochet", "poignard", "seringue", "étoile-chinoise", "bat", "massus", "masse", "marteau", "roche", "cristau", "obsidienne", "couteau-cuisine", "opinel", "oft", "katana", "shuriken", "nunchakou", "vorpal", "excalibur", "durandal", "cuillere", "couteau-a-beur", "estafilad", "willywaller", "carabine", "mini-gun", "heavy-gun", "bazouka", "rocket", "drone", "missil", "fusée", "tmp", "calibre", "arbalette", "fléche", "lame-de-jet", "mayet", "mayoche", "mortier", "mortenzen", "bombe", "grenade", "mine", "m72", "m34", "c4", "c6", "c7", "c8", "c9", "84mm", "beratta", "a400", "m9", "7.62mm", "9mm", "glock", "magnum", "357", "5.54mm", ".38", "ags-30", "amp", "awc-g2", "arme-automatique", "arme-d'épaule", "arme-de-poing", "arme-légère", "arme-semi-automatique", "arme-à-feu", "armurier", "armer-de-zombie", "carabine-de-chasse", "carabine-militaire", "carl-gustav", "m2", "clé-pistolet", "arizaka", "type-44", "canon-revolver", "arme-anti-char", "canon-anti-char", "canon-rayé", "canon-lisse", "colt", "cz-455", "calibre-22", "svu", "dsr-50", "dragunov", "escopette", "lance", "alebard", "ecorcher", "fusil-à-canon-scié", "franchi", "lf-62", "m1915", "m1935", "martin-fakler", "fiat", "revelli", "fusil-à-platines", "fusil-à-poudre", "fusil-à-poudre-noire", "canon-rotatif", "fusil-anti-char", "fusil-de-chasse", "fusil-double-canon", "gw-150", "hawken", "huolongjing", "ksvk", "12-7", "12-à-pompe", "lancer", "machine-gun", "moukhala", "mousquet", "patator", "lance-patate", "pistolet-de-préssision", "platine-à-silex", "pistolet-stylo", "platine-à-mèche", "howdah", "feu", "incendière", "cocktel-molotov", "pulvérin", "qbu-88", "code-sheat", "glitch", "rouet", "ruger", "gp-100", "stealth-recon-scout", "stealth", "recon-scout", "scout", "recon", "tap-rack", "tromblon", "vks", "walther", "wa-2000", "weaver", "wkw", "wilk", "ak47", "ka74", "kalashnikov"]
liste_ennemi = ["Zombie", "Mort-Vivant", "Squelette", "Monstre", "Troll", "Géant", "Vampire", "Loup-garou", "Soldat", "Chevalier", "Démon", "Diable", "Farfadet", "Lutin", "Cobold", "Gobbline", "Orc", "Dragon", "Dinosaure", "Reptil", "Loup", "Serpant", "Basilic", "T-Rex", "Ogre", "Sangsus", "Écorcheur", "Magicien", "Mage", "Sorcier", "Bug", "Fourmis", "Rapace", "Brigan", "Fou", "Tour", "Prètre", "Mandiant", "Féroce", "Minautor", "Sorcière", "Mommie", "Abobinadle", "Maléfique", "Seigneur", "Ténèbre", "Insecte", "Scorpion", "Pieuvre", "Mutand", "Prisonnier", "Psycopate"]
dejavu = 0
equip = 1
arme = ""
ran = 0

#Dans Objet: Tab position objet 3d, couche par couche.
Objet = [[[["Détritus"], ["Porte-en-Fer"], [""], [""], ["huile"]],
          [["Coffre-fort"], ["Mort"], [""], ["moulage"], [""]],
          [[""], [""], ["Échelle"], [""], [""]],
          [["Assensseur"], ["allumette"], [""], ["Voiture"], ["Monte-charge"]],
          [["champignon"], ["Porte-en-Fer"], [""], [""], ["Chaudière-a-charbon"]]],
         [[["baies"], ["poisson"], ["Eau"], ["Foyer"], ["Chute"]],
          [["Troll"], [""], ["herbe"], [""], [""]],
          [[""], [""], ["Boite-a-courrier", "Puis"], ["Forge"], ["Jardin", "mauvaise-herbe", "champignon"]],
          [["Crapaud"], ["moustiques"], [""], ["Arbre", "bois-mort"], ["Fondation", "Altar", "pierre"]],
          [["Chute", "bouteille"], [""], [""], ["Tente", "allumette", "bouteille"], [""]]],
         [[["Zombie"], ["rubis"], ["Mort-Vivant"], [""], ["agate"]],
          [["blood-stone"], [""], ["Squelette"], ["saphire"], ["Zombie"]],
          [["Zombie"], ["Mort-Vivant"], ["émeraude", "couteau"], [""], ["citrine"]],
          [["Monte-Charge"], [""], ["rhodonite"], ["Zombie"], ["Zombie"]],
          [["diamant"], [""], ["Mort-Vivant"], ["améthyste"], ["Zombie"]]]]

#Dans DespO. L’ordre est important pour connecter avec la description des éléments environnement et objet.
DespO = [[[["Des ordures principalement, des vétements moisie et du verre cassé, mais il y a surement autre chose. Essailler de chercher dans détritus."], ["Cette porte en fer elle est déjà ouvrir."], [""], [""], ["Une flasque d'huile lubrifiante."]],
          [["Un gros Coffre-fort est boulonner au planché de la mine. Vous avez besoin d'une spécial pour l'ouvrir."], ["Il porte une cape gris et un chandaille bleu toute déchirér et dans son carquois un boomsticker hore d'état de marche."], [""], ["C'est un moule fait pour fondre la forme d'une grosse clé."], [""]],
          [[""], [""], ["L'échelle va très bien à cette endroit."], [""], [""]],
          [["L'Assensseur qui descent dans les étage inférieur, a besoin peu d'huile et d'entretien pour refonctionner."], ["Une boite d'allumette presque vide."], [""], ["Une Oldsmobile Delta 88 de 1973 Ici! Elle ne marche plus mais semble avoir été convertie en char-d'assault a vapeur pour servir durant la grande guerre."], ["Le Monte-charge a connu des jours meilleurs."]],
          [["Un champignon qui a poussé dans le noire et l'humidité. (Il vous fait penser à la forme d'un bouchon.)"], ["Cette porte en fer elle est déjà ouvrir."], [""], [""], ["La chaudière a besoin de charbon pour fonctionner."]]],
         [[["Les Baies sont fraiche et nourrissante."], ["Le poisson de la rivière pourrait vous faire un bon repas."], ["L'eau fraiche vous fait du bien. (Vous ne pouvez l'emporter avec vous sans un contenant vide.)"], ["Les cendres d'un Foyer de pierre des champs sur la grève. (Vous remarquez qu'une pierre a été déplacé, qu'il y manque plusieurs chose combustible et bois avant d'être allumable)."], ["La Cataracte au Nord Est tombe sur plusieurs mètres dans un bruit époustouflant. C'est un spectacle féérique que la nature vous offre. (Ça vous donne envie d'y jeté un message.)", "Une bouteille vide."]],
          [["Le Troll est assis sur une coffre au trésor, il a l'air affamé!"], [""], ["De l'herbe jaune très sec."], [""], [""]],
          [[""], [""], ["C'est une boite-a-courrier qui porte le numéro 42.", "Vous remarquez qu'une Échelle descend jusqu'au fond."], ["Il semble que cette endroit est été une Forge avant d'être abandonné, il y a une chaudière remplit de bois. Il ne lui manque que du foin sec pour s'allumer.", "Un vieux matelas cramoisie mais confortable."], ["Un jardin non entretenu remplit de maivaise-herbes et de champignon.", "La mauvaise- herbe est une plante de soin.", "Un champignon qui a poussé dans le noire et l'humidité. (La forme vous fait penser à un bouchon.)"]],
          [["Un crapaud bien endormit."], ["Ouille! Un moustique suceur de sang."], [""], ["L'Arbre géant doit avoir poussé depuis de nombreux siècle.", "Plusieurs morceaux de bois sec."], ["La fondation ici est détérioré jusqu'au ras du sol. On dirait l'édifice d’un très vieux château. Parmi ses pierres un Altar attire votre attention, elle n'a pas été usé par le passage du temps.", "L'Altar contient 10 trous de forme géométrique verrier.", "Une grosse pierre de fondation."]],
          [["La Cataracte au Sud Ouest tombe sur plusieurs mètres dans un bruit époustouflant. C'est un spectacle féérique que la nature vous offre. (Ça vous donne envie d'y jeté un message.)", "C'est une bouteille vide ordinaire."], [""], [""], ["La tente est toute déchiré, elle n'offre pas un abri convenable.", "Une boite d'allumette presque vide."], [""]]],
         [[["Le Squelette est animer et il vous attaque."], ["Le rubis est d'un rouge rutilant."], ["Le Squelette est animer et il vous attaque."], [""], ["Le cristal est une agate multicolore à l'intérieur."]],
          [["Un gem polie moitié sang moitié noire."], [""], ["Le Squelette est animer et il vous attaque."], ["Le saphir bleu est très pure."], ["Le Squelette est animer et il vous attaque."]],
          [["Le Squelette est animer et il vous attaque."], ["Le Squelette est animer et il vous attaque."], ["L'émeraude verte a l'état brute a la taille d'un œuf.", "Une lame d'argent sans doute perdus par un aventurier précédent."], [""], ["La pierre précieuse de couleur jaune."]],
          [["Le Monte-charge qui remonte à la mine."], [""], ["Un gem poly moitié rose moitié noire."], ["Le Squelette est animer et il vous attaque."], ["Un vieux monte-charge tout gripper."]],
          [["Un diamant claire comme le cristal"], [""], ["Le Squelette est animer et il vous attaque."], ["Pierre violet cristalline très brillante."], ["Le Squelette est animer et il vous attaque."]]]]

#Dans Lieux
#1) Donner un titre aux lieux visités.
#2) "," Ajouté entre virgule à la fin, la liste d'actions à faire.
#3) "," Termine par un seul objet qui apparait. Nommé en minuscule=prendre, MAJUSCULE=Eléments environnement non déplaçable.
#4) Le nom de l'OBJET peux être accompagné de directions (Nord, Sud, Est, Ouest, NE, NO, SE, SO, Monté, Descendre).
Lieux = [[[["Sous terrain Nord-Ouest", "chercher dans détritus", "ouvrir coffret", "or"], ["Sous terrain NNO"], ["Sous terrain Nord"], ["Sous terrain NNE"], ["Sous terrain Nord Est"]],
          [["Sous terrain NOO", "dévérouiller le coffre-fort avec clé-or", "clé-anglaise"], ["Sous terrain Centre Nord-Ouest", "regarder mort", "note"], ["Sous terrain Centre Nord"], ["Sous terrain Centre Nord Est"], ["Sous terrain NEE"]],
          [["Sous terrain Ouest"], ["Sous terrain Centre Ouest"], ["Sous terrain Centre"], ["Sous terrain Centre Est"], ["Sous terrain Est"]],
          [["Sous terrain SOO", "utilisé huile sur assensseur", "utilisé clé-anglaise sur assensseur", "Descendre"], ["Sous terrain Centre Sud-Ouest"], ["Sous terrain Centre Sud"], ["Sous terrain Centre Sud Est"], ["Sous terrain SEE", "tirer le monte-charge", "charbon"]],
          [["Sous terrain Sud-Ouest,(Champignière)"], ["Sous terrain SSO"], ["Sous terrain Sud"], ["Sous terrain SSE"], ["Sous terrain Sud Est", "placé charbon dans chaudière", "placé or dans moulage", "allumé chaudière avec allumette", "clé-or"]]],
         [[["Surface Nord-Ouest"], ["Surface NNO"], ["Surface Nord", "remplir bouteille avec eau", "bouteille-d'eau"], ["Surface NNE", "placer pierre dans espace foyer", "déposer lettre dans foyer", "déposer bois-mort dans foyer", "allumer foyer avec allumette", "torche"], ["Surface Nord Est", "placé pub dans bouteille", "mettre champignon sur bouchon", "jeter bouteille dans rivière", "repêché bouteille", "lettre"]],
          [["Surface NOO", "parlé au troll", "donné baies au troll", "donné poisson au troll", "donné bouteille-d'eau au troll", "moule-arme"], ["Surface Centre Nord-Ouest"], ["Surface Centre Nord"], ["Surface Centre Nord Est"], ["Surface NEE"]],
          [["Surface Ouest"], ["Surface Centre Ouest"], ["Surface Centre", "ouvrir boite-a-courrier", "pub"], ["Surface Centre Est,Vieille Forge", "entrer par ouverture", "déposé herbe dans chaudière", "allumé chaudière avec torche", "placé pièces-d'argent dans moule-arme", "couteau"], ["Surface Est"]],
          [["Surface SOO", "donner moustiques au crapaud", "pièces-d'argent"], ["Surface Centre Sud-Ouest"], ["Surface Centre Sud"], ["Surface Centre Sud Est"], ["Surface SEE", "placer rubis sur Altar", "placer agate sur Altar", "placer blood-stone sur Altar", "placer saphir sur Altar", "placer émeraude sur Altar", "placer citrine sur Altar", "placer rhodonite sur Altar", "placer diamant sur Altar", "placer améthyste sur Altar", "Castel"]],
          [["Surface Sud-Ouest", "placé pub dans bouteille", "mettre champignon sur bouchon", "jeté bouteille dans rivière", "repêché bouteille", "lettre"], ["Surface SSO"], ["Surface Sud"], ["Surface SSE"], ["Surface Sud Est"]]],
         [[["Enfer Nord-Ouest", "tuer zombie avec couteau", "tuer zombie avec couteau", "couteau"], ["Enfer NNO"], ["Enfer Nord", "tuer mort-vivant avec couteau", "tuer mort-vivant avec couteau", "tuer mort-vivant avec couteau", "couteau"], ["Enfer NNE"], ["Enfer Nord Est"]],
          [["Enfer NOO"], ["Enfer Centre Nord-Ouest"], ["Enfer Centre Nord", "tuer squelette avec couteau", "couteau"], ["Enfer Centre Nord Est"], ["Enfer NEE", "tuer zombie avec couteau", "tuer zombie avec couteau", "couteau"]],
          [["Enfer Ouest", "tuer zombie avec couteau", "tuer zombie avec couteau", "couteau"], ["Enfer Centre Ouest", "tuer mort-vivant avec couteau", "tuer mort-vivant avec couteau", "tuer mort-vivant avec couteau", "couteau"], ["Enfer Centre"], ["Enfer Centre Est"], ["Enfer Est"]],
          [["Enfer SOO", "actionner assensseur", "Monté"], ["Enfer Centre Sud-Ouest"], ["Enfer Centre Sud"], ["Enfer Centre Sud Est", "tuer zombie avec couteau", "tuer zombie avec couteau", "couteau"], ["Enfer SEE", "tuer zombie avec couteau", "tuer zombie avec couteau", "couteau"]],
          [["Enfer Sud-Ouest"], ["Enfer SSE"], ["Enfer Sud", "tuer mort-vivant avec couteau", "tuer mort-vivant avec couteau", "tuer mort-vivant avec couteau", "couteau"], ["Enfer SSO"], ["Enfer Sud Est", "tuer zombie avec couteau", "tuer zombie avec couteau", "couteau"]]]]

#Dans DespL
#1) Faite une description du lieux et évènement qui se produit dans cette destination. A la fin de la description, mettre en Majuscule les directions possibles Nord, Sud, Est, Ouest, Monté, Descendre.
#2) "," Faite une description pour chaque action réussie.
#3) "," Donne la description de l'objet obtenu.
DespL = [[[["C'est un cul-de-sac, le tunnel se termine après quelque mètre. Vous n'avez que trois directions possible l'Est, NE, SE. Il y a beaucoup de détritus dans le coin.", "Parmi les ordures vous repéré un petit coffret.", "Le coffet s'ouvre facilement, il contien un peu d'or.", "Une poigné de pièces d'or."], ["Vous arrivez à une autre bifurcation où trois direction s'offre à vous. Il y a une lourde porte en Fer qui ferme l'accès au Nord. Aller au Sud, à l'Est, à l'Ouest ou NE, SE.", "Vous faite entrer la clé en or dans la serrure et déverrouiller le mécanisme.", "La porte en fer est ouverte au Nord."], ["Vous arrivez à un croisement et trois directions s'offre à vous. Au Sud, à l'Ouest, à l'Est ou NO, SO."], ["C'est un cul-de-sac, le tunnel se termine après quelque mètre. Vous n'avez que deux direction possible l'Ouest et SO."], ["C'est un cul-de-sac, le tunnel se termine après quelque mètre. Il y a de vieux outils cassé dans un coffre en bois. Vous n'avez que deux direction possible au Sud ou SO."]],
          [["C'est un cul-de-sac, le tunnel se termine après quelque mètre. Il y a un gros Coffre-fort vérrouiller a cette endroit. Vous n'avez que deux direction possible au Sud et au SE.", "La clé-or entre parfaitement dans la sérrure, un petit tour et le coffre s'ouvre. Malheureusement la clée se brise dans le mécanisme.", "Une bonne clé-anglaise en parfaite état."], ["C'est un cul-de-sac, le tunnel se termine après quelque mètre. Un mort se trouve par terre. Vous n'avez que trois direction possible au NO, Nord, NE.", "Le mort aux os blanchie tien dans sa main une note écrite.", "JE MEURE, TOI QUI TROUVE SE MESSAGE PREND GARDE. J'AI LIBÈRÉ UN FLÉAU TERRIFIANT EN NE PRONONSSANT PAS LES MOTS DE PROTECTION EXACTE...CLATOU, VERRATA, NICHONS... L'ARME DES TÉNÈBRE RÔDE MAINTENANT DANS LES SOUS-TERRAIN DE CETTE MINE. JE N'ÉTAIS PAS PRÈS POUR LES AFFRONTÉS EN BAS, IL M'AURAIT FALUT UNE SIMPLE LAME D'ARGENT. J'AI CACHÉ MON TRÉSOR AU NORD-OUEST D'ICI, PREND LE ET VANGUE MA MORT. SIGNÉ ASH."], ["Vous êtes dans un tunnel qui va du centre au Nord. Deux direction s'offre à vous Nord ou Sud et sinon NO, NE, SE, SO."], ["C'est un cul-de-sac, le tunnel se termine après quelque mètre et il y a sur une table des objets de fonte. Vous n'avez que trois direction possible l'Est, NE et SE."], ["Ce tunnel devient un croisement où quatre direction s'offre à vous. Vous pouvez aller au Nord et à l'Ouest, au SO et au Sud."]],
          [["Vous arrivez à un croisement et cinq directions s'offre à vous. Au Nord, a l'Est, SO, SE, et au Sud."], ["Vous êtes dans un tunnel qui va de l'Est a l'Ouest. Quatre direction s'offre à vous NO, NE, SO, SE."], ["Vous êtes au centre d'une bifurcation où cinq direction s'offre à vous. Vous pouvez Monter à la surface vis l'échelle au-dessus de vous, comme aller au Nord, au Sud, à l'Est ou à l'Ouest."], ["Vous êtes dans un tunnel qui va de l'Ouest a l'Est. Quatre direction s'offre à vous NO, NE, SO, SE."], ["Vous arrivez à un croisement et cinq directions s'offre à vous. Au Nord, au Sud, à l'Ouest, NO et SE."]],
          [["Vous arrivez à une autre carfour où six direction s'offre à vous. Il y a un vieille Assensseur tout grippé au centre. Vous pouvez aller au Nord, au Sud, à l'Est et à l'Ouest, mais aussi NO, NE.", "Vous arrivez à dégrippé le mécanisme tout juste avec le reste d'huile.", "La porte de la nacelle est ouverte vous pouvez Descendre.", "L'assensseur est réparer, vous pouvez Descendre par là."], ["C'est un cul-de-sac, le tunnel se termine après quelque mètre. Vous avez trois direction possible à l'Ouest, NO et SO."], ["Vous êtes dans un tunnel qui va du Nord au Sud. Quatre direction s'offre à vous NO, NE, SO, SE."], ["C'est un cul-de-sac, le tunnel se termine après quelque mètre. Un véhicule très étrange est remisé dans cette pièce, on dirrait une Voiture! Vous avez trois direction possible au SO, Sud, SE."], ["Ce tunnel fait un crochet dans deux direction. Il y a un petit monte-charge a charbon a cette endroit. Vous pouvez aller au NO, au Nord, au NE, à l'Est et au SE.", "Après une légère remise en état, vous tirer le petit monte-charge jusqu'à vous. il y a un morceau de charbon à l'intérieur.", "Un morceau de charbon ordinaire parfait pour toutes les chaudière."]],
          [["C'est un cul-de-sac, le tunnel se termine après quelque mètre. Des champignons poussent sur le mur humide. Vous avez trois direction possible au NO, au Nord et au NE."], ["Ce tunnel fait un crochet de l'Est en directions Sud à traver une porte en Fer. Vous pouvez aller au NE, SO et SE.", "Vous faite entrer la clé en or dans la serrure et déverrouiller le mécanisme.", "La porte en fer est ouverte au Sud."], ["Vous arrivez à un croisement et trois directions s'offre à vous, au Nord, à l'Ouest et à l'Est. Vous pouvez aussi aller NE et SO."], ["Un autre carrefour avec cette fois trois directions. Vous pouvez aller au Nord, à l'Est et à l'Ouest. Vous pouvez aussi aller au NO."], ["C'est un cul-de-sac, le tunnel se termine après quelque mètre. Il y a une chaudière a cette endroit qui peux servir de forge. Vous n'avez que deux direction possible l'Ouest et NO.", "Le charbon est dans la chaudière pour servir de combustible.", "Le moulage en forme de clé contient un morceau d'or encore solide. Vous le placé sur la chaudière. Il ne manque qu'un bon feu.", "Le feu est allumé dans la chaudière et il dévore le charbon rutilant. Le moule absorbe la précieux minerait et forme une jolie clé doré.", "Cette clé a été mouler à partir d'un morceau d'or."]]],
         [[["Vous êtes au bord d'une rivière qui s'écoule d'Ouest en Est. Ici il y a des buissons de baie sauvage. Vous pouvez aller n'importe où Nord, Sud, Est, Ouest, NE, NO, SE, SO."], ["Vous êtes au bord d'une rivière qui s'écoule d'Ouest en Est. Le courant est fort et quelque poisson saute à contre-courant. Vous pouvez aller n'importe où Nord, Sud, Est, Ouest, NE, NO, SE, SO."], ["Vous êtes au bord d'une rivière qui s'écoule d'Ouest en Est. L'eau est clair à cette endroit, se serait l'endroit idéal pour en récupérez. Vous pouvez aller n'importe où Nord, Sud, Est, Ouest, NE, NO, SE, SO.", "Vous plonger la bouteille vide dans l'eau de la rivière pour la remplir.", "La bouteille contient de l'eau fraiche."], ["Vous êtes au bord d'une rivière qui s'écoule d'Ouest en Est. Il y a une plage sablonneuse et un petit Foyer de pierre des champs. Vous pouvez aller n'importe où Nord, Sud, Est, Ouest, NE, NO, SE, SO.", "La pierre complète parfaitement le pattern du foyer. Ainsi le feu ne pourra se répandre.", "Vous regardez à droite et à gauche avant de détruire cette lettre en petit morceau dans le foyer.", "Le buché est maintenant près pour être enflammé.", "Le feu brule bien. Un morceau de bois en forme de torche serait parfait pour faire une torche.", "La torche fait du bois-mort provient du Foyer sur la grève."], ["Vous êtes au bord d'une rivière qui s'écoule d'Ouest en Est. Elle se termine par une chute au Nord Est. Vous pouvez aller n'importe où Nord, Sud, Est, Ouest, NE, NO, SE, SO.", "La pub entre très bien dans la bouteille.", "Le champignon ferme le goulot de la bouteille.", "L'objet décrit un cercle jusqu'à la rivière et Plouf. Le média coule à pic et une autre bouteille fait surface.", "Vous tendez le bras et repêché l'autre bouteille qui contient une lettre.", "Si vous lisez cette lettre, c'est que vous êtes piégé dans la Matrise. Imaginé un micro cosmos tenant dans une espace de 5x5x5, mais où de nombreuse options s'offre à vous. Vous pouvez vous déplacé de gauche à droite, de l'avant à l'arrière et de haut en bas. Il n'y a pas de bord à cet univers, car vous êtes à l'intérieur d’un loup fermé. Vous pouvez regarder dans le passé avec vision, vous téléporter avec 3 coordonnées, voyagé dans le temps et même changé de dimension. Mais prenez garde à ne pas causer de paradoxe. Signé l'Auteur anonyme."]],
          [["La forêt est accidenté par ici. Il y a une rivière au Nord et un campe à l'Est. Un gros Troll est assis sur un coffre au centre de la forêt et vous regarde. Vous pouvez aller n'importe où Nord, Sud, Est, Ouest, NE, NO, SE, SO.", "-Bonjour Troll, moi ami... -Shlackvug! Miou-miou! Glou-glou! Rugit-il! (Heureusement que vous êtes familier avec le vocabulaire Troll. Tous les mots signifie Manger).", "(Vous donné les baie au Troll). -Shlackvug! Haha! Il les mangent rapidement mais a encore faim.", "(Vous donné le poisson au Troll). -Miou-miou! Haha! Il l'aval d'un coup, mais la il a très soif.", "Vous donné de l'eau au Troll. -Glou-glou! Haha! Il boit tout la bouteille et la bris par terre avant de courir faire ses besoins derrière le coffre, vous en profitez pour l'ouvrir et trouver un moule d'arme.", "C'est un très petit moule-d'arme de la forme d'un couteau."], ["Le champ longe une petite route au Sud et le bord de la rivière au Nord. Vous pouvez aller n'importe où Nord, Sud, Est, Ouest, NE, NO, SE, SO."], ["Le champ continue vers l'Ouest et se termine par une forêt à l'Est. Au Sud vous apercevez une vieille boite à courrier. Vous pouvez aller n'importe où Nord, Sud, Est, Ouest, NE, NO, SE, SO."], ["La forêt est accidenté par ici. Vous voyez une plage au Nord et une petite maison au Sud. Vous pouvez aller n'importe où Nord, Sud, Est, Ouest, NE, NO, SE, SO."], ["La forêt est danse par ici. Vous entendez une cataracte au Nord et voyez un jardin au Sud. Vous pouvez aller n'importe où Nord, Sud, Est, Ouest, NE, NO, SE, SO."]],
          [["La forêt est très danse par ici. Elle se poursuit au Nord, au Sud et il y a une route qui continue vers l'Est. Vous voyez un jardin qui s'éclaircie à l'Ouest. Vous pouvez aller n'importe où Nord, Sud, Est, Ouest, NE, NO, SE, SO."], ["La route est sinueuse entre le bois à l'Ouest et un champ à l'Est. Vous pouvez aller n'importe où Nord, Sud, Est, Ouest, NE, NO, SE, SO."], ["Vous êtes au centre d'un vaste champ au côté d'une petite maison plainte en blanc à l'Est. Une boite-a-courrier est juste devant vous, au côté d'un Puis asséché. Il y a une petite route qui descend au Sud, un jardin à l'Ouest et le reste du champ au Nord. Vous pouvez aller n'importe où Nord, Sud, Est, Ouest, Descendre, NE, NO, SE, SO.", "Vous ouvrer la boite a courrier et y trouver un feuillet publicitaire.", "Faite l'acquisition d'un vrai jeu vidéo. Contacté WarpCorp ou retournez nous ce formulaire par bouteille à la mer."], ["Vous faite chemin vers a bicoque en ruine. Les portes et les fenêtres sont malheureusement condamner, mais vous arrivez à voir par une ouverture dans le mur. La maison est vide mis a pare un matelas sur le sol. Vous devinez qu'elle a jadis servie en tant que Forge, car une chaudière s'y trouve. (Il y fait très noir et il faudrait une torche allumée pour vous éclairer avant d'entrer). Vous pouvez aller n'importe où Nord, Sud, Est, Ouest, NE, NO, SE, SO.", "Vous entrez par l'ouverture dans le mur avec votre torche.", "Vous déposez le foin sec dans chaudière pour servir de combustible.", "Vous allumez la chaudière avec la torche et un bon feu crépite dans son ventre.", "Vous placez le moule sur le feu. La pièce d'argent fond dans moule arme pour donner la forme d'un couteau. Le feu s'éteint avec la torche.", "Un petit couteau d'argent fait d'une seul pièce. Un belle ouvrage."], ["Le jardin est à l'abandon, vous ne trouverez pas de quoi mangé ici juste quelque mauvaise herbe. Il y la forêt au Nord, au Sud, à l'Est et une petite maison à l'Ouest. Vous pouvez aller n'importe où Nord, Sud, Est, Ouest, NE, NO, SE, SO."]],
          [["La forêt est accidenté par ici et marécageuse. Parmi les quenouilles vous voyez un crapaud qui dore. Vous pouvez aller n'importe où Nord, Sud, Est, Ouest, NE, NO, SE, SO.", "Vous donnez les moustiques au Crapaud et celui-ci mange jusqu'à être ropus. Pour vous remercier, il déglutine une pièce d'argent.", "Des pièces de monnaies faite d'argent pure."], ["Un marécage où vivent des bataillons de moustiques. Vous pouvez aller n'importe où Nord, Sud, Est, Ouest, NE, NO, SE, SO."], ["Une clairière tout ce qu'il y a d'ordinaire. Il y a un champ au Nord, une forêt à l'Est et une petite route à l'Ouest. Vous pouvez aller n'importe où Nord, Sud, Est, Ouest, NE, NO, SE, SO."], ["Toujours de la forêt, par contre il y a un très gros arbre à cette endroit. Vous pouvez aller n'importe où Nord, Sud, Est, Ouest, NE, NO, SE, SO."], ["C'est une forêt très rocailleuse entremêlé de racines, vous trouvez les fondations d'une habitation en ruine. Vous pouvez aller n'importe où Nord, Sud, Est, Ouest, NE, NO, SE, SO."]],
          [["Il y a un lac ici juste au pied d'une cataracte peu abrupte au Sud-Ouest. Vous pouvez aller n'importe où Nord, Sud, Est, Ouest, NE, NO, SE, SO.", "La pub entre très bien dans la bouteille", "Le champignon ferme le goulot de la bouteille.", "l'objet décrit un cercle jusqu'à la rivière et Plouf. Le média coule à pic et une autre bouteille fait surface.", "Vous tendez le bras et repêché l'autre bouteille qui contient une lettre.", "Si vous lisez cette lettre, c'est que vous êtes piégé dans la Matrise. Imaginé un micro cosmos tenant dans une espace de 5x5x5, mais où de nombreuse options s'offre à vous. Vous pouvez vous déplacé de gauche à droite, de l'avant à l'arrière et de haut en bas. Il n'y a pas de bord à cet univers, car vous êtes à l'intérieur d’un loup fermé. Vous pouvez regarder dans le passé avec vision, vous téléporter avec 3 coordonnées, voyagé dans le temps et même changé de dimension. Mais prenez garde à ne pas causer de paradoxe. Signé l'Auteur anonyme."], ["Une petite route qui va du champ à l'Est jusqu'au lac à l'Ouest. Vous pouvez aller n'importe où Nord, Sud, Est, Ouest, NE, NO, SE, SO."], ["Une route qui fait un crochet du Nord a l'Ouest à travers champ. Vous pouvez aller n'importe où Nord, Sud, Est, Ouest, NE, NO, SE, SO."], ["Vous marchez dans un éclaircie entre les bois et le champ. Une tente a été plantée ici, mais personne n’a l'intérieur. Vous pouvez aller n'importe où Nord, Sud, Est, Ouest, NE, NO, SE, SO."], ["La forêt est danse par ici. Il y a un petit campement à l'Ouest. Vous pouvez aller n'importe où Nord, Sud, Est, Ouest, NE, NO, SE, SO.", "La pierre rouge s'insère parfaitement dans le trou hexagonal de l'Altar.", "L'agate s'insère parfaitement dans le trou pentagonal de l'Altar.", "La blood-stone s'insère parfaitement dans le trou en forme de goutte de l'Altar.", "Le saphir s'insère parfaitement dans le trou carré de l'Altar.", "L'émeraude s'insère parfaitement dans le trou septagonal de l'Altar.", "La citrine jaune s'insère parfaitement dans le trou ovale de l'Altar.", "La rhodonite s'insère parfaitement dans le trou ennéagonal de l'Altar.", "Le diamant s'insère parfaitement dans le trou octogonal de l'Altar.", "L'améthyste s'insère parfaitement dans le trou rond de l'Altar.", "Les fondations se reconstruit d'elle même si vite, que vous croyez rêver! Vous venez de remonté le temps à l'époque glorieuse où se château trônait dans les bois. Vous êtes arrivé dans le siècle des Héros et des légendes. Félicitation Aventurier!"]]],
         [[["Vous êtes sur une îlot de roche sur une mer de lave. Vous pouvez sauter sur n'importe quel autre îlot au Nord, Sud, Est, Ouest, NO, NE, SO, SE.", "Vous lancez le couteau sur le morte-vivant et toute sa chère se désintègre ne laissant que le squelette.", "Vous tuer le squelette avec couteau de jet a lame d'argent.", "Un petit couteau de jet fait d'argent d'une seul pièce. Un belle ouvrage."], ["Vous êtes sur un îlot de roche sur une mer de lave. Vous pouvez sauter sur n'importe quel autre îlot au Nord, Sud, Est, Ouest, NO, NE, SO, SE."], ["Vous êtes sur un îlot de roche sur une mer de lave. Vous pouvez sauter sur n'importe quel autre îlot au Nord, Sud, Est, Ouest, NO, NE, SO, SE.", "Vous frappez son armure de votre lame et elle disparait en poussière, laissant place à un mort-vivant.", "Vous lancez le couteau sur le morte-vivant et toute sa chère se désintègre ne laissant que le squelette.", "Vous tuer le squelette avec couteau de jet a lame d'argent.", "Un petit couteau de jet fait d'argent d'une seul pièce. Un belle ouvrage."], ["Vous êtes sur un îlot de roche sur une mer de lave. Il y a des ossements morts par terre. Vous pouvez sauter sur n'importe quel autre îlot au Nord, Sud, Est, Ouest, NO, NE, SO, SE."], ["Vous êtes sur un îlot de roche sur une mer de lave. Vous pouvez sauter sur n'importe quel autre îlot au Nord, Sud, Est, Ouest, NO, NE, SO, SE."]], [["Vous êtes sur une îlot de roche sur une mer de lave. Vous pouvez sauter sur n'importe quel autre îlot au Nord, Sud, Est, Ouest, NO, NE, SO, SE."], ["Vous êtes sur un îlot de roche sur une mer de lave. Il y a des ossements morts par terre. Vous pouvez sauter sur n'importe quel autre îlot au Nord, Sud, Est, Ouest, NO, NE, SO, SE."], ["Vous êtes sur un îlot de roche sur une mer de lave. Vous pouvez sauter sur n'importe quel autre îlot au Nord, Sud, Est, Ouest, NO, NE, SO, SE.", "Vous lancez le couteau sur le morte-vivant et toute sa chère se désintègre ne laissant que le squelette.", "Vous tuer le squelette avec couteau de jet a lame d'argent.", "Un petit couteau de jet fait d'argent d'une seul pièce. Un belle ouvrage."], ["Vous êtes sur un îlot de roche sur une mer de lave. Vous pouvez sauter sur n'importe quel autre îlot au Nord, Sud, Est, Ouest, NO, NE, SO, SE."], ["Vous êtes sur un îlot de roche sur une mer de lave. Vous pouvez sauter sur n'importe quel autre îlot au Nord, Sud, Est, Ouest, NO, NE, SO, SE.", "Vous lancez le couteau sur le morte-vivant et toute sa chère se désintègre ne laissant que le squelette.", "Vous tuer le squelette avec couteau de jet a lame d'argent.", "Un petit couteau de jet fait d'argent d'une seul pièce. Un belle ouvrage."]],
          [["Vous êtes sur une îlot de roche sur une mer de lave. Vous pouvez sauter sur n'importe quel autre îlot au Nord, Sud, Est, Ouest, NO, NE, SO, SE.", "Vous lancez le couteau sur le morte-vivant et toute sa chère se désintègre ne laissant que le squelette.", "Vous tuer le squelette avec couteau de jet a lame d'argent.", "Un petit couteau de jet fait d'argent d'une seul pièce. Un belle ouvrage."], ["Vous êtes sur un îlot de roche sur une mer de lave. Vous pouvez sauter sur n'importe quel autre îlot au Nord, Sud, Est, Ouest, NO, NE, SO, SE.", "Vous frappez son armure de votre lame et elle disparait en poussière, laissant place à un mort-vivant.", "Vous lancez le couteau sur le morte-vivant et toute sa chère se désintègre ne laissant que le squelette.", "Vous tuer le squelette avec couteau de jet a lame d'argent.", "Un petit couteau de jet fait d'argent d'une seul pièce. Un belle ouvrage."], ["Vous êtes sur un îlot de roche sur une mer de lave. Vous pouvez sauter sur n'importe quel autre îlot au Nord, Sud, Est, Ouest, NO, NE, SO, SE."], ["Vous êtes sur un îlot de roche sur une mer de lave. Il y a des ossements par terre. Vous pouvez sauter sur n'importe quel autre îlot au Nord, Sud, Est, Ouest, NO, NE, SO, SE."], ["Vous êtes sur un îlot de roche sur une mer de lave. Vous pouvez sauter sur n'importe quel autre îlot au Nord, Sud, Est, Ouest, NO, NE, SO, SE."]],
          [["Vous êtes sur une îlot de roche sur une mer de lave. Vous pouvez aller n'importe où Monter ou sauté sur un autre îlot au Nord, Sud, Est, Ouest, NO, NE, SO, SE.", "Vous dérouillez l'assensseur et le faite descendre jusqu'à vous.", "Le vieille assensseur est arrivé en bas. Vous pouvez remonté."], ["Vous êtes sur un îlot de roche sur une mer de lave. Il y a des ossements morts par terre. Vous pouvez sauter sur n'importe quel autre îlot au Nord, Sud, Est, Ouest, NO, NE, SO, SE."], ["Vous êtes sur un îlot de roche sur une mer de lave. Vous pouvez sauter sur n'importe quel autre îlot au Nord, Sud, Est, Ouest, NO, NE, SO, SE."], ["Vous êtes sur un îlot de roche sur une mer de lave. Vous pouvez sauter sur n'importe quel autre îlot au Nord, Sud, Est, Ouest, NO, NE, SO, SE.", "Vous lancez le couteau sur le morte-vivant et toute sa chère se désintègre ne laissant que le squelette.", "Vous tuer le squelette avec couteau de jet a lame d'argent.", "Un petit couteau de jet fait d'argent d'une seul pièce. Un belle ouvrage."], ["Vous êtes sur un îlot de roche sur une mer de lave. Vous pouvez sauter sur n'importe quel autre îlot au Nord, Sud, Est, Ouest, No, NE, SO, SE.", "Vous lancez le couteau sur le morte-vivant et toute sa chère se désintègre ne laissant que le squelette.", "Vous tuer le squelette avec couteau de jet a lame d'argent.", "Un petit couteau de jet fait d'argent d'une seul pièce. Un belle ouvrage."]],
          [["Vous êtes sur une îlot de roche sur une mer de lave. Vous pouvez sauter sur n'importe quel autre îlot au Nord, Sud, Est, Ouest, NO, NE, SO, SE."], ["Vous êtes sur un îlot de roche sur une mer de lave. Il y a des ossement mort par terre. Vous pouvez sauter sur n'importe quel autre îlot au Nord, Sud, Est, Ouest, NO, NE, SO, SE."], ["Vous êtes sur un îlot de roche sur une mer de lave. Vous pouvez sauter sur n'importe quel autre îlot au Nord, Sud, Est, Ouest, NO, NE, SO, SE.", "Vous frappez son armure de votre lame et elle disparait en poussière, laissant place à un mort-vivant.", "Vous lancez le couteau sur le morte-vivant et toute sa chère se désintègre ne laissant que le squelette.", "Vous tuer le squelette avec couteau de jet a lame d'argent.", "Un petit couteau de jet fait d'argent d'une seul pièce. Un belle ouvrage."], ["Vous êtes sur un îlot de roche sur une mer de lave. Vous pouvez sauter sur n'importe quel autre îlot au Nord, Sud, Est, Ouest, NO, NE, SO, SE."], ["Vous êtes sur un îlot de roche sur une mer de lave. Vous pouvez sauter sur n'importe quel autre îlot au Nord, Sud, Est, Ouest, NO, NE, SO, SE.", "Vous tuer le squelette avec couteau de jet a lame d'argent.", "Un petit couteau de jet fait d'argent d'une seul pièce. Un belle ouvrage."]]]]

#Load nouvelle liste
item = "liste_item.txt"
if (os.path.exists(Rep + item) == True):
    file = open(Rep + item.upper(), "r")
    ligne = 0
    liste_ennemi2 = []
    liste_arme2 = []
    liste_soin2 = []
    for line in file:
        lst = ""
        lst = line[:-1].replace("['","")
        lst = lst.replace("']","")
        lst = lst.split("', '")
        for i in range(len(lst)):
            if ligne == 0:
                liste_arme2.append(lst[i])
            if ligne == 1:
                liste_ennemi2.append(lst[i])
            if ligne == 2:
                liste_soin2.append(lst[i])
        #if ligne == 0:
            #print("Weapon Liste Update Completed.")
        #if ligne == 1:
            #print("Monster Liste Update Completed.")
        #if ligne == 2:
            #print("Healing Liste Update Completed.")
        ligne = ligne + 1
    if (len(liste_ennemi2) > len(liste_ennemi) or len(liste_arme2) > len(liste_arme) or len(liste_soin2) > len(liste_soin)):
        liste_ennemi2 = []
        liste_arme2 = []
        liste_soin2 = []
        liste_ennemi2 = liste_ennemi
        liste_arme2 = liste_arme
        liste_soin2 = liste_soin
        print("Mis-a-jour liste objet Complèté.")

#Load_Map
source = "map.txt"
chargement = 0
if os.path.exists(Rep + source) == True:
    quest = input("Un scénario est détecté. Charger? [O/N]")
if quest.upper() == "O":
    chargement = 1
    if chargement == 1:
        #champs map
        if (os.path.exists(Rep + source) == True):
            print("Nouveau Scénario en Chargement.")
            file = open(Rep + source.upper(), "r")
            ligne = 0
            for line in file:
                if (ligne == 0): #3d
                    #Objet
                    lst = ""
                    lst = line[:-1].replace("[[[['","")
                    lst = lst.replace("']]]]","")
                    lst = lst.replace("]], [[","], [")
                    lst = lst.replace("]], [[","], [")
                    lst = lst.replace('"',"'")
                    lst = lst.split("'], ['")
                    invA = []
                    invB = []
                    invC = []
                    inv1 = []
                    inv2 = []
                    inv3 = []
                    inv4 = []
                    inv5 = []
                    inv6 = []
                    inv7 = []
                    inv8 = []
                    inv9 = []
                    inv10 = []
                    inv11 = []
                    inv12 = []
                    inv13 = []
                    inv14 = []
                    inv15 = []
                    inv = []
                    for i in range(5):
                        if "', '" in lst[i]:
                            for ii in range("', '" in lst[i]):
                                inv1.append(lst[i].split("', '"))
                        else:
                            inv.append(lst[i])
                            inv1.append(inv)
                            inv = []
                        if "', '" in lst[i+5]:
                            for ii in range("', '" in lst[i+5]):
                                inv2.append(lst[i+5].split("', '"))
                        else:
                            inv.append(lst[i+5])
                            inv2.append(inv)
                            inv = []
                        if "', '" in lst[i+10]:
                            for ii in range("', '" in lst[i+10]):
                                inv3.append(lst[i+10].split("', '"))
                        else:
                            inv.append(lst[i+10])
                            inv3.append(inv)
                            inv = []
                        if "', '" in lst[i+15]:
                            for ii in range("', '" in lst[i+15]):
                                inv4.append(lst[i+15].split("', '"))
                        else:
                            inv.append(lst[i+15])
                            inv4.append(inv)
                            inv = []
                        if "', '" in lst[i+20]:
                            for ii in range("', '" in lst[i+20]):
                                inv5.append(lst[i+20].split("', '"))
                        else:
                            inv.append(lst[i+20])
                            inv5.append(inv)
                            inv = []
                        if "', '" in lst[i+25]:
                            for ii in range("', '" in lst[i+25]):
                                inv6.append(lst[ii].split("', '"))
                        else:
                            inv.append(lst[i+25])
                            inv6.append(inv)
                            inv = []
                        if "', '" in lst[i+30]:
                            for ii in range("', '" in lst[i+30]):
                                inv7.append(lst[i+30].split("', '"))
                        else:
                            inv.append(lst[i+30])
                            inv7.append(inv)
                            inv = []
                        if "', '" in lst[i+35]:
                            for ii in range("', '" in lst[i+35]):
                                inv8.append(lst[i+35].split("', '"))
                        else:
                            inv.append(lst[i+35])
                            inv8.append(inv)
                            inv = []
                        if "', '" in lst[i+40]:
                            for ii in range("', '" in lst[i+40]):
                                inv9.append(lst[i+40].split("', '"))
                        else:
                            inv.append(lst[i+40])
                            inv9.append(inv)
                            inv = []
                        if "', '" in lst[i+45]:
                            for ii in range("', '" in lst[i+45]):
                                inv10.append(lst[i+45].split("', '"))
                        else:
                            inv.append(lst[i+45])
                            inv10.append(inv)
                            inv = []
                        if "', '" in lst[i+50]:
                            for ii in range("', '" in lst[i+50]):
                                inv11.append(lst[i+50].split("', '"))
                        else:
                            inv.append(lst[i+45])
                            inv11.append(inv)
                            inv = []
                        if "', '" in lst[i+55]:
                            for ii in range("', '" in lst[i+55]):
                                inv12.append(lst[i+55].split("', '"))
                        else:
                            inv.append(lst[i+50])
                            inv12.append(inv)
                            inv = []
                        if "', '" in lst[i+60]:
                            for ii in range("', '" in lst[i+60]):
                                inv13.append(lst[i+60].split("', '"))
                        else:
                            inv.append(lst[i+60])
                            inv13.append(inv)
                            inv = []
                        if "', '" in lst[i+65]:
                            for ii in range("', '" in lst[i+65]):
                                inv14.append(lst[i+65].split("', '"))
                        else:
                            inv.append(lst[i+65])
                            inv14.append(inv)
                            inv = []
                        if "', '" in lst[i+70]:
                            for ii in range("', '" in lst[i+70]):
                                inv15.append(lst[i+70].split("', '"))
                        else:
                            inv.append(lst[i+70])
                            inv15.append(inv)
                            inv = []
                    for i in range(5):
                        if i == 0:
                            j = inv1
                        if i == 1:
                            j = inv2
                        if i == 2:
                            j = inv3
                        if i == 3:
                            j = inv4
                        if i == 4:
                            j = inv5
                        invA.append(j)
                    for i in range(5):
                        if i == 0:
                            j = inv6
                        if i == 1:
                            j = inv7
                        if i == 2:
                            j = inv8
                        if i == 3:
                            j = inv9
                        if i == 4:
                            j = inv10
                        invB.append(j)
                    for i in range(5):
                        if i == 0:
                            j = inv11
                        if i == 1:
                            j = inv12
                        if i == 2:
                            j = inv13
                        if i == 3:
                            j = inv14
                        if i == 4:
                            j = inv15
                        invC.append(j)
                    Objet = []
                    for i in range(3):
                        if i == 0:
                            j = invA
                        if i == 1:
                            j = invB
                        if i == 2:
                            j = invC
                        Objet.append(j)
                if (ligne == 1): #3d
                    #DespO
                    lst = ""
                    lst = line[:-1].replace("[[[['","")
                    lst = lst.replace("']]]]","")
                    lst = lst.replace("]], [[","], [")
                    lst = lst.replace("]], [[","], [")
                    lst = lst.replace('"], [',"'], ['")#
                    lst = lst.split("'], ['")
                    invA = []
                    invB = []
                    invC = []
                    inv1 = []
                    inv2 = []
                    inv3 = []
                    inv4 = []
                    inv5 = []
                    inv6 = []
                    inv7 = []
                    inv8 = []
                    inv9 = []
                    inv10 = []
                    inv11 = []
                    inv12 = []
                    inv13 = []
                    inv14 = []
                    inv15 = []
                    inv = []
                    for i in range(5):
                        if "', '" in lst[i]:
                            for ii in range("', '" in lst[i]):
                                inv1.append(lst[i].split("', '"))
                        else:
                            inv.append(lst[i])
                            inv1.append(inv)
                            inv = []
                        if "', '" in lst[i+5]:
                            for ii in range("', '" in lst[i+5]):
                                inv2.append(lst[i+5].split("', '"))
                        else:
                            inv.append(lst[i+5])
                            inv2.append(inv)
                            inv = []
                        if "', '" in lst[i+10]:
                            for ii in range("', '" in lst[i+10]):
                                inv3.append(lst[i+10].split("', '"))
                        else:
                            inv.append(lst[i+10])
                            inv3.append(inv)
                            inv = []
                        if "', '" in lst[i+15]:
                            for ii in range("', '" in lst[i+15]):
                                inv4.append(lst[i+15].split("', '"))
                        else:
                            inv.append(lst[i+15])
                            inv4.append(inv)
                            inv = []
                        if "', '" in lst[i+20]:
                            for ii in range("', '" in lst[i+20]):
                                inv5.append(lst[i+20].split("', '"))
                        else:
                            inv.append(lst[i+20])
                            inv5.append(inv)
                            inv = []
                        if "', '" in lst[i+25]:
                            for ii in range("', '" in lst[i+25]):
                                inv6.append(lst[ii].split("', '"))
                        else:
                            inv.append(lst[i+25])
                            inv6.append(inv)
                            inv = []
                        if "', '" in lst[i+30]:
                            for ii in range("', '" in lst[i+30]):
                                inv7.append(lst[i+30].split("', '"))
                        else:
                            inv.append(lst[i+30])
                            inv7.append(inv)
                            inv = []
                        if "', '" in lst[i+35]:
                            for ii in range("', '" in lst[i+35]):
                                inv8.append(lst[i+35].split("', '"))
                        else:
                            inv.append(lst[i+35])
                            inv8.append(inv)
                            inv = []
                        if "', '" in lst[i+40]:
                            for ii in range("', '" in lst[i+40]):
                                inv9.append(lst[i+40].split("', '"))
                        else:
                            inv.append(lst[i+40])
                            inv9.append(inv)
                            inv = []
                        if "', '" in lst[i+45]:
                            for ii in range("', '" in lst[i+45]):
                                inv10.append(lst[i+45].split("', '"))
                        else:
                            inv.append(lst[i+45])
                            inv10.append(inv)
                            inv = []
                        if "', '" in lst[i+50]:
                            for ii in range("', '" in lst[i+50]):
                                inv11.append(lst[i+50].split("', '"))
                        else:
                            inv.append(lst[i+45])
                            inv11.append(inv)
                            inv = []
                        if "', '" in lst[i+55]:
                            for ii in range("', '" in lst[i+55]):
                                inv12.append(lst[i+55].split("', '"))
                        else:
                            inv.append(lst[i+50])
                            inv12.append(inv)
                            inv = []
                        if "', '" in lst[i+60]:
                            for ii in range("', '" in lst[i+60]):
                                inv13.append(lst[i+60].split("', '"))
                        else:
                            inv.append(lst[i+60])
                            inv13.append(inv)
                            inv = []
                        if "', '" in lst[i+65]:
                            for ii in range("', '" in lst[i+65]):
                                inv14.append(lst[i+65].split("', '"))
                        else:
                            inv.append(lst[i+65])
                            inv14.append(inv)
                            inv = []
                        if "', '" in lst[i+70]:
                            for ii in range("', '" in lst[i+70]):
                                inv15.append(lst[i+70].split("', '"))
                        else:
                            inv.append(lst[i+70])
                            inv15.append(inv)
                            inv = []
                    for i in range(5):
                        if i == 0:
                            j = inv1
                        if i == 1:
                            j = inv2
                        if i == 2:
                            j = inv3
                        if i == 3:
                            j = inv4
                        if i == 4:
                            j = inv5
                        invA.append(j)
                    for i in range(5):
                        if i == 0:
                            j = inv6
                        if i == 1:
                            j = inv7
                        if i == 2:
                            j = inv8
                        if i == 3:
                            j = inv9
                        if i == 4:
                            j = inv10
                        invB.append(j)
                    for i in range(5):
                        if i == 0:
                            j = inv11
                        if i == 1:
                            j = inv12
                        if i == 2:
                            j = inv13
                        if i == 3:
                            j = inv14
                        if i == 4:
                            j = inv15
                        invC.append(j)
                    DespO = []
                    for i in range(3):
                        if i == 0:
                            j = invA
                        if i == 1:
                            j = invB
                        if i == 2:
                            j = invC
                        DespO.append(j)
                if (ligne == 2): #3d
                    #Lieux
                    lst = ""
                    lst = line[:-1].replace("[[[['","")
                    lst = lst.replace("']]]]","")
                    lst = lst.replace("]], [[","], [")
                    lst = lst.replace("]], [[","], [")
                    lst = lst.replace('"], [',"'], ['") #Diancre!!
                    lst = lst.split("'], ['")
                    invA = []
                    invB = []
                    invC = []
                    inv1 = []
                    inv2 = []
                    inv3 = []
                    inv4 = []
                    inv5 = []
                    inv6 = []
                    inv7 = []
                    inv8 = []
                    inv9 = []
                    inv10 = []
                    inv11 = []
                    inv12 = []
                    inv13 = []
                    inv14 = []
                    inv15 = []
                    inv = []
                    for i in range(5):
                        if "', '" in lst[i]:
                            for ii in range("', '" in lst[i]):
                                inv1.append(lst[i].split("', '"))
                        else:
                            inv.append(lst[i])
                            inv1.append(inv)
                            inv = []
                        if "', '" in lst[i+5]:
                            for ii in range("', '" in lst[i+5]):
                                inv2.append(lst[i+5].split("', '"))
                        else:
                            inv.append(lst[i+5])
                            inv2.append(inv)
                            inv = []
                        if "', '" in lst[i+10]:
                            for ii in range("', '" in lst[i+10]):
                                inv3.append(lst[i+10].split("', '"))
                        else:
                            inv.append(lst[i+10])
                            inv3.append(inv)
                            inv = []
                        if "', '" in lst[i+15]:
                            for ii in range("', '" in lst[i+15]):
                                inv4.append(lst[i+15].split("', '"))
                        else:
                            inv.append(lst[i+15])
                            inv4.append(inv)
                            inv = []
                        if "', '" in lst[i+20]:
                            for ii in range("', '" in lst[i+20]):
                                inv5.append(lst[i+20].split("', '"))
                        else:
                            inv.append(lst[i+20])
                            inv5.append(inv)
                            inv = []
                        if "', '" in lst[i+25]:
                            for ii in range("', '" in lst[i+25]):
                                inv6.append(lst[ii].split("', '"))
                        else:
                            inv.append(lst[i+25])
                            inv6.append(inv)
                            inv = []
                        if "', '" in lst[i+30]:
                            for ii in range("', '" in lst[i+30]):
                                inv7.append(lst[i+30].split("', '"))
                        else:
                            inv.append(lst[i+30])
                            inv7.append(inv)
                            inv = []
                        if "', '" in lst[i+35]:
                            for ii in range("', '" in lst[i+35]):
                                inv8.append(lst[i+35].split("', '"))
                        else:
                            inv.append(lst[i+35])
                            inv8.append(inv)
                            inv = []
                        if "', '" in lst[i+40]:
                            for ii in range("', '" in lst[i+40]):
                                inv9.append(lst[i+40].split("', '"))
                        else:
                            inv.append(lst[i+40])
                            inv9.append(inv)
                            inv = []
                        if "', '" in lst[i+45]:
                            for ii in range("', '" in lst[i+45]):
                                inv10.append(lst[i+45].split("', '"))
                        else:
                            inv.append(lst[i+45])
                            inv10.append(inv)
                            inv = []
                        if "', '" in lst[i+50]:
                            for ii in range("', '" in lst[i+50]):
                                inv11.append(lst[i+50].split("', '"))
                        else:
                            inv.append(lst[i+45])
                            inv11.append(inv)
                            inv = []
                        if "', '" in lst[i+55]:
                            for ii in range("', '" in lst[i+55]):
                                inv12.append(lst[i+55].split("', '"))
                        else:
                            inv.append(lst[i+50])
                            inv12.append(inv)
                            inv = []
                        if "', '" in lst[i+60]:
                            for ii in range("', '" in lst[i+60]):
                                inv13.append(lst[i+60].split("', '"))
                        else:
                            inv.append(lst[i+60])
                            inv13.append(inv)
                            inv = []
                        if "', '" in lst[i+65]:
                            for ii in range("', '" in lst[i+65]):
                                inv14.append(lst[i+65].split("', '"))
                        else:
                            inv.append(lst[i+65])
                            inv14.append(inv)
                            inv = []
                        if "', '" in lst[i+70]:
                            for ii in range("', '" in lst[i+70]):
                                inv15.append(lst[i+70].split("', '"))
                        else:
                            inv.append(lst[i+70])
                            inv15.append(inv)
                            inv = []
                    for i in range(5):
                        if i == 0:
                            j = inv1
                        if i == 1:
                            j = inv2
                        if i == 2:
                            j = inv3
                        if i == 3:
                            j = inv4
                        if i == 4:
                            j = inv5
                        invA.append(j)
                    for i in range(5):
                        if i == 0:
                            j = inv6
                        if i == 1:
                            j = inv7
                        if i == 2:
                            j = inv8
                        if i == 3:
                            j = inv9
                        if i == 4:
                            j = inv10
                        invB.append(j)
                    for i in range(5):
                        if i == 0:
                            j = inv11
                        if i == 1:
                            j = inv12
                        if i == 2:
                            j = inv13
                        if i == 3:
                            j = inv14
                        if i == 4:
                            j = inv15
                        invC.append(j)
                    Lieux = []
                    for i in range(3):
                        if i == 0:
                            j = invA
                        if i == 1:
                            j = invB
                        if i == 2:
                            j = invC
                        Lieux.append(j)
                if (ligne == 3): #3d
                    #DespL
                    lst = ""
                    lst = line[:-1].replace("[[[['","")
                    lst = lst.replace("']]]]","")
                    lst = lst.replace("]], [[","], [")
                    lst = lst.replace("]], [[","], [")
                    lst = lst.replace('"], [',"'], ['")#
                    lst = lst.split("'], ['")
                    invA = []
                    invB = []
                    invC = []
                    inv1 = []
                    inv2 = []
                    inv3 = []
                    inv4 = []
                    inv5 = []
                    inv6 = []
                    inv7 = []
                    inv8 = []
                    inv9 = []
                    inv10 = []
                    inv11 = []
                    inv12 = []
                    inv13 = []
                    inv14 = []
                    inv15 = []
                    inv = []
                    for i in range(5):
                        if "', '" in lst[i]:
                            for ii in range("', '" in lst[i]):
                                inv1.append(lst[i].split("', '"))
                        else:
                            inv.append(lst[i])
                            inv1.append(inv)
                            inv = []
                        if "', '" in lst[i+5]:
                            for ii in range("', '" in lst[i+5]):
                                inv2.append(lst[i+5].split("', '"))
                        else:
                            inv.append(lst[i+5])
                            inv2.append(inv)
                            inv = []
                        if "', '" in lst[i+10]:
                            for ii in range("', '" in lst[i+10]):
                                inv3.append(lst[i+10].split("', '"))
                        else:
                            inv.append(lst[i+10])
                            inv3.append(inv)
                            inv = []
                        if "', '" in lst[i+15]:
                            for ii in range("', '" in lst[i+15]):
                                inv4.append(lst[i+15].split("', '"))
                        else:
                            inv.append(lst[i+15])
                            inv4.append(inv)
                            inv = []
                        if "', '" in lst[i+20]:
                            for ii in range("', '" in lst[i+20]):
                                inv5.append(lst[i+20].split("', '"))
                        else:
                            inv.append(lst[i+20])
                            inv5.append(inv)
                            inv = []
                        if "', '" in lst[i+25]:
                            for ii in range("', '" in lst[i+25]):
                                inv6.append(lst[ii].split("', '"))
                        else:
                            inv.append(lst[i+25])
                            inv6.append(inv)
                            inv = []
                        if "', '" in lst[i+30]:
                            for ii in range("', '" in lst[i+30]):
                                inv7.append(lst[i+30].split("', '"))
                        else:
                            inv.append(lst[i+30])
                            inv7.append(inv)
                            inv = []
                        if "', '" in lst[i+35]:
                            for ii in range("', '" in lst[i+35]):
                                inv8.append(lst[i+35].split("', '"))
                        else:
                            inv.append(lst[i+35])
                            inv8.append(inv)
                            inv = []
                        if "', '" in lst[i+40]:
                            for ii in range("', '" in lst[i+40]):
                                inv9.append(lst[i+40].split("', '"))
                        else:
                            inv.append(lst[i+40])
                            inv9.append(inv)
                            inv = []
                        if "', '" in lst[i+45]:
                            for ii in range("', '" in lst[i+45]):
                                inv10.append(lst[i+45].split("', '"))
                        else:
                            inv.append(lst[i+45])
                            inv10.append(inv)
                            inv = []
                        if "', '" in lst[i+50]:
                            for ii in range("', '" in lst[i+50]):
                                inv11.append(lst[i+50].split("', '"))
                        else:
                            inv.append(lst[i+45])
                            inv11.append(inv)
                            inv = []
                        if "', '" in lst[i+55]:
                            for ii in range("', '" in lst[i+55]):
                                inv12.append(lst[i+55].split("', '"))
                        else:
                            inv.append(lst[i+50])
                            inv12.append(inv)
                            inv = []
                        if "', '" in lst[i+60]:
                            for ii in range("', '" in lst[i+60]):
                                inv13.append(lst[i+60].split("', '"))
                        else:
                            inv.append(lst[i+60])
                            inv13.append(inv)
                            inv = []
                        if "', '" in lst[i+65]:
                            for ii in range("', '" in lst[i+65]):
                                inv14.append(lst[i+65].split("', '"))
                        else:
                            inv.append(lst[i+65])
                            inv14.append(inv)
                            inv = []
                        if "', '" in lst[i+70]:
                            for ii in range("', '" in lst[i+70]):
                                inv15.append(lst[i+70].split("', '"))
                        else:
                            inv.append(lst[i+70])
                            inv15.append(inv)
                            inv = []
                    for i in range(5):
                        if i == 0:
                            j = inv1
                        if i == 1:
                            j = inv2
                        if i == 2:
                            j = inv3
                        if i == 3:
                            j = inv4
                        if i == 4:
                            j = inv5
                        invA.append(j)
                    for i in range(5):
                        if i == 0:
                            j = inv6
                        if i == 1:
                            j = inv7
                        if i == 2:
                            j = inv8
                        if i == 3:
                            j = inv9
                        if i == 4:
                            j = inv10
                        invB.append(j)
                    for i in range(5):
                        if i == 0:
                            j = inv11
                        if i == 1:
                            j = inv12
                        if i == 2:
                            j = inv13
                        if i == 3:
                            j = inv14
                        if i == 4:
                            j = inv15
                        invC.append(j)
                    DespL = []
                    for i in range(3):
                        if i == 0:
                            j = invA
                        if i == 1:
                            j = invB
                        if i == 2:
                            j = invC
                        DespL.append(j)
                ligne = ligne + 1
            file.close()
            print("Chargement Terminé.")
            print("")
#Début
print("BIENVENU DANS LE TASSERAK. v1.1")
print("")
print("Un jeu dont vous êtes le Héro écrit en multiple possiblilté.")
print("Vous êtes libre d'évolué dans 4 dimension et plus.")
print("Vous allez où vous voulez quand vous le désiré et interagissez avec l'environnement. Vous pouvez regarder, prendre des choses les porté autre pare et transformé ce qui peux l'être.")
print("Bon Jeu. Signé l'auteur.")
print("")
key = input("Appuyez sur Enter pour commencé.")
print("")

while (game == 1):
    #Attaque Opportunité
    for ennemi in liste_ennemi:
        if ennemi in Objet[z][y][x]:
            ran = random.randint(0, 10)
            HP = HP - ran
    if (len(inventaire) >= (equip + 1)):
        arme = inventaire[equip].lower()
    else:
        arme = "Rien"
    if HP < 0:
        HP = 0
    """
    #Random Ennemi
    nom1 = ""
    nom2 = ""
    nom3 = ""
    nom = []
    print("Ennemis de Defi!")
    for i in range(random.randint(1, 6)):
        while(nom1 == nom2 or nom2 == nom3 or nom1 == nom3):
            nom1 = liste_ennemi[random.randint(0, len(liste_ennemi) - 1)]
            nom2 = liste_ennemi[random.randint(0, len(liste_ennemi) - 1)]
            nom3 = liste_ennemi[random.randint(0, len(liste_ennemi) - 1)]
        nom.append(liste_ennemi.index(nom1))
        nom.append(liste_ennemi.index(nom2))
        nom.append(liste_ennemi.index(nom3))
        nom = sorted(nom)
        nom[0] = liste_ennemi[nom[0]]
        nom[1] = liste_ennemi[nom[1]]
        nom[2] = liste_ennemi[nom[2]]
        #print(liste_ennemi.index(nom[0]),liste_ennemi.index(nom[1]),liste_ennemi.index(nom[2]))
        print("  ", nom[0], nom[1], nom[2])
        nom1 = ""
        nom2 = ""
        nom3 = ""
        nom = []
    """
    #Action
    print("********************************************************************************")
    print("HP:", HP, "  Score:", score, "  Action:", move, "  Équippement:", arme)
    dejavu = 0
    for i in range(len(timeline)):#Bug au chargement
        if (x == int(timeline[i].split(":")[4]) and y == int(timeline[i].split(":")[5]) and z == int(timeline[i].split(":")[3])):
            dejavu = 1
            #print("Vous avez un sentiment de DEJAVU...")
    #Lieux
    if upsidedown == 1:
        print(Lieux[z][y][x][0][::-1])
    else:
        print(Lieux[z][y][x][0])
    #Description lieux
    if dejavu == 1:
        if upsidedown == 1:
            print(DespL[z][y][x][0][::-1].split(". ")[0])
        else:
            print(DespL[z][y][x][0].split(". ")[len(DespL[z][y][x][0].split(". "))-1])
    else:
        dejavu = 0
        if upsidedown == 1:
            print(DespL[z][y][x][0][::-1])
        else:
            print(DespL[z][y][x][0])        
    #Objet(s) se trouventy ici.
    for i in range(len(Objet[z][y][x])):
        if Objet[z][y][x][i] == "":
            score = score #rien faire
        else:
            if Objet[z][y][x][i] == Objet[z][y][x][i].lower():
                if upsidedown == 1: #Objet local déplacable
                    if i == 0:
                        print(Objet[z][y][x][i][::-1], "Vous trouvez,"[::-1])
                    else:
                        print(Objet[z][y][x][i][::-1])
                else:
                    if i == 0:
                        print("Vous trouvez,", Objet[z][y][x][i])
                    else:
                        print(Objet[z][y][x][i])
            else:
                if upsidedown == 1: #Objet Environement fix
                    if i == 0:
                        print(Objet[z][y][x][i][::-1], "Il y a ici,"[::-1])
                    else:
                        print(Objet[z][y][x][i][::-1])
                else:
                    if i == 0:
                        print("Il y a ici,", Objet[z][y][x][i])
                    else:
                        print(Objet[z][y][x][i])
    #Info Combat
    for ennemi in liste_ennemi:
        if ennemi in Objet[z][y][x]:
            print("")
            if HP <= 0:
                print("")
                print("VOUS ÊTES MORT!")
                key = input("Appuyer sur Enter.")
                game = 0
                break
            else:
                print("VOUS ÊTES ATTAQUER!")
                if ran == 0:
                    print("Écheque critique!", ran)
                else:
                    print("Le monstre vous frappe!", ran, "point de dégas.")

    #Retroaction++
    for i in range(len(timeline)):
        move = ceil(move)
        if (move == int(timeline[i].split(":")[0][6:])):
            if (x == int(timeline[i].split(":")[4]) and y == int(timeline[i].split(":")[5]) and z == int(timeline[i].split(":")[3])):
                retroaction = timeline[i].split(":")[1][21:]
                retroinventaire = timeline[i].split(":")[2][18:]
                retroDespI = spaceline[i].split(":")[3]
                retroinventaire = list(retroinventaire[1:-1].split(","))#
                retroDespI = list(retroDespI[1:-1].split(","))#
                if (retroaction == ""):
                    if upsidedown == 1:
                        retroaction = "Rien."[::-1]
                    else:
                        retroaction = "Rien."
                if upsidedown == 1:
                    print(retroaction[::-1], "Vous voyez une personne qui s'apprête à faire"[::-1])
                    #print(retroinventaire[::-1], "Elle transporte avec elle"[::-1])
                else:
                    print("Vous voyez une personne qui s'apprête à faire", retroaction)
                    print("Elle transporte avec elle", retroinventaire)
                    #print(retroDespI)

    reponse = 0
    key = input("?")
    log.append(key)

    #Mode édition intéractive
    if (key.upper() == "/OBJET" or key.upper() == "/ITEM" or key.upper() == "/CHOSE"):
        print("'NOM OBJET' (Si Début par Majuscule = NON TRANSPORTABLE. Ex: 'Maison'=Non,'lettre'=Oui).")
        print("A0:", Objet[z][y][x])
        modif = input("Nommez Objet(au Sol): ")
        if modif == "":
            modif = "junk"
        if Objet[z][y][x] == []:
            Objet[z][y][x].append(modif)
            print("")
            print("'DESCRIPTION OBJET.' (Fait sa publicité et/ou donner indices quand vous l'examiné).")
            modif = input("Description Objet(au Sol): ")
            if modif == "":
                modif = "Juste de la cochonnerie."
            DespO[z][y][x].append(modif)
        else:
            print("B0:", Objet[z][y][x])
            test = input("Ajouter/Remplacé?[A/R]")
            if (test.upper() == "R"):
                if (len(Objet[z][y][x]) > 1):
                    print("Quel Objet Voulez-vous remplacer? Ex: 0)'"+Objet[z][y][x][0]+"', 1)'"+Objet[z][y][x][1]+"'")
                    r = input("Emplacement(#): ")
                    if (r.isdigit()):
                        r = abs(int(r))
                    else:
                        r = abs(int(r))
                        #Pourait ne pas y avoir de chiffre du tout??
                        if (r.isdigit()):
                            r = r
                        else:
                            r = 0
                    if (r <= len(Objet[z][y][x])):
                        Objet[z][y][x][r] = modif
                        print("")
                        print("'DESCRIPTION OBJET.' (Fait sa publicité et/ou donner indices quand vous l'examiné).")
                        modif = input("Description Objet(au Sol): ")
                        if modif == "":
                            modif = "Juste de la cochonnerie."
                        DespO[z][y][x][r] = modif
                    else:
                        Objet[z][y][x][-1] = modif
                        print("")
                        print("'DESCRIPTION OBJET.' (Fait sa publicité et/ou donner indices quand vous l'examiné).")
                        modif = input("Description Objet(au Sol): ")
                        if modif == "":
                            modif = "Juste de la cochonnerie."
                        DespO[z][y][x][-1] = modif
            else:
                test = "A" #Si l'usager se trompe de réponse Ajoute le dernier objet par default
            if (test.upper() == "A"):
                Objet[z][y][x].append(modif)
                print("")
                print("'DESCRIPTION OBJET.' (Fait sa publicité et/ou donner indices quand vous l'examiné).")
                modif = input("Description Objet(au Sol): ")
                if modif == "":
                    modif = "Juste de la cochonnerie."
                DespO[z][y][x].append(modif)

    if (key.upper() == "/ACTION" or key.upper() == "/TRESOR" or key.upper() == "/NOMMER" or key.upper() == "/NOM LIEUX" or key.upper() == "/LIEUX" or key.upper() == "/NOM"):
        print("(Nom Lieux), liste actions a faire avec ou sans OBJET(s),,,Nom objet")
        print("C0:", Lieux[z][y][x])
        modif1 = input("Nom_Lieux/Action/Nom_Objet: ")
        if modif1 == "":
            modif1 = "Nowhere"
        if Lieux[z][y][x] == []:
            Lieux[z][y][x].append(modif1)
            print("")
            print("D0:", Lieux[z][y][x])
            print("'Grand Description'. 'Petite Description'. 'Destinations possible.(Début MAJ)'")
            modif2 = input("Description Lieux: ")
            if modif2 == "":
                modif2 = "Juste au milieu de nulle part."
            DespL[z][y][x].append(modif2)
        else:
            test = input("Ajouter/Remplacé?[A/R]")
            if (test.upper() == "R"):
                if (len(Lieux[z][y][x]) > 1):
                    print("Quel Element voulez-vous remplacer? Ex: 0)Nom '", Lieux[z][y][x][0], "', 1)Action1,'", Lieux[z][y][x][1],"'")
                    r = input("Emplacement(#): ")
                    if (r.isdigit()):
                        r = abs(int(r))
                    else:
                        r = abs(int(r))
                        #Pourait ne pas y avoir de chiffre du tout??
                        if (r.isdigit()):
                            r = r
                        else:
                            r = 0
                    if (r <= len(Lieux[z][y][x])):
                        Lieux[z][y][x][r] = modif1
                        print("")
                        print("'LIEUX/ACTION/OBJET' (Nommer Lieux/Objet ou Donner phrase action).")
                        modif2 = input("Nom_Lieux-Objet/Syntaxe: ")
                        if modif2 == "":
                            modif2 = "Juste au milieu de nulle part."
                        DespL[z][y][x][r] = modif2
                    else:
                        Lieux[z][y][x][-1] = modif1
                        print("")
                        print("'LIEUX/ACTION/OBJET' (Nommer Lieux/Objet ou Donner phrase action).")
                        modif2 = input("Nom_Lieux-Objet/Syntaxe: ")
                        if modif2 == "":
                            modif2 = "Juste au milieu de nulle part."
                        DespL[z][y][x][-1] = modif2
            else:
                test = "A" #Si l'usager se trompe de réponse Ajoute le dernier objet par default
            if (test.upper() == "A"):
                Lieux[z][y][x].append(modif)
                print("")
                print("'ACTION/OBJET' (Donner phrase action ou Nommer Objet).")
                print("ATTENTION, Il ne peux y avoir un seul Objet a la fin!")
                modif = input("Syntaxe ou Nom: ")
                if modif == "":
                    modif = "Juste au milieu de nulle part."
                DespL[z][y][x].append(modif)

    if (key.upper() == "/INVENTAIRE"):
        print("'NOM OBJET' (Minuscule=TRANSPORTABLE).")
        print("E0:", inventaire)
        modif = input("Nommez un Objet(dans inventaire): ")
        if modif == "":
            modif = "junk"
        if inventaire == []:
            inventaire.append(modif.lower())
            print("")
            print("'DESCRIPTION OBJET.' (Fait sa publicité et/ou donner indices quand vous l'examiné).")
            print("F0:", DespI)
            modif = input("Description Objet(dans inventaire): ")
            if modif == "":
                modif = "Juste une cochonnerie."
            DespI.append(modif)
        else:
            test = input("Ajouter/Remplacé?[A/R]")
            if (test.upper() == "R"):
                if (len(inventaire) > 1):
                    print("Quel Objet Voulez-vous remplacer? Ex:0", inventaire[0], "1", inventaire[1])
                    r = input("Emplacement(#): ")
                    if (r.isdigit()):
                        r = abs(int(r))
                    else:
                        r = abs(int(r))
                        #Pourait ne pas y avoir de chiffre du tout??
                        if (r.isdigit()):
                            r = r
                        else:
                            r = 0
                    if (r <= len(inventaire)):
                        inventaire[r] = modif
                        print("")
                        print("'DESCRIPTION OBJET.' (Fait sa publicité et/ou donner indices quand vous l'examiné).")
                        modif = input("Description Objet(dans inventaire): ")
                        if modif == "":
                            modif = "Juste une cochonnerie."
                        DespI[r] = modif
                    else:
                        inventaire[-1] = modif
                        print("")
                        print("'DESCRIPTION OBJET.' (Fait sa publicité et/ou donner indices quand vous l'examiné).")
                        modif = input("Description Objet(dans inventaire): ")
                        if modif == "":
                            modif = "Juste une cochonnerie."
                        DespI[-1] = modif
            else:
                test = "A" #Si l'usager se trompe de réponse Ajoute le dernier objet par default
            if (test.upper() == "A"):
                inventaire.append(modif)
                print("")
                print("'DESCRIPTION OBJET.' (Fait sa publicité et/ou donner indices quand vous l'examiné).")
                modif = input("Description Objet(dans inventaire): ")
                if modif == "":
                    modif = "Juste une cochonnerie."
                DespI.append(modif)
                
    #Plus grande simplification
    inv = str(inventaire)[1:-1].replace("', '", ",")
    despi = str(DespI)[1:-1].replace(", ", ",")
    despo = str(DespO[z][y][x])[1:-1].replace(", ", ",")
    lieu = str(Lieux[z][y][x][0]).replace(", ", ",")
    despl = str(DespL[z][y][x][0]).replace(", ", ",")
    obj = str(Objet[z][y][x])[1:-1].replace("', '", ",")
    timeline.append("Point " + str(move) + ":Vous pensiez à faire " + key + ":Vous transportiez " + inv + ":" + str(z)  + ":" + str(x)  + ":" + str(y))
    spaceline.append("Vous étiez dans " + str(lieu) + ":Vous voyez que " + str(despl) + ":Il y avait aussi " + str(obj) + ":" + str(despi) + ":" + str(despo))
    move = move + (temps * speed)

    #Equipper Arme
    if (key[0:8].lower() == "équipper"):
        if (key[9:].lower() in inventaire):
            if (key[9:].lower() in liste_arme):
                equip = int(inventaire.index(key[9:].lower()))
                reponse = 1
                print("Fait!")
            else:
                print(key[9:].lower(), "n'est pas une arme reconnu!")
                new = input("Voulez-vous qu'elle le soit?[O/N]")
                if new.upper() == "O":
                    liste_arme.append(key[9:].lower())
                    print("Fait.")
                    reponse = 1
        else:
            print("Vous n'avais pas de", key[9:].lower())

    #Action Quête
    if (key.lower() in Lieux[z][y][x]): #vérif. de la syntaxe clé
        message = 0
        for i in range(len(key.split(" "))):
            if ((key.split(" ")[i] in inventaire) or (key.split(" ")[i].lower() in str(Objet[z][y][x]).lower())): #cherche si mot clé existe dans inv ou area
                #liste ennemi dans la même case
                for ii in range(len(liste_ennemi)):
                    if liste_ennemi[ii] in Objet[z][y][x]: #if (("Zombie" in Objet[z][y][x]) or ("Mort-Vivant" in Objet[z][y][x]) or ("Squelette" in Objet[z][y][x]) or ("Monstre" in Objet[z][y][x]) or ("Troll" in Objet[z][y][x]) or ("Géant" in Objet[z][y][x]) or ("Vampire" in Objet[z][y][x]) or ("Loup-garou" in Objet[z][y][x]) or ("Soldat" in Objet[z][y][x]) or ("Chevalier" in Objet[z][y][x]) or ("Démon" in Objet[z][y][x]) or ("Diable" in Objet[z][y][x]) or ("Farfadet" in Objet[z][y][x]) or ("Lutin" in Objet[z][y][x]) or ("Cobold" in Objet[z][y][x]) or ("Gobbline" in Objet[z][y][x]) or ("Orc" in Objet[z][y][x]) or ("Dragon" in Objet[z][y][x]) or ("Dinosaure" in Objet[z][y][x]) or ("Reptil" in Objet[z][y][x]) or ("Loup" in Objet[z][y][x]) or ("Serpant" in Objet[z][y][x]) or ("Basilic" in Objet[z][y][x]) or ("T-Rex" in Objet[z][y][x]) or ("Ogre" in Objet[z][y][x]) or ("Sangsus" in Objet[z][y][x]) or ("Écorcheur" in Objet[z][y][x]) or ("Magicien" in Objet[z][y][x]) or ("Mage" in Objet[z][y][x]) or ("Sorcier" in Objet[z][y][x]) or ("Bug" in Objet[z][y][x]) or ("Fourmis" in Objet[z][y][x]) or ("Rapace" in Objet[z][y][x]) or ("Brigan" in Objet[z][y][x]) or ("Fou" in Objet[z][y][x]) or ("Tour" in Objet[z][y][x]) or ("Prètre" in Objet[z][y][x]) or ("Mandiant" in Objet[z][y][x]) or ("Féroce" in Objet[z][y][x]) or ("Minautor" in Objet[z][y][x]) or ("Sorcière" in Objet[z][y][x]) or ("Mommie" in Objet[z][y][x]) or ("Abobinadle" in Objet[z][y][x]) or ("Maléfique" in Objet[z][y][x]) or ("Seigneur" in Objet[z][y][x]) or ("Ténèbre" in Objet[z][y][x]) or ("Insecte" in Objet[z][y][x]) or ("Scorpion" in Objet[z][y][x]) or ("Pieuvre" in Objet[z][y][x]) or ("Mutand" in Objet[z][y][x]) or ("Prisonnier" in Objet[z][y][x]) or ("Psycopate" in Objet[z][y][x])):
                        #liste d'arme populaire
                        if inventaire[equip] in liste_arme:
                            if message == 0:
                                print("Fait.")
                                print("")
                                print(DespL[z][y][x][Lieux[z][y][x].index(key.lower())]) #Révèle une Description Action pré-enregistré DespL
                                message = 1
                            if key.split(" ")[i] in inventaire:
                                del DespI[inventaire.index(key.split(" ")[i])] #efface description objet dans inventaire même position
                                inventaire.remove(key.split(" ")[i]) #retire le première objet mentionner
                                print(key.split(" ")[i], "sort de l'inventaire.")
                            reponse = 1
                            score = score + 5
                        else:
                            print("Vous n'est pas armé!")
                            log.pop() #retir cette dernière commande de la réalité :P
                    else:
                        if message == 0:
                            print("Fait.")
                            print("")
                            print(DespL[z][y][x][Lieux[z][y][x].index(key.lower())]) #Révèle une Description Action pré-enregistré DespL
                            message = 1
                        if key.split(" ")[i] in inventaire:
                            del DespI[inventaire.index(key.split(" ")[i])] #efface description objet dans inventaire même position
                            inventaire.remove(key.split(" ")[i]) #retire le première objet mentionner
                            print(key.split(" ")[i], "sort de l'inventaire.")
                        reponse = 1
                        score = score + 5
        ok = 0
        # Il faut que toute les actions soit dite correctement au moins 1 fois
        Xcond = len(Lieux[z][y][x]) - 2
        for i in range(Xcond):
            if (str(Lieux[z][y][x][i+1]).lower() in str(log).lower()): #erreur minuscule
                ok = ok + 1
        if (ok >= Xcond): #pourrait faire bug si plus d'une quête inachevé en parallèle
            #ok = 0
            Objet[z][y][x].append(Lieux[z][y][x][-1]) #fait apparaitre là objet en fin de liste
            DespO[z][y][x].append(DespL[z][y][x][-1]) #ajoute la description dans liste lieux
            for iv in range(len(liste_ennemi)):
                if liste_ennemi[iv] in Objet[z][y][x]:#retir le monstre
                    Objet[z][y][x].remove(liste_ennemi[iv])
            #Liste de créature
            Lieux[z][y][x].remove(Lieux[z][y][x][-1]) #Efface l'objet de la quête liste
            DespL[z][y][x].remove(DespL[z][y][x][-1]) #Efface la description dans lieux
            for j in range(Xcond):
                ok = ok - 1 #Soustrait que le nécessaire
                Lieux[z][y][x].remove(Lieux[z][y][x][-1]) #Efface l'étape de la quête liste
                DespL[z][y][x].remove(DespL[z][y][x][-1]) #Efface description de l'étape aussi ??
            Xcond = 0
            if ok < 0: #si l'impossible se produit
                ok = 0
    #Temps
    if (key.lower() == "attendre" or key.lower() == ""):
        reponse = 1
        print("Le temps passe.")
    if (key.lower() == "reposer" or key.lower() == "repos" or key.lower() == "dormir"):
        reponse = 1
        print("Le temps passe. Vous vous réveillez plus tard en pleine forme.")
    if (key.lower() == "stop" or key.lower() == "pause"):
        reponse = 1
        print("Le temps s'arrête.")
        speed = 0
    if (key.lower() == "play" or key.lower() == "go"):
        reponse = 1
        print("Le temps est repartie.")
        speed = 1
    if (key.lower() == "ralentir"):
        reponse = 1
        if (abs(speed) == .5):
            print("Le temps ralentie.")
        if (speed == 0):
            print("Le temps s'arrête.")
        if (speed > 0):
            speed = speed - .5
        else:
            print("Vous ne pouvez pouvez plus ralentir.")
    if (key.lower() == "accélèrer"):
        reponse = 1
        print("Le temps accélère.")
        if (speed < 2.5):
            speed = speed + .5
        else:
            print("Vous ne pouvez pas aller plus vite.")
        if (abs(speed) == .5):
            print("Le temps ralentie.")
        if (speed == 0):
            print("Le temps s'arrête.")
    if (key.lower() == "reculé" or key.lower() == "reculé le temps" or key.lower() == "reculé dans le temps" or key.lower() == "reculé dans temps" or key.lower() == "revenir en arrière" or key.lower() == "revenir dans passé"):
        reponse = 1
        print("Le temps recule.")
        temps = -1
    if (key.lower() == "avancé" or key.lower() == "avancé le temps" or key.lower() == "avancé dans temps" or key.lower() == "revenir en avant" or key.lower() == "revenir dans futur"):
        print("Le temps passe.")
        reponse = 1
        temps = 1
    if (key.lower() == "voyager dans le temps" or key.lower() == "voyage temporelle" or key.lower() == "voyager temps" or key.lower() == "voyager dans temps" or key.lower() == "voyage passé" or key.lower() == "voyage futur" or key.lower() == "voyage temps"):
        reponse = 1
        warp = input("Penser à un chiffre?")
        print("Vous faite un saut dans le temps de", int(warp), "unité.")
        move = move + int(warp)
        print("Voila.")
    if (key.lower() == "matrix"):
        reponse = 1
        print("DespO:", DespO)
        print(Objet)
        print("DespI", DespI)
        print(inventaire)
        print("TimeLine",timeline)
        print("SpaceLine",spaceline)
        test = input("Enter")
    if (key.lower() == "vision" or key.lower() == "vision temps" or key.lower() == "vision passé" or key.lower() == "flash back" or key.lower() == "phaser temps"):
        reponse = 1
        evenement = input("Concentré vous sur un chiffre?")
        evenement = ceil(int(evenement))
        if (evenement):
            if (int(evenement) <= move):
                print("")
                print("Parfait. Vous fermez les yeux et vous vous projeté dans un souvenir...")
                for i in range(3):
                    print(timeline[int(evenement)].split(":")[i])
                    print(spaceline[int(evenement)].split(":")[i])
                print("...Puis la vision s'arrête.")
            else:
                print(timeline)
                if evenement in timeline: #?
                    for i in range(3):
                        print(timeline.index(evenement).split(":")[i])
                        print(spaceline.index(evenement).split(":")[i])
                        print("...Puis la vision s'arrête.")
                else:
                    print("Les brumes de l'avenir sont incertaines.")
        else:
            print("Vous n'êtes pas asser cencentré.")
    if (key.lower() == "téléporter" or key.lower() == "saut espace"):
        reponse = 1
        coordonner = input("Concentré sur les coordonnées x,y,z?")
        if (coordonner): #zxy
            if (int(coordonner.split(",")[0]) >= 0 and int(coordonner.split(",")[1]) >= 0 and int(coordonner.split(",")[2]) >= 0 and int(coordonner.split(",")[0]) < 5 and int(coordonner.split(",")[1]) < 5 and int(coordonner.split(",")[2]) < 3):
                print("Parfait. Vous fermez votre esprit sur le lieu imaginé...")
                x = int(coordonner.split(",")[0])
                y = int(coordonner.split(",")[1])
                z = int(coordonner.split(",")[2])
                print("Fait.")
            else:
                print("Ce lieux n'est pas accessible.")
        else:
            print("Vous n'êtes pas concentré.")
    if (key.lower() == "retroaction" or key.lower() == "retroaction temps" or key.lower() == "voyager passé" or key.lower() == "voyager temps"):
        reponse = 1
        evenement = input("Concentré vous sur un chiffre?")
        if (evenement):
            if (int(evenement) <= move): # Voyage temporelle
                print("Parfait. Vous fermez votre esprit et vous voyager dans le temps...")
                z = int(timeline[int(evenement)].split(":")[3])
                x = int(timeline[int(evenement)].split(":")[4])
                y = int(timeline[int(evenement)].split(":")[5])
                move = int(timeline[int(evenement)].split(":")[0][6:])
                Lieux[z][y][x] = []
                Lieux[z][y][x].append(spaceline[int(evenement)].split(":")[0][16:])
                inventaire = []
                DespI = []
                if (len(list(timeline[int(evenement)].split(":")[2][20:-2].split("', '"))) > 1):
                    #Ca marche seulement si plus d'un objet
                    for i in range(len(timeline[int(evenement)].split(":")[2][20:-2].split("', '"))):
                        inventaire.append(timeline[int(evenement)].split(":")[2][20:-2].split("', '")[i])
                else:
                    #Ca marche si seulement 1 objet
                    inventaire.append(timeline[int(evenement)].split(":")[2][20:-2])
                if (len(list(spaceline[int(evenement)].split(":")[3][2:-2].split("', '"))) > 1):
                    for i in range(len(spaceline[int(evenement)].split(":")[3][2:-2].split("', '"))):
                        DespI.append(spaceline[int(evenement)].split(":")[3][2:-2].split("', '")[i]) #Bug retroaction ??
                else:
                    DespI.append(spaceline[int(evenement)].split(":")[3][2:-2])
                DespL[z][y][x] = []
                DespL[z][y][x].append(spaceline[int(evenement)].split(":")[1])
                Objet[z][y][x] = []
                DespO[z][y][x] = []
                if (len(list(spaceline[int(evenement)].split(":")[2][17:-2].split("', '"))) > 1):
                    for i in range(len(spaceline[int(evenement)].split(":")[2][17:-2].split("', '"))):
                        Objet[z][y][x].append(spaceline[int(evenement)].split(":")[2][17:-2].split("', '")[i])
                        DespO[z][y][x].append(spaceline[int(evenement)].split(":")[4][2:-2].split('", "')[i])
                else:
                    Objet[z][y][x].append(spaceline[int(evenement)].split(":")[2][17:-2])
                    DespO[z][y][x].append(spaceline[int(evenement)].split(":")[4][2:-2])
            else:
                print("Les brumes de l'avenir sont incertaines.")
        else:
            print("Vous n'êtes pas assez concentré.")

    #Monde a l'enver
    if (key.lower() == "upsidedown" or key.lower() == "autre dimension" or key.lower() == "monde a l'enver" or key.lower() == "changer dimension"):
        reponse = 1
        print("Vous passez dans l'autre dimension et voyez que la végétation et les pierres change de couleur. Le jour est la nuit aussi ont changé de place")
        if upsidedown == 1:
            upsidedown = 0
            print("Mais le Monde est revenu à sa transposé d'origine...")
            print("...Tout reviens en marche avant.")
            temps = 1
        else:
            upsidedown = 1
            print("Les angles sont anormal par ici, vous devez ajusté votre navigation...")
            print("...Tout semble être en marche arrière.")
            temps = -1
        print("")

    #Navigation
    if (key.lower() == "est" or key.lower() == "e"):
        reponse = 1
        if (('Est' in DespL[z][y][x][0]) or ('Est' in Objet[z][y][x])):
            if upsidedown == 0:
                x = x + 1
            else:
                y = y + 1
        else:
            print("Vous ne pouvez aller dans cette direction.")
    if (key.lower() == "ouest" or key.lower() == "o"):
        reponse = 1
        if (('Ouest' in DespL[z][y][x][0]) or ('Ouest' in Objet[z][y][x])):
            if upsidedown == 0:
                x = x - 1
            else:
                y = y - 1
        else:
             print("Vous ne pouvez aller dans cette direction.")
    if (key.lower() == "sud" or key.lower() == "s"):
        reponse = 1
        if (('Sud' in DespL[z][y][x][0]) or ('Sud' in Objet[z][y][x])):
            if upsidedown == 0:
                y = y + 1
            else:
                x = x + 1
        else:
            print("Vous ne pouvez aller dans cette direction.")
    if (key.lower() == "nord" or key.lower() == "n"):
        reponse = 1
        if (('Nord' in DespL[z][y][x][0]) or ('Nord' in Objet[z][y][x])):
            if upsidedown == 0:
                y = y - 1
            else:
                x = x - 1
        else:
            print("Vous ne pouvez aller dans cette direction.")
    if (key.lower() == "sud-ouest" or key.lower() == "sud ouest" or key.lower() == "so"):
        reponse = 1
        if (('SO' in DespL[z][y][x][0]) or ('SO' in Objet[z][y][x])):
            if upsidedown == 0:
                x = x - 1
                y = y + 1
            else:
                y = y - 1
                x = x + 1
        else:
            print("Vous ne pouvez aller dans cette direction.")
    if (key.lower() == "nord-ouest" or key.lower() == "nord ouest" or key.lower() == "no"):
        reponse = 1
        if (('NO' in DespL[z][y][x][0]) or ('NO' in Objet[z][y][x])):
            #if upsidedown == 0: no need
            x = x - 1
            y = y - 1
        else:
            print("Vous ne pouvez aller dans cette direction.")
    if (key.lower() == "sud-est" or key.lower() == "sud est" or key.lower() == "se"):
        reponse = 1
        if (('SE' in DespL[z][y][x][0]) or ('SE' in Objet[z][y][x])):
            y = y + 1
            x = x + 1
        else:
            print("Vous ne pouvez aller dans cette direction.")
    if (key.lower() == "nord-est" or key.lower() == "nord est" or key.lower() == "ne"):
        reponse = 1
        if (('NE' in DespL[z][y][x][0]) or ('NE' in Objet[z][y][x])):
            if upsidedown == 0:
                y = y - 1
                x = x + 1
            else:
                x = x - 1
                y = y + 1
        else:
            print("Vous ne pouvez aller dans cette direction.")
    if (key.lower() == "monter" or key.lower() == "grimper" or key.lower() == "escalader" or key.lower() == "aller en haut"):
        reponse = 1
        if (('Monter' in DespL[z][y][x][0]) or ('Monter' in Objet[z][y][x])):
            z = z + 1
        else:
            print("Vous ne savez pas volé.")
    if (key.lower() == "tunel" or key.lower() == "bouche-égou" or key.lower() == "descendre" or key.lower() == "glisser" or key.lower() == "en rappel" or key.lower() == "aller en bas"):
        reponse = 1
        if (('Tunel' in DespL[z][y][x][0]) or ('Bouche-Égou' in DespL[z][y][x][0]) or ('Descendre' in DespL[z][y][x][0]) or ('Descendre' in Objet[z][y][x])):
            z = z - 1
        else:
            print("Vous ne pouvez pas descendre.")        
        
    #Gestion objets
    if (key.lower() == "inventaire"):
        reponse = 1
        print("Vous cherchez dans vos poches est trouver:")
        if (inventaire):
            for i in range(len(inventaire)):
                print(inventaire[i])
        else:
            print("Vous avez les mains vide.")
    """        
    if (key.lower() == "regarder tout" or key.lower() == "examiner tout"):
        print("Vous n'avez pas la capacité d'observation global.")
       """ 
    if (key[0:8].lower() == "regarder" or key[0:8].lower() == "examiner"):
        reponse = 1
        if (key[9:]): #Si regarder nom objet
            if (key[9:].lower() in str(Objet[z][y][x]).lower()): # Cherche dans environnement 1er
                for i in range(len(DespO[z][y][x])):
                    if (str(Objet[z][y][x][i]).lower() == key[9:].lower()):
                        print(DespO[z][y][x][i])
                        key = ""
                    if (key[9:].lower() == " tout"): #capacité observation global Env
                        print(Objet[z][y][x][i], ": ", DespO[z][y][x][i])
                        key = ""
            else:
                if (inventaire): #Cherche Inventaire 2e
                    if (key[9:] in inventaire):
                        for i in range(len(inventaire)):
                            if (inventaire[i] == key[9:]):
                                print(DespI[i])
                                key = ""
                            if (key[9:].lower() == " tout"): #capacité d'observation global Inv
                                print(inventaire[i], ": ", DespI[i])
                                key = ""
                else:
                    print("Vous ne voyez aucun", key[9:], "ici.")
        else: #Si il doit précisé recherche
            print("Que voulez-vous ", key[0:8].lower(), "?")
            if (Objet[z][y][x]):
                objet = input("?")
                if (objet):
                    if (objet in Objet[z][y][x]):
                        for i in range(len(Objet[z][y][x])): #Cherche Objet
                            if (Objet[z][y][x][i] == objet):
                                print(DespO[z][y][x][i]) #lit description coord
                                key = ""
                    else:
                        if (objet in inventaire):
                            for i in range(len(inventaire)):
                                if (inventaire[i] == objet):
                                    print(DespI[i])
                                    key = ""
                else:
                    print("Rien?")
            else:
                print("Pas de trace d'objet par ici.")

    if (key.lower() == "tout jeté" or key.lower() == "tout déposé" or key.lower() == "jeté tout" or key.lower() == "déposé tout"):
        reponse = 1
        #Si vous avez encore un ou plusieurs objet
        if (inventaire):
            print("Vous jettez tout par terre.")
            for i in range(len(inventaire)):
                Objet[z][y][x].append(inventaire[i])
                DespO[z][y][x].append(DespI[i]) #Bug retroaction
                if inventaire[i] == "dés":
                    jet = random.randint(1, roll)
                    print("Le dés magique roule sur", jet)
                    if jet == 1: #Mort
                        HP = 0
                    if jet == 2: #Empoisonement
                        HP = HP - 10
                        print("(Poison! Vous perdez de la force).")
                    if jet == 3: #soin mineur
                        HP = HP + 15
                        score = score + 5
                        print("(Adrénaline! Vous récupérez de la force).")
                    if jet == 4: #Total guerrison
                        HP = 100
                        score = score + 10
                        print("(Résurection! Votre santé vous revien).")
                    if jet == 5: #efface 1 ennemi
                        for ennemi in Objet[z][y][x]:
                            if ennemi in liste_ennemi:
                                DespO[z][y][x].remove(DespO[z][y][x][Objet[z][y][x].index(ennemi)])
                                Objet[z][y][x].remove(ennemi)
                                print("("+ennemi, "disparait!)")
                                score = score + 5
                                break
                    if jet == 6: #efface tout ennemi
                        for ennemi in Objet[z][y][x]:
                            if ennemi in liste_ennemi:
                                DespO[z][y][x].remove(DespO[z][y][x][Objet[z][y][x].index(ennemi)])
                                Objet[z][y][x].remove(ennemi)
                                print("("+ennemi, "disparait!)")
                                score = score + 5
            inventaire = []
            DespI = []
            print("Fait.")
            #for i in range(len(Objet[z][y][x])): #Efface erreurs possible
                #if (Objet[z][y][x][i] == ""):
                    #Objet[z][y][x].remove(Objet[z][y][x][i])
            #for i in range(len(DespO[z][y][x])):
                #if (DespO[z][y][x][i] == ""):
                    #DespO[z][y][x].remove(DespO[z][y][x][i])
            key = ""
        else:
            print("Vous avez les mains vide.")
    if (key.lower() == "tout prendre" or key.lower() == "tout ramassé" or key.lower() == "prendre tout" or key.lower() == "ramassé tout"):
        reponse = 1
        #Si il y a un ou plusieurs objet ici
        if (Objet[z][y][x]):
            print("Vous prenez tout ce qu'il y a par terre.")
            #for i in range(len(inventaire)):
                #if (inventaire[i] == ""):
                    #inventaire.remove(inventaire[i])
            #for i in range(len(DespI)):
                #if (DespI[i] == ""):
                    #DespI.remove(DespI[i]) #Efface des espaces vide
            for i in range(len(Objet[z][y][x])):
                objet = Objet[z][y][x][i]
                if (objet[0] == objet[0].upper()):
                    #Test Maj compte pour Gros Encombrement
                    print(objet, "est trop lourd pour être transporter.")
                else:
                    if (len(inventaire) <= maxitem):
                        inventaire.append(Objet[z][y][x][i]) #ajoute tous les objets
                        DespI.append(DespO[z][y][x][i]) #récupère tous les descriptions attaché
                        Objet[z][y][x][i] = "" #remplace l'objet du sol par vide
                        DespO[z][y][x][i] = ""
                    else:
                        print("Vous n'avez pas la place pour ça.")
            for i in range(len(DespO)):
                if (DespO[i] == ""):
                    DespO.remove(DespO[i])
            for i in range(len(Objet)):
                if (Objet[i] == ""):
                    Objet.remove(Objet[i]) #Efface espace vide ensuite
            print("Fait.")
            key = ""
        else:
            print("Vous ne trouvez rien.")
        if Objet[z][y][x] == []:
            Objet[z][y][x].append('')
        if DespO[z][y][x] == []:
            DespO[z][y][x].append('')

    if (key[0:7].lower() == "prendre" or key[0:7].lower() == "ramassé"):
        #Ramassé un objet par terre ou sur son homolog
        reponse = 1
        test = 0
        if (key[8:]):
            chercher = key[8:].lower()
            #Thief paradox
            for i in range(len(timeline)):
                move = ceil(move)
                if (move == int(timeline[i].split(":")[0][6:])):
                    if ((x == int(timeline[i].split(":")[4])) and (y == int(timeline[i].split(":")[5])) and (z == int(timeline[i].split(":")[3]))):            
                        #print("***")
                        if (chercher in retroinventaire):
                            inventaire.append(chercher)
                            for i in range(len(retroinventaire)):
                                if (retroinventaire[i].lower() == chercher):
                                    DespI.append(retroDespI[i]) #si ca marche j'ai mon voyage
                                    retroDespI.remove(retroDespI[i]) #Il l'ajoute a la fin et le retir a son dernier emplacement
                            retroinventaire.remove(chercher)
                            if (retroinventaire == []):
                                retroinventaire.append('')
                            print("Anachronisme détecté.")
                            chercher = ""
                            test = 1
                        else:
                            print("Impossible de volé", key[0:7], chercher+".")
            if (chercher in Objet[z][y][x]):
                inventaire.append(chercher)
                for i in range(len(Objet[z][y][x])):
                    if (Objet[z][y][x][i].lower() == chercher):
                        DespI.append(DespO[z][y][x][i]) #j'ai retiré .lower() pour conserver l'intégrité de la description
                        DespO[z][y][x].remove(DespO[z][y][x][i])
                Objet[z][y][x].remove(chercher)
                if (Objet[z][y][x] == []):
                    Objet[z][y][x].append('')
                print("Fait.")
                key = ""
            else:
                if test == 0:
                    print("Impossible de", key[0:7], chercher+".")
        else:
            if (Objet[z][y][x]):
                print("Que voulez-vous", key[0:7]+"?")
                key = input("?")
                if (key):
                    if (key in Objet[z][y][x]):
                        for i in range(len(inventaire)):
                            if (inventaire[i] == ""):
                                inventaire.remove(inventaire[i])
                        for i in range(len(Objet[z][y][x])):
                            if (Objet[z][y][x][i] == ""):
                                Objet[z][y][x].remove(Objet[z][y][x][i])
                        #if (inventaire.count(key) == 2):
                            #inventaire.append("paire de " + key)
                        #else:
                            #inventaire.append(key)
                        for i in range(len(Objet[z][y][x])):
                            if (Objet[z][y][x][i] == key):
                                DespI.append(DespO[z][y][x][i])
                                DespO[z][y][x].remove(DespO[z][y][x][i])
                        Objet[z][y][x].remove(key)
                        print("Fait.")
                        key = ""
                    else:
                        print("Pas de trace de", key, "par ici.")
            else:
                print("Il n'y a rien par ici.")
    if (key[0:4].lower() == "jeté" or key[0:5].lower() == "lancé" or key[0:5].lower() == "boire" or key[0:5].lower() == "mangé" or key[0:5].lower() == "avalé"):
        reponse = 1
        if (key.split(" ")[1]):
            objet = key.split(" ")[1].lower()
            if (objet in inventaire):
                if (key.split(" ")[0].lower() == "jeté" or key.split(" ")[0].lower() == "lancé"):
                    Objet[z][y][x].append(objet)
                for i in range(len(inventaire)):
                    if (objet == inventaire[i]):
                        if (key.split(" ")[0].lower() == "jeté" or key.split(" ")[0].lower() == "lancé"):
                            DespO[z][y][x].append(DespI[i].lower())
                        else:
                            if objet in liste_soin:
                                soin = random.randint(1, roll)
                                HP = HP + soin
                                print(soin, "point(s) de santé ajouté.")
                            else:
                                print("Vous essaillez de", objet, "mais vous recraché immédiatement!")
                        DespI.remove(DespI[i])
                        break
                inventaire.remove(objet)
                if key[5:] == "dés":
                    jet = random.randint(1, roll)
                    print("Le dés magique roule sur", jet)
                    if jet == 1: #Mort
                        HP = 0
                    if jet == 2: #Empoisonement
                        HP = HP - 10
                        print("(Poison! Vous perdez de la force).")
                    if jet == 3: #soin mineur
                        HP = HP + 15
                        score = score + 5
                        print("(Adrénaline! Vous récupérez de la force).")
                    if jet == 4: #Total guerrison
                        HP = 100
                        score = score + 10
                        print("(Résurection! Votre santé vous revien).")
                    if jet == 5: #efface 1 ennemi
                        for ennemi in Objet[z][y][x]:
                            if ennemi in liste_ennemi:
                                DespO[z][y][x].remove(DespO[z][y][x][Objet[z][y][x].index(ennemi)])
                                Objet[z][y][x].remove(ennemi)
                                print("("+ennemi, "disparait)!")
                                score = score + 5
                                break
                    if jet == 6: #efface tout ennemi
                        for ennemi in Objet[z][y][x]:
                            if ennemi in liste_ennemi:
                                DespO[z][y][x].remove(DespO[z][y][x][Objet[z][y][x].index(ennemi)])
                                Objet[z][y][x].remove(ennemi)
                                print("("+ennemi, "disparait)!")
                                score = score + 5
                print("Fait.")
                for i in range(len(Objet[z][y][x])): #Efface les erreurs
                    if (Objet[z][y][x][i] == ""):
                        Objet[z][y][x].remove(Objet[z][y][x][i])
                for i in range(len(DespO[z][y][x])):
                    if (DespO[z][y][x][i] == ""):
                        DespO[z][y][x].remove(DespO[z][y][x][i])
                key = ""
            else:
                print("Vous n'avez pas de", objet, "dans vos poches.")
        else:
            if (inventaire):
                print("Que voulez-vous",key[0:5],"?")
                objet = input("?")
                if (objet):
                    if (objet in inventaire):
                        for i in range(len(Objet[z][y][x])):
                            if (Objet[z][y][x][0] == ""):
                                Objet[z][y][x].remove(Objet[z][y][x][0])
                            if (DespO[z][y][x][0] == ""):
                                DespO[z][y][x].remove(DespO[z][y][x][0])
                        Objet[z][y][x].append(objet.lower())
                        for i in range(len(inventaire)):
                            if (objet == inventaire[i]):
                                DespO[z][y][x].append(DespI[i].lower())
                                DespI.remove(DespI[i])
                        inventaire.remove(objet)
                        if key[5:] == "dés":
                            print(random.randint(1, roll))
                        print("Fait.")
                        key = ""
                    else:
                        print("Pas de trace de", objet, "dans vos poches.")
            else:
                print("Vous n'avez que vos mains vide.")

    #Autre commandes
    if (key.lower() == "help" or key.lower() == "aide" or key.lower() == "?" or key.lower() == "cmd" or key.lower() == "commande"):
        reponse = 1
        print("Pour navigué dans cette univers les commandes de base sont: quit,")
        print("nord, sud, est, ouest, monté, descendre, regarder, prendre, jetté,")
        print("inventaire, nord est, nord ouest, sud est, sud ouest, attendre,")
        print("tout jetté, tout ramassé, vision, téléporter, save, load, aide,")
        print("pause, go, reculé, avancé, accélèrer, ralentir, voyage temps,")
        print("Edition Interactive: /objet, /lieux, /action, /inventaire.")
        
    if (key.lower() == "save" or key.lower() == "enregistrer" or key.lower() == "sauvegarder"):
        reponse = 1
        source = input("Nom ?(Default 'jeu-save.txt')")
        if (source == ""): #Default 'jeu-save.txt'
            source = sourcefile
        if (source[-4:] == ".txt"):
            source = source
        else:
            source = source + ".txt"
        if (os.path.exists(Rep + source) == True): #Efface la dernière
            os.remove(source)
        else:
            print("Nouveau fichier", source, "créer.")
        file = open(Rep + source.upper(), "a")
        file.write(str(x) + "\n") #integer
        file.write(str(y) + "\n")
        file.write(str(z) + "\n")
        file.write(str(temps) + "\n")
        file.write(str(speed) + "\n")
        file.write(str(score) + "\n")
        file.write(str(move) + "\n")
        file.write(str(inventaire) + "\n") #list
        file.write(str(DespI) + "\n")
        file.write(str(timeline) + "\n")
        file.write(str(spaceline) + "\n")
        file.write(str(Objet) + "\n")

        DespOtmp = str(DespO)
        DespOtmp = DespOtmp.replace('"',"'")
        file.write(DespOtmp + "\n")
        DespOtmp = ""

        Lieuxtmp = str(Lieux)
        Lieuxtmp = Lieuxtmp.replace('"',"'")
        file.write(Lieuxtmp + "\n")
        Lieuxtmp = ""

        DespLtmp = str(DespL)
        DespLtmp = DespLtmp.replace('"',"'")
        file.write(DespLtmp + "\n")
        DespLtmp = ""
        
        file.write(sourcefile + "\n") #string
        file.close()
        print("Sauvegarder.")
        
    if (key.lower() == "load" or key.lower() == "restor" or key.lower() == "charger"):
        reponse = 1
        source = input("Nom? (Default 'jeu-save.txt')")
        if (source == ""):
            source = sourcefile
        if (source[-4:] == ".txt"):
            source = source
        else:
            source = source + ".txt"
        if (os.path.exists(Rep + source) == True):
            file = open(Rep + source.upper(), "r")
            ligne = 0
            for line in file:
                if (ligne == 0):
                    x = int(line[:-1])
                if (ligne == 1):
                    y = int(line[:-1])
                if (ligne == 2):
                    z = int(line[:-1])
                if (ligne == 3):
                    temps = int(line[:-1])
                if (ligne == 4):
                    speed = int(line[:-1])
                if (ligne == 5):
                    score = int(line[:-1])
                if (ligne == 6):
                    move = int(line[:-1])
                if (ligne == 7): #liste
                    inventaire = []
                    for i in range(len(line[2:-3].split("', '"))):
                        inventaire.append(line[2:-3].split("', '")[i])
                if (ligne == 8):
                    DespI = []
                    for i in range(len(line[2:-3].split("', '"))):
                        DespI.append(line[2:-3].split("', '")[i])
                if (ligne == 9):
                    #timeline = []
                    for i in range(len(line[2:-3].split("','"))):
                        timeline.append(line[2:-3].split("','")[i])
                if (ligne == 10):
                    #spaceline = []
                    for i in range(len(line[2:-3].split("','"))):
                        spaceline.append(line[2:-3].split("','")[i])
                if (ligne == 11): #3d
                    #Objet
                    lst = ""
                    lst = line[:-1].replace("[[[['","")
                    lst = lst.replace("']]]]","")
                    lst = lst.replace("]], [[","], [")
                    lst = lst.replace("]], [[","], [")
                    lst = lst.replace('"',"'")
                    lst = lst.split("'], ['")
                    invA = []
                    invB = []
                    invC = []
                    inv1 = []
                    inv2 = []
                    inv3 = []
                    inv4 = []
                    inv5 = []
                    inv6 = []
                    inv7 = []
                    inv8 = []
                    inv9 = []
                    inv10 = []
                    inv11 = []
                    inv12 = []
                    inv13 = []
                    inv14 = []
                    inv15 = []
                    inv = []
                    for i in range(5):
                        if "', '" in lst[i]:
                            for ii in range("', '" in lst[i]):
                                inv1.append(lst[i].split("', '"))
                        else:
                            inv.append(lst[i])
                            inv1.append(inv)
                            inv = []
                        if "', '" in lst[i+5]:
                            for ii in range("', '" in lst[i+5]):
                                inv2.append(lst[i+5].split("', '"))
                        else:
                            inv.append(lst[i+5])
                            inv2.append(inv)
                            inv = []
                        if "', '" in lst[i+10]:
                            for ii in range("', '" in lst[i+10]):
                                inv3.append(lst[i+10].split("', '"))
                        else:
                            inv.append(lst[i+10])
                            inv3.append(inv)
                            inv = []
                        if "', '" in lst[i+15]:
                            for ii in range("', '" in lst[i+15]):
                                inv4.append(lst[i+15].split("', '"))
                        else:
                            inv.append(lst[i+15])
                            inv4.append(inv)
                            inv = []
                        if "', '" in lst[i+20]:
                            for ii in range("', '" in lst[i+20]):
                                inv5.append(lst[i+20].split("', '"))
                        else:
                            inv.append(lst[i+20])
                            inv5.append(inv)
                            inv = []
                        if "', '" in lst[i+25]:
                            for ii in range("', '" in lst[i+25]):
                                inv6.append(lst[ii].split("', '"))
                        else:
                            inv.append(lst[i+25])
                            inv6.append(inv)
                            inv = []
                        if "', '" in lst[i+30]:
                            for ii in range("', '" in lst[i+30]):
                                inv7.append(lst[i+30].split("', '"))
                        else:
                            inv.append(lst[i+30])
                            inv7.append(inv)
                            inv = []
                        if "', '" in lst[i+35]:
                            for ii in range("', '" in lst[i+35]):
                                inv8.append(lst[i+35].split("', '"))
                        else:
                            inv.append(lst[i+35])
                            inv8.append(inv)
                            inv = []
                        if "', '" in lst[i+40]:
                            for ii in range("', '" in lst[i+40]):
                                inv9.append(lst[i+40].split("', '"))
                        else:
                            inv.append(lst[i+40])
                            inv9.append(inv)
                            inv = []
                        if "', '" in lst[i+45]:
                            for ii in range("', '" in lst[i+45]):
                                inv10.append(lst[i+45].split("', '"))
                        else:
                            inv.append(lst[i+45])
                            inv10.append(inv)
                            inv = []
                        if "', '" in lst[i+50]:
                            for ii in range("', '" in lst[i+50]):
                                inv11.append(lst[i+50].split("', '"))
                        else:
                            inv.append(lst[i+45])
                            inv11.append(inv)
                            inv = []
                        if "', '" in lst[i+55]:
                            for ii in range("', '" in lst[i+55]):
                                inv12.append(lst[i+55].split("', '"))
                        else:
                            inv.append(lst[i+50])
                            inv12.append(inv)
                            inv = []
                        if "', '" in lst[i+60]:
                            for ii in range("', '" in lst[i+60]):
                                inv13.append(lst[i+60].split("', '"))
                        else:
                            inv.append(lst[i+60])
                            inv13.append(inv)
                            inv = []
                        if "', '" in lst[i+65]:
                            for ii in range("', '" in lst[i+65]):
                                inv14.append(lst[i+65].split("', '"))
                        else:
                            inv.append(lst[i+65])
                            inv14.append(inv)
                            inv = []
                        if "', '" in lst[i+70]:
                            for ii in range("', '" in lst[i+70]):
                                inv15.append(lst[i+70].split("', '"))
                        else:
                            inv.append(lst[i+70])
                            inv15.append(inv)
                            inv = []
                    for i in range(5):
                        if i == 0:
                            j = inv1
                        if i == 1:
                            j = inv2
                        if i == 2:
                            j = inv3
                        if i == 3:
                            j = inv4
                        if i == 4:
                            j = inv5
                        invA.append(j)
                    for i in range(5):
                        if i == 0:
                            j = inv6
                        if i == 1:
                            j = inv7
                        if i == 2:
                            j = inv8
                        if i == 3:
                            j = inv9
                        if i == 4:
                            j = inv10
                        invB.append(j)
                    for i in range(5):
                        if i == 0:
                            j = inv11
                        if i == 1:
                            j = inv12
                        if i == 2:
                            j = inv13
                        if i == 3:
                            j = inv14
                        if i == 4:
                            j = inv15
                        invC.append(j)
                    Objet = []
                    for i in range(3):
                        if i == 0:
                            j = invA
                        if i == 1:
                            j = invB
                        if i == 2:
                            j = invC
                        Objet.append(j)
                if (ligne == 13): #3d
                    #Lieux
                    lst = ""
                    lst = line[:-1].replace("[[[['","")
                    lst = lst.replace("']]]]","")
                    lst = lst.replace("]], [[","], [")
                    lst = lst.replace("]], [[","], [")
                    lst = lst.replace('"], [',"'], ['") #Diancre!!
                    lst = lst.split("'], ['")
                    invA = []
                    invB = []
                    invC = []
                    inv1 = []
                    inv2 = []
                    inv3 = []
                    inv4 = []
                    inv5 = []
                    inv6 = []
                    inv7 = []
                    inv8 = []
                    inv9 = []
                    inv10 = []
                    inv11 = []
                    inv12 = []
                    inv13 = []
                    inv14 = []
                    inv15 = []
                    inv = []
                    for i in range(5):
                        if "', '" in lst[i]:
                            for ii in range("', '" in lst[i]):
                                inv1.append(lst[i].split("', '"))
                        else:
                            inv.append(lst[i])
                            inv1.append(inv)
                            inv = []
                        if "', '" in lst[i+5]:
                            for ii in range("', '" in lst[i+5]):
                                inv2.append(lst[i+5].split("', '"))
                        else:
                            inv.append(lst[i+5])
                            inv2.append(inv)
                            inv = []
                        if "', '" in lst[i+10]:
                            for ii in range("', '" in lst[i+10]):
                                inv3.append(lst[i+10].split("', '"))
                        else:
                            inv.append(lst[i+10])
                            inv3.append(inv)
                            inv = []
                        if "', '" in lst[i+15]:
                            for ii in range("', '" in lst[i+15]):
                                inv4.append(lst[i+15].split("', '"))
                        else:
                            inv.append(lst[i+15])
                            inv4.append(inv)
                            inv = []
                        if "', '" in lst[i+20]:
                            for ii in range("', '" in lst[i+20]):
                                inv5.append(lst[i+20].split("', '"))
                        else:
                            inv.append(lst[i+20])
                            inv5.append(inv)
                            inv = []
                        if "', '" in lst[i+25]:
                            for ii in range("', '" in lst[i+25]):
                                inv6.append(lst[ii].split("', '"))
                        else:
                            inv.append(lst[i+25])
                            inv6.append(inv)
                            inv = []
                        if "', '" in lst[i+30]:
                            for ii in range("', '" in lst[i+30]):
                                inv7.append(lst[i+30].split("', '"))
                        else:
                            inv.append(lst[i+30])
                            inv7.append(inv)
                            inv = []
                        if "', '" in lst[i+35]:
                            for ii in range("', '" in lst[i+35]):
                                inv8.append(lst[i+35].split("', '"))
                        else:
                            inv.append(lst[i+35])
                            inv8.append(inv)
                            inv = []
                        if "', '" in lst[i+40]:
                            for ii in range("', '" in lst[i+40]):
                                inv9.append(lst[i+40].split("', '"))
                        else:
                            inv.append(lst[i+40])
                            inv9.append(inv)
                            inv = []
                        if "', '" in lst[i+45]:
                            for ii in range("', '" in lst[i+45]):
                                inv10.append(lst[i+45].split("', '"))
                        else:
                            inv.append(lst[i+45])
                            inv10.append(inv)
                            inv = []
                        if "', '" in lst[i+50]:
                            for ii in range("', '" in lst[i+50]):
                                inv11.append(lst[i+50].split("', '"))
                        else:
                            inv.append(lst[i+45])
                            inv11.append(inv)
                            inv = []
                        if "', '" in lst[i+55]:
                            for ii in range("', '" in lst[i+55]):
                                inv12.append(lst[i+55].split("', '"))
                        else:
                            inv.append(lst[i+50])
                            inv12.append(inv)
                            inv = []
                        if "', '" in lst[i+60]:
                            for ii in range("', '" in lst[i+60]):
                                inv13.append(lst[i+60].split("', '"))
                        else:
                            inv.append(lst[i+60])
                            inv13.append(inv)
                            inv = []
                        if "', '" in lst[i+65]:
                            for ii in range("', '" in lst[i+65]):
                                inv14.append(lst[i+65].split("', '"))
                        else:
                            inv.append(lst[i+65])
                            inv14.append(inv)
                            inv = []
                        if "', '" in lst[i+70]:
                            for ii in range("', '" in lst[i+70]):
                                inv15.append(lst[i+70].split("', '"))
                        else:
                            inv.append(lst[i+70])
                            inv15.append(inv)
                            inv = []
                    for i in range(5):
                        if i == 0:
                            j = inv1
                        if i == 1:
                            j = inv2
                        if i == 2:
                            j = inv3
                        if i == 3:
                            j = inv4
                        if i == 4:
                            j = inv5
                        invA.append(j)
                    for i in range(5):
                        if i == 0:
                            j = inv6
                        if i == 1:
                            j = inv7
                        if i == 2:
                            j = inv8
                        if i == 3:
                            j = inv9
                        if i == 4:
                            j = inv10
                        invB.append(j)
                    for i in range(5):
                        if i == 0:
                            j = inv11
                        if i == 1:
                            j = inv12
                        if i == 2:
                            j = inv13
                        if i == 3:
                            j = inv14
                        if i == 4:
                            j = inv15
                        invC.append(j)
                    Lieux = []
                    for i in range(3):
                        if i == 0:
                            j = invA
                        if i == 1:
                            j = invB
                        if i == 2:
                            j = invC
                        Lieux.append(j)
                if (ligne == 14): #3d
                    #DespL
                    lst = ""
                    lst = line[:-1].replace("[[[['","")
                    lst = lst.replace("']]]]","")
                    lst = lst.replace("]], [[","], [")
                    lst = lst.replace("]], [[","], [")
                    lst = lst.replace('"], [',"'], ['")#
                    lst = lst.split("'], ['")
                    invA = []
                    invB = []
                    invC = []
                    inv1 = []
                    inv2 = []
                    inv3 = []
                    inv4 = []
                    inv5 = []
                    inv6 = []
                    inv7 = []
                    inv8 = []
                    inv9 = []
                    inv10 = []
                    inv11 = []
                    inv12 = []
                    inv13 = []
                    inv14 = []
                    inv15 = []
                    inv = []
                    for i in range(5):
                        if "', '" in lst[i]:
                            for ii in range("', '" in lst[i]):
                                inv1.append(lst[i].split("', '"))
                        else:
                            inv.append(lst[i])
                            inv1.append(inv)
                            inv = []
                        if "', '" in lst[i+5]:
                            for ii in range("', '" in lst[i+5]):
                                inv2.append(lst[i+5].split("', '"))
                        else:
                            inv.append(lst[i+5])
                            inv2.append(inv)
                            inv = []
                        if "', '" in lst[i+10]:
                            for ii in range("', '" in lst[i+10]):
                                inv3.append(lst[i+10].split("', '"))
                        else:
                            inv.append(lst[i+10])
                            inv3.append(inv)
                            inv = []
                        if "', '" in lst[i+15]:
                            for ii in range("', '" in lst[i+15]):
                                inv4.append(lst[i+15].split("', '"))
                        else:
                            inv.append(lst[i+15])
                            inv4.append(inv)
                            inv = []
                        if "', '" in lst[i+20]:
                            for ii in range("', '" in lst[i+20]):
                                inv5.append(lst[i+20].split("', '"))
                        else:
                            inv.append(lst[i+20])
                            inv5.append(inv)
                            inv = []
                        if "', '" in lst[i+25]:
                            for ii in range("', '" in lst[i+25]):
                                inv6.append(lst[ii].split("', '"))
                        else:
                            inv.append(lst[i+25])
                            inv6.append(inv)
                            inv = []
                        if "', '" in lst[i+30]:
                            for ii in range("', '" in lst[i+30]):
                                inv7.append(lst[i+30].split("', '"))
                        else:
                            inv.append(lst[i+30])
                            inv7.append(inv)
                            inv = []
                        if "', '" in lst[i+35]:
                            for ii in range("', '" in lst[i+35]):
                                inv8.append(lst[i+35].split("', '"))
                        else:
                            inv.append(lst[i+35])
                            inv8.append(inv)
                            inv = []
                        if "', '" in lst[i+40]:
                            for ii in range("', '" in lst[i+40]):
                                inv9.append(lst[i+40].split("', '"))
                        else:
                            inv.append(lst[i+40])
                            inv9.append(inv)
                            inv = []
                        if "', '" in lst[i+45]:
                            for ii in range("', '" in lst[i+45]):
                                inv10.append(lst[i+45].split("', '"))
                        else:
                            inv.append(lst[i+45])
                            inv10.append(inv)
                            inv = []
                        if "', '" in lst[i+50]:
                            for ii in range("', '" in lst[i+50]):
                                inv11.append(lst[i+50].split("', '"))
                        else:
                            inv.append(lst[i+45])
                            inv11.append(inv)
                            inv = []
                        if "', '" in lst[i+55]:
                            for ii in range("', '" in lst[i+55]):
                                inv12.append(lst[i+55].split("', '"))
                        else:
                            inv.append(lst[i+50])
                            inv12.append(inv)
                            inv = []
                        if "', '" in lst[i+60]:
                            for ii in range("', '" in lst[i+60]):
                                inv13.append(lst[i+60].split("', '"))
                        else:
                            inv.append(lst[i+60])
                            inv13.append(inv)
                            inv = []
                        if "', '" in lst[i+65]:
                            for ii in range("', '" in lst[i+65]):
                                inv14.append(lst[i+65].split("', '"))
                        else:
                            inv.append(lst[i+65])
                            inv14.append(inv)
                            inv = []
                        if "', '" in lst[i+70]:
                            for ii in range("', '" in lst[i+70]):
                                inv15.append(lst[i+70].split("', '"))
                        else:
                            inv.append(lst[i+70])
                            inv15.append(inv)
                            inv = []
                    for i in range(5):
                        if i == 0:
                            j = inv1
                        if i == 1:
                            j = inv2
                        if i == 2:
                            j = inv3
                        if i == 3:
                            j = inv4
                        if i == 4:
                            j = inv5
                        invA.append(j)
                    for i in range(5):
                        if i == 0:
                            j = inv6
                        if i == 1:
                            j = inv7
                        if i == 2:
                            j = inv8
                        if i == 3:
                            j = inv9
                        if i == 4:
                            j = inv10
                        invB.append(j)
                    for i in range(5):
                        if i == 0:
                            j = inv11
                        if i == 1:
                            j = inv12
                        if i == 2:
                            j = inv13
                        if i == 3:
                            j = inv14
                        if i == 4:
                            j = inv15
                        invC.append(j)
                    DespL = []
                    for i in range(3):
                        if i == 0:
                            j = invA
                        if i == 1:
                            j = invB
                        if i == 2:
                            j = invC
                        DespL.append(j)
                if (ligne == 12): #3d
                    #DespO
                    lst = ""
                    lst = line[:-1].replace("[[[['","")
                    lst = lst.replace("']]]]","")
                    lst = lst.replace("]], [[","], [")
                    lst = lst.replace("]], [[","], [")
                    lst = lst.replace('"], [',"'], ['")#
                    lst = lst.split("'], ['")
                    invA = []
                    invB = []
                    invC = []
                    inv1 = []
                    inv2 = []
                    inv3 = []
                    inv4 = []
                    inv5 = []
                    inv6 = []
                    inv7 = []
                    inv8 = []
                    inv9 = []
                    inv10 = []
                    inv11 = []
                    inv12 = []
                    inv13 = []
                    inv14 = []
                    inv15 = []
                    inv = []
                    for i in range(5):
                        if "', '" in lst[i]:
                            for ii in range("', '" in lst[i]):
                                inv1.append(lst[i].split("', '"))
                        else:
                            inv.append(lst[i])
                            inv1.append(inv)
                            inv = []
                        if "', '" in lst[i+5]:
                            for ii in range("', '" in lst[i+5]):
                                inv2.append(lst[i+5].split("', '"))
                        else:
                            inv.append(lst[i+5])
                            inv2.append(inv)
                            inv = []
                        if "', '" in lst[i+10]:
                            for ii in range("', '" in lst[i+10]):
                                inv3.append(lst[i+10].split("', '"))
                        else:
                            inv.append(lst[i+10])
                            inv3.append(inv)
                            inv = []
                        if "', '" in lst[i+15]:
                            for ii in range("', '" in lst[i+15]):
                                inv4.append(lst[i+15].split("', '"))
                        else:
                            inv.append(lst[i+15])
                            inv4.append(inv)
                            inv = []
                        if "', '" in lst[i+20]:
                            for ii in range("', '" in lst[i+20]):
                                inv5.append(lst[i+20].split("', '"))
                        else:
                            inv.append(lst[i+20])
                            inv5.append(inv)
                            inv = []
                        if "', '" in lst[i+25]:
                            for ii in range("', '" in lst[i+25]):
                                inv6.append(lst[ii].split("', '"))
                        else:
                            inv.append(lst[i+25])
                            inv6.append(inv)
                            inv = []
                        if "', '" in lst[i+30]:
                            for ii in range("', '" in lst[i+30]):
                                inv7.append(lst[i+30].split("', '"))
                        else:
                            inv.append(lst[i+30])
                            inv7.append(inv)
                            inv = []
                        if "', '" in lst[i+35]:
                            for ii in range("', '" in lst[i+35]):
                                inv8.append(lst[i+35].split("', '"))
                        else:
                            inv.append(lst[i+35])
                            inv8.append(inv)
                            inv = []
                        if "', '" in lst[i+40]:
                            for ii in range("', '" in lst[i+40]):
                                inv9.append(lst[i+40].split("', '"))
                        else:
                            inv.append(lst[i+40])
                            inv9.append(inv)
                            inv = []
                        if "', '" in lst[i+45]:
                            for ii in range("', '" in lst[i+45]):
                                inv10.append(lst[i+45].split("', '"))
                        else:
                            inv.append(lst[i+45])
                            inv10.append(inv)
                            inv = []
                        if "', '" in lst[i+50]:
                            for ii in range("', '" in lst[i+50]):
                                inv11.append(lst[i+50].split("', '"))
                        else:
                            inv.append(lst[i+45])
                            inv11.append(inv)
                            inv = []
                        if "', '" in lst[i+55]:
                            for ii in range("', '" in lst[i+55]):
                                inv12.append(lst[i+55].split("', '"))
                        else:
                            inv.append(lst[i+50])
                            inv12.append(inv)
                            inv = []
                        if "', '" in lst[i+60]:
                            for ii in range("', '" in lst[i+60]):
                                inv13.append(lst[i+60].split("', '"))
                        else:
                            inv.append(lst[i+60])
                            inv13.append(inv)
                            inv = []
                        if "', '" in lst[i+65]:
                            for ii in range("', '" in lst[i+65]):
                                inv14.append(lst[i+65].split("', '"))
                        else:
                            inv.append(lst[i+65])
                            inv14.append(inv)
                            inv = []
                        if "', '" in lst[i+70]:
                            for ii in range("', '" in lst[i+70]):
                                inv15.append(lst[i+70].split("', '"))
                        else:
                            inv.append(lst[i+70])
                            inv15.append(inv)
                            inv = []
                    for i in range(5):
                        if i == 0:
                            j = inv1
                        if i == 1:
                            j = inv2
                        if i == 2:
                            j = inv3
                        if i == 3:
                            j = inv4
                        if i == 4:
                            j = inv5
                        invA.append(j)
                    for i in range(5):
                        if i == 0:
                            j = inv6
                        if i == 1:
                            j = inv7
                        if i == 2:
                            j = inv8
                        if i == 3:
                            j = inv9
                        if i == 4:
                            j = inv10
                        invB.append(j)
                    for i in range(5):
                        if i == 0:
                            j = inv11
                        if i == 1:
                            j = inv12
                        if i == 2:
                            j = inv13
                        if i == 3:
                            j = inv14
                        if i == 4:
                            j = inv15
                        invC.append(j)
                    DespO = []
                    for i in range(3):
                        if i == 0:
                            j = invA
                        if i == 1:
                            j = invB
                        if i == 2:
                            j = invC
                        DespO.append(j)
                if (ligne == 15):
                    sourcefile = line[:-1] #string
                ligne = ligne + 1
            file.close()
            print("Charger.")
        else:
            print("Pas de fichier", source)
    #sortie du jeu
    if (key.lower() == "quit"):
        reponse = 1
        print("Si vous quittez sans savez, vous perdrez tous vos progrès.") #
        choix = input("Est-vous sure de quitter? [oui/non]")
        if (choix == "o" or choix == "oui" or choix == "y" or choix == "yes"):
            print("Bye bye")
            game = 0
            break
            exit()
    #N'est pas une entrer valide
    if (reponse == 0):
        print("Je ne comprend pas", key.upper())
    #Fin du tour
    print("")
    
    #Supression des rebord de la simulation
    if x > 4:
        x = 0
    if y > 4:
        y = 0
    if z > 2:
        z = 0
    if x < 0:
        x = 4
    if y < 0:
        y = 4
    if z < 0:
        z = 2
