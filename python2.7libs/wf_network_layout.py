import hou
import toolutils
import wf_selection

def pin () :
    for node in hou.selectedNodes():
        node.setGenericFlag(hou.nodeFlag.DisplayComment,False)
        if node.comment() == "`" :
            node.setComment("")
        else:
            node.setComment("`")



def getConnectedNodes(node,got):
    iteration = []

    inout = []
    try:
        inout += node.inputs()
    except:
        has_no_inputs = 1
        
    try:
        inout += node.outputs()
    except:
        has_no_outputs = 1

    for n in inout:
        if n not in got:
            got.append(n)
            iteration.append(n)
            iteration += getConnectedNodes(n,got)

    return iteration


def node_prefixes () :

    node_prefixes = []

    node_prefixes.append( 'mat' )
    node_prefixes.append( 'MAT' )
    node_prefixes.append( 'QQMAT' )

    node_prefixes.append( 'chop' )
    node_prefixes.append( 'CHOP' )
    node_prefixes.append( 'QQCHOP' )

    node_prefixes.append( 'ref' )
    node_prefixes.append( 'REF' )
    node_prefixes.append( 'QQREF' )

    node_prefixes.append( 'pre' )
    node_prefixes.append( 'PRE' )
    node_prefixes.append( 'QQPRE' )

    return node_prefixes
    


def lay () :


    parm_pane = wf_selection.pane_linkGroup( hou.paneTabType.NetworkEditor )
    containernode = parm_pane.currentNode().parent()


    ################################
    ########   the pins    #########
    ################################

    childrenArr = containernode.children()
    pinStatesArr = []
    pinNodesArr = []
    positionsArr = []

    # store all positions
    for child in childrenArr:
        pinned = 0
        if child.comment() == "`" :
            pinned = 1
            pinNodesArr.append( child )
            
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
                no_connected = 1
            
        # cleanup
        pinNode.setPosition(pinpos)
        pinNode.setComment("`")
       

       
    ################################
    #######   net  to  set  ########
    ################################

    # define offset
    offsetx = 3
    offsety = 0

    containerpath = containernode.path()

    prefixes = node_prefixes()

    for prefix in prefixes :
            
            name_dat = prefix + "dat_"
            name_app = prefix + "app_"

            dats = hou.node(containerpath).glob(name_dat+"*")

            # for all
            for dat in dats:
                xxx,task = dat.name().split("_")
                
                # appropriate channel node
                path_dat = containerpath + "/" + name_dat + task
                path_app = containerpath + "/" + name_app + task
                
                node_dat = hou.node(path_dat)    
                node_app = hou.node(path_app)

                # get pos
                posx = node_app.position()[0] + offsetx
                posy = node_app.position()[1] + offsety

                # set pos
                if node_dat.comment() != "`" :
                    # typical dat node
                    node_dat.setPosition( [posx,posy] )
                else :
                    # dat has custom pos, probably because it collided
                    # so dont move it
                    pass

                # shape
                node_dat.setUserData("nodeshape", "clipped_right")
                node_app.setUserData("nodeshape", "clipped_left")