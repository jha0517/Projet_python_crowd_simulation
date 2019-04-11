import maya.cmds as cmds
import math
#Add your geometry
#Create 5 locator and place 
# locator 1 - root, 2- neck, 3-elbow, 4- wrist, 5-knee, 6-toe
for i in range(1,7):
    posX_i =cmds.getAttr('locator'+str(i)+'.translateX')
    posY_i =cmds.getAttr('locator'+str(i)+'.translateX')
    posZ_i =cmds.getAttr('locator'+str(i)+'.translateX')
    cmds.select(d=True)
characterName= 'Men'
#total length between root and neck
lengthY = posY_2-posY_1
lengthZ = abs(posZ_1)+abs(posZ_2)
#length between root and toe
legY = posY_1-posY_6 
#place spline joint
def placeJoint(x,y,z,jointName):
    cmds.joint(p=(x,y,z),n = characterName + '_Jnt_'+jointName)
    cmds.joint(e=True,zso=True, oj='xyz', sao='xup')
    print(characterName + '_Jnt_'+jointName)
    
placeJoint(posX_1,posY_1,posZ_1,'root')
placeJoint(0,posY_1 + lengthY*0.43, posZ_1 + lengthZ*0.43,'spline_01')
placeJoint(0,posY_1 + lengthY*0.8,posZ_1 + lengthZ*0.18,'spline_02')

'''cmds.joint(p=(x,y,z),n = characterName + '_Jnt_'+jointName)
print(characterName + '_Jnt_'+jointName)
cmds.joint(str(characterName + '_Jnt_'+jointName), e=True,zso=True, oj='xyz', sao='xup')
print('done')
'''
#cmds.joint('spline_1',p=(0,posY_1 + lengthY*0.8,posZ_1 + lengthZ*0.18), n='spline_2')
cmds.joint('spline_2',p=(posX_2,posY_2,posZ_2), n= 'spline_3')
cmds.joint('spline_3',p=(posX_2,posY_2+lengthY*0.1,posZ_2+lengthY*0.05), n= 'neck_1')
cmds.joint('neck_1',p=((posX_2+posX)/2,posY_2+lengthY/4,(posZ_2+posZ_1+lengthY*0.15)/2), n= 'jaw_1')
cmds.joint('jaw_1',p=((posX_2+posX)/4,posY_2+lengthY/2.8,(posZ_2+posZ_1+lengthY*0.15)/2), n= 'eye_1')
cmds.joint('eye_1',p=(posX,posY_2+lengthY/1.8, posZ_1+lengthY*0.03 ),n='head_1')
#place arm joint
cmds.select(d=True)
cmds.joint('spline_3',p=(posX_1+lengthY*0.1,posY_2,posZ_1+lengthZ*0.1), n = 'shoulder_1')
cmds.joint(p=(posX_1+lengthY*0.24,posY_2-lengthY*0.05,posZ_1-lengthZ*0.2), n= 'shoulder_2')
cmds.joint(p=((posX_1+lengthY*0.24+posX_3-lengthZ*0.1)/2,(posY_2-lengthY*0.05+posY_3+lengthZ*0.1)/2,(posZ_1-lengthZ*0.2+posZ_3)/2), n= 'arm_1')
cmds.joint(p=(posX_3-lengthZ*0.1,posY_3+lengthZ*0.1,posZ_3), n='arm_2')
cmds.joint(p=(posX_3+lengthZ*0.1,posY_3-lengthZ*0.1,posZ_3), n='arm_3')
cmds.joint(p=((posX_3+lengthZ*0.1+posX_4)/2,(posY_3-lengthZ*0.1+posY_4)/2,(posZ_3+posZ_4)/2), n='arm_4')
cmds.joint(p=(posX_4,posY_4,posZ_4),n='wrist_1')    
#place leg joint
cmds.select(d=True)
cmds.joint('root',p=(posX_1+lengthY*0.08,posY_1,posZ_1-lengthZ/3.9),n='hip_1')
cmds.joint(p=(posX_1+lengthY*0.21,posY_1+legY*0.03,posZ_1-lengthZ/1.86),n='thigh_1')
cmds.joint(p=(posX_5-legY*0.005,posY_5+legY*0.05,posZ_5), n = 'knee_01')
cmds.joint(p=(posX_5+legY*0.005,posY_5-legY*0.05,posZ_5-legY*0.03), n = 'knee_02')
cmds.joint(p=(posX_6-posX_5*0.3,posY_6+posY_5*0.17,posZ_5-legY*0.03-(posZ_6-posZ_5)/6),n='ankie_1')
cmds.joint(p=((posX_6-posX_5*0.3+posX_6)/2,posY_6,posZ_5+posZ_6/1.9),n='ball_1')
cmds.joint(p=(posX_6,posY_6,posZ_6),n='toe_1')




