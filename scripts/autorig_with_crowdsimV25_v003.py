import maya.cmds as cmds
from random import *
from math import *
import time

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#                                     AUTORIG
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------

#Add your geometry
def CreationLoc():
    if cmds.objExists('Loc_master'):
        print("Exists already")
    else:  
        cmds.group(n='Loc_master', em=True)
        global list
        list = ['root', 'neck','elbow','wrist','knee','toe']
        for i in range (len(list)):
            loc = cmds.spaceLocator(n='Loc+'+list[i])
            cmds.parent(loc, 'Loc_master')    
def Check():
    charName = cmds.textFieldGrp(NameInput,q= True,text = True)

        
def CreateJoints():
    charName = cmds.textFieldGrp(NameInput,q= True,text = True)
    if charName == "":
        print("Write your character name")
    else :
      #Create directory
        listDirectory = [['_Joints_','_Controls_','_ikHandle_'],'_GlobalControl_','_Geo_']
        cmds.group(em=True, n= charName+'_Main_01')
        for i in range (len(listDirectory)-1):
            cmds.group(em=True, n= charName + listDirectory[i+1]+'01')
            cmds.parent(charName + listDirectory[i+1]+'01',charName+'_Main_01')
        for i in range(len(listDirectory[0])):
            cmds.group(em = True, n= charName + listDirectory[0][i]+'01')
            cmds.parent(charName + listDirectory[0][i]+'01',charName + listDirectory[1]+'01')
        cmds.select(d=True)
        global locXYZ
        locXYZ= [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        for i in range(len(list)):
            locXYZ[i][0]= cmds.getAttr('Loc_'+list[i]+'.translateX')
            print('translateX calcule done')
            locXYZ[i][1]= cmds.getAttr('Loc_'+list[i]+'.translateY')
            print('translateY calcule done')
            locXYZ[i][2]= cmds.getAttr('Loc_'+list[i]+'.translateZ')
            print('translateZ calcule done')
        #total length between root and neck
        lengthY = locXYZ[1][1]-locXYZ[0][1]
        lengthZ = abs(locXYZ[0][2])+abs(locXYZ[1][2])
        #length between root and toe
        legY = locXYZ[0][1]-locXYZ[5][1] 
        lengthY = locXYZ[1][1]-locXYZ[0][1]
        lengthZ = abs(locXYZ[0][2])+abs(locXYZ[1][2])
        #length between root and toe
        legY = locXYZ[0][1]-locXYZ[5][1]
        cmds.joint(p=(locXYZ[0][0],locXYZ[0][1],locXYZ[0][2]),n = charName + '_root'+'_Jnt_01')
        def PlaceJoint(OrientThisJoint,x,y,z,jointName,o):
            cmds.joint(p=(x,y,z),n = jointName)
            cmds.joint(OrientThisJoint,e=True,zso=True, oj='xyz', sao= o+'up')
        #place spline-head joint    
        PlaceJoint(charName + '_root'+'_Jnt_01',0,locXYZ[0][1] + lengthY*0.43, locXYZ[0][2] + lengthZ*0.43,charName + '_spline'+'_Jnt_01','x')
        PlaceJoint(charName + '_spline'+'_Jnt_01',0,locXYZ[0][1] + lengthY*0.8,locXYZ[0][2] + lengthZ*0.18,charName + '_spline'+'_Jnt_02','x')
        PlaceJoint(charName + '_spline'+'_Jnt_02',locXYZ[1][0],locXYZ[1][1],locXYZ[1][2],charName + '_spline'+'_Jnt_03', 'x')
        PlaceJoint(charName + '_spline'+'_Jnt_03',locXYZ[1][0],locXYZ[1][1]+lengthY*0.1,locXYZ[1][2]+lengthY*0.05,charName + '_neck'+'_Jnt_01','x')
        PlaceJoint(charName + '_neck'+'_Jnt_01',(locXYZ[1][0]+locXYZ[1][0])/2,locXYZ[1][1]+lengthY/4,(locXYZ[1][2]+locXYZ[0][2]+lengthY*0.15)/2,charName + '_jaw'+'_Jnt_01','x')
        PlaceJoint(charName + '_jaw'+'_Jnt_01',(locXYZ[1][0]+locXYZ[1][0])/4,locXYZ[1][1]+lengthY/2.8,(locXYZ[1][2]+locXYZ[0][2]+lengthY*0.15)/2,charName + '_eye'+'_Jnt_01','x')
        PlaceJoint(charName + '_eye'+'_Jnt_01',0,locXYZ[1][1]+lengthY/1.8, locXYZ[0][2]+lengthY*0.03,charName + '_head'+'_Jnt_01','x')
        cmds.joint(charName + '_head'+'_Jnt_01', e=True,oj='none', ch=True,zso=True)
        
        #place arm joint
        cmds.select(d=True)
        cmds.joint(charName + '_spline'+'_Jnt_03',p=(locXYZ[0][0]+lengthY*0.1,locXYZ[1][1],locXYZ[0][2]+lengthZ*0.1), n = charName + '_L'+'_shoulder'+'_Jnt_01')
        PlaceJoint(charName + '_L'+'_shoulder'+'_Jnt_01',locXYZ[0][0]+lengthY*0.24,locXYZ[1][1]-lengthY*0.05,locXYZ[0][2]-lengthZ*0.2,charName +'_L'+ '_shoulder'+'_Jnt_02','y')
        PlaceJoint(charName + '_L'+'_shoulder'+'_Jnt_02',(locXYZ[0][0]+lengthY*0.24+locXYZ[2][0]-lengthZ*0.1)/2,(locXYZ[1][1]-lengthY*0.05+locXYZ[2][1]+lengthZ*0.1)/2,(locXYZ[0][2]-lengthZ*0.2+locXYZ[2][2])/2,charName +'_L'+ '_arm'+'_Jnt_01','y')
        PlaceJoint(charName +'_L'+ '_arm'+'_Jnt_01',locXYZ[2][0]-lengthZ*0.1,locXYZ[2][1]+lengthZ*0.1,locXYZ[2][2],charName + '_L'+'_arm'+'_Jnt_02','y')
        PlaceJoint(charName + '_L'+'_arm'+'_Jnt_02',locXYZ[2][0]+lengthZ*0.1,locXYZ[2][1]-lengthZ*0.1,locXYZ[2][2],charName + '_L'+'_arm'+'_Jnt_03','y')
        PlaceJoint(charName + '_L'+'_arm'+'_Jnt_03',(locXYZ[2][0]+lengthZ*0.1+locXYZ[3][0])/2,(locXYZ[2][1]-lengthZ*0.1+locXYZ[3][1])/2,(locXYZ[2][2]+locXYZ[3][2])/2,charName + '_L'+'_arm'+'_Jnt_04','y')
        PlaceJoint(charName +'_L'+ '_arm'+'_Jnt_04',locXYZ[3][0],locXYZ[3][1],locXYZ[3][2],charName + '_L'+'_wrist'+'_Jnt_01','y')
        PlaceJoint(charName + '_L'+'_wrist'+'_Jnt_01',locXYZ[3][0],locXYZ[3][1]+lengthY*-0.20,locXYZ[3][2],charName + '_L'+'_hand'+'_Jnt_01','y')
        cmds.joint(charName + '_L'+'_hand'+'_Jnt_01', e=True,oj='none', ch=True,zso=True)
        
        #place leg joint
        cmds.select(d=True)
        cmds.joint(charName + '_root'+'_Jnt_01',p=(locXYZ[0][0]+lengthY*0.08,locXYZ[0][1],locXYZ[0][2]-lengthZ/3.9),n=charName +'_L'+ '_hip'+'_Jnt_01')
        PlaceJoint(charName +'_L'+ '_hip'+'_Jnt_01',locXYZ[0][0]+lengthY*0.21,locXYZ[0][1]+legY*0.03,locXYZ[0][2]-lengthZ/1.86,charName + '_L'+'_thigh'+'_Jnt_01','x')
        PlaceJoint(charName +'_L'+ '_thigh'+'_Jnt_01',locXYZ[4][0]-legY*0.005,locXYZ[4][1]+legY*0.05,locXYZ[4][2],charName +'_L'+ '_knee'+'_Jnt_01','x')
        PlaceJoint(charName + '_L'+'_knee'+'_Jnt_01',locXYZ[4][0]+legY*0.005,locXYZ[4][1]-legY*0.05,locXYZ[4][2]-legY*0.03,charName +'_L'+ '_knee'+'_Jnt_02','x')
        PlaceJoint(charName + '_L'+'_knee'+'_Jnt_02',locXYZ[5][0]-locXYZ[4][0]*0.3,locXYZ[5][1]+locXYZ[4][1]*0.17,locXYZ[4][2]-legY*0.03-(locXYZ[5][2]-locXYZ[4][2])/6,charName + '_L'+'_ankie'+'_Jnt_01','x')
        PlaceJoint(charName +'_L'+ '_ankie'+'_Jnt_01',(locXYZ[5][0]-locXYZ[4][0]*0.3+locXYZ[5][0])/2,locXYZ[5][1],locXYZ[4][2]+locXYZ[5][2]/1.9,charName +'_L'+ '_ball'+'_Jnt_01','x')
        PlaceJoint(charName +'_L'+ '_ball'+'_Jnt_01',locXYZ[5][0],locXYZ[5][1],locXYZ[5][2],charName +'_L'+ '_toe'+'_Jnt_01','x')
        cmds.joint(charName +'_L'+ '_toe'+'_Jnt_01', e=True,oj='none', ch=True,zso=True)
    
#Mirror joint
def MirrorJoints():
    charName = cmds.textFieldGrp(NameInput,q= True,text = True)
    cmds.mirrorJoint(charName +'_L'+ '_hip'+'_Jnt_01',mirrorYZ=True,mirrorBehavior=True,searchReplace=('_L_', '_R_') )
    cmds.joint(charName +'_R'+ '_hip_Jnt_01', e=True,oj='xyz', ch=True,zso=True, sao='xup')
    cmds.mirrorJoint(charName +'_L'+ '_shoulder'+'_Jnt_01',mirrorYZ=True,mirrorBehavior=True,searchReplace=('_L_', '_R_') )
    cmds.joint(charName +'_R'+ '_shoulder_Jnt_01', e=True,oj='xyz', ch=True,zso=True, sao='yup')
    cmds.joint(charName + '_R'+'_wrist'+'_Jnt_01', e=True,oj='none', ch=True,zso=True)
    cmds.joint(charName +'_R'+ '_toe'+'_Jnt_01', e=True,oj='none', ch=True,zso=True)
    cmds.select(d=True)

#Create IK Handle 
#for Legs
def Controllers():
    charName = cmds.textFieldGrp(NameInput,q= True,text = True)
    lengthY = locXYZ[1][1]-locXYZ[0][1]
    lengthZ = abs(locXYZ[0][2])+abs(locXYZ[1][2])
    legY = locXYZ[0][1]-locXYZ[5][1] 
    side =['_L_','_R_']
    nb = [1,-1]    
    for i in range(len(side)):
        cmds.ikHandle(n=  charName +'_Leg'+side[i]+'ikHandle', sj= charName+side[i]+'thigh_Jnt_01', ee=charName+side[i]+'ankie_Jnt_01')
        cmds.spaceLocator(n= charName +'_poleVector'+side[i]+'leg',p=(nb[i]*locXYZ[4][0]-legY*0.005,locXYZ[4][1]+legY*0.05,locXYZ[4][2]))
        cmds.xform(centerPivots=1)
        # aims the pole vector of 1 at 2.
        cmds.poleVectorConstraint(  charName +'_poleVector'+side[i]+'leg',  charName +'_Leg'+side[i]+'ikHandle' )
        cmds.move(nb[i]*lengthY*0.75,-lengthY*0.75, charName +'_poleVector'+side[i]+'leg',moveXY=True)
        cmds.setAttr( charName +'_Leg'+side[i]+'ikHandle.twist',nb[i]*90)
        cmds.ParentConstraint( charName +'controllerfoot', charName +'_poleVector'+side[i]+'leg')
        cmds.parent(  charName +'_poleVector'+side[i]+'leg',  charName +'_Leg'+side[i]+'ikHandle', relative=True )
        cmds.ikHandle(n=  charName +'_Foot'+side[i]+'ball_ikHandle', sj = charName + side[i]+'ankie'+'_Jnt_01', ee = charName +side[i]+'ball'+'_Jnt_01')
        cmds.ikHandle(n=  charName +'_Foot'+side[i]+'toe_ikHandle', sj = charName +side[i]+ 'ball'+'_Jnt_01', ee = charName +side[i]+'toe'+'_Jnt_01')
        cmds.group( charName +'_Leg'+side[i]+'ikHandle', n=  charName +'_Foot'+side[i]+'heelPeel')
        #change pivot position
        Xpos = cmds.getAttr( charName +'_Foot'+side[i]+'ball_ikHandle.translateX' )
        Ypos = cmds.getAttr( charName +'_Foot'+side[i]+'ball_ikHandle.translateY' )
        Zpos = cmds.getAttr( charName +'_Foot'+side[i]+'ball_ikHandle.translateZ' )
        cmds.move(Xpos, Ypos, Zpos,  charName +'_Foot'+side[i]+'heelPeel.scalePivot', charName +'_Foot'+side[i]+'heelPeel.rotatePivot', absolute=True)
        cmds.group( charName +'_Foot'+side[i]+'ball_ikHandle', charName +'_Foot'+side[i]+'toe_ikHandle', n =  charName +'_Foot'+side[i]+'toeTap')
        cmds.move(Xpos, Ypos, Zpos,  charName +'_Foot'+side[i]+'toeTap.scalePivot', charName +'_Foot'+side[i]+'toeTap.rotatePivot', absolute=True)
        cmds.group( charName +'_Foot'+side[i]+'ball_ikHandle', charName +'_Foot'+side[i]+'toeTap', n =  charName +'_Foot'+side[i]+'TipToe')
        cmds.group(n =  charName +'_Foot'+side[i]+'1',em=True)
        cmds.parent(  charName +'_Foot'+side[i]+'heelPeel', charName +'_Foot'+side[i]+'TipToe',  charName +'_Foot'+side[i]+'1', relative=True )
        cmds.move(Xpos, Ypos, Zpos,  charName +'_Foot'+side[i]+'1.scalePivot', charName +'_Foot'+side[i]+'1.rotatePivot', absolute=True)
        Xpos = cmds.getAttr( charName +'_Foot'+side[i]+'ball_ikHandle.translateX' )
        Ypos = cmds.getAttr( charName +'_Foot'+side[i]+'ball_ikHandle.translateY' )
        Zpos = cmds.getAttr( charName +'_Foot'+side[i]+'ball_ikHandle.translateZ' )
        CreateCtr(charName+'_Foot'+side[i]+'Crl',charName+'_Foot'+side[i]+'1',(Xpos,Ypos,Zpos),(lengthY/60*10,lengthY/60*10,lengthY/60*16),(0,0,0))
    #left Arm
    for i in range(len(side)):
        cmds.ikHandle(n=  charName +'_Arm'+str(side[i])+'ikHandle', sj = charName + str(side[i])+'shoulder'+'_Jnt_02', ee = charName + str(side[i])+'wrist'+'_Jnt_01')
        cmds.CreateNURBSCircle()
        cmds.rename('nurbsCircle1', charName +'_Elbow'+str(side[i])+'Crl')
        cmds.move(nb[i]*locXYZ[2][0],locXYZ[2][1],locXYZ[2][2]*30)
        cmds.scale(2,2,3)
        cmds.rotate(90,0,0)
        cmds.move(nb[i]*locXYZ[2][0], locXYZ[2][1],locXYZ[2][2],  charName +'_Elbow'+str(side[i])+'Crl.scalePivot', charName +'_Elbow'+str(side[i])+'Crl.rotatePivot', absolute=True)
        cmds.makeIdentity(apply=True)
        cmds.xform(centerPivots=1)
        cmds.poleVectorConstraint(  charName +'_Elbow'+str(side[i])+'Crl',  charName +'_Arm'+str(side[i])+'ikHandle' )
        #left Arm controller
        CreateCtr(charName+'_Arm'+side[i]+'Crl',charName+'_Arm'+side[i]+'ikHandle',(nb[i]*locXYZ[3][0],locXYZ[3][1],locXYZ[3][2]),(lengthY/60*5,lengthY/60*5,lengthY/60*8),(0,0,nb[i]*30))
    #spline
    cmds.parent(charName+'_R_shoulder_Jnt_01', w=True)    
    cmds.parent(charName+'_L_shoulder_Jnt_01', w=True)    
    cmds.select(d=True)
    cmds.select(charName+'_spline_Jnt_03')
    cmds.DisconnectJoint(charName+'_spline_Jnt_03')
    cmds.rename(charName+'_spline_Jnt_03',charName+'_neck_Jnt_00')
    cmds.rename('joint1',charName+'_spline_Jnt_03')
    cmds.rename(charName + '_root'+'_Jnt_01',charName+'_spline_Jnt_00')
    cmds.parent(charName+'_R_hip_Jnt_01', w=True)    
    cmds.parent(charName+'_L_hip_Jnt_01', w=True) 
    cmds.select(d=True)
    cmds.joint(p=(locXYZ[0][0],locXYZ[0][1],locXYZ[0][2]),n = charName + '_root'+'_Jnt_01')
    cmds.parent(charName+'_L_hip_Jnt_01')
    cmds.select(charName + '_root'+'_Jnt_01')
    cmds.parent(charName+'_R_hip_Jnt_01')
    cmds.curve(n=charName+'_SplineIK_Crv_01', p=[(locXYZ[0][0], locXYZ[0][1],locXYZ[0][2]), (0.0,locXYZ[0][1] + lengthY*0.43, locXYZ[0][2] + lengthZ*0.43), (0.0,locXYZ[0][1] + lengthY*0.8,locXYZ[0][2] + lengthZ*0.18), (locXYZ[1][0],locXYZ[1][1],locXYZ[1][2])] )
    cmds.ikHandle(n= charName+'SplineIK_01',sj= charName+'_spline_Jnt_00', ee = charName+'_spline_Jnt_03',curve = charName+'_SplineIK_Crv_01',sol='ikSplineSolver',createCurve = False,parentCurve= False )
    for i in range(4):
        cmds.select(charName+'_SplineIK_Crv_01'+'.cv['+str(i)+']')
        cmds.cluster(n='cluster_'+str(i+1))
    CreateCtr(charName+'_Spline_Ctrl_01','cluster_1Handle',(0,locXYZ[0][1]*1.05,0),(lengthY/60*25,lengthY/60*25,lengthY/60*25),(0,0,0))
    cmds.parentConstraint(charName+'_Spline_Ctrl_01',charName+'_root_Jnt_01', maintainOffset=True)
    CreateCtr(charName+'_Chest_Ctrl_01','cluster_4Handle',(0,locXYZ[1][1],0),(lengthY/60*25,lengthY/60*25,lengthY/60*25),(0,0,0))
    for i in range(len(side)):
        cmds.parentConstraint(charName+'_Chest_Ctrl_01',charName+side[i]+'shoulder_Jnt_01', maintainOffset=True)
        cmds.parent(charName+'_Arm'+side[i]+'Crl_grp',charName+'_Chest_Ctrl_01')
        cmds.parent(charName+'_Elbow'+side[i]+'Crl',charName+'_Chest_Ctrl_01')
    CreateCtr(charName+'_Chest_Ctrl_02','cluster_2Handle',(0,(locXYZ[0][1]+locXYZ[1][1])/2,0),(lengthY/60*20,lengthY/60*20,lengthY/60*20),(0,0,0))
    cmds.parentConstraint(charName+'_Chest_Ctrl_01',charName+'_neck_Jnt_00', maintainOffset=True,w=1)
    cmds.parentConstraint(charName+'_Chest_Ctrl_01','cluster_3Handle', maintainOffset=True, weight=0.5)
    cmds.parentConstraint(charName+'_Chest_Ctrl_01',charName+'_Chest_Ctrl_02_grp', maintainOffset=True, weight=0.5)
    cmds.parentConstraint(charName+'_Spline_Ctrl_01',charName+'_Chest_Ctrl_02_grp', maintainOffset=True, weight=0.5)
    cmds.CreateNURBSCircle()
    cmds.rename('nurbsCircle1',charName+'_Hip_Ctrl_01')
    cmds.move(0,locXYZ[0][1],0)
    cmds.scale(lengthY/60*30,lengthY/60*30,lengthY/60*30)
    cmds.makeIdentity(apply=True)
    cmds.parentConstraint(charName+'_Hip_Ctrl_01',charName+'_Spline_Ctrl_01', maintainOffset=True, weight=0.5)
    cmds.parentConstraint(charName+'_Hip_Ctrl_01',charName+'_Chest_Ctrl_01', maintainOffset=True, weight=0.5)
    #clean
    for i in range(len(side)):
        cmds.parent(charName+side[i]+'shoulder_Jnt_01',charName+'_Joints_01')
        cmds.parent(charName+'_Chest_Ctrl_0'+str(i+1)+'_grp',charName+'_Controls_01')
        cmds.parent( charName +'_Foot'+side[i]+'1',charName+'_Controls_01')
        cmds.parent( charName +'_Foot'+side[i]+'Crl_grp',charName+'_Controls_01')
        cmds.parent( charName +'_Arm'+side[i]+'ikHandle',charName+'_ikHandle_01')
        cmds.parent('cluster_'+str(i+1)+'Handle',charName+'_ikHandle_01')
        cmds.parent('cluster_'+str(i+3)+'Handle',charName+'_ikHandle_01')
    cmds.parent(charName+'SplineIK_01',charName+'_ikHandle_01')
    cmds.parent(charName+'_SplineIK_Crv_01',charName+'_ikHandle_01')
    cmds.parent(charName+'_neck_Jnt_00',charName+'_Joints_01')
    cmds.parent(charName+'_root_Jnt_01',charName+'_Joints_01')
    cmds.parent(charName+'_spline_Jnt_00',charName+'_Joints_01')    
    cmds.parent(charName+'_Spline_Ctrl_01_grp',charName+'_Controls_01')
    cmds.parent(charName+'_Hip_Ctrl_01',charName+'_Controls_01')
    
def CreateCtr(nameCtr,ObjToParent,(posX,posY,posZ),(scaleX,scaleY,scaleZ),(rotateX,rotateY,rotateZ)):
    cmds.CreateNURBSCircle()
    cmds.rename('nurbsCircle1',nameCtr)
    cmds.move(posX,posY,posZ)
    cmds.scale(scaleX,scaleY,scaleZ)
    cmds.makeIdentity(apply=True)
    cmds.group(nameCtr, n= nameCtr+'_grp')
    cmds.rotate(rotateX,rotateY,rotateZ)
    cmds.parentConstraint(nameCtr,ObjToParent, mo=True)
'''def ImportOBJ():
    def importImage( fileName, fileType):
       cmds.file( fileName, i=True );
       return 1
    cmds.fileBrowserDialog( m=0, fc=ImportOBJ(), ft='OBJ', an='Import_Image', om='Import' )
'''

def Bind():
    charName = cmds.textFieldGrp(NameInput,q= True,text = True)
    cmds.select(charName+'_Joints_01',hi=True)
    # if charName+'_Geo_01' null print 'put your model in Main>Geo group'
    cmds.select(charName+'_Geo_01',hi=True,add= True)
    cmds.bindSkin()
    
def SetKeyAnimation(object,time,attr,value):
    cmds.currentTime(time)
    cmds.setKeyframe(object, v=value, attribute=attr)
def Anim():
    charName = cmds.textFieldGrp(NameInput,q= True,text = True)
    SetKeyAnimation(charName+'_Chest_Ctrl_01',7,'translateX',-8)
    SetKeyAnimation(charName+'_Chest_Ctrl_01',19,'translateX',8)
    SetKeyAnimation(charName+'_Chest_Ctrl_01',31,'translateX',-8)
    SetKeyAnimation(charName+'_Chest_Ctrl_01',1,'translateZ',0)
    SetKeyAnimation(charName+'_Chest_Ctrl_01',13,'translateZ',5)
    SetKeyAnimation(charName+'_Chest_Ctrl_01',25,'translateZ',0)
    SetKeyAnimation(charName+'_Chest_Ctrl_01',1,'rotateY',-5)
    SetKeyAnimation(charName+'_Chest_Ctrl_01',13,'rotateY',5)
    SetKeyAnimation(charName+'_Chest_Ctrl_01',1,'rotateY',-5)
    SetKeyAnimation(charName+'_Arm_L_Crl',1,'translateX',-10)
    SetKeyAnimation(charName+'_Arm_L_Crl',13,'translateX',-5)
    SetKeyAnimation(charName+'_Arm_L_Crl',25,'translateX',-10)
    SetKeyAnimation(charName+'_Arm_L_Crl',1,'translateY',10)
    SetKeyAnimation(charName+'_Arm_L_Crl',13,'translateY',5)
    SetKeyAnimation(charName+'_Arm_L_Crl',25,'translateY',10)
    SetKeyAnimation(charName+'_Arm_L_Crl',1,'translateZ',15)
    SetKeyAnimation(charName+'_Arm_L_Crl',13,'translateZ',-25)
    SetKeyAnimation(charName+'_Arm_L_Crl',25,'translateZ',15)
    SetKeyAnimation(charName+'_Elbow_L_Crl',1,'translateX',20)
    SetKeyAnimation(charName+'_Elbow_L_Crl',13,'translateX',-10)
    SetKeyAnimation(charName+'_Elbow_L_Crl',25,'translateX',20)
    SetKeyAnimation(charName+'_Arm_R_Crl',1,'translateY',5)
    SetKeyAnimation(charName+'_Arm_R_Crl',13,'translateY',10)
    SetKeyAnimation(charName+'_Arm_R_Crl',25,'translateY',5)
    SetKeyAnimation(charName+'_Arm_R_Crl',1,'translateZ',5)
    SetKeyAnimation(charName+'_Arm_R_Crl',13,'translateZ',10)
    SetKeyAnimation(charName+'_Arm_R_Crl',25,'translateZ',5)
    SetKeyAnimation(charName+'_Elbow_R_Crl',1,'translateX',10)
    SetKeyAnimation(charName+'_Elbow_R_Crl',13,'translateX',-20)
    SetKeyAnimation(charName+'_Elbow_R_Crl',25,'translateX',10)
    SetKeyAnimation(charName+'_Foot_L_Crl',1,'translateY',0)
    SetKeyAnimation(charName+'_Foot_L_Crl',7,'translateY',15)
    SetKeyAnimation(charName+'_Foot_L_Crl',13,'translateY',0)
    SetKeyAnimation(charName+'_Foot_L_Crl',19,'translateY',0)
    SetKeyAnimation(charName+'_Foot_L_Crl',1,'translateZ',-20)
    SetKeyAnimation(charName+'_Foot_L_Crl',13,'translateZ',20)
    SetKeyAnimation(charName+'_Foot_L_Crl',25,'translateZ',-20)
    SetKeyAnimation(charName+'_Foot_L_Crl',1,'rotateX',20)
    SetKeyAnimation(charName+'_Foot_L_Crl',13,'rotateX',-15)
    SetKeyAnimation(charName+'_Foot_L_Crl',16,'rotateX',0)
    SetKeyAnimation(charName+'_Foot_L_Crl',19,'rotateX',0)
    SetKeyAnimation(charName+'_Foot_L_Crl',25,'rotateX',20)
    SetKeyAnimation(charName+'_Chest_Ctrl_02',1,'translateZ',-10)
    SetKeyAnimation(charName+'_Chest_Ctrl_02',13,'translateZ',-5)
    SetKeyAnimation(charName+'_Chest_Ctrl_02',25,'translateZ',-10)
    SetKeyAnimation(charName+'_Foot_R_Crl',7,'translateY',0)
    SetKeyAnimation(charName+'_Foot_R_Crl',13,'translateY',0)
    SetKeyAnimation(charName+'_Foot_R_Crl',19,'translateY',15)
    SetKeyAnimation(charName+'_Foot_R_Crl',25,'translateY',0)
    SetKeyAnimation(charName+'_Foot_R_Crl',1,'translateZ',20)
    SetKeyAnimation(charName+'_Foot_R_Crl',13,'translateZ',-20)
    SetKeyAnimation(charName+'_Foot_R_Crl',25,'translateZ',20)
    SetKeyAnimation(charName+'_Foot_R_Crl',1,'rotateX',-20)
    SetKeyAnimation(charName+'_Foot_R_Crl',4,'rotateX',0)
    SetKeyAnimation(charName+'_Foot_R_Crl',7,'rotateX',0)
    SetKeyAnimation(charName+'_Foot_R_Crl',13,'rotateX',15)
    SetKeyAnimation(charName+'_Foot_R_Crl',25,'rotateX',-20)
    SetKeyAnimation(charName+'_Spline_Ctrl_01',7,'translateX',-8)
    SetKeyAnimation(charName+'_Spline_Ctrl_01',19,'translateX',8)
    SetKeyAnimation(charName+'_Spline_Ctrl_01',31,'translateX',-8)
    SetKeyAnimation(charName+'_Spline_Ctrl_01',1,'rotateX',-2)
    SetKeyAnimation(charName+'_Spline_Ctrl_01',7,'rotateX',10)
    SetKeyAnimation(charName+'_Spline_Ctrl_01',13,'rotateX',-2)
    SetKeyAnimation(charName+'_Spline_Ctrl_01',7,'rotateX',10)
    SetKeyAnimation(charName+'_Spline_Ctrl_01',1,'rotateY',15)
    SetKeyAnimation(charName+'_Spline_Ctrl_01',13,'rotateY',-15)
    SetKeyAnimation(charName+'_Spline_Ctrl_01',25,'rotateY',15)
    SetKeyAnimation(charName+'_Hip_Ctrl_01',4,'translateY',-2)
    SetKeyAnimation(charName+'_Hip_Ctrl_01',10,'translateY',2)
    SetKeyAnimation(charName+'_Hip_Ctrl_01',16,'translateY',-2)
    SetKeyAnimation(charName+'_Hip_Ctrl_01',7,'rotateX',10)
    SetKeyAnimation(charName+'_Hip_Ctrl_01',13,'rotateX',-2)
    SetKeyAnimation(charName+'_Hip_Ctrl_01',19,'rotateX',10)
    
    
#cmds.setAttr('men_alembic:men_alembic_AlembicNode.cycleType',1)


#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#                                   CROWD SIMULATOR
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------

#Class

class Agents():
    
    
    def __init__(self,name,nbPopulation,targetX,targetZ,minFriendDistance,coeffA,coeffC,coeffS):
        nbPopulation=cmds.intSliderGrp(nbAgentsSlider,q=True,value=True)
        charName = cmds.textFieldGrp(NameInput,q= True,text = True) 
        self.createAgent(name,nbPopulation)
            
    
    def createAgent(self,name,nbPopulation):
        name = cmds.textFieldGrp(NameInput,q= True,text = True)
        nbPopulation=cmds.intSliderGrp(nbAgentsSlider,q=True,value=True) 
        '''
        createAgent():
            Generate a flock of agents at the user specfied position on a 2D plane (60 meters x 60 meters).
            @param:    name: root name of the agent [type: string]
                       nbPopulation: number of agents [type: int]
                       targetX: position of the target on the X axis [type: float]
                       targetZ: position of the target on the Z axis [type: float]
                       minFriendDistance: minimum distance to be maintained between agents [type: float]
                       coeffA: coefficient assigned to the alignment force [type: float]
                       coeffC: coefficient assigned to the cohesion force [type: float]
                       coeffS: coefficient assigned to the separation force [type: float]                                                                                                                 
            @return:   none
        '''
        #capture the user defined spawn position
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
#            A REGLER POUR FAIRE L'ANIM
#            cmds.setAttr('men_alembic2_AlembicNode.cycleType',1)
#            cmds.setAttr('men_alembic2_men_alembic2_AlembicNode'+str(i-2)+'.cycleType',1)
            
            
            # A AMELIORER : REGLER L'ATTRIBUT NEAR CLIP PLANE DE LA CAMERA COURANTE A 0.1
            cmds.move(targetzoneCoord[0]-uniform(-500,500),0,targetzoneCoord[2]-uniform(-500,500),name+"_"+str(i+1))
          
                
    def alignmentMove(self,name,nbPopulation,targetX,targetZ,coeffA):
        nbPopulation=cmds.intSliderGrp(nbAgentsSlider,q=True,value=True)
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
        nbPopulation=cmds.intSliderGrp(nbAgentsSlider,q=True,value=True)
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
        nbPopulation=cmds.intSliderGrp(nbAgentsSlider,q=True,value=True)
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


def launchSim():
    nbPopulation=cmds.intSliderGrp(nbAgentsSlider,q=True,value=True)
    #check=checkDistanceFromTarget(nbPopulation,targetPosX,targetPosZ,maxDistanceFromTarget)
    duration=400
    i=0
    
    while(i<duration):
                 
        cmds.currentTime(i+1)
        charName = cmds.textFieldGrp(NameInput,q= True,text = True) 
        foule.alignmentMove(charName,nbPopulation,targetPosX,targetPosZ,coeffA)
        #foule.cohesionMove("individu",25,1)
        foule.separationMove(charName,nbPopulation,minFriendDistance,coeffS)
        
        for j in range(nbPopulation):
            cmds.select(charName+"_"+str(j+1))
            cmds.setKeyframe(at="translateX")
            cmds.setKeyframe(at="translateZ")
        #for i in range(nbPopulation)
        
        #checkDistanceFromTarget(nbPopulation,targetPosX,targetPosZ,maxDistanceFromTarget)
        
        i=i+1



#------------------------------------------------------------------------------------
# MAIN VARIABLES
#------------------------------------------------------------------------------------

coeffA=9
coeffC=1
coeffS=1
minFriendDistance=120
#maxDistanceFromTarget=2
targetPosX,targetPosZ=createRandomTarget("target")



#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#                                   INTERFACE
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------



cmds.window("Lavazza", w= 300, h= 600)
cmds.columnLayout(adj= True)
imagePath = cmds.workspace(q=True, rd=True)+"/scripts/image_2.jpg"
cmds.image(w=300,h=100,image=imagePath)
cmds.rowLayout( numberOfColumns=1, columnWidth3=(80, 75, 300), adjustableColumn=2, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)] )
#cmds.button( label='Import character',command= 'ImportOBJ()')

