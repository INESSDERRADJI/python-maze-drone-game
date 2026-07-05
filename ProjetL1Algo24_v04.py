#!/usr/bin/env python
# -*- coding: utf-8 -*-
#v02


#Modules importés
from tkinter import *
import random
import math
import numpy as np

# ----------------------------------------------------------------
# Variables globales
# ----------------------------------------------------------------

#Liste des drones (ID)
drones=[]
#Liste des types ddrones
typesDrone=[]
TYPE_UTILISATEUR=30
TYPE_ENNEMI_ALEA=41
TYPE_ENNEMI_INTELLIGENT=42

#A intégrer
etats_fonctionnement=[]
ETAT_FONCTIONNEMENT_INITIAL=100
DEGAT_ENNEMI=10

#Coordonnées initiales de tous les drones
coord_iDrones_Init=[]#Abscisse Drones
coord_jDrones_Init=[]#Ordonnée Drones

#Coordonnées actuelles de tous les drones
coord_iDrones=[]#Abscisse Drones >> nombre réél à convertir en entier pour utiliser en coordonnées matricielle
coord_jDrones=[]#Ordonnée Drones

#Vitesses actuelles de tous les drones
vitX=[]
vitY=[]
#Distance incrémentée à chaque déplacement
VIT_MAX_Utilisateur = 0.2
VIT_MAX_Ennemi = 0.1

#Legende des Matrices de décor
ZV=0#Zone Vide
ZO=10#Zone Obstacle
ZC=20#Zones cibles

#Matrice de décor du Niveau 1
matValDecorN1 = [
    [ZO, ZO, ZO, ZO, ZO, ZO, ZO, ZO, ZO, ZO, ZO, ZO, ZO, ZO, ZO, ZO, ZO],
    [ZO, ZC, ZC, ZV, ZV, ZV, ZV, ZV, ZO, ZV, ZV, ZV, ZV, ZV, ZV, ZV, ZO],
    [ZO, ZC, ZO, ZO, ZV, ZO, ZO, ZV, ZO, ZV, ZO, ZO, ZV, ZO, ZO, ZV, ZO],
    [ZO, ZV, ZV, ZV, ZV, ZV, ZV, ZV, ZV, ZV, ZV, ZV, ZV, ZV, ZV, ZV, ZO],
    [ZO, ZV, ZO, ZO, ZV, ZO, ZV, ZO, ZO, ZO, ZV, ZO, ZV, ZO, ZO, ZV, ZO],
    [ZO, ZV, ZV, ZV, ZV, ZO, ZV, ZV, ZO, ZV, ZV, ZO, ZC, ZV, ZV, ZV, ZO],
    [ZO, ZV, ZO, ZO, ZV, ZO, ZO, ZV, ZO, ZV, ZO, ZO, ZV, ZO, ZO, ZO, ZO],
    [ZO, ZV, ZO, ZO, ZV, ZO, ZV, ZV, ZV, ZV, ZV, ZO, ZV, ZO, ZO, ZO, ZO],
    [ZO, ZV, ZV, ZC, ZV, ZV, ZV, ZO, ZO, ZO, ZV, ZV, ZV, ZV, ZV, ZV, ZO],
    [ZO, ZO, ZO, ZO, ZV, ZO, ZV, ZV, ZV, ZV, ZV, ZO, ZV, ZO, ZO, ZV, ZO],
    [ZO, ZV, ZV, ZV, ZV, ZV, ZV, ZV, ZO, ZC, ZV, ZV, ZV, ZV, ZV, ZV, ZO],
    [ZO, ZV, ZO, ZO, ZV, ZO, ZO, ZV, ZO, ZV, ZO, ZO, ZO, ZO, ZO, ZV, ZO],
    [ZO, ZV, ZV, ZO, ZV, ZV, ZV, ZV, ZV, ZV, ZV, ZV, ZV, ZO, ZV, ZV, ZO],
    [ZO, ZO, ZV, ZO, ZV, ZO, ZV, ZO, ZO, ZO, ZV, ZO, ZV, ZO, ZV, ZO, ZO],
    [ZO, ZV, ZV, ZV, ZV, ZO, ZV, ZV, ZO, ZV, ZV, ZO, ZV, ZV, ZV, ZV, ZO],
    [ZO, ZV, ZC, ZV, ZV, ZV, ZV, ZV, ZV, ZV, ZV, ZV, ZC, ZV, ZV, ZV, ZO],
    [ZO, ZO, ZO, ZO, ZO, ZO, ZO, ZO, ZO, ZO, ZO, ZO, ZO, ZO, ZO, ZO, ZO]
]
matValDecorN1_initial=np.copy(matValDecorN1)#Copie pout conservation des valeurs initiales durant la simulation

