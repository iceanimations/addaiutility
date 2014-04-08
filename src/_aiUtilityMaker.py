'''
Created on Apr 8, 2014

@author: qurban.ali
'''

import pymel.core as pc

def doTheMagic():
    currentLayer = pc.PyNode(pc.editRenderLayerGlobals(currentRenderLayer=True, q=True))
    objects = currentLayer.listMembers()
    if not objects:
        pc.warning("No objects found in the selected layer")
        return
    
    newLayer = pc.createRenderLayer(objects, name='layer', noRecurse=True)
    pc.editRenderLayerGlobals(currentRenderLayer=newLayer)
    
    meshes = pc.ls(objects, dag=True, type='mesh')
    aiShaders = set()
    for mesh in meshes:
        sgs = mesh.connections(type=pc.nt.ShadingEngine)
        for sg in sgs:
            try:
                ai = sg.surfaceShader.inputs()[0]
            except: continue
            aiShaders.add(ai)
    for aiSh in aiShaders:
        aiUtility = pc.PyNode(pc.Mel.eval('createRenderNodeCB -asShader "surfaceShader" aiUtility ""'))
        utilsg = aiUtility.connections(type=pc.nt.ShadingEngine)[0]
        attr = None
        try:
            attr = aiSh.color.inputs(plugs=True)[0]
        except:
            aiUtility.color.set(aiSh.color.get())
        aiUtility.shadeMode.set(2)
        for sg in aiSh.connections(type=pc.nt.ShadingEngine):
            pc.sets(utilsg, fe=pc.sets(sg, q=True))
            
    
    