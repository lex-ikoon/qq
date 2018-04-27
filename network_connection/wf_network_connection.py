import hou
import wf_selected


def sort_by_x () :
    node_merge = wf_selected.parmnode()
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

