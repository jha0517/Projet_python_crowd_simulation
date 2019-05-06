import maya.cmds as cmds
from random import *
from math import *
import time



#------------------------------------------------------------------------------------
# CLASS
#------------------------------------------------------------------------------------

class Agents():
    
    
    def __init__(self,name,nbPopulation,targetX,targetZ,minFriendDistance,coeffA,coeffC,coeffS):
        '''
        __init__():
            [Constructeur] Exécute la fonction createCube() dont l'exécution créé une foule d'agents (cubes) dans un espace défini autour du centre de la scène.
            @param:    name : nom de l'agent (type string)
                       nbPopulation : nombre d'agents dans le groupe (type int)
                       targetX : position en X de la cible (type float)
                       targetZ : position en Z de la cible (type float)
                       minFriendDistance : rayon de la zone circulaire autour de chaque agent dans laquelle la présence de tout voisin entraîne un mouvement de séparation (répulsion) dudit agent par rapport audit voisin (type float)                       
            @return:   rien
        '''
        self.createAgent(name,nbPopulation)
            
    
    def createAgent(self,name,nbPopulation):
        '''
        createAgent():
            Créé une foule d'agents disposés aléatoirement dans un espace 2D de 5 unités de distance sur 5 unités de distance (par défaut, le cm) autour du centre de la scène.
            @param:    name : nom de l'agent (type string)
                       nbPopulation : nombre d'agents dans le groupe (type int)
            @return:   rien
        '''
        # CAPTURE POSITION OF SPAWNING POSITION SELECTED BY USER
        targetZone=cmds.ls(sl=True)
        targetzoneCoord=cmds.xform(targetZone,q=True,t=True,ws=True)
            
        for i in range(nbPopulation):
            
            # PREPARE FUTURE SELECTION OF ASSET TO BE IMPORTED
            # List all transforms in scene before import
            allTransformsBeforeImport=cmds.listRelatives(cmds.ls(shapes=True),allParents=True)
            # Assign to variable "count" the number of elements in list "allTransformsBeforeImport"
            count=len(allTransformsBeforeImport)
                
            # IMPORT ASSET AT ORIGIN OF SCENE
            assetPath= cmds.internalVar(upd = True)+"scripts/lavazza/men_alembic.abc"
            cmds.file(assetPath,i=True)
                    
            # SELECT IMPORTED ASSET
            # List all transforms in scene after import
            allTransformsAfterImport=cmds.listRelatives(cmds.ls(shapes=True),allParents=True)
            # Compare all elements in lists of transforms in scene before and after import
            for j in range(count):
                for k in allTransformsAfterImport:
                    # If any element is common to both lists of transforms in scene before and after import
                    if k==allTransformsBeforeImport[j]:
                        # Remove this element
                        allTransformsAfterImport.remove(k)
            # Select the one element remaining in list of transforms in scene after import, i.e., the imported asset
            cmds.select(allTransformsAfterImport[0])

            # Rename the newly imported mesh
            cmds.rename(name+"_"+str(i+1))
       
            # A AMELIORER : REGLER L'ATTRIBUT NEAR CLIP PLANE DE LA CAMERA COURANTE A 0.1
            cmds.move(targetzoneCoord[0]-uniform(-500,500),0,targetzoneCoord[2]-uniform(-500,500),name+"_"+str(i+1))
          
                
    def alignmentMove(self,name,nbPopulation,targetX,targetZ,coeffA):
        '''
        alignmentMove():
            Déplace chaque agent (cube) d une unite de distance vers la cible.
            @param:    name : nom de l'agent (type string)
                       nbPopulation : nombre d'agents dans le groupe (type int)
                       targetX : position en X de la cible (type float)
                       targetZ : position en Z de la cible (type float)
            @return:   rien
        '''
        for i in range(nbPopulation):
    
            currentPos=cmds.xform(name+"_"+str(i+1),q=True,translation=True)
            # Calcul du vecteur de direction vers la cible
            vAlignment=[targetX-currentPos[0],0,targetZ-currentPos[2]]
            alignmentNorm=sqrt(vAlignment[0]*vAlignment[0]+vAlignment[2]*vAlignment[2])
            
            if (alignmentNorm!=0):
                # Normalisation du vecteur de direction vers la cible
                vNormalizedAlignment=[vAlignment[0]/alignmentNorm,0,vAlignment[2]/alignmentNorm]
                # Deplacement d une unite de distance vers la cible
                cmds.move(coeffA*vNormalizedAlignment[0],0,coeffA*vNormalizedAlignment[2],name+"_"+str(i+1),r=True)


    def cohesionMove(self,name,nbPopulation,coeffC):
        '''
        cohesionMove():
            Déplace chaque agent (cube) d une unite de distance vers le centre (barycentre) du groupe d'agents.
            @param:    name : nom de l'agent (type string)
                       nbPopulation : nombre d'agents dans le groupe (type int)
            @return:   rien
        '''
        sumPosX=0
        sumPosZ=0
        
        # Determination des coordonees du barycentre du groupe d agents
        for i in range(nbPopulation):
            currentPos=cmds.xform(name+"_"+str(i+1),q=True,translation=True)
            sumPosX=+currentPos[0]
            sumPosZ=+currentPos[2]
        
        averagePos=[sumPosX/nbPopulation,0,sumPosZ/nbPopulation]
        
        # Calcul du vecteur de deplacement
        for i in range(nbPopulation):
            currentPos=cmds.xform(name+"_"+str(i+1),q=True,translation=True)
            # Calcul du vecteur de direction vers barycentre du groupe d agents
            vCohesion=[averagePos[0]-currentPos[0],0,averagePos[2]-currentPos[2]]
            cohesionNorm=sqrt(vCohesion[0]*vCohesion[0]+vCohesion[2]*vCohesion[2])
                        
            if (cohesionNorm!=0):
                # Normalisation du vecteur de direction vers barycentre du groupe d agents
                vNormalizedCohesion=[vCohesion[0]/cohesionNorm,0,vCohesion[2]/cohesionNorm]
                # Deplacement d une unite de distance vers barycentre du groupe d agents
                cmds.move(coeffC*vNormalizedCohesion[0],0,coeffC*vNormalizedCohesion[2],name+"_"+str(i+1),r=True)


    def separationMove(self,name,nbPopulation,minFriendDistance,coeffS):
        '''
        separationMove():
            Déplace chaque agent (cube) d une unite de distance dans la direction opposée à la position moyenne de ses voisins situés dans un rayon inférieur à une valeur fixée par l'utilisateur ("minFriendDistance").
            Des coefficients de pondération sont affectés préalablement à chacune des positions desdits voisins, de telle sorte qu'au sein de la zone de voisinage considérée, les voisins les plus proches de l'agent 
            concerné entraînent un éloignement de ce dernier proportionnellement plus grand que celui qu'entraînent des voisins plus éloignés.
            @param:    name : nom de l'agent (type string)
                       nbPopulation : nombre d'agents dans le groupe (type int)
                       minFriendDistance : rayon de la zone circulaire autour de chaque agent dans laquelle la présence de tout voisin entraîne un mouvement de séparation (répulsion) dudit agent par rapport audit voisin (type float)
            @return:   rien
        '''
        for i in range(nbPopulation):
            
            startingPos=cmds.xform(name+"_"+str(i+1),q=True,translation=True)
            
            for j in range(nbPopulation):
                
                # Pour chaque agent du groupe, calcul de la distance entre celui ci et chacun des autres agents du groupe
                if(name+"_"+str(j+1)!=name+"_"+str(i+1)):
                    currentFriendPos=cmds.xform(name+"_"+str(j+1),q=True,translation=True)
                    vFriendDistance=[currentFriendPos[0]-startingPos[0],0,currentFriendPos[2]-startingPos[2]]
                    friendDistanceNorm=sqrt(vFriendDistance[0]*vFriendDistance[0]+vFriendDistance[2]*vFriendDistance[2])
                    
                    # Deplace l agent concerne d une unite de distance (deplacement standard arbitraire) dans l'hypothese hautement improbable ou deux agents seraient generes a l exacte meme position
                    if(friendDistanceNorm==0):
                        cmds.move(minFriendDistance,0,0,name+"_"+str(i+1),r=True)
                    
                    # Deplace chaque agent selon la proximite ou l eloignement relatif de ses voisins directs
                    if(0<friendDistanceNorm<minFriendDistance):
                        vSeparation=[-vFriendDistance[0]*minFriendDistance/friendDistanceNorm,0,-vFriendDistance[2]*minFriendDistance/friendDistanceNorm]
                        cmds.move(vSeparation[0],0,vSeparation[2],name+"_"+str(i+1),r=True)   
        
            endingPos=cmds.xform(name+"_"+str(i+1),q=True,translation=True)
            
            # Calcul du vecteur de separation intermediaire
            vAggregateSeparation=[endingPos[0]-startingPos[0],0,endingPos[2]-startingPos[2]]
            aggregateSeparationNorm=sqrt(vAggregateSeparation[0]*vAggregateSeparation[0]+vAggregateSeparation[2]*vAggregateSeparation[2])
            
            if(aggregateSeparationNorm!=0):
                # Normalisation du vecteur de separation intermediaire
                vNormalizedAggregateSeparation=[vAggregateSeparation[0]/aggregateSeparationNorm,0,vAggregateSeparation[2]/aggregateSeparationNorm]
                # Deplacement d une unite de distance dans la direction opposee aux voisins directs (application du vecteur de separation intermediaire apres sa normalisation)
                cmds.move(coeffS*vNormalizedAggregateSeparation[0],0,coeffS*vNormalizedAggregateSeparation[2],name+"_"+str(i+1),r=True)