#Dimension de chaque case en pixel
LARG_CASE=40#Largeur
HAUT_CASE=40#Hauteur

#Dimensions
LARG_CANVAS = len(matValDecorN1)*LARG_CASE
HAUT_CANVAS = len(matValDecorN1[0])*HAUT_CASE

#Etat des animations et déplacements
etat_actif_depl_anim = False

#Demande d'arrêt
dde_arret = False

#Gestion du score
score=0
SCORE_CIBLE=10#Points obtenus pour chaque cible atteinte par l'utilisateur

# ----------------------------------------------------------------
# Fonctions
# ----------------------------------------------------------------

"""
Obj: Tirage aléatoire d'un emplacement sans Obstacle
Retour : liste de 2 élements : Coordonnées (en matriciel et non en pixel)

"""
def getCoordAleatoiresSansObstacle():

    dispo=False
    while (not dispo):
        
        i=random.randint(0,len(matValDecorN1)-1)
        j=random.randint(0,len(matValDecorN1[0])-1)
        #i=random.randint(0,3)
        #j=random.randint(0,3)
        
        if (matValDecorN1[j][i]==0):
            dispo=True

    return [i,j]

"""
Obj: Convertion des coordonnées réélles en coordonnées entières pour conulter la matrice
Permet ainsi de connaître le type d'item qui occupe la case occupé par le drone
Retour : liste de 2 élements : Coordonnées (en matriciel et non en pixel)

"""
def getCelluleDrone(pNoDrone):
    return [round(coord_iDrones[pNoDrone]),round(coord_jDrones[pNoDrone])]

"""
Obj: Convertir les indices de tableau en coordonnées pixel 
Paramètres : indices du tableau niveau
Retour : liste des 2 coordonnées en pixel 
"""
def getConvertCoordNiveauEnCoordPixels(i,j):
    x=LARG_CASE*i
    y=HAUT_CASE*j
    return [x,y]

"""
Obj: Convertir les coordonnées pixel en indices de tableau niveau
Paramètres : coordonnées pixel
Retour : liste des 2 indices du tableau matValDecorN1
"""
def getConvertCoordPixelsEnCoordNiveau(x,y):
    i=int(x/(LARG_CASE-(x%LARG_CASE)))
    j=int(y/(HAUT_CASE-(y%HAUT_CASE)))
    return [i,j]

"""
Obj: Convertir les coordonnées pixel en indices de tableau niveau
Paramètres : image et nouvelles coordonnées en pixel
"""
def deplacerImage(im,newX,newY):
    global gestionCanvas
    gestionCanvas.coords(im,newX,newY,
                         newX+LARG_CASE,newY+HAUT_CASE)


"""
Obj: Gestion des évènements du clavier

"""
def evenements(event):
    
    
    if event.keysym=="Up":
        pilotage(0,0,-VIT_MAX_Utilisateur)# demarrage(0,-VIT_MAX_Utilisateur)#,btnHaut)
    elif event.keysym=="Down":
        pilotage(0,0,VIT_MAX_Utilisateur)#,btnBas)
    elif event.keysym=="Left":
        pilotage(0,-VIT_MAX_Utilisateur,0)#,btnGauche)
    elif event.keysym=="Right":
        pilotage(0,VIT_MAX_Utilisateur,0)#,btnDroite)
    
    if event.keysym=="Escape":
        arret()
    elif event.keysym=="space":
        depart()
 

