import maya.cmds as cmds
import math
#Add your geometry
#Create 5 locator and place 

#get position of root
posX_1 =cmds.getAttr('locator1.translateX')
posY_1 =cmds.getAttr('locator1.translateY')
posZ_1 =cmds.getAttr('locator1.translateZ')

#get position of neck
posX_2 =cmds.getAttr('locator2.translateX')
posY_2 =cmds.getAttr('locator2.translateY')
posZ_2 =cmds.getAttr('locator2.translateZ')
cmds.select(d=True)
#get position of wrist 3
posX_3 =cmds.getAttr('locator3.translateX')
posY_3 =cmds.getAttr('locator3.translateY')
posZ_3 =cmds.getAttr('locator3.translateZ')
cmds.select(d=True)

#get position of wrist 4
posX_4 =cmds.getAttr('locator4.translateX')
posY_4 =cmds.getAttr('locator4.translateY')
posZ_4 =cmds.getAttr('locator4.translateZ')
cmds.select(d=True)

#get position of knee 5
posX_5 =cmds.getAttr('locator5.translateX')
posY_5 =cmds.getAttr('locator5.translateY')
posZ_5 =cmds.getAttr('locator5.translateZ')
cmds.select(d=True)

#total length between root and neck

lengthY = posY_2-posY_1
lengthZ = abs(posZ_1)+abs(posZ_2)
#place spline joint 
cmds.select(d=True)
cmds.joint(p=(posX_1,posY_1,posZ_1), n = 'root')
posX= 0
posY = posY_1 + lengthY*0.43
posZ = posZ_1 + lengthZ*0.43
cmds.joint('root',p=(posX,posY, posZ), n='spline_1')
posY = posY+ lengthY*0.28
posZ = posZ + lengthZ*-0.25
cmds.joint('spline_1',p=(posX,posY, posZ), n='spline_2')
cmds.joint('spline_2',p=(posX_2,posY_2,posZ_2), n= 'spline_3')
cmds.joint('spline_3',p=(posX_2,posY_2+lengthY*0.1,posZ_2+lengthY*0.05), n= 'neck_1')
cmds.joint('neck_1',p=((posX_2+posX)/2,posY_2+lengthY/4,(posZ_2+posZ_1+lengthY*0.15)/2), n= 'jaw_1')
cmds.joint('jaw_1',p=((posX_2+posX)/4,posY_2+lengthY/2.8,(posZ_2+posZ_1+lengthY*0.15)/2), n= 'eye_1')
cmds.joint('eye_1',p=(posX,posY_2+lengthY/1.8, posZ_1+lengthY*0.03 ),n='head_1')
#place arm joint
cmds.select(d=True)
cmds.joint(p=(posX_1+lengthY*0.1,posY_2,posZ_1+lengthZ*0.1), n = 'shoulder_1')
cmds.joint(p=(posX_1+lengthY*0.24,posY_2-lengthY*0.05,posZ_1-lengthZ*0.2), n= 'shoulder_2')
cmds.joint(p=((posX_1+lengthY*0.24+posX_3-lengthZ*0.1)/2,(posY_2-lengthY*0.05+posY_3+lengthZ*0.1)/2,(posZ_1-lengthZ*0.2+posZ_3)/2), n= 'arm_1')
cmds.joint(p=(posX_3-lengthZ*0.1,posY_3+lengthZ*0.1,posZ_3), n='arm_2')
cmds.joint(p=(posX_3+lengthZ*0.1,posY_3-lengthZ*0.1,posZ_3), n='arm_3')
cmds.joint(p=((posX_3+lengthZ*0.1+posX_4)/2,(posY_3-lengthZ*0.1+posY_4)/2,(posZ_3+posZ_4)/2), n='arm_4')
cmds.joint(p=(posX_4,posY_4,posZ_4),n='wrist_1')

#place leg joint
