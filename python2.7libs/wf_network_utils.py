import hou
import wf_selection
reload(wf_selection)
import wf_network_parm
reload(wf_network_parm)


def create_node(type) :
    nodes = hou.selectedNodes()
    connections = hou.selectedConnections()
    
    if nodes :
        if type == 'merge' or type == 'switch' :
            # one node, multiple inputs
            node_create = nodes[0].parent().createNode( type )
            for node in nodes:
                node_create.setNextInput(node)
            node_create.moveToGoodPosition(relative_to_inputs=True, move_inputs=False, move_outputs=True, move_unconnected=False)
    
        if type == 'null' or type == 'xform' or type == 'attribwrangle':
            # multiple nodes, one input
            
            for node in nodes:
                node_create = node.createOutputNode( type )
                node_create.moveToGoodPosition(relative_to_inputs=True, move_inputs=False, move_outputs=True, move_unconnected=False)

        # set current
        parm_pane = wf_selection.pane_linkGroup( hou.paneTabType.NetworkEditor )
        parm_pane.setCurrentNode(node_create)
        # set display
        # wf_network_parm.flag_display ()

            
    if connections :
        for connection in connections :
            node_up = connection.inputNode()
            node_dn = connection.outputNode()
            node_up_index = connection.outputIndex()
            node_dn_index = connection.inputIndex()

            node_create = node_dn.createInputNode(node_dn_index, type )
            node_create.setNextInput(node_up, node_up_index)
            node_create.moveToGoodPosition(relative_to_inputs=False, move_inputs=False, move_outputs=True, move_unconnected=False)

        # set current
        parm_pane = wf_selection.pane_linkGroup( hou.paneTabType.NetworkEditor )
        parm_pane.setCurrentNode(node_create)
        # set display
        # wf_network_parm.flag_display ()

            

def create_object_merge () :

    offsetx = 3
    offsety = 0
    color = hou.Color(0.0, 0.0, 0.0)

    for node_src in hou.selectedNodes() :

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
    container = wf_selection.parmnode()
    nodes = container.allSubChildren()
    for node in nodes :
        node.cook(force=True)
