'''
Created on Apr 8, 2014

@author: qurban.ali
'''

import pymel.core as pc
import maya.cmds as mc

def doTheMagic():
    currentLayer = mc.editRenderLayerGlobals(currentRenderLayer=True, q=True)
    objects = mc.editRenderLayerMembers(currentLayer, q=True, noRecurse=True)
#     if not objects:
#         pc.warning("No objects found in the selected layer")
#         return

#    newLayer = mc.createRenderLayer(objects, name='newLayer', noRecurse=True)
#    mc.editRenderLayerGlobals(currentRenderLayer=newLayer)

    meshes = set()
    for obj in objects:
        try:
            meshes.add(mc.ls(obj, dag=True, type='mesh'))
        except: pass
    aiShaders = set()
    for mesh in meshes:
        sgs = mc.listConnections(mesh, type='shadingEngine')
        if sgs:
            sgs = set(sgs)
            for sg in sgs:
                try:
                    ai = mc.listConnections(sg +'.surfaceShader')[0]
                except: continue
            if type(pc.PyNode(ai)) == pc.nt.AiStandard:
                aiShaders.add(ai)
    for aiSh in aiShaders:
        aiUtility = str(pc.Mel.eval('createRenderNodeCB -asShader "surfaceShader" aiUtility ""'))
        utilsg = mc.listConnections(aiUtility, type='shadingEngine')[0]
        try:
            mc.connectAttr(mc.listConnections(aiSh + '.color')[0] +'.outColor', aiUtility + '.color', f=True)
        except IndexError:
            mc.setAttr(aiUtility +'.color', mc.getAttr(aiSh +'.color'))
        except: pass
        mc.setAttr(aiUtility +'.shadeMode', 2)
        for sg in mc.listConnections(aiSh, type='shadingEngine'):
            temp = []
            members = mc.sets(sg, q=True)
            if members:
                for mem in members:
                    try:
                        temp.append(pc.PyNode(mem))
                    except: pass
            try:
                pc.sets(pc.PyNode(utilsg), e=True, fe=temp)
            except:
                pass