import hou
import wf_selection
reload(wf_selection)



def view_sets() :
    pane = wf_selection.pane_linkGroup( hou.paneTabType.SceneViewer )
    settings = pane.curViewport().settings()
    # SceneObject  (visible when in top level "/obj")
    # DisplayModel (visible when inside /obj/...)
    set_scen = settings.displaySet(hou.displaySetType.SceneObject)
    set_disp = settings.displaySet(hou.displaySetType.DisplayModel)
    set_ghos = settings.displaySet(hou.displaySetType.GhostObject)
    return set_scen, set_disp, set_ghos


def frame_selected () :
    pane = wf_selection.pane_linkGroup( hou.paneTabType.SceneViewer )
    pane.curViewport().frameSelected()


def frame_all () :
    pane = wf_selection.pane_linkGroup( hou.paneTabType.SceneViewer )
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

    #script = "vieweroption -a " + view_ghost + " %s`run('viewls -n')`"
    script = "vieweroption -a " + view_ghost + " `run('viewls -n')`"
    hou.hscript(script)


def toggle_maskoverlay () :
    view_maskoverlay = hou.getenv("view_maskoverlay", "1.0")
    if view_maskoverlay == "1.0": view_maskoverlay = "0.4"
    else:            view_maskoverlay = "1.0"
    hou.putenv("view_maskoverlay", view_maskoverlay)

    script = "viewmaskoverlay -o " + view_maskoverlay + " *"
    hou.hscript(script)  


def toggle_objkinoverride () :
    view_objkinoverride = hou.getenv("view_objkinoverride", "none")
    if view_objkinoverride == "none": view_objkinoverride = "capture"
    else:            view_objkinoverride = "none"
    hou.putenv("view_objkinoverride", view_objkinoverride)

    script = "objkinoverride " + view_objkinoverride
    hou.hscript(script)

    paneTabs = hou.ui.currentPaneTabs()
    for paneTab in paneTabs:
        if paneTab.type().name() == 'SceneViewer':
            paneTab.curViewport().draw()


def toggle_objectselection () :
    paneTabs = hou.ui.currentPaneTabs()
    for paneTabs in paneTabss:
        if paneTabs.type().name() == 'SceneViewer':
            guide = hou.viewportGuide.ObjectSelection
            val = paneTabs.curViewport().settings().guideEnabled(guide)
            paneTabs.curViewport().settings().enableGuide(guide, not val)
            # just a test:
            # pane.curViewport().settings().setVisibleObjects("name*")


def toggle_constructionplane () :
    pane = wf_selection.pane_linkGroup( hou.paneTabType.SceneViewer )
    cplane = pane.constructionPlane()
    cplane.setIsVisible(not cplane.isVisible()) 


def toggle_grid () :
    pane = wf_selection.pane_linkGroup( hou.paneTabType.SceneViewer )
    settings = pane.curViewport().settings()
    settings.setDisplayOrthoGrid(not settings.displayOrthoGrid())

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
    pane           = wf_selection.pane_linkGroup( hou.paneTabType.SceneViewer )
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
    message = "visualise " + str(vis_attrib) + " : " + str(not active)
    hou.ui.setStatusMessage(message)
    # hou.ui.triggerUpdate()


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
