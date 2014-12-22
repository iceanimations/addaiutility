'''
Created on Apr 8, 2014

@author: qurban.ali
'''

import pymel.core as pc

def getFlatDiffuseIndex(sg):
    for i in sg.aiCustomAOVs.getArrayIndices():
        if 'flat_diffuse' in sg.aiCustomAOVs[i].get():
            return i

def doTheMagic():
    try:
        arnolds = pc.ls(sl=True, type=pc.nt.AiStandard)
    except AttributeError:
        pc.confirmDialog(title="Error", message="It seems like Arnold is not loaded or installed", button="Ok")
        return
    if not arnolds:
        pc.confirmDialog(title="Error", message="No selection found in the scene", button="Ok")
        return
    try:
        value = getFlatDiffuseIndex(pc.ls(type=pc.nt.ShadingEngine)[0])
        if value is not None:
            pass
        else:
            pc.confirmDialog(title="Error", message="No AOV named \"flat_diffuse\" found in the scene", button="Ok")
            return
    except IndexError:
        pc.confirmDialog(title="Error", message="No Shading engine found in the scene", button="Ok")
        return
    for aiSh in arnolds:
        aiUtility = str(pc.Mel.eval('createRenderNodeCB -asShader "surfaceShader" aiUtility ""'))
        aiUtility = pc.PyNode(aiUtility)
        utilsg = pc.listConnections(aiUtility, type='shadingEngine')
        for sg in utilsg:
            pc.delete(sg)
        for sg in pc.listConnections(aiSh, type='shadingEngine'):
            aiUtility.outColor.connect(sg.aiCustomAOVs[getFlatDiffuseIndex(sg)].aovInput, f=True)
        try:
            aiSh.color.inputs(plugs=True)[0].connect(aiUtility.color, f=True)
        except IndexError:
            pass
        aiUtility.shadeMode.set(2)
        pc.rename(aiUtility, '_'.join([aiSh.name().split(':')[-1].split('|')[-1], 'aiUtility']))