"""
Obj: Instanciation d'un nouvel Drone
Param : true si on souhaite créer un drone ennemi
"""
def creationDrone(pTypeDrone):
    global vitX,vitY,coord_iDrones_Init,coord_jDrones_Init,drones,typesDrone,etats_fonctionnement
    
    posInitDrone=getCoordAleatoiresSansObstacle()
    coord_i_Drone=posInitDrone[0]
    coord_j_Drone=posInitDrone[1]

    coord_iDrones_Init.append(coord_i_Drone)
    coord_jDrones_Init.append(coord_j_Drone)
    coord_iDrones.append(coord_i_Drone)
    coord_jDrones.append(coord_j_Drone)

    vitX.append(0)
    vitY.append(0)
    
    coordPixel=getConvertCoordNiveauEnCoordPixels(posInitDrone[0],posInitDrone[1])
      
    matValDecorN1[coord_j_Drone][coord_i_Drone]=pTypeDrone
    if (pTypeDrone==TYPE_UTILISATEUR):
        drones.append(gestionCanvas.create_image(coordPixel[0],coordPixel[1], image=imgUtilisateur,anchor=NW))
        
    elif (pTypeDrone==TYPE_ENNEMI_ALEA):
        drones.append(gestionCanvas.create_image(coordPixel[0],coordPixel[1], image=imgEnnemiAlea,anchor=NW))

    elif (pTypeDrone==TYPE_ENNEMI_INTELLIGENT):
        drones.append(gestionCanvas.create_image(coordPixel[0],coordPixel[1], image=imgEnnemiIntelligent,anchor=NW))

    typesDrone.append(pTypeDrone)
    etats_fonctionnement.append(ETAT_FONCTIONNEMENT_INITIAL)

"""
Obj: Démarrage des déplacements du Joueur et de l'Drone ennemi
Param :
    pVitesseX : Vitesse demandée par le joueur sur l'axe des abcisses
    pVitesseY : Vitesse demandée par le joueur sur l'axe des ordonnées
    pBtn : Bouton utilisé dont l'apparence doit mise à jour
"""
def pilotage(pNoDrone,pVitesseX,pVitesseY):
    global dde_arret,etat_actif_depl_anim,vitX,vitY
    
    if etat_actif_depl_anim == True:
        vitX[pNoDrone]=pVitesseX
        vitY[pNoDrone]=pVitesseY

"""
Obj: Appel récursif des déplacements de tous les drones
Basculer la valeur de dde_arretà True pour stopper les déplacements
"""
def lancement_deplacements():

    global etat_actif_depl_anim, dde_arret
    
    for noDrone in range(len(drones)):
        deplacement(noDrone)#,typesDrone[i])
    
    if dde_arret == False :#Tant que le jeu ne doit pas être arrêté
        fen_princ.after(100, lancement_deplacements)#Patienter 100ms afin d'appeler à nouveau cette même fonction (récursivité)
    else:
        dde_arret = False #Arrêt pris en compte et réinitialisé
        etat_actif_depl_anim = False #Animation désactivée
        
"""
Obj: Gestion de la logique de déplacement des ennemis
Param :
    pNoDrone : Identifiant du drone concerné
"""
def chgtDirectionEnnemis(pNoDrone):
    global vitX, vitY,typesDrone
    #Tirage aléatoire d'un pourcentage de la direction
    
    if (typesDrone[pNoDrone]==TYPE_ENNEMI_INTELLIGENT):
        if (random.randint(1,2)==1):
            if (coord_iDrones[pNoDrone]>coord_iDrones[0]):
                vitX[pNoDrone]=-VIT_MAX_Ennemi
            else:
                vitX[pNoDrone]=VIT_MAX_Ennemi
        else:
            if (coord_jDrones[pNoDrone]>coord_jDrones[0]):
                vitY[pNoDrone]=-VIT_MAX_Ennemi
            else:
                vitY[pNoDrone]=VIT_MAX_Ennemi        
    else:
        direction = random.randint(1,100)
    
        if (vitX[pNoDrone]==0 and vitY[pNoDrone]==0): #Changement de direction si nous sommes à l'arrêt
            if direction <= 25 :#25% de chance qu'il parte à droite
                vitX[pNoDrone] = VIT_MAX_Ennemi
                vitY[pNoDrone] = 0
    
            elif direction <= 50 :#25% de chance qu'il parte à gauche
                vitX[pNoDrone] = -VIT_MAX_Ennemi
                vitY[pNoDrone] = 0
    
            elif direction <= 75 :#25% de chance qu'il parte en bas
                vitX[pNoDrone] = 0
                vitY[pNoDrone] = VIT_MAX_Ennemi
    
            else:# de 75% et 100% inclus
                vitX[pNoDrone] = 0#25% de chance qu'il parte en haut
                vitY[pNoDrone] = -VIT_MAX_Ennemi


