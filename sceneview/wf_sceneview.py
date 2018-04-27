import hou

def view_pane() :
    return hou.ui.curDesktop().paneTabOfType(hou.paneTabType.SceneViewer)


def view_sets() :
    pane = view_pane()
    settings = pane.curViewport().settings()
    # SceneObject  (visible when in top level "/obj")
    # DisplayModel (visible when inside /obj/...)
    set_scen = settings.displaySet(hou.displaySetType.SceneObject)
    set_disp = settings.displaySet(hou.displaySetType.DisplayModel)
    set_ghos = settings.displaySet(hou.displaySetType.GhostObject)
    return set_scen, set_disp, set_ghos


def frame_selected () :
    pane = view_pane()
    pane.curViewport().frameSelected()


def frame_all () :
    pane = view_pane()
    pane.curViewport().frameAll()


def toggle_points () :
    set_scen, set_disp, set_ghos = view_sets()
    # toggle
    set_disp.showPointMarkers(not set_disp.isShowingPointMarkers())
    set_scen.showPointMarkers(set_disp.isShowingPointMarkers())


def toggle_pointnumbers () :
    set_scen, set_disp, set_ghos = view_sets()
    # toggle
    set_disp.showPointNumbers(not set_disp.isShowingPointNumbers())
    set_scen.showPointNumbers(set_disp.isShowingPointNumbers())


def toggle_primnumbers () :
    set_scen, set_disp, set_ghos = view_sets()
    # toggle
    set_disp.showPrimNumbers(not set_disp.isShowingPrimNumbers())
    set_scen.showPrimNumbers(set_disp.isShowingPrimNumbers())    


def toggle_trails () :
    set_scen, set_disp, set_ghos = view_sets()
    # toggle
    set_disp.showPointTrails(not set_disp.isShowingPointTrails())
    set_scen.showPointTrails(set_disp.isShowingPointTrails())


def toggle_ghostother () :
    view_ghost = hou.getenv("view_ghost", "2")
    if view_ghost == "0": view_ghost = "2"
    else:            view_ghost = "0"
    hou.putenv("view_ghost", view_ghost)

    script = "vieweroption -a " + view_ghost + " %s`run('viewls -n')`"
    hou.hscript(script)
    

def toggle_objectselection () :
    panes = hou.ui.currentPaneTabs()
    for pane in panes:
        if pane.type().name() == 'SceneViewer':
            guide = hou.viewportGuide.ObjectSelection
            val = pane.curViewport().settings().guideEnabled(guide)
            pane.curViewport().settings().enableGuide(guide, not val)


def toggle_constructionplane () :
    pane = view_pane()
    cplane = pane.constructionPlane()
    cplane.setIsVisible(not cplane.isVisible()) 


def toggle_wireframe () :
    set_scen, set_disp, set_ghos = view_sets()
    view_wire = hou.getenv("view_wire", "0")

    # toggle
    if set_disp.shadedMode() != hou.glShadingType.WireGhost:
        set_disp.setShadedMode(hou.glShadingType.WireGhost)
        set_scen.setShadedMode(hou.glShadingType.WireGhost)
        set_ghos.setShadedMode(hou.glShadingType.WireGhost)

    elif set_disp.shadedMode() == hou.glShadingType.WireGhost and view_wire == "0":
        set_disp.setShadedMode(hou.glShadingType.Smooth)
        set_scen.setShadedMode(hou.glShadingType.Smooth)
        set_ghos.setShadedMode(hou.glShadingType.Smooth)

    elif set_disp.shadedMode() == hou.glShadingType.WireGhost and view_wire == "1":
        set_disp.setShadedMode(hou.glShadingType.SmoothWire)
        set_scen.setShadedMode(hou.glShadingType.SmoothWire)
        set_ghos.setShadedMode(hou.glShadingType.SmoothWire)


def toggle_wireover () :
    set_scen, set_disp, set_ghos = view_sets()
    view_wire = hou.getenv("view_wire", "0")
    if view_wire == "0": view_wire = "1"
    else:            view_wire = "0"
    hou.putenv("view_wire", view_wire)

    if set_disp.shadedMode() == hou.glShadingType.SmoothWire and view_wire == "0":
        set_disp.setShadedMode(hou.glShadingType.Smooth)
        set_scen.setShadedMode(hou.glShadingType.Smooth)
        set_ghos.setShadedMode(hou.glShadingType.Smooth)

    if set_disp.shadedMode() == hou.glShadingType.Smooth and view_wire == "1":
        set_disp.setShadedMode(hou.glShadingType.SmoothWire)
        set_scen.setShadedMode(hou.glShadingType.SmoothWire)
        set_ghos.setShadedMode(hou.glShadingType.SmoothWire)


def toggle_visualizer_point_vector (vis_attrib, r,g,b) :
    pane           = view_pane()
    cur_viewport   = pane.curViewport()
    existed        = False
    visualizer_list = hou.viewportVisualizers.visualizers(category=hou.viewportVisualizerCategory.Scene)
    for visualizer in visualizer_list :
        if visualizer.name() == vis_attrib :
            visualizer_obj = visualizer
            existed = True

    if not existed :
        vis_type       = hou.viewportVisualizers.types()[0] # vis_types:   0=vis_marker   1=vis_color   2=vis_generic   3=vis_volume   4=vis_tag   5=vis_constraints   6=vis_captureweight  
        vis_category   = hou.viewportVisualizerCategory.Scene
        visualizer_obj = hou.viewportVisualizers.createVisualizer(vis_type, vis_category)
        visualizer_obj.setName(vis_attrib)
        visualizer_obj.setLabel(vis_attrib)
        visualizer_obj.setParm("attrib",vis_attrib)
        visualizer_obj.setParm("style",4) # vis_styles:  0=text   4=vector
        visualizer_obj.setParm("class",1) # vis_classes: 0=vertex   1=point   2=prim
        visualizer_obj.setParm("lengthscale",0.2)
        visualizer_obj.setParm("markercolorr",r)
        visualizer_obj.setParm("markercolorg",g)
        visualizer_obj.setParm("markercolorb",b)

    active = visualizer_obj.isActive(viewport=cur_viewport)
    visualizer_obj.setIsActive(not active, viewport=cur_viewport)


def toggle_velocities () :
    vis_attrib = "v"
    r          = 0.5
    g          = 0.5
    b          = 1
    toggle_visualizer_point_vector (vis_attrib, r,g,b)


def toggle_ups () :
    vis_attrib = "up"
    r          = 0
    g          = 1
    b          = 0
    toggle_visualizer_point_vector (vis_attrib, r,g,b)


def toggle_normals () :
    vis_attrib = "N"
    r          = 0
    g          = 0
    b          = 1
    toggle_visualizer_point_vector (vis_attrib, r,g,b)
