import maya.cmds as cmds
import math
#Add your geometry
#Character name
charName = 'men'

def CreationLoc():
    if cmds.objExists('Loc_master'):
        print("Exists already")
    else:  
        cmds.group(n='Loc_master', em=True)
        for i in range (len(list)):
            loc = cmds.spaceLocator(n='Loc+'+list[i])
            cmds.parent(loc, 'Loc_master')    
def CreateJoints():
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
    list = ['root', 'neck','elbow','wrist','knee','toe']
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
    lengthY = locXYZ[1][1]-locXYZ[0][1]
    lengthZ = abs(locXYZ[0][2])+abs(locXYZ[1][2])
    legY = locXYZ[0][1]-locXYZ[5][1] 
    side =['_L_','_R_']
    nb = [1,-1]    
    for i in range(len(side)):
        cmds.ikHandle(n= 'Leg'+side[i]+'ikHandle', sj= charName+side[i]+'thigh_Jnt_01', ee=charName+side[i]+'ankie_Jnt_01')
        cmds.spaceLocator(n='poleVector'+side[i]+'leg',p=(nb[i]*locXYZ[4][0]-legY*0.005,locXYZ[4][1]+legY*0.05,locXYZ[4][2]))
        cmds.xform(centerPivots=1)
        # aims the pole vector of 1 at 2.
        cmds.poleVectorConstraint( 'poleVector'+side[i]+'leg', 'Leg'+side[i]+'ikHandle' )
        cmds.move(nb[i]*lengthY*0.75,-lengthY*0.75,'poleVector'+side[i]+'leg',moveXY=True)
        cmds.setAttr('Leg'+side[i]+'ikHandle.twist',nb[i]*90)
        cmds.ParentConstraint('controllerfoot','poleVector'+side[i]+'leg')
        cmds.parent( 'poleVector'+side[i]+'leg', 'Leg'+side[i]+'ikHandle', relative=True )
        cmds.ikHandle(n= 'Foot'+side[i]+'ball_ikHandle', sj = charName + side[i]+'ankie'+'_Jnt_01', ee = charName +side[i]+'ball'+'_Jnt_01')
        cmds.ikHandle(n= 'Foot'+side[i]+'toe_ikHandle', sj = charName +side[i]+ 'ball'+'_Jnt_01', ee = charName +side[i]+'toe'+'_Jnt_01')
        cmds.group('Leg'+side[i]+'ikHandle', n= 'Foot'+side[i]+'heelPeel')
        #change pivot position
        Xpos = cmds.getAttr('Foot'+side[i]+'ball_ikHandle.translateX' )
        Ypos = cmds.getAttr('Foot'+side[i]+'ball_ikHandle.translateY' )
        Zpos = cmds.getAttr('Foot'+side[i]+'ball_ikHandle.translateZ' )
        cmds.move(Xpos, Ypos, Zpos, 'Foot'+side[i]+'heelPeel.scalePivot','Foot'+side[i]+'heelPeel.rotatePivot', absolute=True)
        cmds.group('Foot'+side[i]+'ball_ikHandle','Foot'+side[i]+'toe_ikHandle', n = 'Foot'+side[i]+'toeTap')
        cmds.move(Xpos, Ypos, Zpos, 'Foot'+side[i]+'toeTap.scalePivot','Foot'+side[i]+'toeTap.rotatePivot', absolute=True)
        cmds.group('Foot'+side[i]+'ball_ikHandle','Foot'+side[i]+'toeTap', n = 'Foot'+side[i]+'TipToe')
        cmds.group(n = 'Foot'+side[i]+'1',em=True)
        cmds.parent( 'Foot'+side[i]+'heelPeel','Foot'+side[i]+'TipToe', 'Foot'+side[i]+'1', relative=True )
        cmds.move(Xpos, Ypos, Zpos, 'Foot'+side[i]+'1.scalePivot','Foot'+side[i]+'1.rotatePivot', absolute=True)
        Xpos = cmds.getAttr('Foot'+side[i]+'ball_ikHandle.translateX' )
        Ypos = cmds.getAttr('Foot'+side[i]+'ball_ikHandle.translateY' )
        Zpos = cmds.getAttr('Foot'+side[i]+'ball_ikHandle.translateZ' )
        CreateCtr('Foot'+side[i]+'Crl','Foot'+side[i]+'1',(Xpos,Ypos,Zpos),(10,10,16),(0,0,0))
    #left Arm
    for i in range(len(side)):
        cmds.ikHandle(n= 'Arm'+str(side[i])+'ikHandle', sj = charName + str(side[i])+'shoulder'+'_Jnt_02', ee = charName + str(side[i])+'wrist'+'_Jnt_01')
        cmds.CreateNURBSCircle()
        cmds.rename('nurbsCircle1','Elbow'+str(side[i])+'Crl')
        cmds.move(nb[i]*locXYZ[2][0],locXYZ[2][1],locXYZ[2][2]*30)
        cmds.scale(2,2,3)
        cmds.rotate(90,0,0)
        cmds.move(nb[i]*locXYZ[2][0], locXYZ[2][1],locXYZ[2][2], 'Elbow'+str(side[i])+'Crl.scalePivot','Elbow'+str(side[i])+'Crl.rotatePivot', absolute=True)
        cmds.makeIdentity(apply=True)
        cmds.xform(centerPivots=1)
        cmds.poleVectorConstraint( 'Elbow'+str(side[i])+'Crl', 'Arm'+str(side[i])+'ikHandle' )
        #left Arm controller
        CreateCtr('Arm'+side[i]+'Crl','Arm'+side[i]+'ikHandle',(nb[i]*locXYZ[3][0],locXYZ[3][1],locXYZ[3][2]),(5,5,8),(0,0,30))
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
        CreateCtr(charName+'_Spline_Ctrl_01','cluster_1Handle',(0,locXYZ[0][1],0),(25,25,25),(0,0,0))
        cmds.parentConstraint(charName+'_Spline_Ctrl_01',charName+'_root_Jnt_01', maintainOffset=True)
        CreateCtr(charName+'_Chest_Ctrl_01','cluster_4Handle',(0,locXYZ[1][1],0),(25,25,25),(0,0,0))
        for i in range(len(side)):
            cmds.parentConstraint(charName+'_Chest_Ctrl_01',charName+side[i]+'shoulder_Jnt_01', maintainOffset=True)
            cmds.parent('Arm'+side[i]+'Crl_grp',charName+'_Chest_Ctrl_01')
            cmds.parent('Elbow'+side[i]+'Crl',charName+'_Chest_Ctrl_01')
        CreateCtr(charName+'_Chest_Ctrl_02','cluster_2Handle',(0,(locXYZ[0][1]+locXYZ[1][1])/2,0),(20,20,20),(0,0,0))
        cmds.parentConstraint(charName+'_Chest_Ctrl_01','men_neck_Jnt_00', maintainOffset=True,w=1)
        cmds.parentConstraint(charName+'_Chest_Ctrl_01','cluster_3Handle', maintainOffset=True, weight=0.5)
        cmds.parentConstraint(charName+'_Chest_Ctrl_01',charName+'_Chest_Ctrl_02_grp', maintainOffset=True, weight=0.5)
        cmds.parentConstraint(charName+'_Spline_Ctrl_01',charName+'_Chest_Ctrl_02_grp', maintainOffset=True, weight=0.5)
    #clean
    for i in range(len(side)):
        cmds.parent(charName+side[i]+'shoulder_Jnt_01',charName+'_Joints_01')
        cmds.parent(charName+'_Chest_Ctrl_0'+str(i+1)+'_grp',charName+'_Controls_01')
        cmds.parent('Foot'+side[i]+'1',charName+'_Controls_01')
        cmds.parent('Foot'+side[i]+'Crl_grp',charName+'_Controls_01')
        cmds.parent('Arm'+side[i]+'ikHandle',charName+'_ikHandle_01')
        cmds.parent('cluster_'+str(i+1)+'Handle',charName+'_ikHandle_01')
        cmds.parent('cluster_'+str(i+3)+'Handle',charName+'_ikHandle_01')
    cmds.parent(charName+'SplineIK_01',charName+'_ikHandle_01')
    cmds.parent(charName+'_SplineIK_Crv_01',charName+'_ikHandle_01')
    cmds.parent(charName+'_neck_Jnt_00',charName+'_Joints_01')
    cmds.parent(charName+'_root_Jnt_01',charName+'_Joints_01')
    cmds.parent(charName+'_spline_Jnt_00',charName+'_Joints_01')    
    cmds.parent(charName+'_Spline_Ctrl_01_grp',charName+'_Controls_01')

