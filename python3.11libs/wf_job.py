import hou
import imp
import wf_network_connection
import wf_job_archetype_data
import wf_job_archetype_karma
imp.reload(wf_job_archetype_karma)


def copypaste_ptg_folder( which_folder, insert_before_folder, node_src, node_dst ) :

    ptg_dst = node_dst.parmTemplateGroup()
    ptg_src = node_src.parmTemplateGroup()

    # remove target folder if already exists
    try:
        ptg_dst.remove(  ptg_dst.findFolder( which_folder )  )
        node_dst.setParmTemplateGroup(ptg_dst)
    except:
        pass
    
    # find and insert the folder, set PTG
    cargo    = ptg_src.findFolder( which_folder )
    location = ptg_dst.findFolder( insert_before_folder )
    # :) debug in 20.5.487 
    # print ("cargo: ")
    # print (cargo)
    # print ("location: ")
    # print (location)
    # ptg_dst.insertBefore( 0 , cargo )
    ptg_dst.insertBefore( location , cargo )
    node_dst.setParmTemplateGroup(ptg_dst)



def copypaste_all_contents( container_src, container_dst ) :

    # copy contents

    temp_path = hou.getenv("wf_path") + "/temp/__archetype.temp"
    items     = container_src.allItems()
    container_src.saveItemsToFile(items, temp_path)

    # paste contents
    container_dst.loadItemsFromFile(temp_path)



def jobify_obj () :
    obj_nodes = hou.selectedNodes()
    for obj_node in obj_nodes :

        if obj_node.type().name() == "geo" :
            jobify_node_ptg_and_contents( obj_node, "archetype_job_geo_network" )
            obj_node.setComment("`")


        if obj_node.type().name() == "cam" :

            # --------------------------------------
            # jobify cam 
            jobify_node_ptg_and_contents( obj_node, "archetype_job_cam" )
            obj_node.setComment("`")

            # --------------------------------------
            # create and jobify focus node

            # offsetx = 4
            # offsety = 0
            # color_focus  = hou.Color(0.4, 0.4, 0.4)

            # name
            # focus_name = obj_node.name() + "_focus"

            # create focus node
            # node_focus = obj_node.parent().createNode("geo", 
            #     node_name = focus_name,
            #     run_init_scripts = True, 
            #     load_contents = True, 
            #     exact_type_name = True)

            # posx = obj_node.position()[0] + offsetx
            # posy = obj_node.position()[1] + offsety
            # node_focus.setPosition( [posx,posy] )
            # node_focus.setColor( color_focus )
            # node_focus.setUserData("nodeshape", "diamond")
            # node_focus.setGenericFlag(hou.nodeFlag.Selectable,False)

            # jobify_node_ptg_and_contents( node_focus, "archetype_job_cam_focus" )

            # layout pin position
            # node_focus.setComment("`")

            # --------------------------------------
            # link the nodes
            # obj_node.parm("focus_node").set(   node_focus.path()   )
            # node_focus.parm("job_camera").set(   obj_node.path()   )




