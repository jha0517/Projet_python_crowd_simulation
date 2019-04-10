import maya.cmds as cmds
import math
posX_r =cmds.getAttr('locator1.translateX')
posY_r =cmds.getAttr('locator1.translateY')
posZ_r =cmds.getAttr('locator1.translateZ')
cmds.select(d=True)
cmds.joint(p=(posX_r,posY_r,posZ_r), n = 'root')


posX_s =cmds.getAttr('locator2.translateX')
posY_s =cmds.getAttr('locator2.translateY')
posZ_s =cmds.getAttr('locator2.translateZ')
cmds.select(d= True)
cmds.joint(p=(posX_s,posY_s,posZ_s), n= 'spline')

lengthY = posY_s-posY_r
lengthZ = abs(posZ_r)+abs(posZ_s)
posX= 0
posY = posY_r + lengthY*0.43
posZ = posZ_r + lengthZ*0.43
cmds.joint('root',p=(posX,posY, posZ), n='spline_1')
posY = posY_r+lengthY*0.188
posZ = posZ_r + lengthZ*0.4777
cmds.joint('spline_1',p=(posX,posY, posZ), n='spline_2')
