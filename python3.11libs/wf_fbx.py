# import wf_fbx; import imp; imp.reload(wf_fbx); node = kwargs["node"] ; wf_fbx.show_all(node)
# network_tab = hou.ui.curDesktop().findPaneTab("pt_parmeditor_1")
# fbx_node    = network_tab.pwd()

import hou

# --------------------------------------------------------------------------------------------------------------------------------------------


def importer (importer_node, name, objpath):

    # --------------------
    # create object merge



    # --------------------
    # create object merge

    name_merge = "IN_" + name
    node_merge = importer_node.parent().createNode('object_merge',name_merge)
    node_merge.parm("objpath1").set(objpath)
    node_merge.parm("xformtype").set(1)
    node_merge.moveToGoodPosition()

    # --------------------
    # create filecache
    node_filecache = node_merge.createOutputNode("filecache", node_name = "cache_" + name)
    node_filecache.parm("loadfromdisk").set(1)
    node_filecache.parm("timedependent").set(0)
    node_filecache.parm("enableversion").set(0)
    node_filecache.parm("basename").set("$OS")
    node_filecache.parm("basedir").set("$HIP/fbx_merge")
    node_filecache.parm("cachedir").set('`chs("basedir")`')

    # --------------------
    # create null
    node_null = node_filecache.createOutputNode("null", node_name = name)












def import_one (importer_node):
    fbx_node  = importer_node.parm("fbx_node").evalAsNode()
    nodes     = hou.selectedNodes()
    name      = importer_node.parm("name").evalAsString()
    color_yes = hou.Color(0.996, 0.933, 0)

    if name == "":  
        name = "in"
    
    # --------------------
    # objpath

    objpath = ""
    for node in nodes:
        objpath += node.renderNode().path() + " "


    # --------------------
    # import

    importer (importer_node, name, objpath)

    # --------------------
    # create color inside
    for node in nodes:
        node_render = node.renderNode()
        node_color  = node_render.createOutputNode("color")
        node_color.parm("colorr").set(1)
        node_color.parm("colorg").set(1)
        node_color.parm("colorb").set(0)
        node_color.setDisplayFlag(True)
        node_color.setRenderFlag(True)

    for node in nodes:
        objpath += node.path() + " "

    # --------------------
    # set as YES
    for node in nodes:
        node.setColor(color_yes)




# --------------------------------------------------------------------------------------------------------------------------------------------


def show_all (importer_node):
    fbx_node    = importer_node.parm("fbx_node").evalAsNode()
    nodes       = fbx_node.children()
    for node in nodes:
        try:
            node.setDisplayFlag(True)
        except:
            noflag = 1



def hide_all (importer_node):
    fbx_node    = importer_node.parm("fbx_node").evalAsNode()
    nodes       = fbx_node.children()
    for node in nodes:
        try:
            node.setDisplayFlag(False)
        except:
            noflag = 1


def select_all (importer_node):
    fbx_node    = importer_node.parm("fbx_node").evalAsNode()
    nodes       = fbx_node.children()
    for node in nodes:
        try:
            if node.type().name() == "geo":
                node.setSelected(True)
        except:
            noflag = 1



# --------------------------------------------------------------------------------------------------------------------------------------------

def show_yes (importer_node):
    fbx_node  = importer_node.parm("fbx_node").evalAsNode()
    nodes     = fbx_node.children()
    color_yes = hou.Color(0.996, 0.933, 0)

    for node in nodes:
        try:
            if node.color() == color_yes:
                node.setDisplayFlag(True)
        except:
            noflag = 1



def hide_yes (importer_node):
    fbx_node  = importer_node.parm("fbx_node").evalAsNode()
    nodes     = fbx_node.children()
    color_yes = hou.Color(0.996, 0.933, 0)

    for node in nodes:
        try:
            if node.color() == color_yes:
                node.setDisplayFlag(False)
        except:
            noflag = 1



def select_yes (importer_node):
    fbx_node  = importer_node.parm("fbx_node").evalAsNode()
    nodes     = fbx_node.children()
    color_yes = hou.Color(0.996, 0.933, 0)

    for node in nodes:
        try:
            if node.color() == color_yes and node.type().name() == "geo":
                node.setSelected(True)
        except:
            noflag = 1


# --------------------------------------------------------------------------------------------------------------------------------------------


def show_no (importer_node):
    fbx_node  = importer_node.parm("fbx_node").evalAsNode()
    nodes     = fbx_node.children()
    color_no = hou.Color(0, 0, 0)

    for node in nodes:
        try:
            if node.color() == color_no:
                node.setDisplayFlag(True)
        except:
            noflag = 1



def hide_no (importer_node):
    fbx_node  = importer_node.parm("fbx_node").evalAsNode()
    nodes     = fbx_node.children()
    color_no = hou.Color(0, 0, 0)

    for node in nodes:
        try:
            if node.color() == color_no:
                node.setDisplayFlag(False)
        except:
            noflag = 1



def select_no (importer_node):
    fbx_node  = importer_node.parm("fbx_node").evalAsNode()
    nodes     = fbx_node.children()
    color_no = hou.Color(0, 0, 0)

    for node in nodes:
        try:
            if node.color() == color_no and node.type().name() == "geo":
                node.setSelected(True)
        except:
            noflag = 1



# --------------------------------------------------------------------------------------------------------------------------------------------



def show_waiting (importer_node):
    fbx_node  = importer_node.parm("fbx_node").evalAsNode()
    nodes     = fbx_node.children()
    color_no  = hou.Color(0, 0, 0)
    color_yes = hou.Color(0.996, 0.933, 0)

    for node in nodes:
        try:
            if node.color() != color_no and node.color() != color_yes and node.type().name() == "geo":
                node.setDisplayFlag(True)
        except:
            noflag = 1



def hide_waiting (importer_node):
    fbx_node  = importer_node.parm("fbx_node").evalAsNode()
    nodes     = fbx_node.children()
    color_no  = hou.Color(0, 0, 0)
    color_yes = hou.Color(0.996, 0.933, 0)

    for node in nodes:
        try:
            if node.color() != color_no and node.color() != color_yes and node.type().name() == "geo":
                node.setDisplayFlag(False)
        except:
            noflag = 1



def select_waiting (importer_node):
    fbx_node  = importer_node.parm("fbx_node").evalAsNode()
    nodes     = fbx_node.children()
    color_no  = hou.Color(0, 0, 0)
    color_yes = hou.Color(0.996, 0.933, 0)

    for node in nodes:
        try:
            if node.color() != color_no and node.color() != color_yes and node.type().name() == "geo":
                node.setSelected(True)
        except:
            noflag = 1



# --------------------------------------------------------------------------------------------------------------------------------------------



