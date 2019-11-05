import hou
import PyTake2



def create_ogl_rop () :
    obj_nodes = hou.selectedNodes()
    ogl_container = hou.node("/obj/rop_OGL")
    if not ogl_container :
        ogl_container = hou.node("/obj").createNode("ropnet", "rop_OGL") 


    for obj_node in obj_nodes :
        name_long = obj_node.name()
        name_short = name_long.split("_")[0]

        # create ROP
        ogl_node = ogl_container.createNode( "opengl", name_short )
        ogl_node.setPosition(obj_node.position())

        # set take
        take_parm = ogl_node.parm("take")
        take_parm.set(name_long)

        
        ogl_node.parm("trange").set(2)
        # set range
        if name_long.find("_") != -1 :
            start = name_long.split("_")[1]
            end   = name_long.split("_")[2]
            ogl_node.parm("f1").set(start)
            ogl_node.parm("f2").set(end)

        
        # gamma
        ogl_node.parm("gamma").set(2.2)
        ogl_node.parm("shadows").set(0)
        ogl_node.parm("hqlighting").set(0)
        
        # set picture name
        path = "$HIP/render/" + name_short + "/" + name_short + "_$F4.png"
        ogl_node.parm("picture").set(path)



def create_rs_rop () :
    obj_nodes = hou.selectedNodes()
    rs_container = hou.node("/obj/rop_RS")


    for obj_node in obj_nodes :
        name_long = obj_node.name()
        name_short = name_long.split("_")[0]

        # create ROP
        rs_node = rs_container.createNode( "Redshift_ROP", name_short )
        rs_node.setPosition(obj_node.position())

        # set take
        take_parm = rs_node.parm("take")
        take_parm.set(name_long)

        rs_node.parm("trange").set(2)
        # set range
        if name_long.find("_") != -1 :
            start = name_long.split("_")[1]
            end   = name_long.split("_")[2]
            
            rs_node.parm("f1").deleteAllKeyframes()
            rs_node.parm("f2").deleteAllKeyframes()

            rs_node.parm("f1").set(start)
            rs_node.parm("f2").set(end)

        # 
        rs_node.parm("RS_nonBlockingRendering").set(0)
        rs_node.parm("RS_renderToMPlay").set(0)
        rs_node.parm("RS_outputFileFormat").set(3) # .png

        # set picture name
        path = "$HIP/render/" + name_short + "/" + name_short + "_$F4.png"
        rs_node.parm("RS_outputFileNamePrefix").set(path)





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
    path_bat = path_hip + '/_render.bat'
    file_rop = open( path_bat, "w")
    file_rop.write(script_bat)




def start () :
    pane = hou.ui.curDesktop().paneTabOfType(hou.paneTabType.IPRViewer)
    pane.killRender()
    pane.startRender()


def kill () :
    pane = hou.ui.curDesktop().paneTabOfType(hou.paneTabType.IPRViewer)
    pane.killRender()


def take_from_name () :
    for node in hou.selectedNodes():
        name = node.name()
        new_take = PyTake2.Take(name)
        new_take.includeDisplayFlag(node)
        PyTake2.returnToMainTake()