def CreateCtr(nameCtr,ObjToParent,(posX,posY,posZ),(scaleX,scaleY,scaleZ),(rotateX,rotateY,rotateZ)):
    cmds.CreateNUR BSCircle()
    cmds.rename('nurbsCircle1',nameCtr)
    cmds.move(posX,posY,posZ)
    cmds.scale(scaleX,scaleY,scaleZ)
    cmds.makeIdentity(apply=True)
    cmds.group(nameCtr, n= nameCtr+'_grp')
    cmds.rotate(rotateX,rotateY,rotateZ)
    cmds.parentConstraint(nameCtr,ObjToParent, mo=True)
#Interface
cmds.window("Generator de foule")
cmds.showWindow()
#cmds.rowColumnLayout( numberOfColumns=2, columnAttach=(1, 'right', 0), columnWidth=[(1, 100), (2, 250)] )
#cmds.text( label='Character Name' )
#charName = cmds.textField()
#cmds.setParent( '..' )
#cmds.rowColumnLayout()
#cmds.button( label='Import character',command='ImportCharacter()')
#cmds.setParent( '..' )
#cmds.setParent( '..' )
cmds.frameLayout(label='Auto Rig',collapsable=True,collapse=True)
cmds.rowColumnLayout()
#cmds.button( label='Calcule',command='Calcule()')
cmds.button( label='Import character')
cmds.button( label='Create locators',command='CreationLoc()')
cmds.button(label= 'Create joints',command='CreateJoints()')
cmds.button(label= 'Mirror',command='MirrorJoints()')
cmds.button(label= 'Controllers',command='Controllers()')
