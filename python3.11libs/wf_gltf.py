# import wf_gltf; import imp; imp.reload(wf_gltf); node = kwargs["node"] ; wf_gltf.create_obj_imports(node)


# wf::gltf_export_points::1.0
# wf // gltf / export points
# Q:/_gd/houdini_packages/wf_workflow/otls/wf_gltf_export_points.hdalc

import hou

# --------------------------------------------------------------------------------------------------------------------------------------------


def create_obj_imports (importer_node):

    node_points = importer_node.node("points")
    geo         = node_points.geometry()
    npoints     = geo.attribValue("npoints")
    name        = importer_node.parm("name").evalAsString()


    for index in range(npoints):
        # posx = 0;
        # posy = 3 * index;
        # print (import_name)

        import_name = name + "__" + (f'{index:04}')
        import_node = hou.node("/obj").createNode('geo',import_name)
        import_box  = import_node.createNode('box',"box_" + import_name)
        import_box.parm("scale").set("0.1")

        expression_path = node_points.path()
        expression_x = 'point("' + expression_path + '",opdigits("."),"P",0)'
        expression_y = 'point("' + expression_path + '",opdigits("."),"P",1)'
        expression_z = 'point("' + expression_path + '",opdigits("."),"P",2)'

        import_node.parm("tx").setExpression(expression_x)
        import_node.parm("ty").setExpression(expression_y)
        import_node.parm("tz").setExpression(expression_z)




        # ----------------------------------------------
        parm   = import_node.parm("tx")
        values = []
        for i in range(300):
            val = parm.evalAsFloatAtFrame(i)
            values.append(val)
        parm.deleteAllKeyframes()
        for i in range(300):
            if i == 1 or i == 150 or i == 299 :
                myKey = hou.Keyframe()
                myKey.setFrame(i)
                myKey.setValue(values[i])
                parm.setKeyframe(myKey)


        # ----------------------------------------------
        parm   = import_node.parm("ty")
        values = []
        for i in range(300):
            val = parm.evalAsFloatAtFrame(i)
            values.append(val)
        parm.deleteAllKeyframes()
        for i in range(300):
            if i == 1 or i == 150 or i == 299 :
                myKey = hou.Keyframe()
                myKey.setFrame(i)
                myKey.setValue(values[i])
                parm.setKeyframe(myKey)

        # ----------------------------------------------
        parm   = import_node.parm("tz")
        values = []
        for i in range(300):
            val = parm.evalAsFloatAtFrame(i)
            values.append(val)
        parm.deleteAllKeyframes()
        for i in range(300):
            if i == 1 or i == 150 or i == 299 :
                myKey = hou.Keyframe()
                myKey.setFrame(i)
                myKey.setValue(values[i])
                parm.setKeyframe(myKey)


        print("done: " + str(index))


    # # --------------------
    # # create object merge

    # name_merge = name
    # node_merge = importer_node.parent().createNode('object_merge',name_merge)
    # node_merge.parm("objpath1").set(objpath)
    # node_merge.parm("xformtype").set(1)
    # node_merge.moveToGoodPosition()

    # # --------------------
    # # create filecache
    # node_filecache = node_merge.createOutputNode("filecache", node_name = "cache_" + name)
    # node_filecache.parm("loadfromdisk").set(1)
    # node_filecache.parm("timedependent").set(0)
    # node_filecache.parm("enableversion").set(0)
    # node_filecache.parm("basename").set("$OS")
    # node_filecache.parm("basedir").set("$HIP/fbx_merge")
    # node_filecache.parm("cachedir").set('`chs("basedir")`')

    # # --------------------
    # # create null
    # node_null = node_filecache.createOutputNode("null", node_name = name)