NameInput = cmds.textFieldGrp(label = "Name of the agent  ",editable= True)
cmds.setParent( '..' )
cmds.setParent( '..' )
cmds.setParent( '..' )

cmds.frameLayout(label='Auto Rig',collapsable=True,collapse=False)
cmds.rowColumnLayout(numberOfColumns=5, columnWidth=[(1, 81), (2, 81), (3, 81), (4, 81), (5, 81)])
cmds.button( label='Create locators',command='CreationLoc()')
cmds.button(label= 'Create joints',command='CreateJoints()')
cmds.button(label= 'Mirror',command='MirrorJoints()')
cmds.button(label= 'Controllers',command='Controllers()')
cmds.button(label= 'bindSkin',command='Bind()')

cmds.setParent( '..' )
cmds.setParent( '..' )

cmds.frameLayout(label='Animation',collapsable=True,collapse=False)
cmds.rowColumnLayout()
cmds.button( label='Walking cycle', c= 'Anim()')

cmds.setParent( '..' )
cmds.setParent( '..' )

cmds.frameLayout(label='Crowd simulator',collapsable=True,collapse=False)
cmds.rowColumnLayout()
nbAgentsSlider = cmds.intSliderGrp(label = 'Number of agents  ', min = 1, max= 100, value= 25,field=True)
cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1, 135), (2, 135), (3, 135)])
cmds.button(label="Create Ground",c="createGround()")
charName = cmds.textFieldGrp(NameInput,q= True,text = True) 
nbPopulation=cmds.intSliderGrp(nbAgentsSlider,q=True,value=True)
cmds.button(label="Spawn Agents",c="foule=Agents(charName,nbPopulation,targetPosX,targetPosZ,minFriendDistance,coeffA,coeffC,coeffS)")
cmds.button(label="Execute",c="launchSim()")

cmds.showWindow()

