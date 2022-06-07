import hou





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




def start () :
    sceneview_main = hou.ui.curDesktop().findPaneTab("pt_sceneview_1")
    # if sceneview_main.currentState() == "karma" :
    try:
        if sceneview_main.currentHydraRenderer() == "Karma" :
            sceneview_main.restartRenderer()
        else :
            sceneview_main.setHydraRenderer("Karma")
    except:
        pass


def kill () :
    sceneview_main = hou.ui.curDesktop().findPaneTab("pt_sceneview_1")
    # if sceneview_main.currentState() == "karma" :
    try:
        sceneview_main.setHydraRenderer("Houdini GL")
        sceneview_main.restartRenderer()
    except:
        pass

