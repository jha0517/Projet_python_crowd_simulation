import maya.cmds as cmds
import math
#Interface
cmds.window("Auto-Rig")
cmds.showWindow()
cmds.rowColumnLayout()
cmds.button( label='Create locators',command='CreationLoc()')
cmds.button(label= 'Create joints',command='CreateJoints()')
cmds.button(label= 'Mirror',command='MirrorJoints()')
cmds.button(label='Delete all locators')
cmds.button(label= 'IKhandleLeg',command='IKhandleLeg()')
cmds.button(label= 'ReverseFoot',command='ReverseFoot()')
cmds.button(label= 'controllerFoot',command='controllerFoot()')
cmds.button(label= 'IKhandleAndControllerArm',command='IKhandleAndControllerArm()')

####################################################################################################
#Add your geometry
#Character name
charName = 'men'
#Create 5 locator and place 
list = ['root', 'neck','elbow','wrist','knee','toe']
def CreationLoc():
    if cmds.objExists('Loc_master'):
        print("Exists already")
    else:  
        cmds.group(n='Loc_master', em=True)
        for i in range (len(list)):
            loc = cmds.spaceLocator(n='Loc+'+list[i])
            cmds.parent(loc, 'Loc_master')
#def DeleteAllLocators():

def CreateJoints():
    cmds.select(d=True)
    locXYZ= [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    for i in range(len(list)):    
        locXYZ[i][0]= cmds.getAttr('Loc_'+list[i]+'.translateX')
        locXYZ[i][1]= cmds.getAttr('Loc_'+list[i]+'.translateY')
        locXYZ[i][2]= cmds.getAttr('Loc_'+list[i]+'.translateZ')

    #total length between root and neck
    lengthY = locXYZ[1][1]-locXYZ[0][1]
    lengthZ = abs(locXYZ[0][2])+abs(locXYZ[1][2])
    #length between root and toe
    legY = locXYZ[0][1]-locXYZ[5][1] 
    cmds.joint(p=(locXYZ[0][0],locXYZ[0][1],locXYZ[0][2]),n = charName + '_root'+'_Jnt_01')
    
    def PlaceJoint(OrientThisJoint,x,y,z,jointName,o):
        cmds.joint(p=(x,y,z),n = jointName)
        cmds.joint(OrientThisJoint,e=True,zso=True, oj='xyz', sao= o+'up')
        print("Done")
    
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
    cmds.mirrorJoint(charName +'_L'+ '_hip'+'_Jnt_01',mirrorYZ=True,mirrorBehavior=True,searchReplace=('_L_', '_R_') )
    cmds.joint(charName +'_R'+ '_hip_Jnt_01', e=True,oj='xyz', ch=True,zso=True, sao='xup')
    cmds.mirrorJoint(charName +'_L'+ '_shoulder'+'_Jnt_01',mirrorYZ=True,mirrorBehavior=True,searchReplace=('_L_', '_R_') )
    cmds.joint(charName +'_R'+ '_shoulder_Jnt_01', e=True,oj='xyz', ch=True,zso=True, sao='yup')
    cmds.joint(charName + '_R'+'_wrist'+'_Jnt_01', e=True,oj='none', ch=True,zso=True)
    cmds.joint(charName +'_R'+ '_toe'+'_Jnt_01', e=True,oj='none', ch=True,zso=True)
    cmds.select(d=True)

    
#Create directory
listDirectory = [['_GlobalScale_','_Joints_','_IK_','_Controls_'],'_GlobalControl_','_Geo_','_BlendShapes_','_ExtraNodes_' ]
cmds.group(em=True, n= charName+'_Main_01')
for i in range (len(listDirectory)-1):
    cmds.group(em=True, n= charName + listDirectory[i+1]+'01')
    cmds.parent(charName + listDirectory[i+1]+'01',charName+'_Main_01')
for i in range(len(listDirectory[0])):
    cmds.group(em = True, n= charName + listDirectory[0][i]+'01')
    cmds.parent(charName + listDirectory[0][i]+'01',charName + listDirectory[1]+'01')

#Create IK Handle 
#for Legs
def IKhandleLeg():
    cmds.ikHandle(n= 'Leg_ikHandle', sj= charName+'_L_thigh_Jnt_01', ee=charName+'_L_ankie_Jnt_01')
    cmds.spaceLocator(n='poleVector_L_leg',p=(locXYZ[4][0]-legY*0.005,locXYZ[4][1]+legY*0.05,locXYZ[4][2]))
    cmds.xform(centerPivots=1)
    # aims the pole vector of 1 at 2.
    cmds.poleVectorConstraint( 'poleVector_L_leg', 'Leg_ikHandle' )
    cmds.move(lengthY*0.75,-lengthY*0.75,'poleVector_L_leg',moveXY=True)
    cmds.setAttr('Leg_ikHandle.twist',90)
    cmds.ParentConstraint('controllerfoot','poleVector_L_leg')
    cmds.parent( 'poleVector_L_leg', 'Leg_ikHandle', relative=True )

def ReverseFoot(): 
    cmds.ikHandle(n= 'Foot_L_ball_ikHandle', sj = charName + '_L'+'_ankie'+'_Jnt_01', ee = charName +'_L'+ '_ball'+'_Jnt_01')
    cmds.ikHandle(n= 'Foot_L_toe_ikHandle', sj = charName +'_L'+ '_ball'+'_Jnt_01', ee = charName +'_L'+ '_toe'+'_Jnt_01')
    cmds.group('Leg_ikHandle', n= 'Foot_L_heelPeel')
    #change pivot position
    Xpos = cmds.getAttr('Foot_L_ball_ikHandle.translateX' )
    Ypos = cmds.getAttr('Foot_L_ball_ikHandle.translateY' )
    Zpos = cmds.getAttr('Foot_L_ball_ikHandle.translateZ' )
    cmds.move(Xpos, Ypos, Zpos, 'Foot_L_heelPeel.scalePivot','Foot_L_heelPeel.rotatePivot', absolute=True)
    cmds.group('Foot_L_ball_ikHandle','Foot_L_toe_ikHandle', n = 'Foot_L_toeTap')
    cmds.move(Xpos, Ypos, Zpos, 'Foot_L_toeTap.scalePivot','Foot_L_toeTap.rotatePivot', absolute=True)
    cmds.group('Foot_L_ball_ikHandle','Foot_L_toeTap', n = 'Foot_L_TipToe')
    cmds.group(n = 'Foot_L',em=True)
    cmds.parent( 'Foot_L_heelPeel','Foot_L_TipToe', 'Foot_L', relative=True )
    cmds.move(Xpos, Ypos, Zpos, 'Foot_L.scalePivot','Foot_L.rotatePivot', absolute=True)
def controllerFoot():
    Xpos = cmds.getAttr('Foot_L_ball_ikHandle.translateX' )
    Ypos = cmds.getAttr('Foot_L_ball_ikHandle.translateY' )
    Zpos = cmds.getAttr('Foot_L_ball_ikHandle.translateZ' )
    cmds.CreateNURBSCircle()
    cmds.rename('nurbsCircle1','Foot_L_Crl')
    cmds.move(Xpos,Ypos,Zpos)
    cmds.scale(10,10,16)
    cmds.makeIdentity(apply=True)
    cmds.group('Foot_L_Crl', n= 'Foot_L_Crl_grp')
    cmds.parent('Foot_L','Foot_L_Crl')
    # tip toe controller
    cmds.CreateNURBSCircle()
    cmds.rename('nurbsCircle1','FootTip_L_Crl')
    cmds.move(Xpos,Ypos*30,Zpos)
    cmds.scale(3,3,3)
    cmds.rotate(0,90,-90)
    cmds.move(Xpos, Ypos, Zpos, 'FootTip_L_Crl.scalePivot','FootTip_L_Crl.rotatePivot', absolute=True)
    cmds.makeIdentity(apply=True)
    cmds.parentConstraint('Foot_L_heelPeel','FootTip_L_Crl')
#    cmds.xform(centerPivots=1)
def IKhandleAndControllerArm():
#left Arm
    cmds.ikHandle(n= 'Arm_L_ikHandle', sj = charName + '_L'+'_shoulder'+'_Jnt_02', ee = charName + '_L'+'_wrist'+'_Jnt_01')
    cmds.CreateNURBSCircle()
    cmds.rename('nurbsCircle1','Elbow_L_Crl')
    cmds.move(locXYZ[2][0],locXYZ[2][1],locXYZ[2][2]*30)
    cmds.scale(2,2,3)
    cmds.rotate(90,0,0)
    cmds.move(locXYZ[2][0], locXYZ[2][1],locXYZ[2][2], 'Elbow_L_Crl.scalePivot','Elbow_L_Crl.rotatePivot', absolute=True)
    cmds.makeIdentity(apply=True)
    cmds.xform(centerPivots=1)
    cmds.poleVectorConstraint( 'Elbow_L_Crl', 'Arm_L_ikHandle' )
    #left Arm controller
    cmds.CreateNURBSCircle()
    cmds.rename('nurbsCircle1','Arm_L_Crl')
    cmds.move(locXYZ[3][0],locXYZ[3][1],locXYZ[3][2])
    cmds.scale(5,5,8)
    cmds.makeIdentity(apply=True)
    cmds.group('Arm_L_Crl', n= 'Arm_L_Crl_grp')
    cmds.rotate(0,0,30)
    cmds.parent('Arm_L_ikHandle','Arm_L_Crl')
    
def CreateCtr(nameCtr,ObjToParent,posX,posY,posZ,scaleX,scaleY,scaleZ,rotateX,rotateY,rotateZ):
    cmds.CreateNURBSCircle()
    cmds.rename('nurbsCircle1',nameCtr)
    cmds.move(posX,posY,posZ)
    cmds.scale(scaleX,scaleY,scaleZ)
    cmds.makeIdentity(apply=True)
    cmds.group(nameCtr, n= nameCtr+'_grp')
    cmds.rotate(0,0,30)
    cmds.parent(ObjToParent,nameCtr)

def IKhandleAndControllerSpline():
    cmds.CreateNURBSCircle()
    cmds.CreateNURBSCircle()
    cmds.CreateNURBSCircle()
    
    
