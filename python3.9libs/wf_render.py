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
    sceneview_SOP = hou.ui.curDesktop().findPaneTab("pt_sceneview_1")
    sceneview_LOP = hou.ui.curDesktop().findPaneTab("pt_sceneview_3")

    try:
        sceneview_LOP.setHydraRenderer("Houdini GL")
        sceneview_LOP.restartRenderer()
    except:
        pass




def start () :

    sceneview_SOP = hou.ui.curDesktop().findPaneTab("pt_sceneview_1")
    sceneview_LOP = hou.ui.curDesktop().findPaneTab("pt_sceneview_3")
    pe_1          = hou.ui.curDesktop().findPaneTab("pt_parmeditor_1")
    nw_1          = hou.ui.curDesktop().findPaneTab("pt_network_1")


    # find active lopnet
    #-----------------------------------------------
    root          = hou.node("/obj")
    matcher       = nodesearch.NodeType( "lopnet", exact=True )
    lopnets       = matcher.nodes( root, recursive=False )
    lopnet_active = lopnets[0]

    for lopnet in lopnets :
        if lopnet.userData("lopnet_active") == "on":
            lopnet_active = lopnet


    # remember pwd
    #-----------------------------------------------
    remember_pwd = pe_1.pwd()
    remember_pin = pe_1.linkGroup()

    # lock
    #-----------------------------------------------
    sceneview_LOP.setLinkGroup(hou.paneLinkType.Pinned)
    sceneview_SOP.setLinkGroup(hou.paneLinkType.Pinned)
    pe_1.setLinkGroup(hou.paneLinkType.Pinned)
    nw_1.setLinkGroup(hou.paneLinkType.Pinned)



    # set viewer pwd and camera
    #-----------------------------------------------
    lopnet_camera = lopnet_active.parm("job_camera").evalAsNode()
    ######## this is a bug
    ######## sceneview_LOP.curViewport().setCamera(lopnet_camera)
    ######## wf_desktop.pt_sceneview_1.solaris
    sceneview_LOP.setPwd(lopnet_active)
    sceneview_LOP.setIsCurrentTab()
    # print(lopnet_camera.name())
    cam_command = "viewcamera -c /" + lopnet_camera.name() + " wf_desktop.pt_sceneview_3.solaris.persp1"
    hou.hscript(cam_command)


    # unlock edit
    #-----------------------------------------------
    pe_1.setLinkGroup(remember_pin)
    nw_1.setLinkGroup(remember_pin)
    sceneview_SOP.setLinkGroup(hou.paneLinkType.FollowSelection)

    # restore pwd
    #-----------------------------------------------
    pe_1.setPwd(remember_pwd)


    # restart Karma render (or set Karma as renderer)
    #-----------------------------------------------
    try:
        if sceneview_LOP.currentHydraRenderer() == "Karma" :
            sceneview_LOP.restartRenderer()
        else :
            sceneview_LOP.setHydraRenderer("Karma")
    except:
        pass