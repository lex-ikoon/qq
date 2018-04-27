import hou

def parmnode () :
    parm_pane = hou.ui.curDesktop().paneTabOfType(hou.paneTabType.Parm)
    parmnode = parm_pane.currentNode()
    return parmnode

def container () :
    parm_pane = hou.ui.curDesktop().paneTabOfType(hou.paneTabType.Parm)
    parmnode = parm_pane.currentNode()
    container = parmnode.parent()
    return container
