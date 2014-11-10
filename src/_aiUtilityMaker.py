'''
Created on Apr 8, 2014

@author: qurban.ali
'''

import pymel.core as pc
import maya.cmds as mc

def doTheMagic():
    currentLayer = pc.editRenderLayerGlobals(currentRenderLayer=True, q=True)
    objects = pc.editRenderLayerMembers(currentLayer, q=True, noRecurse=True)
#     if not objects:
#         pc.warning("No objects found in the selected layer")
#         return

#    newLayer = mc.createRenderLayer(objects, name='newLayer', noRecurse=True)
#    mc.editRenderLayerGlobals(currentRenderLayer=newLayer)

    meshes = pc.ls(type='mesh')
    aiShaders = set()
    for mesh in meshes:
        sgs = pc.listConnections(mesh, type='shadingEngine')
        if sgs:
            sgs = set(sgs)
            for sg in sgs:
                try:
                    ai = pc.listConnections(sg +'.surfaceShader')[0]
                except: continue
            if type(pc.PyNode(ai)) == pc.nt.AiStandard:
                aiShaders.add(ai)
    for aiSh in aiShaders:
        aiUtility = str(pc.Mel.eval('createRenderNodeCB -asShader "surfaceShader" aiUtility ""'))
        utilsg = pc.listConnections(aiUtility, type='shadingEngine')[0]
        try:
            pc.connectAttr(pc.listConnections(aiSh + '.color')[0] +'.outColor', aiUtility + '.color', f=True)
        except IndexError:
            pc.setAttr(aiUtility +'.color', pc.getAttr(aiSh +'.color'))
        except: pass
        pc.setAttr(aiUtility +'.shadeMode', 2)
        for sg in pc.listConnections(aiSh, type='shadingEngine'):
            temp = []
            members = pc.sets(sg, q=True)
            if members:
                for mem in members:
                    try:
                        temp.append(pc.PyNode(mem))
                    except: pass
            try:
                pc.sets(pc.PyNode(utilsg), e=True, fe=temp)
            except:
                pass