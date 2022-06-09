import hou
import imp
import wf_network_connection
import wf_job_archetype_data
# imp.reload(wf_network_connection)

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
    ptg_dst.insertBefore( location , cargo )
    node_dst.setParmTemplateGroup(ptg_dst)



def copypaste_all_contents( container_src, container_dst ) :

    # copy contents

    temp_path = hou.getenv("wf_path") + "/temp/__archetype.temp"
    items     = container_src.allItems()
    container_src.saveItemsToFile(items, temp_path)

    # paste contents
    container_dst.loadItemsFromFile(temp_path)



def jobify () :
    obj_nodes = hou.selectedNodes()
    for obj_node in obj_nodes :

        if obj_node.type().name() == "geo" :
            jobify_node_ptg_and_contents( obj_node, "archetype_job_geo_network" )

        if obj_node.type().name() == "cam" :
            jobify_node_ptg_and_contents( obj_node, "archetype_job_cam" )





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


    if archetype_name == "archetype_job_lopnet" :

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
        # set camera
        # set render location
        






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
        node_target.parm("shop_materialpath").set("matnet/MX")
        node_target.setUserData("descriptiveparm","job_range_descriptiveparm")
        node_target.parm("picking").set(0)
        wf_job_archetype_data.job_data_update_range_descriptiveparm(node_target)

        

    if archetype_name == "archetype_job_geo_network" :
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


def create_job_lopnet_from_geo(node_geos) :

    # define offset
    offsetx = 3
    offsety = 0

    for node_geo in node_geos :
        # name
        lopnet_name = "lop_" + node_geo.name()

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

        # jobify lopnet
        jobify_node_ptg_and_contents( node_lopnet, "archetype_job_lopnet" )




def create_job_geo_data_from_nulls() :

    node_nulls = hou.selectedNodes()
    parent     = node_nulls[0].parent()
    color_red  = hou.Color(0.8, 0.016, 0.016)

    for node_null in node_nulls :

        #color the Null
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

        # create GL_ROP
        create_rop_gl(geo_data)

        # create RS_ROP


        


def create_job_geo_data_from_geos() :
    pass



def create_rop_gl ( obj_node ) :

    obj_name = obj_node.name()

    # create ropnet
    manager_GL = hou.node("/obj/rop_GL")
    if not manager_GL :
        manager_GL = hou.node("/obj").createNode("ropnet", "rop_GL") 

    # create ROP
    gl_node = manager_GL.createNode( "opengl", obj_name )
    gl_node.setPosition(obj_node.position())

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
    path = "$JOB/__data.render/$OS/${OS}_$F4.png"
    gl_node.parm("picture").set(path)



def create_rop_rs (obj_node) :

    obj_name = obj_node.name()

    # create ropnet
    manager_RS = hou.node("/obj/rop_RS")
    if not manager_RS :
        manager_RS = hou.node("/obj").createNode("ropnet", "rop_RS") 

    # create ROP
    rs_node = manager_RS.createNode( "Redshift_ROP", obj_name )
    rs_node.setPosition(obj_node.position())

    #------------------------------------------------------------

    # strict range
    rs_node.parm("trange").set(2)

    # range start, end
    rs_node.parm("f1").deleteAllKeyframes()
    rs_node.parm("f2").deleteAllKeyframes()
    rs_node.parm("f1").setExpression('ch("/obj/$OS/job_rangex")')
    rs_node.parm("f2").setExpression('ch("/obj/$OS/job_rangey")')

    # camera
    rs_node.parm("RS_renderCamera").set('`chs("/obj/$OS/job_camera")`')

    # candidate objects
    rs_node.parm("RS_objects_candidate").set("")

    # force objects
    rs_node.parm("RS_objects_force").set("/obj/$OS")

    # candidate lights
    rs_node.parm("RS_lights_candidate").set("")

    # resolution preview
    rs_node.parm("RS_overrideResScale").set(7)
    rs_node.parm("RS_overrideRes1").setExpression('ch(chs("camera") + "/res_previewx")')
    rs_node.parm("RS_overrideRes2").setExpression('ch(chs("camera") + "/res_previewy")')

    # redshift parms
    rs_node.parm("RS_nonBlockingRendering").set(0)
    rs_node.parm("RS_renderToMPlay").set(0)
    rs_node.parm("RS_outputFileFormat").set(3) # .png
    
    # set picture name
    path = "$JOB/__data.render/$OS/${OS}_$F4.png"
    rs_node.parm("RS_outputFileNamePrefix").set(path)
