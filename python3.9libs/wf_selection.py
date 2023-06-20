import hou

# current_desktop = hou.ui.curDesktop()   
# cursor_pane     = current_desktop.paneTabUnderCursor()
# cursor_pane.pane().setIsSplitMaximized(False)
# c = hou.ui.curDesktop() 
# c.findPane(13).setIsSplitMaximized(False)
# hou.ui.curDesktop().panes()[2].setIsSplitMaximized(False)
# (<hou.Pane 4>, <hou.Pane 6>, <hou.Pane 10>, <hou.Pane 13>, <hou.Pane 16>, <hou.Pane 18>)
# cursor_pane.pane().currensetSplitFraction(0.5)
# print (cursor_pane.pane())
# hou.ui.curDesktop().findPane(354)
# print ("ok")





def cursor_linkGroup() :
    try:
        current_desktop = hou.ui.curDesktop()
        cursor_pane     = current_desktop.paneTabUnderCursor()
        cursor_group    = cursor_pane.linkGroup()
        # if cursor_group == hou.paneLinkType.FollowSelection or cursor_group == hou.paneLinkType.Pinned :
        #     return hou.paneLinkType.Group1
        # else :
        #     return cursor_group
        return cursor_group

    except:
        # not a pane
        return hou.paneLinkType.Group1


def pane_linkGroup( panetype ) :
    cursor_group = cursor_linkGroup()
    current_desktop = hou.ui.curDesktop()
    pane_under_cursor = current_desktop.paneTabUnderCursor()

    # pane_under_cursor.type()
    # current_desktop.panes()[0].createTab(hou.paneTabType.ChannelEditor) 
    # first check under cursor
    try:
        if pane_under_cursor.type() == panetype :
            return pane_under_cursor
    except:
        # not a pane
        pass

    # try it for the right group
    for pane in current_desktop.paneTabs() :
        if pane.type() == panetype :
            if pane.linkGroup() == cursor_group :
                return pane

    # if none found, then first
    for pane in current_desktop.paneTabs() :
        if pane.type() == panetype :
            if pane.isCurrentTab() :
                return pane


    # if none found, then Group1
    # cursor_group = hou.paneLinkType.Group1
    # for pane in current_desktop.paneTabs() :
    #     if pane.type() == panetype :
    #         if pane.linkGroup() == cursor_group :
    #             return pane



#def parm_pane () :
#    pass


def parmnode () :
    panetab_under_cursor = hou.ui.curDesktop().paneTabUnderCursor()
    try:
        panetab_name = panetab_under_cursor.name()
    except:
        panetab_name = "probably_stowbar"

    if panetab_name == "pt_network_2" or panetab_name == "pt_parmeditor_2" :
        parm_pane = hou.ui.curDesktop().findPaneTab("pt_parmeditor_2")
        parmnode  = parm_pane.currentNode()
    else :
        parm_pane = hou.ui.curDesktop().findPaneTab("pt_parmeditor_1")
        parmnode  = parm_pane.currentNode()

    # print (parmnode)
    return parmnode


def parmnode_obj () :
    parmnode = parmnode ()
    parent   = parmnode.parent()

    try:
        for i in range(8):
            if parent.type().category() == hou.objNodeTypeCategory() :
                return parent
            else :
                parent = parent.parent()
    except:
        return parmnode


def container () :
    container = parmnode().parent()
    return container
