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
    cmds.joint(charName + '_L'+'_wrist'+'_Jnt_01', e=True,oj='none', ch=True,zso=True)
    
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
cmds.ikHandle(n= 'Leg_ikHandle', sj= charName+'_L_thigh_Jnt_01', ee=charName+'_L_ankie_Jnt_01')

cmds.spaceLocator(n='poleVector_L_leg',p=(locXYZ[4][0]-legY*0.005,locXYZ[4][1]+legY*0.05,locXYZ[4][2]))
cmds.xform(obj, cp=1)
cmds.poleVectorConstraint( 'poleVector_L_leg', 'Leg_ikHandle' )
cmds.move(locXYZ[5][0]-locXYZ[4][0]*0.3,locXYZ[5][1]+locXYZ[4][1]*0.17,locXYZ[4][2]-legY*0.03-(locXYZ[5][2]-locXYZ[4][2])/6,'poleVector_L_leg',ws=True)
