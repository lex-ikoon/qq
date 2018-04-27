import hou
import wf_selected

def create_object_merge () :
    # define
    offsetx = 3
    offsety = 0
    color = hou.Color(0.0, 0.0, 0.0)

    node_src = wf_selected.parmnode()
    name_src = node_src.name()

    posx = node_src.position()[0] + offsetx
    posy = node_src.position()[1] + offsety

    #create, name, pos
    container = node_src.parent().path()
    name_mrg = "IN_" + name_src
    node_mrg = hou.node(container).createNode('object_merge',name_mrg)
    node_mrg.setPosition( [posx,posy] )

    #parm
    path_src = node_src.path()
    parm = node_mrg.parm("objpath1")
    parm.set(path_src)

    #setcol
    node_src.setColor(color)
    node_mrg.setColor(color)


def recook_container () :
    container = wf_selected.parmnode()
    nodes = container.allSubChildren()
    for node in nodes :
        node.cook(force=True)