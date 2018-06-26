import re
import hou
import wf_network_ui
import wf_selection
reload(wf_selection)

def digits(name) :
    after_underscore = 1 + name.rindex("_")
    digits_string = name[after_underscore:]
    return digits_string


def midi_button_rename (node, parm) :
    index          = digits(parm)

    # parm and snippet
    parm_attribute = node.parm("midi_attribute_"+index)
    attribute_old  = str(    parm_attribute.parmTemplate().defaultValue()[0]    )
    attribute_new  = parm_attribute.eval()
    snippet_old    = node.parm("snippet").unexpandedString()
    snippet_new    = snippet_old.replace('"'+attribute_old+'"','"'+attribute_new+'"')

    # set
    node.parm("snippet").set(snippet_new)
    wf_network_ui.parm_update (node, "string", "midi_attribute_" + index, attribute_new)

    # mixer node rename
    path_mix = "/obj/midi/mixer/"
    node_array = hou.node(path_mix + attribute_old )
    try:
        node_array.setName(attribute_new,True)
    except:
        hou.ui.displayMessage("Renaming of Node failed. Probably does not exist?") 



def midi_button_select (node, parm) :
    index      = digits(parm)
    path_mix   = "/obj/midi/mixer/"
    array_name = node.parm("midi_attribute_"+index).eval()

    if hou.node("/obj/midi/mixer/" + array_name ) :
        node_array = hou.node(path_mix + array_name )
        for pane in hou.ui.curDesktop().paneTabs() :
            if pane.type() == hou.paneTabType.NetworkEditor :
                if pane.linkGroup() == hou.paneLinkType.Group3 :
                    pane.setCurrentNode(node_array)
    else :
        hou.ui.displayMessage("Node doesn't exist") 



def midi_button_create (node, parm) :
    index      = digits(parm)
    array_name = node.parm("midi_attribute_"+index).eval()
    menu_parm  = node.parm("midi_menu_"+index)
    array_type = menu_parm.menuItems()[menu_parm.eval()]
    path_mix   = "/obj/midi/mixer/"

    if hou.node("/obj/midi/mixer/" + array_name ) :
        hou.ui.displayMessage("Node already exists") 
    else:
        if array_type == "(type)" :
            hou.ui.displayMessage("Select array type") 
        else:
            new_node = hou.node(path_mix).createNode(array_type, array_name)
            new_node.moveToGoodPosition()
            midi_button_select(node,parm)



def midi_button_filter (node, parm) :
    index          = digits(parm)
    path_mix       = "/obj/midi/mixer/"
    parm_attribute = node.parm("midi_attribute_"+index).eval()
    node_array     = hou.node(path_mix + parm_attribute )
    node_filter    = hou.node(path_mix + "midi_filter" )

    # disconnect
    for connection in node_array.outputConnections() :
        output_node = connection.outputNode()
        index = connection.inputIndex()
        output_node.setInput(index, None)

    # remove empty connections
    inputs = node_filter.inputs()
    for x in xrange(0,len(node_filter.inputs())) :
        node_filter.setInput(x, None)

    # recreate without None
    for i in inputs :
        if not i == None :
            node_filter.setNextInput(i)
    node_filter.setNextInput(node_array)

    # focus
    for pane in hou.ui.curDesktop().paneTabs() :
        if pane.type() == hou.paneTabType.NetworkEditor :
            if pane.linkGroup() == hou.paneLinkType.Group3 :
                pane.setCurrentNode(node_filter)



def parm_update_join (node, name, join) :
    ptg_update = node.parmTemplateGroup()
    parmedit = ptg_update.find( name )
    parmedit.setJoinWithNext( join )
    ptg_update.replace( name, parmedit )
    node.setParmTemplateGroup( ptg_update )



def parm_create_button (node, name, label, join, callback) :

    new_template = hou.ButtonParmTemplate (name, label, join_with_next=join, script_callback=callback, script_callback_language=hou.scriptLanguage.Python)

    try :
        ptg = node.parmTemplateGroup()
        ptg.addParmTemplate(new_template)
        node.setParmTemplateGroup( ptg )
        existed = 0
    except:
        existed = 1


def parm_create_menu (node, name, label, join, callback) :
    pass
    menu_labels = ['(type)','Beat','Area','Connect','Mask','Sign']
    menu_items = ['(type)','midi_beat','midi_area','midi_connect','midi_mask','midi_sign']
    new_template = hou.MenuParmTemplate (name, label, menu_items, menu_labels, join_with_next=True, script_callback=None, script_callback_language=hou.scriptLanguage.Python)

    try :
        ptg = node.parmTemplateGroup()
        #new_template.setMenuItems(menu_items)
        #new_template.setMenuLabels(menu_items)
        ptg.addParmTemplate(new_template)
        node.setParmTemplateGroup( ptg )
        existed = 0
    except:
        existed = 1




def check_midi(node, line, linenum) :
    attrib_names = re.findall('coord_midi\(\"(\w+)\"', line)
    index = str(linenum)

    if attrib_names :
        # string
        attrib_default            = str(attrib_names[0])
        wf_network_ui.parm_create (node, "string",    "midi_attribute_" + index, "midi_attribute")
        node.parm                 (   "midi_attribute_" + index   ).set( attrib_default )
        wf_network_ui.parm_update (node, "string", "midi_attribute_" + index, attrib_default)

        # menu and buttons
        callback_rename = 'import wf_midi ; reload(wf_midi) ; node = kwargs["node"] ; parm = kwargs["parm"].name() ; wf_midi.midi_button_rename(node,parm)'
        callback_menu   = 'import wf_midi ; reload(wf_midi) ; node = kwargs["node"] ; parm = kwargs["parm"].name() ; wf_midi.midi_button_menu  (node,parm)'
        callback_create = 'import wf_midi ; reload(wf_midi) ; node = kwargs["node"] ; parm = kwargs["parm"].name() ; wf_midi.midi_button_create(node,parm)'
        callback_select = 'import wf_midi ; reload(wf_midi) ; node = kwargs["node"] ; parm = kwargs["parm"].name() ; wf_midi.midi_button_select(node,parm)'
        callback_filter = 'import wf_midi ; reload(wf_midi) ; node = kwargs["node"] ; parm = kwargs["parm"].name() ; wf_midi.midi_button_filter(node,parm)'

        parm_create_button(node, "midi_rename_"+index, "rename", False, callback_rename)
        parm_create_menu  (node, "midi_menu_"  +index, "node",    True, callback_menu)
        parm_create_button(node, "midi_create_"+index, "create", True,  callback_create)
        parm_create_button(node, "midi_select_"+index, "select", True,  callback_select)
        parm_create_button(node, "midi_filter_"+index, "filter", False, callback_filter)

        # separator
        wf_network_ui.parm_create (node, "separator", "midi_separator_" + index, "midi_separator" + index)

        # update join with next
        parm_update_join (node, "midi_attribute_"+index, True)
        parm_update_join (node, "midi_menu_"+index, True)
        parm_update_join (node, "midi_create_"+index, True)
        parm_update_join (node, "midi_select_"+index, True)
    pass