def jobify_node_ptg_and_contents( node_target, archetype_name ) :

    # --------------------------------------------------------------------------------------
    # settings
    color_node_grey = hou.Color(0.8, 0.8, 0.8)
    color_node_dark = hou.Color(0.306, 0.306, 0.306)
    
    # --------------------------------------------------------------------------------------
    # create the archetype node

    node_archetype_hda = node_target.parent().createNode(archetype_name)
    node_archetype     = node_archetype_hda.node(archetype_name)

    node_target.setUserData("archetype", archetype_name)


    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------
    # ui and contents


    if archetype_name == "archetype_job_karma" :

        # group initial parms
        PTG_initial = node_target.parmTemplateGroup()
        PTG_new     = hou.ParmTemplateGroup()
        entries     = PTG_initial.entries()

        FOLDER_init = hou.FolderParmTemplate("folder", "Initial Parms")
        FOLDER_init.setFolderType(hou.folderType.Tabs)

        for entry in entries :
            FOLDER_init.addParmTemplate(entry)
        
        PTG_new.append(FOLDER_init)
        node_target.setParmTemplateGroup(PTG_new)


        # copy parms
        which_folder         = "JOB"
        insert_before_folder = "Initial Parms"
        node_src             = node_archetype
        node_dst             = node_target
        copypaste_ptg_folder( which_folder, insert_before_folder, node_src, node_dst )

        # copy contents
        container_src = node_archetype
        container_dst = node_target
        copypaste_all_contents( container_src, container_dst )

        # finetune
        node_target.parm("rendergallerysource").set("$HIP/galleries/rendergallery.db")


    # --------------------------------------------------------------------------------------
    else :
        # copy parms
        which_folder         = "JOB"
        insert_before_folder = "Transform"
        node_src             = node_archetype
        node_dst             = node_target
        copypaste_ptg_folder( which_folder, insert_before_folder, node_src, node_dst )
    # --------------------------------------------------------------------------------------


    if archetype_name == "archetype_job_cam" :

        # copy contents
        # container_src = node_archetype
        # container_dst = node_target
        # copypaste_all_contents( container_src, container_dst )

        # finetune
        node_target.setColor(color_node_grey)
        node_target.parm("use_dcolor").set(1)
        node_target.parmTuple("dcolor").set((1.0, 1.0, 0.0))
        # node_target.parm("picking").set(0)



    if archetype_name == "archetype_job_geo_data" :

        # copy contents
        container_src = node_archetype
        container_dst = node_target
        copypaste_all_contents( container_src, container_dst )
        
        # finetune
        node_target.setUserData("nodeshape", "chevron_down")
        node_target.parmTuple("t").setAutoscope((0,0,0))
        node_target.parmTuple("r").setAutoscope((0,0,0))
        node_target.parmTuple("s").setAutoscope((0,0,0))
        # node_target.parm("shop_materialpath").set("matnet/MX")
        node_target.setUserData("descriptiveparm","job_range_descriptiveparm")
        node_target.parm("picking").set(0)
        wf_job_archetype_data.job_data_update_range_descriptiveparm(node_target)


    if archetype_name == "archetype_job_cam_focus" :

        # copy contents
        container_src = node_archetype
        container_dst = node_target
        copypaste_all_contents( container_src, container_dst )



    if archetype_name == "archetype_job_geo_network" :

        # copy contents
        container_src = node_archetype
        container_dst = node_target
        copypaste_all_contents( container_src, container_dst )

        # copy parms
        # finetune
        node_target.setUserData("nodeshape", "tabbed_left")
        node_target.parmTuple("t").setAutoscope((0,0,0))
        node_target.parmTuple("r").setAutoscope((0,0,0))
        node_target.parmTuple("s").setAutoscope((0,0,0))
        node_target.setColor(color_node_dark)
        node_target.setUserData("descriptiveparm","job_range_descriptiveparm")
        node_target.parm("picking").set(0)
        wf_job_archetype_data.job_data_update_range_descriptiveparm(node_target)



    if archetype_name == "archetype_job_subnet" :
        # copy parms
        # finetune
        pass

    # --------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------

    # delete the archetype
    node_archetype_hda.destroy()




