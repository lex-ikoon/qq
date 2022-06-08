import hou
import nodesearch


# create .py script for each selected ROP, to render it
# create .bat file, which renders all the created .py with hython simultaneously
def batch_script_rop () :

    import os

    path_hip     = hou.expandString('$HIP')
    path_hipfile = hou.expandString('$HIPFILE')
    path_hython  = hou.expandString('$HB') + '/hython.exe'
    path_scripts = path_hip + '/scripts/'

    if not os.path.exists(path_scripts):
        os.makedirs(path_scripts)

    script_bat = 'REM This batch file runs multiple .py scripts at once \n'

    for rop in hou.selectedNodes() :
        # .py script
        script_rop  = '# This .py script opens a file and renders single rop\n'
        script_rop += 'hou.hipFile.load("' + path_hipfile + '")\n'
        script_rop += 'node = hou.node("' + rop.path() + '")\n'
        script_rop += 'node.render(verbose=True,output_progress=True)'
        
        # write .py to disk
        path_py = path_scripts + rop.name() + '.py'
        file_py = open( path_py, "w")
        file_py.write(script_rop)

        # .bat script
        script_bat += 'start "Render: ' + rop.name() + '" "'
        script_bat += path_hython + '" "'
        script_bat += path_py + '"\n'


    # write .bat to disk
    path_bat = path_hip + '/_render_' + rop.name() + '.bat'
    file_rop = open( path_bat, "w")
    file_rop.write(script_bat)




def kill () :
    sceneview_main = hou.ui.curDesktop().findPaneTab("pt_sceneview_1")
    # if sceneview_main.currentState() == "karma" :
    try:
        sceneview_main.setHydraRenderer("Houdini GL")
        sceneview_main.restartRenderer()
    except:
        pass




def start () :

    sceneview_main = hou.ui.curDesktop().findPaneTab("pt_sceneview_1")
    sceneview_edit = hou.ui.curDesktop().findPaneTab("pt_sceneview_2")

    pe_1 = hou.ui.curDesktop().findPaneTab("pt_parmeditor_1")
    nw_1 = hou.ui.curDesktop().findPaneTab("pt_network_1")
                     
    # find active lopnet
    #-----------------------------------------------
    root          = hou.node("/obj")
    matcher       = nodesearch.NodeType( "lopnet", exact=True )
    lopnets       = matcher.nodes( root, recursive=False )
    lopnet_active = lopnets[0]

    for lopnet in lopnets :
        if lopnet.userData("lopnet_active") == "on":
            lopnet_active = lopnet


    # lock
    #-----------------------------------------------
    sceneview_main.setLinkGroup(hou.paneLinkType.Pinned)
    sceneview_edit.setLinkGroup(hou.paneLinkType.Pinned)
    pe_1.setLinkGroup(hou.paneLinkType.Pinned)
    nw_1.setLinkGroup(hou.paneLinkType.Pinned)

    # set pwd
    #-----------------------------------------------
    sceneview_main.setPwd(lopnet_active)
    hou.hscript("viewcamera -c /cam  wf_desktop.pt_sceneview_1.solaris.persp1")


    # unlock edit
    #-----------------------------------------------
    pe_1.setLinkGroup(hou.paneLinkType.FollowSelection)
    # nw_1.setLinkGroup(hou.paneLinkType.FollowSelection)
    sceneview_edit.setLinkGroup(hou.paneLinkType.FollowSelection)

    # set camera
    #-----------------------------------------------
    # this is a bug
    # lopnet_camera = lopnet_active.parm("force_cam").evalAsNode()
    # sceneview_main.curViewport().setCamera(lopnet_camera)
    # wf_desktop.pt_sceneview_1.solaris



    # restart Karma render (or set Karma as renderer)
    #-----------------------------------------------
    try:
        if sceneview_main.currentHydraRenderer() == "Karma" :
            sceneview_main.restartRenderer()
        else :
            sceneview_main.setHydraRenderer("Karma")
    except:
        pass