"""
Obj: Gestion des déplacements de chaque drone
Param :
    pNoDrone : Identifiant du drone concerné

"""
def deplacement(pNoDrone):
    global drones, vitX, vitY,coord_iDrones,typesDrone,etats_fonctionnement,score
        
    #Interdire le déplacement si son etat de fonctionnement est nul
    if (etats_fonctionnement[pNoDrone]<=0):
        vitX[pNoDrone]=0
        vitY[pNoDrone]=0
    else:
        #Cas de changement d'axe de direction > Réaligner l'ancien
        if (vitX[pNoDrone]!=0):
            coord_jDrones[pNoDrone]=round(coord_jDrones[pNoDrone])
        else:#vitY!=0
            coord_iDrones[pNoDrone]=round(coord_iDrones[pNoDrone])
        
        #Incrémentation des coordonnées en fonction de la vitesse du drone
        coord_iDrones[pNoDrone]+=vitX[pNoDrone]
        coord_jDrones[pNoDrone]+=vitY[pNoDrone]    
        
        #identification des coordonnées de la cellule sur laquelle le drone s'engage 
        if (vitX[pNoDrone]>0 or vitY[pNoDrone]>0):
            coord_iDrone_matDecor=math.ceil(coord_iDrones[pNoDrone])
            coord_jDrone_matDecor=math.ceil(coord_jDrones[pNoDrone])
        else:
            coord_iDrone_matDecor=math.floor(coord_iDrones[pNoDrone])
            coord_jDrone_matDecor=math.floor(coord_jDrones[pNoDrone])
        #identification du type de décor présent sur cette cellule
        typeDecor=(matValDecorN1[coord_jDrone_matDecor][coord_iDrone_matDecor])
        
        if (typeDecor==ZO):#Cas de colision avec des obstacles
            #Repositionnement du drone
            if (vitX[pNoDrone]>0):
                coord_iDrones[pNoDrone]=coord_iDrone_matDecor-1
            elif (vitX[pNoDrone]<0):
                coord_iDrones[pNoDrone]=coord_iDrone_matDecor+1
            elif (vitY[pNoDrone]>0):
                coord_jDrones[pNoDrone]=coord_jDrone_matDecor-1
            elif (vitY[pNoDrone]<0):
                coord_jDrones[pNoDrone]=coord_jDrone_matDecor+1
            
            #Arrêt du drone
            vitX[pNoDrone]=0
            vitY[pNoDrone]=0
            
            #Relancer les drones ennemis
            if (typesDrone[pNoDrone]!=TYPE_UTILISATEUR):
                chgtDirectionEnnemis(pNoDrone)
                
            
        elif (typeDecor==ZC and typesDrone[pNoDrone]==TYPE_UTILISATEUR):#Cas des zones cibles
                #Changer le statut de la cible
                matValDecorN1[coord_jDrone_matDecor][coord_iDrone_matDecor]=-ZC
                #Supprimer l'image
                gestionCanvas.delete(matImgDecorN1[coord_jDrone_matDecor][coord_iDrone_matDecor])
                #incrémentation du score            
                score=int(score)+SCORE_CIBLE
                lblScore.config(text = "Score : "+str(score))

        
        #Recherche de collision avec d'autres drones
        for a in range(0,len(drones)):
            if (typesDrone[pNoDrone]==TYPE_UTILISATEUR and typesDrone[a]!=TYPE_UTILISATEUR): #2 drones dans des cas adverses                    
                if (getCelluleDrone(a)==getCelluleDrone(pNoDrone)):#2 drones occupant le même emplacement
                        etats_fonctionnement[pNoDrone]-=DEGAT_ENNEMI
                        lblEtat.config(text = "Etat : "+str(etats_fonctionnement[0])+"%")

        #Potentielle victoire et défaite
        if (typesDrone[pNoDrone]==TYPE_UTILISATEUR):
            VictoireDefaite()
        
        #Repositonnement de l'image du drone en fonction de ses nouvelles coordonnées
        gestionCanvas.coords(drones[pNoDrone],coord_iDrones[pNoDrone]*LARG_CASE,coord_jDrones[pNoDrone]*HAUT_CASE)

