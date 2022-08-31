import hou
import imp
import toolutils
import wf_selection
imp.reload(wf_selection)


def pin () :
    for node in hou.selectedNodes():
        node.setGenericFlag(hou.nodeFlag.DisplayComment,False)
        if node.comment() == "`" :
            node.setComment("")
        else:
            node.setComment("`")



def getConnectedNodes(node,got):
    iteration = []

    inouts = []
    try:
        inouts += node.inputs()
    except:
        pass

    try:
        inouts += node.outputs()
    except:
        pass

    # MOVABLE ITEMS-----
    try:
        items = node.parent().allItems()
        # print (items)
        for item in items:
            if (item.networkItemType() == hou.networkItemType.NetworkDot or  item.networkItemType() == hou.networkItemType.SubnetIndirectInput):
                if item.outputs()[0] == node :
                    temporary = []
                    temporary.append(item)
                    inouts += temporary
    except:
        pass
    # MOVABLE ITEMS-----
    for inout in inouts:
        if inout not in got and inout != None:
            if inout.parent() == node.parent(): # because inputs may lead out of subnet
                got.append(inout)
                iteration.append(inout)
                iteration += getConnectedNodes(inout,got)

    return iteration


# BACKUP BEFORE DOTS AND MOVABLEITEMS
# def getConnectedNodes(node,got):
#     iteration = []

#     inout = []
#     try:
#         inout += node.inputs()
#     except:
#         has_no_inputs = 1
        
#     try:
#         inout += node.outputs()
#     except:
#         has_no_outputs = 1

#     for n in inout:
#         if n not in got:
#             got.append(n)
#             iteration.append(n)
#             iteration += getConnectedNodes(n,got)

#     return iteration



def lay () :

    parm_pane = wf_selection.pane_linkGroup( hou.paneTabType.NetworkEditor )
    containernode = parm_pane.currentNode().parent()
    containerpath = containernode.path()

    ################################
    ########   the pins    #########
    ################################

    # childrenArr = containernode.children()
    childrenArr = containernode.allItems()
    pinStatesArr = []
    pinNodesArr = []
    positionsArr = []

    # store all positions
    for child in childrenArr:
        pinned = 0
        try:
            if child.comment() == "`" :
                pinned = 1
                pinNodesArr.append( child )
        except:
            pass

        pinStatesArr.append( pinned )
        positionsArr.append( child.position() )


    # store pinned positions
    for pinNode in pinNodesArr:
        pos = pinNode.position()
        comment = str(pos[0]) + "," + str(pos[1])
        pinNode.setComment(comment)

        
    # classic layoutChildren()
    containernode.layoutChildren()

    # reposition the branches
    for pinNode in pinNodesArr:

        pinpos = pinNode.comment()
        pinpos = pinpos.split(",")
        pinpos = [ float(pinpos[0]) , float(pinpos[1]) ]
        
        allConnected = []
        allConnected = getConnectedNodes(pinNode,allConnected)

        pos = pinNode.position()
        move = [ pinpos[0] - pos[0] , pinpos[1] - pos[1] ]
        
        for connected in allConnected:
            try:
                connected.move(move)
            except:
                pass
            
        # cleanup
        pinNode.setPosition(pinpos)
        pinNode.setComment("`")
       

       
    ################################
    #######   dat  to  app  ########
    ################################

    # define offset
    offsetx = 3
    offsety = 0

    prefix = "REF_"

    refs = hou.node(containerpath).glob(prefix+"*")

    # for all
    for ref in refs:
        xxx,peer = ref.name().split("_")
        
        # appropriate channel node
        path_REF = containerpath + "/" + prefix + peer
        path_net = containerpath + "/" + peer
        
        node_REF = hou.node(path_REF)    
        node_net = hou.node(path_net)



        # get pos
        posx = node_net.position()[0] + offsetx
        posy = node_net.position()[1] + offsety

        # check collisions
        tolerance = 2.0;
        for check in containernode.children() :
            distance = hou.Vector2.length(   check.position()-hou.Vector2([posx,posy])   )
            # print distance
            if distance < tolerance and check != node_REF:
                posx = posx - 2*offsetx
                break

        # set pos
        if node_REF.comment() != "`" :
            # typical dat node
            node_REF.setPosition( [posx,posy] )
        else :
            # REF has custom pos, probably because it collided
            # so dont move it
            pass

        # shape
        node_REF.setUserData("nodeshape", "clipped_right")
        node_net.setUserData("nodeshape", "clipped_left")