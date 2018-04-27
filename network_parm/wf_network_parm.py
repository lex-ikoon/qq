import hou
import toolutils
import wf_selected

def flag_render () :
    for node in hou.selectedNodes():
        node.setRenderFlag(not node.isRenderFlagSet())


def flag_display () :
    parmnode = wf_selected.parmnode()
    containername = parmnode.parent().name()
    nodetype = "multiflag"

    if hou.sopNodeTypeCategory() == parmnode.parent().childTypeCategory():
        nodetype = "singleflag"

    if hou.dopNodeTypeCategory() == parmnode.parent().childTypeCategory():
        nodetype = "singleflag"

    ################################
    ## unflag to the last flagged ##
    ################################

    if nodetype == "singleflag":

        # get this
        if len(hou.selectedNodes()) == 0:
            thisnode = parmnode
        else:
            thisnode = hou.selectedNodes()[0]
        thispath = thisnode.path()

        # get last
        lastpath = hou.getenv("unflagged", thispath)
        try:
            #node exists
            if hou.node(lastpath).parent().name() != containername:
                lastpath = thispath
        except:
            #node was deleted / renamed
            lastpath = thispath
        
        # get flag
        flagpath = hou.getenv("flag", thispath)
        try:
            #node exists    
            if hou.node(flagpath).parent().name() != containername:
                flagpath = thispath
        except:
            #node was deleted / renamed
            flagpath = thispath

            
        try:
            flag = hou.node(thispath).isDisplayFlagSet()
        except:
            flag = 2
            

        if flag == 0 :
        
            # setting clean
            setpath = thispath
            unflag = flagpath
            hou.putenv("unflagged", unflag )

            # set
            hou.putenv("flag", setpath )    
            setnode = hou.node( setpath )
            setnode.setDisplayFlag(True)

        if flag == 1 :
        
            # setting flagged
            setpath = lastpath
            unflag = thispath
            hou.putenv("unflagged", unflag )

            # set
            hou.putenv("flag", setpath )    
            setnode = hou.node( setpath )
            setnode.setDisplayFlag(True)

    ################################
    ####  not SOP, just toggle  ####
    ################################

    if nodetype == "multiflag":
        # none is selected
        if len(hou.selectedNodes()) == 0:
            parmnode.setDisplayFlag(not parmnode.isDisplayFlagSet())

        # for all selected    
        for node in hou.selectedNodes():
            try:
                node.setDisplayFlag(not node.isDisplayFlagSet())
            except:
                hasnoflag = True


def flag_bypass () :
    for node in hou.selectedNodes():
        node.bypass(not node.isBypassed())


def flag_template () :
    for node in hou.selectedNodes():
        node.setTemplateFlag(not node.isTemplateFlagSet())


def autoscope_off () :
    default_autoparms = ["tx","ty","tz","rx","ry","rz","sx","sy","sz"]
    for node in hou.selectedNodes() :
        for autoparm in default_autoparms:
            try:
                parm = node.parm(autoparm)
                parm.setAutoscope(False)
            except:
                print "parm [" + autoparm +"] doesn't exist"



def opencl_container () :
    container = wf_selected.container()
    nodes = container.allSubChildren()
    for node in nodes:
        if not node.isInsideLockedHDA():
            parms = node.parms()
            for parm in parms:
                if parm.name()=='opencl':
                    try:
                        parm.set(1)
                    except hou.PermissionError: 
                        pass
