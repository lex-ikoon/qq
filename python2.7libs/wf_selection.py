import hou


def cursor_linkGroup() :
    try:
        current_desktop = hou.ui.curDesktop()
        cursor_pane     = current_desktop.paneTabUnderCursor()
        cursor_group    = cursor_pane.linkGroup()

        if cursor_group == hou.paneLinkType.FollowSelection or cursor_group == hou.paneLinkType.Pinned :
            return hou.paneLinkType.Group1
        else :
            return cursor_group

    except:
        # not a pane
        return hou.paneLinkType.Group1


def pane_linkGroup( panetype ) :
    cursor_group = cursor_linkGroup()
    current_desktop = hou.ui.curDesktop()

    for pane in current_desktop.paneTabs() :
        if pane.type() == panetype :
            if pane.linkGroup() == cursor_group :
                return pane



def parm_pane () :
    pass


def parmnode () :
    parm_pane = hou.ui.curDesktop().paneTabOfType(hou.paneTabType.Parm)
    parmnode = parm_pane.currentNode()
    return parmnode


def container () :
    parm_pane = hou.ui.curDesktop().paneTabOfType(hou.paneTabType.Parm)
    parmnode = parm_pane.currentNode()
    container = parmnode.parent()
    return container
