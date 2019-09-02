import hou
import wf_selection
reload(wf_selection)


def get_siblings ( current, inputs, outputs ) :
    siblings = []
    for input in inputs :
        for candidate in input.outputs() :
            if candidate != current  :    siblings.append(candidate)
    for output in outputs :
        for candidate in output.inputs() :
            if candidate != current  :    siblings.append(candidate)
    return siblings


def selection_find ( current, direction, candidates ) :
    target_list  = []

    for target in candidates :
        vec_target    = hou.Vector2.normalized(    target.position() - current.position()    )
        vec_direction = hou.Vector2.normalized(    hou.Vector2(direction)    )
        len_target    = hou.Vector2.length(        target.position() - current.position()    )
        dot           = vec_target.dot(vec_direction)
        weight        = dot / (len_target+0.01)
        # print str(child) + " / " + str(dot)
        target_list.append([target,weight])

    target_list = sorted(target_list, key=lambda x: -x[1])
    closest = target_list[0]
    return closest[0]


def selection_go( direction, parent ) :
    parm_pane = wf_selection.pane_linkGroup( hou.paneTabType.NetworkEditor )
    if parent == True   :   current   = parm_pane.currentNode().parent()
    else                :   current   = parm_pane.currentNode()

    target        = current
    inputs        = current.inputs()
    outputs       = current.outputs()
    inputs_count  = len(inputs)
    outputs_count = len(outputs)

    if direction == [0,1] :
        if inputs_count > 0   :   target = inputs[0]
        else                  :   target = selection_find(current, direction, current.parent().children())

    if direction == [0,-1] :
        if outputs_count > 0  :   target = outputs[0]
        else                  :   target = selection_find(current, direction, current.parent().children())

    if direction == [-1,0] or  direction == [1,0] :
        siblings = get_siblings ( current, inputs, outputs )
        if len(siblings) == 0 :   target = selection_find(current, direction, current.parent().children())
        else                  :   target = selection_find(current, direction, siblings)

    if parent == True   :   parm_pane.cd(target.path())
    else                :   parm_pane.setCurrentNode(target)



def sort_by_x () :
    node_merge = wf_selection.parmnode()
    # list contains pairs [  [node,position] , [node,position] , ... ]
    node_list  = []
    for node in node_merge.inputs():
        node_list_pair = []
        node_list_pair.append(node)
        node_list_pair.append(node.position()[0])
        node_list.append(node_list_pair)

    # first item is left
    node_list = sorted(node_list, key=lambda x: x[1])
    # create connections    
    for (i,pair) in enumerate(node_list):
        node_merge.setInput(i, pair[0])


def create_by_y () :
    # list contains pairs [  [node,position] , [node,position] , ... ]
    node_list      = []
    for node in hou.selectedNodes() :
        node_list_pair = []
        node_list_pair.append(node)
        node_list_pair.append(node.position()[1])
        node_list.append(node_list_pair)

    # first item is top
    node_list = sorted(node_list, key=lambda x: -x[1])
    # create connections
    for (i,pair) in enumerate(node_list):
        if i>0 :
            node_this = pair[0]
            node_prev = node_list[i-1][0]
            node_this.setInput(0, node_prev)

def toggle_dependencies () :
    parm_pane = wf_selection.pane_linkGroup( hou.paneTabType.NetworkEditor )
    view_dependencies = hou.getenv("view_dependencies", "0")
    if view_dependencies == "0": view_dependencies = "1"
    else:                        view_dependencies = "0"
    hou.putenv("view_dependencies", view_dependencies)
    parm_pane.setPref('showdep',str(view_dependencies))