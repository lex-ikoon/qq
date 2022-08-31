import hou
import imp
import wf_ui_panetab
imp.reload(wf_ui_panetab)



def parm_check(node_selected, parm_name) :

    try:
        parm_eval    = node_selected.parm(parm_name).evalAsString()
        node_target  = node_selected.node( parm_eval )

        while node_target.isInsideLockedHDA() :
            node_target = node_target.parent()

        path_checked = node_target.path()
        return path_checked

    except:
        return "VOID"


def find_first_valid_target(node_selected) :

    # ------------------------------------------------
    # --------------- PARAMETERS ---------------------
    for parm in node_selected.parms() :
        try:
            path_checked = parm_check(node_selected, parm.name())
            if path_checked != "VOID" :
                return path_checked
        except:
            pass

    # ------------------------------------------------
    # --------------- DEPENDENTS ---------------------
    try:
        allSubChildren = node_selected.allSubChildren()
        for dependent in node_selected.dependents(False) :
            if dependent not in allSubChildren:
                while dependent.isInsideLockedHDA() :
                    dependent = dependent.parent()
                path_checked = dependent.path()
                return path_checked
    except:
            pass
    
    # if no node found then "VOID"
    return "VOID"




def network_set( panetab_name, node_selected, parm_name) :
    
    if panetab_name == "pt_network_2" :
        wf_ui_panetab.panetab_restore(script_456 = False, force_split = True)
    
    if parm_name == "ENTER_THIS_NODE" :
        hou.ui.curDesktop().findPaneTab(panetab_name).cd( node_selected.path() )

    elif parm_name == "ENTER_FIRST_VALID" :
        path_found = find_first_valid_target(node_selected)
        hou.ui.curDesktop().findPaneTab(panetab_name).setCurrentNode( hou.node(path_found) )

    else :
        # print (panetab_name, node_selected, parm_name)
        path_checked = parm_check(node_selected, parm_name)
        if path_checked != "VOID" :
            hou.ui.curDesktop().findPaneTab(panetab_name).setCurrentNode( hou.node(path_checked) )



def enter_execute(node_selected, ctrl, alt, shift ) :
    node_type = node_selected.type().name()
    archetype = node_selected.userData("archetype")


    # --------------------------
    # exception: camera
    if node_type == "cam" :
        if alt   : hou.ui.curDesktop().findPaneTab("pt_sceneview_2").curViewport().setCamera(node_selected)
        if ctrl  : hou.ui.curDesktop().findPaneTab("pt_sceneview_1").curViewport().setCamera(node_selected)

    # --------------------------
    # exception: lights
    elif node_type == "light" :
        if alt   : hou.ui.curDesktop().findPaneTab("pt_sceneview_2").curViewport().setCamera(node_selected)
        if ctrl  : hou.ui.curDesktop().findPaneTab("pt_sceneview_1").curViewport().setCamera(node_selected)

    # --------------------------
    # exception: music
    elif node_type == "qmusic*" :
        # set sceneview_2
        # set network_2
        pass

    # --------------------------
    # exception: networks
    elif node_type in {"chopnet", "cop2net", "dopnet", "lopnet", "matnet", "ropnet", "shopnet", "topnet"} :
        # if alt   : network_set( "pt_network_1" , node_selected, "ENTER_THIS_NODE")
        if ctrl  : network_set( "pt_network_1" , node_selected, "ENTER_THIS_NODE")

    # --------------------------
    # gotoparm: geo NOT data
    elif node_type == "geo" and archetype != "archetype_job_geo_data" :
        # if alt   : network_set( "pt_network_1" , node_selected, "ENTER_THIS_NODE")
        if ctrl  : network_set( "pt_network_1" , node_selected, "ENTER_THIS_NODE")

    # --------------------------
    # gotoparm: geo DATA
    elif node_type == "geo" and archetype == "archetype_job_geo_data": 
        if alt  and not shift  : network_set( "pt_network_1" , node_selected, "shop_materialpath")
        # if alt  and shift      : network_set( "pt_network_1" , node_selected, "material")
        if ctrl and not shift  : network_set( "pt_network_1" , node_selected, "job_source")
        # if ctrl and shift      : network_set( "pt_network_1" , node_selected, "shop_materialpath")

    # --------------------------
    # gotoparm: Material SOP
    elif node_type == "material": 
        if alt  and not shift  : network_set( "pt_network_1" , node_selected, "shop_materialpath1")
        # if alt  and shift      : network_set( "pt_network_1" , node_selected, "material")
        # if ctrl and not shift  : network_set( "pt_network_1" , node_selected, "job_source")
        # if ctrl and shift      : network_set( "pt_network_1" , node_selected, "shop_materialpath")



    # --------------------------
    else:
        if alt   : network_set( "pt_network_1" , node_selected, "ENTER_FIRST_VALID")
        if ctrl  : network_set( "pt_network_2" , node_selected, "ENTER_FIRST_VALID")