#------------------------------------------------------------------------------------
# FUNCTIONS
#------------------------------------------------------------------------------------

def createGround():
    cmds.polyPlane(n="ground",w=6000,h=6000,sx=100,sy=100)
    # A AMELIORER : MULTIPLIER AUTOMATIQUEMENT PAR 10 L'ATTRIBUT FAR CLIP PLANE DE LA CAMERA COURANTE


def createRandomTarget(name):
    # Cree la cible
    cmds.polyCylinder(n=name,r=10,h=300)
    # EN COURS / A FAIRE : REMPLACER POSITION DE TARGET PAR UNE ZONE SELECTIONNEE PAR UTILISATEUR
    targetPos=[randint(-2800,2800),150,randint(-2800,2800)]
    cmds.move(targetPos[0],targetPos[1],targetPos[2],name)
           
    # Cree et applique un shader rouge a la cible
    targetShader=cmds.shadingNode("lambert",asShader=True)
    cmds.sets(renderable=True,noSurfaceShader=True,empty=True,name=targetShader+"SG")
    cmds.connectAttr(targetShader+".outColor",targetShader+"SG.surfaceShader")
                
    cmds.sets(name,e=True,fe=targetShader+"SG")
           
    cmds.setAttr(targetShader+".colorR",1)
    cmds.setAttr(targetShader+".colorG",0)
    cmds.setAttr(targetShader+".colorB",0)
            
    return targetPos[0],targetPos[2]