"""
Obj: Réinitiaisation toutes les positions et les vitesses et arrêt des animations et déplacements
"""
def depart():

    global vitX, vitY,typesDrone,dde_arret,etat_actif_depl_anim,score,etats_fonctionnement
    
    if (etat_actif_depl_anim==False):
        #Annulation de la vitesse en cours
        for i in range (len(vitX)):
            vitX[i]=0
        for i in range (len(vitY)):
            vitY[i]=0
            
        #Réinitialisation des états de fonctionnement
        for i in range (len(etats_fonctionnement)):
            etats_fonctionnement[i]=ETAT_FONCTIONNEMENT_INITIAL
        lblEtat.config(text = "Etat : "+str(etats_fonctionnement[0])+"%")
    
        #Arrêt des animations et déplacement
        dde_arret = False
        etat_actif_depl_anim = True
    
        #Repositionnement aux valeurs initiales        
        for noDrone in range(0,len(drones)):  
            coord_iDrones[noDrone]=coord_iDrones_Init[noDrone]
            coord_jDrones[noDrone]=coord_jDrones_Init[noDrone]
            gestionCanvas.coords(drones[noDrone],coord_iDrones[noDrone]*LARG_CASE,coord_jDrones[noDrone]*HAUT_CASE)
    
            if (typesDrone[noDrone]!=TYPE_UTILISATEUR):
                chgtDirectionEnnemis(noDrone)
        
        #initialisation du score            
        score=0
        lblScore.config(text = "Score : "+str(score))
        #initialisation de message de victoire & défaite
        lblMessage.config(text="")
        
        CreationImagesDecor()
        
        lancement_deplacements()
    

"""
Obj: Arrêt des animations et déplacements sans repositionner
"""
def arret():
    global dde_arret,etat_actif_depl_anim
        
    if (etat_actif_depl_anim==True):
        #Mise à jour de la variale globale utilisée dans les déplacements
        dde_arret = True
        etat_actif_depl_anim=False


"""
Obj: Verification des conditions de Victoire et de Défaite
Dans le cas de victoire comme de défait, le jeu sera arrêté et un message mis à jour
"""
def VictoireDefaite():

    #Gestion de la défaite
    NbUtilisateursEnBonEtat=0#Tous les alliés doivent avoir un état de fonctionnement nul
    for noDrone in range(0,len(drones)):#Parcours de tous les drones
        if (typesDrone[noDrone]==TYPE_UTILISATEUR) and etats_fonctionnement[noDrone]>0:#Drone Utilisateur encore actif (bon état)
            NbUtilisateursEnBonEtat=NbUtilisateursEnBonEtat+1
    if (NbUtilisateursEnBonEtat==0):#Plus aucun joueur n'est actif
        arret()
        lblMessage.config(text="Défaite",fg='#f00')
    else:
        #Gestion de la victoire
        NbCiblesRestantes=0
        #Recherche des cibles restantes dans la matrice
        for i in range(len(matValDecorN1)):
            for j in range(len(matValDecorN1[i])):
                if (matValDecorN1[i][j]==ZC):
                    NbCiblesRestantes=NbCiblesRestantes+1
        if (NbCiblesRestantes==0):
            arret()
            lblMessage.config(text="Victoire",fg='#0f0')
            
