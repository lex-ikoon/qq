import hou
import imp
import nodesearch
import wf_network_connection
import wf_job
import wf_network_utils


def create_sop_import(node):
  
    # -----------------------
    # define
    offsetx = 4
    offsety = 0


    # -----------------------
    # find the LOP karma
    # create it if needed
    node_lop = hou.node("/obj/karma_" + node.parent().name())
    if node_lop == None :
        wf_job.create_job_karma_from_geo(   node.parent()   )
    node_lop = hou.node("/obj/karma_" + node.parent().name())
    node_GEO = node_lop.node("GEO")

    # -----------------------
    # position
    root                = node_lop
    matcher             = nodesearch.NodeType( "sopimport", hou.lopNodeTypeCategory() )
    existing_sopimports = matcher.nodes( root, recursive=True )

    if len(existing_sopimports) == 0:
        posx = node_GEO.position()[0] + 0
        posy = node_GEO.position()[1] + 6

    else:
        posx = -10000
        posy = -10000
        for existing_sopimport in existing_sopimports:
            posx = max(posx,existing_sopimport.position()[0])
            posy = max(posy,existing_sopimport.position()[1])
        posx = posx + offsetx
        posy = posy + offsety


    # -----------------------
    # create SOP Import
    node_sopimport = node_lop.createNode( "sopimport", node.name() )
    node_sopimport.setPosition( [posx,posy] )
    node_sopimport.setComment("`")
    node_sopimport.parm("soppath").set(node.path())
    node_sopimport.parm("bindmaterials").set("createbind")
    node_sopimport.parm("pathprefix").set("geo/$OS")
    node_sopimport.parm("enable_savepath").set(1)
    node_sopimport.parm("savepath").set('$JOB/_usd/`chs("../file")`_${OS}_savepath.usd')

    # -----------------------
    # create Filecache
    node_filecache = node_sopimport.createOutputNode("filecache", 
        node_name = "cache_" + node.name(),
        run_init_scripts = True, 
        load_contents = True, 
        exact_type_name = True)
    node_filecache.parm("loadfromdisk").set(1)
    node_filecache.parm("filemethod").set(1)
    node_filecache.parm("file").set('$JOB/_usd/`chs("../file")`_${OS}_cache.usd')
    node_filecache.parm("trange").set(1)
    node_filecache.parm("f1").set(node_lop.parm("job_rangex"))
    node_filecache.parm("f2").set(node_lop.parm("job_rangey"))
    node_filecache.bypass(True)

    # -----------------------
    # create Fetch
    node_fetch = wf_network_utils.create_object_merge(node_filecache,True)
    node_GEO.setInput(len(node_GEO.inputs()), node_fetch)



def check_usdmaterialpath(node):
    geo = node.geometry()

    try:
        usdmaterialpath = geo.findPointAttrib("usdmaterialpath")
        if usdmaterialpath != None:
            point = geo.iterPoints()[0]
            return (   point.attribValue(usdmaterialpath)   )
    except:
        pass

    try:
        usdmaterialpath = geo.findPrimAttrib("usdmaterialpath")
        if usdmaterialpath != None:
            prim = geo.iterPrims()[0]
            return (   prim.attribValue(usdmaterialpath)   )
    except:
        pass

    return None



def check_material(node):

    # -----------------------
    # SOP nodes
    if node.type().category() == hou.sopNodeTypeCategory() :

        # -----------------------
        # try this node
        material = check_usdmaterialpath(node)
        if material != None :
            return material

        # -----------------------
        # try last_descendant 
        last_descendant = wf_network_connection.get_last_descendant(node)
        material        = check_usdmaterialpath(last_descendant)
        if material != None :
            return material


    # -----------------------
    # LOP nodes
    if node.type().category() == hou.lopNodeTypeCategory() :

        # -----------------------
        # sopimport
        if node.type().name() == "sopimport" :
            referenced_node = node.parm("soppath").evalAsNode()
            material        = check_usdmaterialpath(referenced_node)
            if material != None :
                return material

        # -----------------------
        # filecache
        if node.type().name() == "filecache" :
            sopimport_node  = node.inputs()[0]
            referenced_node = sopimport_node.parm("soppath").evalAsNode()
            material        = check_usdmaterialpath(referenced_node)
            if material != None :
                return material

        # -----------------------
        # fetch
        if node.type().name() == "fetch" :
            filecache_node  = node.parm("loppath").evalAsNode()
            sopimport_node  = filecache_node.inputs()[0]
            referenced_node = sopimport_node.parm("soppath").evalAsNode()
            material        = check_usdmaterialpath(referenced_node)
            if material != None :
                return material



def find_material(node):
    print(  check_material(node)  )

    # OPEN BOTTOM 