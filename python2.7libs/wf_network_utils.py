import re
import hou
import wf_selection
reload(wf_selection)
import wf_network_parm
reload(wf_network_parm)


def selection_switch () :
    nodes = hou.selectedNodes()
    count = len(nodes)
    if count > 1 :
        # if few nodes are selected, then initialize, save that selection
        selection_stack = ','.join(node.path() for node in nodes)
        hou.putenv('selection_stack', selection_stack )
        hou.putenv('selection_current', '0' )
        hou.putenv('selection_count'  , str(count) )
    else :
        # hou.ui.displayMessage("ikoon: select more than one node") 
        # return
        pass

    # even if one node is selected...
    selection_stack   = hou.getenv('selection_stack', 'none')
    selection_current = hou.getenv('selection_current', 'none')
    selection_count   = hou.getenv('selection_count', 'none')
    
    # go to next node...
    stack   = selection_stack.split(',')
    current = int(selection_current) + 1
    count   = int(selection_count)
    if current == count :
        current = 0

    # update the saved variable
    hou.putenv('selection_current', str(current) )

    # select that node in current pane
    target = hou.node(stack[current])
    parm_pane = wf_selection.pane_linkGroup( hou.paneTabType.Parm )
    parm_pane.setCurrentNode(target,True)


def go_parm(node,parm) :
    parm = parm.rawValue()
    path = re.findall('[\"\'](.*?)[\"\']',parm)[0]
    path = path[:path.rindex('/')]
    target = node.node(path)
    parm_pane = wf_selection.pane_linkGroup( hou.paneTabType.Parm )
    parm_pane.setCurrentNode(target,True)



def parm_round(parms) :

    def actual_ndigits(number) :
        ndigits  = 6
        thr = 10e-8
        if abs(number) < thr :
            # number is zero, don't % because it fails
            return -7
        else:
            while abs(  number - round (number,ndigits)  ) < thr:
                ndigits = ndigits -1
            return ndigits+1

    ndigits_all = []
    for parm in parms:
        ndigits = actual_ndigits(parm.eval())
        ndigits_all.append(ndigits)

    # start by rounding to 3 digits
    ndigits_new = min( 3  ,  max(ndigits_all) - 1 )

    for parm in parms:
        new_val = round (parm.eval(),ndigits_new)
        parm.set( new_val )


# def parm_relative_to_absolute_all(node) :
#     print "------"
#     for parm in node.parms() :
#         parm_rel     = parm.getReferencedParm()
#         path_abs     = parm_rel.node().path()
#         print parm_rel
        # print path_abs
        # parm_raw_abs = parm_raw.replace(path,path_abs)
        # parm.setExpression(parm_raw_abs,  replace_expression=True)



def parm_relative_to_absolute_all(node) :
    for parm in node.parms() :
        parm_raw     = parm.rawValue()
        try:
            path         = re.findall('[\"\'](.*?)[\"\']',parm_raw)[0]
            path         = path[:path.rindex('/')]
            path_abs     = node.node(path).path()
            parm_raw_abs = parm_raw.replace(path,path_abs)
            parm.setExpression(parm_raw_abs,  replace_expression=True)
        except:
            # not expression
            pass



def find_parm(parmname) :

    if parmname == None :
        text = hou.ui.readInput("Search text:", buttons=("Search", "Cancel"))[1]
    else :
        text = parmname

    container     = wf_selection.container()
    nodes         = container.allSubChildren()
    pattern       = ''
    pattern_count = 0

    print '----    found:   ----'
    for node in nodes :
        parms = node.parms()
        for parm in parms :
            raw = parm.rawValue()
            if raw.find(text) > -1 :
                if pattern_count > 0 :
                    pattern   += ' | '
                pattern       += parm.name() + '~=*' + text + '*'
                pattern_count += 1
                print 'NODE: ' + str(node) + '   // PARM: ' + parm.description() + "   // RAW: " + raw
    print '--------------------------'

    hou.ui.copyTextToClipboard(pattern)


def create_node(type) :
    nodes = hou.selectedNodes()
    connections = hou.selectedConnections()
    
    if nodes :

        if type == 'g' and nodes[0].type().category() == hou.objNodeTypeCategory() :
            type = 'geo'

        if type == 'g' and nodes[0].type().category() == hou.sopNodeTypeCategory() :
            type = 'groupcreate'

        if type == 'merge' or type == 'switch' :
            # one node, multiple inputs
            node_create = nodes[0].parent().createNode( type )
            for node in nodes:
                node_create.setNextInput(node)
            node_create.moveToGoodPosition(relative_to_inputs=True, move_inputs=False, move_outputs=True, move_unconnected=False)
    
        if type == 'null' or type == 'xform' or type == 'attribwrangle' or type == 'geo' or type == 'blast' or type == 'groupcreate':
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

        if type == 'g' and connections[0].inputNode().type().category() == hou.objNodeTypeCategory() :
            type = 'geo'

        if type == 'g' and connections[0].inputNode().type().category() == hou.sopNodeTypeCategory() :
            type = 'groupcreate'

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
    selected = hou.selectedNodes()

    for node_src in selected :

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
        parm_path = node_mrg.parm("objpath1")
        parm_path.set(path_src)
        parm_transform = node_mrg.parm("xformtype")
        parm_transform.set(1)

        #setcol
        node_src.setColor(color)
        node_mrg.setColor(color)

        #selection
        node_src.setSelected(False)
        node_mrg.setSelected(True)



def create_hqueue_render () :

    offsetx = 3
    offsety = 0
    color = hou.Color(0.35, 0.35, 0.35)
    selected = hou.selectedNodes()

    for node_src in selected :

        name_src = node_src.name()

        posx = node_src.position()[0] + offsetx
        posy = node_src.position()[1] + offsety

        #create, name, pos
        container = node_src.parent().path()
        name_hqr = "hq_" + name_src
        node_hqr = hou.node(container).createNode('qrender',name_hqr)
        node_hqr.setPosition( [posx,posy] )

        #parm
        path_src = node_src.path()
        parm_path = node_hqr.parm("hq_driver")
        parm_path.set("../" + name_src)

        #setcol
        node_hqr.setColor(color)

        #selection
        node_src.setSelected(False)
        node_hqr.setSelected(True)



def recook_container () :
    container = wf_selection.parmnode()
    nodes = container.allSubChildren()
    for node in nodes :
        node.cook(force=True)




def fc_list_print (filecaches) :
    import wf_network_ui
    reload(wf_network_ui)

    # remove duplicates
    filecaches = list(dict.fromkeys(filecaches))

    # create search pattern
    print '\n-------    found:  -------'
    pattern       = ''
    pattern_count = 0

    for fc in filecaches :
        # set session Id
        session_id = fc.sessionId()
        wf_network_ui.parm_create (fc, "integer", "session_id", "session_id")
        wf_network_ui.parm_update (fc, "integer", "session_id", hidden="True")
        fc.parm("session_id").set(session_id)

        # create search pattern
        if pattern_count > 0 :
            pattern   += ' | '
        pattern       += "session_id" + '=' + str(session_id) + ''
        pattern_count += 1
        print 'FILECACHE: ' + str(fc.path()) + ''

    hou.ui.copyTextToClipboard(pattern)
    print '--------------------------'