"""
Obj: Créer ou Recréer les images de décor : rues, obstacles et zones sensibles
"""
def CreationImagesDecor():
    global matValDecorN1,matImgDecorN1
    
    #Suppression de toutes les images de décor déjà présentes (cas de redémarrage)
    for imgDecorLigne in matImgDecorN1:
        for j in imgDecorLigne:
            gestionCanvas.delete(j)
    matImgDecorN1.clear()
    
    #réinitialisation des valeurs de la matrice
    matValDecorN1=np.copy(matValDecorN1_initial)
    
    #Création
    for i in range(len(matValDecorN1)):
        imgDecorLigne=[]
        for j in range(len(matValDecorN1[i])):
            if (matValDecorN1[i][j]==ZV):
                imgDecorLigne.append(gestionCanvas.create_image(j*LARG_CASE, i*HAUT_CASE, image=imgVide,anchor=NW))
            elif (matValDecorN1[i][j]==ZO):
                imgDecorLigne.append(gestionCanvas.create_image(j*LARG_CASE, i*HAUT_CASE, image=imgObstacle,anchor=NW))
            elif (matValDecorN1[i][j]==ZC):
                imgDecorLigne.append(gestionCanvas.create_image(j*LARG_CASE, i*HAUT_CASE, image=imgZoneSensible,anchor=NW))
        matImgDecorN1.append(imgDecorLigne)

# ----------------------------------------------------------------
# Corps du programme
# ----------------------------------------------------------------

#Paramétrage de la fenêtre principale
fen_princ = Tk()
fen_princ.title("DRONE WAR L1 SPI")
fen_princ.geometry("900x700")#Dimensions de la fenêtre
fen_princ.bind("<Key>",evenements)#Définition de la fonction de gestion des évènements clavier

#Paramétrage du Canvas
gestionCanvas = Canvas(fen_princ, width=LARG_CANVAS, height=HAUT_CANVAS, bg='ivory', bd=0, highlightthickness=0)
gestionCanvas.grid(row=0,column=0, padx=10,pady=10)

#Affichage des Obstacles du niveau 1
imgVide=PhotoImage(width=LARG_CASE, height=HAUT_CASE)
imgObstacle=PhotoImage(file = ("img/immeuble.gif"),master=fen_princ)
imgZoneSensible=PhotoImage(file = ("img/zone sensible.gif"),master=fen_princ)
matImgDecorN1 = []

#Création et positionnement des images du décor en fonction des valeurs de matValDecorN1
CreationImagesDecor()

#Images utilisées pour l'affichage des drones
imgUtilisateur=PhotoImage(file = ("img/allie.gif"),master=fen_princ)
imgEnnemiAlea=PhotoImage(file = ("img/ennemiA.gif"),master=fen_princ)
imgEnnemiIntelligent=PhotoImage(file = ("img/ennemiI.gif"),master=fen_princ)

#Affichage du drone géré par l'utilisateur
nbDroneUtilisateur=1
for i in range(nbDroneUtilisateur):
    creationDrone(TYPE_UTILISATEUR)

#Affichage des drones ennemis
nbDroneEnnemisAlea=2
for i in range(nbDroneEnnemisAlea):
    creationDrone(TYPE_ENNEMI_ALEA)
nbDroneEnnemisIntelligent=1
for i in range(nbDroneEnnemisIntelligent):
    creationDrone(TYPE_ENNEMI_INTELLIGENT)

#Zone dédiée aux boutons
zoneBtn = Frame(fen_princ)
zoneBtn.grid(row=0,column=1,ipadx=5)
  
#Boutons d'arrêt et de réinitialisation
lblMessage = Label(zoneBtn, text="")
Font_tuple = ("Comic Sans MS", 20, "bold")  
lblMessage.configure(font = Font_tuple) 
lblMessage.pack(fill=X)
lblScore = Label(zoneBtn, text="Score")
lblScore.pack(fill=X)
lblEtat = Label(zoneBtn, text="Etat : "+str(ETAT_FONCTIONNEMENT_INITIAL)+" %")
lblEtat.pack(fill=X)
btnArret = Button(zoneBtn, text="STOP", fg="yellow", bg="red", command=arret)
btnArret.pack(fill=X)
btnInit = Button(zoneBtn, text="START", fg="yellow", bg="green", command=depart)
btnInit.pack(fill=X)

#Rafraichissement de la fenêtre et de tout son contenu
fen_princ.mainloop()
