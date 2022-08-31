import hou



def panetab_restore(script_456, force_split) :

    if script_456 == True :
        panetab_cursor = hou.ui.curDesktop().findPaneTab("pt_network_1")
    else :
        panetab_cursor = hou.ui.curDesktop().paneTabUnderCursor()

    # for pane in hou.ui.curDesktop().panes() :
    #     print "pane:"
    #     for tab in pane.tabs() :
    #         print tab.name()

    # check if swap is needed
    if hou.ui.curDesktop().panes()[0].tabs()[0].type() == hou.paneTabType.ChannelEditor :
        hou.ui.curDesktop().panes()[2].splitSwap()
        hou.ui.curDesktop().findPaneTab("pt_channelview").pane().setIsSplitMaximized( True )
        hou.ui.curDesktop().findPaneTab("pt_sceneview_2").pane().setIsSplitMaximized( False )


    # check what is under cursor
    if panetab_cursor.type() == hou.paneTabType.SceneViewer:
        # do the sceneview
        panetab_cursor.enterViewState()


    # check what is under cursor
    if panetab_cursor.type() != hou.paneTabType.SceneViewer and script_456 == False :

        # do the network
        pe_1 = hou.ui.curDesktop().findPaneTab("pt_parmeditor_1").pane()
        pe_2 = hou.ui.curDesktop().findPaneTab("pt_parmeditor_2").pane()
        nw_1 = hou.ui.curDesktop().findPaneTab("pt_network_1").pane()
        nw_2 = hou.ui.curDesktop().findPaneTab("pt_network_2").pane()

        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        split_top = pe_1.getSplitParent() #isSplitMaximized()
        split_bot = pe_2.getSplitParent() #isSplitMaximized()

        if split_top.isSplitMaximized() == False and split_bot.isSplitMaximized() == False:
            # was SPLIT
            if force_split == False :
                if panetab_cursor.linkGroup() == hou.paneLinkType.Group2 :
                    # maximize 2 only when hovering over 2
                    # print "B"
                    #### order: MAX 2
                    split_bot.setIsSplitMaximized( True )
                    split_top.setIsSplitMaximized( False )


                else :
                    # maximize 1 in all other cases
                    # print "A"
                    #### order: MAX 1
                    split_top.setIsSplitMaximized( True )
                    split_bot.setIsSplitMaximized( False )

                    ### UNLINK 1
                    hou.ui.curDesktop().findPaneTab("pt_parmeditor_1").setLinkGroup(hou.paneLinkType.FollowSelection)
                    hou.ui.curDesktop().findPaneTab("pt_network_1").setLinkGroup(hou.paneLinkType.FollowSelection)


        else :
            # was MAXIMIZED

            # remember pwd
            remember_1_pwd    = hou.ui.curDesktop().findPaneTab("pt_network_1").pwd()

            ### LINK 1
            # pin group
            hou.ui.curDesktop().findPaneTab("pt_parmeditor_1").setLinkGroup(hou.paneLinkType.Group1)
            hou.ui.curDesktop().findPaneTab("pt_network_1").setLinkGroup(hou.paneLinkType.Group1)

            # set remembered
            hou.ui.curDesktop().findPaneTab("pt_network_1").setPwd(remember_1_pwd)

            if split_top.isSplitMaximized() == True :
                # print "C"
                #### order: EVEN from 1
                split_top.setIsSplitMaximized( False )
                split_bot.setIsSplitMaximized( True ) ## was true

            if split_bot.isSplitMaximized() == True :
                # print "D"
                #### order: MAX 1
                split_top.setIsSplitMaximized( True )
                split_bot.setIsSplitMaximized( False )

                #### order: EVEN from 2
                split_top.setIsSplitMaximized( False )
                split_bot.setIsSplitMaximized( True )



        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------


def panetab_ctrl() :
    panetab_cursor = hou.ui.curDesktop().paneTabUnderCursor()

    if panetab_cursor.type() == hou.paneTabType.SceneViewer :
        # sceneview lock/unlock
        if panetab_cursor.linkGroup() == hou.paneLinkType.FollowSelection :
            panetab_cursor.setLinkGroup(hou.paneLinkType.Pinned)
        else:
            panetab_cursor.setLinkGroup(hou.paneLinkType.FollowSelection)


    # unfortunately ChannelEditor does not pin right
    # if panetab_cursor.type() == hou.paneTabType.ChannelEditor :


    else :
        # swap parms and network
        # pe_1 = hou.ui.curDesktop().findPaneTab("pt_parmeditor_1")
        # pe_2 = hou.ui.curDesktop().findPaneTab("pt_parmeditor_2")
        nw_1 = hou.ui.curDesktop().findPaneTab("pt_network_1")
        nw_2 = hou.ui.curDesktop().findPaneTab("pt_network_2")

        # remember pwd, node, bounds
        remember_1_pwd    = nw_1.pwd()
        remember_1_node   = nw_1.currentNode()
        remember_1_bounds = nw_1.visibleBounds()

        remember_2_pwd    = nw_2.pwd()
        remember_2_node   = nw_2.currentNode()
        remember_2_bounds = nw_2.visibleBounds()

        # set remembered
        nw_2.setPwd(remember_1_pwd)
        nw_2.setCurrentNode(remember_1_node)
        nw_2.setVisibleBounds(remember_1_bounds)

        nw_1.setPwd(remember_2_pwd)
        nw_1.setCurrentNode(remember_2_node)
        nw_1.setVisibleBounds(remember_2_bounds)



def panetab_set(number) :
    # print number
    # hotkey is 1, 2


    # panetab_net    = hou.ui.curDesktop().findPaneTab("pt_network_1")
    # panetab_sce    = hou.ui.curDesktop().findPaneTab("pt_sceneview_2")

    # node_left_network = panetab_net.currentNode()
    # node_left_scene   = panetab_sce.currentNode()
    # nodes_entered     = node.selectedChildren()
    # count             = len(nodes_entered)

    # panetab_MA = hou.ui.curDesktop().findPaneTab("pt_network_2")
    # panetab_GL = hou.ui.curDesktop().findPaneTab("pt_network_1")

    # material_path     = node_entered.parm("shop_materialpath").evalAsString()
    # material_fullpath = node_entered.node(material_path).parent()


    # ----------------------------------------------
    # TAB MA (2)
    # panetab_MA.setPwd(material_fullpath)
    # panetab_MA.cd(material_fullpath.path())

    # ----------------------------------------------
    # TAB GL (3)


    # ----------------------------------------------
    # TAB RS (4)

    
    pass


def panetab_clone(number) :
    # hotkey was ctrl+1, ctrl+2
    # unused
    pass

   