#------------------------------------------------------------------------------------
# INTERFACE
#------------------------------------------------------------------------------------

# Pour une raison non identifiée, la commande "if cmds.window("Mesh Modifier", exists=True): cmds.deleteUI("Mesh Modifer")" ne 
# fonctionne pas ici du fait que le système ne semble reconnaître que des fenêtres du nom de window1, window2, window3, 
# etc. à chaque nouvelle exécution du script. La boucle for ci-dessous a donc été ajoutée comme solution temporaire permettant 
# la suppression d'au plus 10 fenêtres de ce plug-in dans l'hypothèse où celles-ci n'auraient été successivement ouvertes que 
# via l'exécution partielle de ce script (c'est-à-dire sans que ne soit exécutée au préalable la commande ci-dessous automatisant
# la suppression de fenêtres pré-existantes).
boidName="individu"

# Variables
coeffA=9
coeffC=1
coeffS=1
minFriendDistance=120
#maxDistanceFromTarget=2
nbPopulation=10
targetPosX,targetPosZ=createRandomTarget("target")

for i in range(10):
    if cmds.window("window"+str(i+1),exists=True):
        cmds.deleteUI("window"+str(i+1))
    
cmds.window()
cmds.columnLayout(adjustableColumn=True)
    
cmds.separator(h=12)
    
cmds.button(label="Create Ground",c="createGround()")

cmds.separator(h=5)
    
cmds.button(label="Spawn Agents",c="foule=Agents(boidName,nbPopulation,targetPosX,targetPosZ,minFriendDistance,coeffA,coeffC,coeffS)")

cmds.separator(h=5)
    
cmds.button(label="Execute",c="launchSim()")
    
#cmds.separator(h=5)
    
#cmds.button(label="Validate Spawn Spot",c="spawnzoneCoord[0],spawnzoneCoord[2]=capturespawnCoords()")

cmds.separator(h=12)

cmds.showWindow()



#------------------------------------------------------------------------------------
# SCENE MANAGER
#------------------------------------------------------------------------------------

def launchSim():

    #fps=fpsExtractor()
    #createGround()
    
    #foule=Agents(boidName,nbPopulation,spawnzoneCoord[0],spawnzoneCoord[2],targetPosX,targetPosZ,minFriendDistance,coeffA,coeffC,coeffS)
    
    #check=checkDistanceFromTarget(nbPopulation,targetPosX,targetPosZ,maxDistanceFromTarget)
    
    i=0
    
    while(i<400):
        
        #start=time.time()
         
        cmds.currentTime(i+1)
         
        foule.alignmentMove(boidName,nbPopulation,targetPosX,targetPosZ,coeffA)
        #foule.cohesionMove("individu",25,1)
        foule.separationMove(boidName,nbPopulation,minFriendDistance,coeffS)
        
        for j in range(nbPopulation):
            cmds.select(boidName+"_"+str(j+1))
            cmds.setKeyframe(at="translateX")
            cmds.setKeyframe(at="translateZ")
        #for i in range(nbPopulation)
        
        
        #checkDistanceFromTarget(nbPopulation,targetPosX,targetPosZ,maxDistanceFromTarget)
        
        i=i+1
    #end=time.time()    
    #print(end-start)

    #A NE PAS UTILISER -> FAIT PLANTER LE SCRIPT PROBABLEMENT DU A UNE TROP GROSSE VARIATION DE TEMPS DE CALCUL A CHAQUE NOUVELLE ITERATION DE LA BOUCLE WHILE, CE QUI ENTRAINE DES TEMPS DE VEILLE NEGATIFS"
    #if(fps<30.1):
    #    time.sleep(1/fps-(end-start))