def create_job_karma_from_geo(node_geo) :

    # define
    offsetx = 0
    offsety = 1.3
    color_lop  = hou.Color(1.0, 0.725, 0.0)

    # name
    lopnet_name = "karma_" + node_geo.name()

    # create lopnet
    node_lopnet = node_geo.parent().createNode("lopnet", 
        node_name = lopnet_name,
        run_init_scripts = True, 
        load_contents = True, 
        exact_type_name = True)

    # layout pin position
    node_lopnet.setComment("`")

    # get pos
    posx = node_geo.position()[0] + offsetx
    posy = node_geo.position()[1] + offsety
    node_lopnet.setPosition( [posx,posy] )
    node_lopnet.setColor( color_lop )

    # jobify lopnet
    jobify_node_ptg_and_contents( node_lopnet, "archetype_job_karma" )

    # link parms
    node_lopnet.parm("job_rangex").set(    node_geo.parm("job_rangex")    )
    node_lopnet.parm("job_rangey").set(    node_geo.parm("job_rangey")    )
    node_lopnet.parm("job_camera").set(    node_geo.parm("job_camera")    )
    node_lopnet.parm("job_camera").setAutoscope(False)

    # filename
    node_lopnet.parm("file").set(node_geo.name())


    # focus DOF parameters
    expression_distance = 'detail("' + node_geo.path() + '/DOF","job_distance",0)'
    expression_fstop    = 'detail("' + node_geo.path() + '/DOF","job_fstop",0)'
    node_lopnet.node("focus").parm("focusDistance").setExpression(  expression_distance  )
    node_lopnet.node("focus").parm("fStop").setExpression(          expression_fstop     )




def create_job_import(node_null) :

    parent     = node_null.parent()
    color_red  = hou.Color(0.8, 0.016, 0.016)

    # ----------------------------------------------------------------------------------------------------
    # KARMA
    wf_job_archetype_karma.create_sop_import(node_null)
    

    # ----------------------------------------------------------------------------------------------------
    # OBJ

    # color the Null
    node_null.setColor(color_red)

    # create node_nulls
    last_descendant = wf_network_connection.get_last_descendant(parent)
    geo_data = last_descendant.createOutputNode("geo", 
        node_name = node_null.name(),
        run_init_scripts = True, 
        load_contents = True, 
        exact_type_name = True)

    # jobify geo
    jobify_node_ptg_and_contents( geo_data, "archetype_job_geo_data" )

    # link to the null
    geo_data.parm("job_source").set(node_null.path())

    # range from parent
    geo_data.parm("job_rangex").set(node_null.parent().parm("job_rangex").eval())
    geo_data.parm("job_rangey").set(node_null.parent().parm("job_rangey").eval())
    wf_job_archetype_data.job_data_update_range_descriptiveparm(geo_data)

    # cam from parent
    geo_data.parm("job_camera").set(node_null.parent().parm("job_camera").eval())


    # create GL_ROP
    create_rop_gl(geo_data)


        


def create_rop_gl ( obj_node ) :

    obj_name = obj_node.name()

    # create ropnet
    manager_GL = hou.node("/obj/rop_GL")
    if not manager_GL :
        manager_GL = hou.node("/obj").createNode("ropnet", "rop_GL") 
        manager_GL.setComment("`")

    # create ROP
    gl_node = manager_GL.createNode( "opengl", obj_name )
    gl_node.setPosition(obj_node.position())
    gl_node.setComment("`")

    #------------------------------------------------------------

    # strict range
    gl_node.parm("trange").set(2)

    # range start, end
    gl_node.parm("f1").setExpression('ch("/obj/$OS/job_rangex")')
    gl_node.parm("f2").setExpression('ch("/obj/$OS/job_rangey")')

    # camera
    gl_node.parm("camera").set('`chs("/obj/$OS/job_camera")`')

    # candidate objects
    gl_node.parm("vobjects").set("")

    # force objects
    gl_node.parm("forceobjects").set("/obj/$OS")

    # candidate lights
    gl_node.parm("alights").set("")

    # resolution preview
    gl_node.parm("res1").setExpression('ch(chs("camera") + "/res_previewx")')
    gl_node.parm("res2").setExpression('ch(chs("camera") + "/res_previewy")')

    # gamma
    gl_node.parm("gamma").set(2.2)
    gl_node.parm("shadows").set(0)
    gl_node.parm("hqlighting").set(0)

    # max sprite resolution
    gl_node.parm("spritetexmaxresx").set(2048)
    gl_node.parm("spritetexmaxresy").set(2048)

    # antialias
    gl_node.parm("aamode").set(4)
    
    # set picture name
    path = "$HIP/__data.render/$OS/${OS}_$F4.png"
    gl_node.parm("picture").set(path)

