import hou


def promote_to_HDA () :
    selectedNodes  = hou.selectedNodes()
    hdanode        = selectedNodes[0].parent()
    hda_definition = hdanode.type().definition()


    ptg = hda_definition.parmTemplateGroup()


    # folder name
    new_folder_name = ()
    new_folder_name = hou.ui.readInput(
        message = "new_folder_name:",
        initial_contents = "l_arm")
    
    new_folder_name = new_folder_name[1]
    new_folder      = hou.FolderParmTemplate(new_folder_name, new_folder_name)


    ##################
    ## create parms ##

    for selectedNode in selectedNodes :
        parm_list = promote_to_HDA_parm_list(selectedNode)
        for parm_name in parm_list :
            # new template
            new_template = selectedNode.parmTuple(parm_name).parmTemplate()
            new_name     = selectedNode.name() + "_" + parm_name

            new_template.setName(new_name)
            new_template.setLabel(new_name)
            new_folder.addParmTemplate(new_template)

    ptg.append(new_folder)
    hda_definition.setParmTemplateGroup(ptg)

    #####################
    ## reference parms ##

    for selectedNode in selectedNodes :
        parm_list = promote_to_HDA_parm_list(selectedNode)
        for parm_name in parm_list :
            parm_node     = selectedNode.parmTuple(parm_name)
            parm_name_hda = selectedNode.name() + "_" + parm_name
            parm_hda      = selectedNode.parent().parmTuple(parm_name_hda)
            parm_hda.set(parm_node.eval())
            parm_node.set(parm_hda)

    # hda_definition.save(hda_definition.libraryFilePath())



def promote_to_HDA_parm_list (node) :
    if node.type().name() == "null" :
        parm_list = ["t", "r"]
    if node.type().name() == "bone" :
        parm_list = ["r", "length"]

    return parm_list


def yoga_save_pose() :
    # parm_store.deleteAllKeyframes()
    node_edit  = hou.node("/obj/edit")
    node_store = hou.node("/obj/store")
    parms      = node_edit.parms()

    for parm in parms :
        name       = parm.name()
        parm_store = node_store.parm(name)

        if len(parm_store.keyframes()) > 0 :
            value      = parm.eval()
            key        = hou.Keyframe(value)
            parm_store.setKeyframe(key)





def yoga_load_pose() :
    node_edit  = hou.node("/obj/edit")
    node_store = hou.node("/obj/store")
    parms      = node_store.parms()

    for parm in parms :
        if len(parm.keyframes()) > 0 :
            name       = parm.name()
            value      = parm.eval()
            parm_edit  = node_edit.parm(name)
            parm_edit.set(value)