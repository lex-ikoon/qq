import hou
import toolutils
import nodesearch
import wf_selection

def flag_template_all_off () :
    parmnode = wf_selection.parmnode()
    container = parmnode.parent()
    for node in container.children():
        try:
            node.setTemplateFlag(False)
            node.setSelectableTemplateFlag(False)
        except:
            has_no_flag = 1


def light_link () :
    # parm_names = ["light_enabled","light_enable","ogl_enablelight"]
    parm_names = ["ogl_enablelight"]
    expression = '''flag_parent = hou.pwd().parent().isGenericFlagSet(hou.nodeFlag.Display)
flag_this   = hou.pwd().isGenericFlagSet(hou.nodeFlag.Display)
if flag_parent and flag_this :
    return 1
else :
    return 0'''

    for light in hou.selectedNodes() :
        for parm_name in parm_names :
            try :
                parm = light.parm(parm_name)
                parm.setExpression(expression, language=hou.exprLanguage.Python) 
                light.setUserData("nodeshape", "light")
            except:
                # parm_doesnt_exist = 1
                pass


def flag_render () :
    for node in hou.selectedNodes():
        node.setRenderFlag(not node.isRenderFlagSet())


def hda_unlock () :
    parmnode = wf_selection.parmnode()
    parmnode.allowEditingOfContents(propagate=True)


def flag_display () :
    parmnode = wf_selection.parmnode()
    containername = parmnode.parent().name()

    nodetype = "multiflag"

    if hou.sopNodeTypeCategory() == parmnode.parent().childTypeCategory():
        nodetype = "singleflag"

    if hou.dopNodeTypeCategory() == parmnode.parent().childTypeCategory():
        nodetype = "singleflag"

    if hou.lopNodeTypeCategory() == parmnode.parent().childTypeCategory():
        nodetype = "singleflag"


    if parmnode.type().name() == "lopnet" :
        nodetype = "lopnet"


    ################################
    ##      set active lopnet     ##
    ################################

    if nodetype == "lopnet":

        # settings
        color_node_on  = hou.Color(1.0, 0.725, 0.0)
        color_node_off = hou.Color(0.306, 0.306, 0.306)

        root    = hou.node("/obj")
        matcher = nodesearch.NodeType( "lopnet", exact=True )
        lopnets = matcher.nodes( root, recursive=False )

        # set all OFF
        for lopnet in lopnets :
            lopnet.setColor(color_node_off)
            lopnet.setUserData("lopnet_active", "off")

        # set active ON
        parmnode.setColor(color_node_on)
        parmnode.setUserData("lopnet_active", "on")




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

        if node.type().name().find("light") != -1      and      hou.objNodeTypeCategory() == node.parent().childTypeCategory():

            # ---------------------------------------
            # OBJ toggle light

            color_light_on  = hou.Color(1.0, 0.75, 0.2)
            color_light_off = hou.Color(0.306, 0.306, 0.306)

            enabled = node.parm("ogl_enablelight").eval()

            if enabled == 1 :
                node.setColor(color_light_off)
                node.parm("ogl_enablelight").set(0)

            if enabled == 0 :
                node.setColor(color_light_on)
                node.parm("ogl_enablelight").set(1)


        else :
            # ---------------------------------------
            # SOP bypass
            try:
                node.bypass(not node.isBypassed())
            except:
                pass






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
                print ("parm [" , autoparm ,"] doesn't exist")



def opencl_container () :
    container = wf_selection.container()
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
