import hou
import math, numpy
import bisect
import wf_selection #span edit

_node_music    = hou.node("/obj/music")
_node_tracks   = hou.node("/obj/music/tracks")
_node_spectrum = hou.node("/obj/music/spectrum")
_node_vex      = "vex"
_node_arrays   = "vis_arrays"
_node_clones   = "vis_clones"

_track_lines_first     = "line_first_"
_track_lines_last      = "line_last_"
_track_lines_iteration = "line_iteration_"

# sec   4.67 = 140.1 = frame 141 (h 138.5) ~ 0.9821
# sec  27.34 = 820.2 = frame 821 (h 811)   ~ 0.9878
# sec  46.00 = 1380  = frame 1381 (h 1364) ~ 0.9877
# sec  86.00 = 2580  = frame 2581 (h 2550) ~ 0.9879
# sec 124.90 = 3747  = frame 3748 (h 3704) ~ 0.9882

#####################
#####################


def panes_music() :
    d          = hou.ui.curDesktop()
    pane_net   = d.findPaneTab("music_net")
    pane_parm  = d.findPaneTab("music_parm")
    pane_scene = d.findPaneTab("pt_sceneview_2")
    return pane_net, pane_parm, pane_scene


def pane_scene_selectpositions(number) :
    pane_net, pane_parm, pane_scene = panes_music()
    positions = pane_scene.selectPositions(prompt='Click to specify a position',
        number_of_positions=number,
        connect_positions=True,
        show_coordinates=True,
        bbox=hou.BoundingBox(),
        position_type=hou.positionType.WorldSpace,
        icon=None,
        label=None)
    return positions


def panes_music_activate(toggle) :
    pane_net, pane_parm, pane_scene = panes_music()
    pane_scene_settings = pane_scene.curViewport().settings()

    if toggle == True:
        pane_scene_settings.setLighting(hou.viewportLighting.Headlight)
        pane_scene.setLinkGroup(hou.paneLinkType.Group3)
        camera_set_ortho(True)

    else:
        pane_scene_settings.setLighting(hou.viewportLighting.Normal)
        pane_scene.setLinkGroup(hou.paneLinkType.Group1)
        camera_set_ortho(False)
    


#####################
#####################


def music_parm(name) :
    parm = _node_music.parm(name)
    return parm


def tracks_select() :
    pane_net, pane_parm, pane_scene = panes_music()
    node = _node_tracks;
    pane_net.setCurrentNode(node, True)
    pane_parm.setCurrentNode(node, True)


def tracks_activate(dir_active) :
    maximum    = -1 + len(_node_tracks.children())
    old_active = music_parm("track_active").eval()
    new_active = sorted((0, old_active + dir_active, maximum))[1]
    music_parm("track_active").set( new_active )

    # reposition the nodes
    music_redraw()

    # panes
    pane_net, pane_parm, pane_scene = panes_music()

    # pwd only for the first time
    if pane_parm.pwd() != _node_tracks :
        pane_parm.setPwd(_node_tracks)

    # select but don't highlight
    node = track_item_active_node();
    node.setSelected(False, clear_all_selected=True)
    node.setCurrent(False, clear_all_selected=True)
    pane_parm.setCurrentNode(node, False)

    # set to Group3
    panes_music_activate(True)

    ####### update visualizers switches
    tracks_visualizers_switch()


def tracks_visualizers_switch() :
    tracks = list(  _node_tracks.children()  )

    # hide all
    for track in tracks :
        switch_vis = track.node("notes/visualizers/switch")
        switch_tmk = track.node("notes/tmark/switch")
        switch_vis.parm("input").set(0)
        switch_tmk.parm("input").set(0)

    # show only the active
    track_active = track_item_active_node()
    switch_vis   = track_active.node("notes/visualizers/switch")
    switch_tmk   = track_active.node("notes/tmark/switch")
    switch_vis.parm("input").set(1)
    switch_tmk.parm("input").set(1)


def tracks_visualize_toggle(item) :
    # used by hotkeys
    parm = music_parm("visualize_" + item)
    parm.set(not parm.eval())


#####################
#####################

#
#                        def track_item_create() :
#                            dialog = hou.ui.readInput(
#                                message ="track_item_create()\n\ntrack name:", 
#                                severity=hou.severityType.Message, 
#                                close_choice=2,
#                                buttons=("dots", "lines", "cancel"))
#                        
#                            if dialog[0] == 0 :
#                                node_type_name = "music_track_dots"
#                            if dialog[0] == 1 :
#                                node_type_name = "music_track_lines"
#                            if dialog[0] == 2 :
#                                return
#
#                            # name
#                            node_name = dialog[1]
#                            if not node_name: node_name = "default_name"
#                            new_track = _node_tracks.createNode(node_type_name, node_name)
#                            new_track.moveToGoodPosition()
#
#                            # move the span down
#                            new_track.node("span").parm("ty").set(-3)
#
#                            # flag Selectable false
#                            new_track.setGenericFlag(hou.nodeFlag.Selectable,False)
#
#                            # clean the inside
#                            notes_delete_all(new_track)
#                            # if node_type_name == "music_track_dots" :
#                            span_scope_camera(new_track)
#
#                                
#                            return new_track
#

def track_item_type(node) :
    #('', 'ikoon', 'music_track_dots', '1.0')
    if node.type().nameComponents()[2] == "music_track_dots" :
        track_type = "music_track_dots"
    if node.type().nameComponents()[2] == "music_track_lines" :
        track_type = "music_track_lines"
    return track_type



def track_item_parm(name) :
    track = track_item_active_node()
    parm  = track.parm(name)
    return parm


def track_item_active_node() :
    tracks = list(  _node_tracks.children()  )
    positions = []
    for t in tracks :
        positions.append(t.position()[1])
    keydict = dict(zip(tracks, positions))
    tracks.sort(key=keydict.get)

    # check if music_parm greater than len(tracks)
    track_active_parm = music_parm("track_active")
    if track_active_parm.eval() >= len(tracks) :
        track_active_parm.set(len(tracks)-1)
    return tracks[  track_active_parm.eval()  ]



def track_item_delete() :
    node_track = track_item_active_node()
    node_track.destroy()



def track_item_tx(track) :
    if track_item_type(track) == "music_track_dots" :
        span = track.node("span")
        tx   = span.parm("centerx").eval() - 0.5 * span.parm("sizex").eval()

    if track_item_type(track) == "music_track_lines" :
        pattern = _track_lines_first
        notes = track.node("notes").glob(pattern)
        tx    = 0
        for note in notes :
            tx   = max(tx, note.parm("tx"))

    return tx    



def track_item_bbox_LRY_dots(track) :
    span         = track.node("span")
    span_sizex   = span.parm("sizex").eval()
    span_centerx = span.parm("centerx").eval()
    span_left    = span_centerx - span_sizex/2
    span_right   = span_centerx + span_sizex/2

    notes_GEO_zoom = track.node("vex/GEO_zoom").geometry()

    if len(   notes_GEO_zoom.points()   )>0 :
        notes_left     = notes_GEO_zoom.boundingBox().minvec()[0]
        notes_right    = notes_GEO_zoom.boundingBox().maxvec()[0]
        left  = min(   span_left  , notes_left )
        right = max(   span_right , notes_right )
    else:
        left  = span_left
        right = span_right

    y     = track.parm("ty").eval()

    return left, right, y



def track_item_bbox_LRY_lines(track) :
    notes = track.node("notes").glob("ikn_note*")
    l_all  = []
    r_all  = []
    y_all  = []
    for note in notes :
        centerx = note.parm("centerx").eval()
        sizex   = note.parm("sizex").eval()
        y       = note.parm("ty").eval()
        l       = centerx-sizex/2
        r       = centerx+sizex/2
        l_all.append(l)
        r_all.append(r)
        y_all.append(y)

    left  = min(l_all)
    right = max(r_all)
    y     = numpy.mean(y_all)

    return left, right, y




def track_item_bbox_LRY(track) :

    if track_item_type(track) == "music_track_dots" :
        left, right, y = track_item_bbox_LRY_dots(track)

    if track_item_type(track) == "music_track_lines" :
        left, right, y = track_item_bbox_LRY_lines(track)

    return left, right, y


def track_item_sort_notes(track) :
    # lines
    if track_item_type(track) == "music_track_lines" :
        notes = list(   track.node("notes").glob("ikn_note*")   )

        # sort notes
        x_min = []
        for note in notes :
            centerx = note.parm("centerx").eval()
            sizex   = note.parm("sizex").eval()
            left = centerx - sizex/2 
            x_min.append(left)
        keydict = dict(zip(notes, x_min))
        notes.sort(key=keydict.get)

        # rename notes TEMP
        for (notenum, note) in enumerate(notes) :
            note.parm("pitch").set(notenum)





#####################
#####################


def music_redraw() :
    
    tracks = list(  _node_tracks.children()  )
    
    # remember active node
    track_active = track_item_active_node()
    
    ####### sort tracks[] by the span_x
    x_min = []
    for track in tracks :
        left = track_item_tx(track)
        x_min.append(left)
    keydict = dict(zip(tracks, x_min))
    tracks.sort(key=keydict.get)

    ####### network positions 
    for (tracknum, track) in enumerate(tracks) :
        track.setPosition([0,tracknum])
        if track == track_active :
            # this tracknum is the remembered active node
            music_parm("track_active").set( tracknum )

    ####### sceneview ty
    # span all and remember track_active_y
    y_span_accumulate = 0
    for (tracknum, track) in enumerate(tracks) :
        track.parm("ty").set(y_span_accumulate)
        if track == track_active :
            track_active_y = y_span_accumulate
        y_span_accumulate += track.parm("viewspan").eval()

    ####### spectrum
    music_parm("spectrum_ty").set( track_active_y )

    ####### sort line notes
    for track in tracks :
        track_item_sort_notes(track)


#####################
#####################


def note_create(node) :
    # track_active = track_item_active_node()
    # notes_net    = track_active.node("notes")

    notes_net = node.parent()

    positions = pane_scene_selectpositions(1)[0]
    new_note  = notes_net.createNode("qmusic::note","note")
    new_note.moveToGoodPosition()
    new_note.parm("tx").set(positions[0])
    new_note.parm("ty").set(positions[1]) # - track_active.parm("ty").eval())

    note_create(node)
        
    #                       if track_item_type(track_active) == "music_track_lines" :
    #                           positions = pane_scene_selectpositions(2)
    #                           pos_first = positions[0]
    #                           pos_last  = positions[1]
    #                           new_note  = notes_net.createNode("ikn::music_note_line","ikn_note")
    #                           centerx   = (pos_first[0] + pos_last[0]) / 2
    #                           sizex     = pos_last[0] - pos_first[0]
    #                           new_note.moveToGoodPosition()
    #                           new_note.parm("sizex").set(sizex)
    #                           new_note.parm("centerx").set(centerx)
    #                           new_note.parm("ty").set(pos_first[1] - track_active.parm("ty").eval())



def notes_delete_all(track) :
    notes = track.node("notes").glob("ikn_note*")
    for note in notes :
        note.destroy()



def notes_align_y(node) :
    notes = node.parent().glob("note*")
    for note in notes :
        ty = note.parm("ty").eval()
        ty = round (ty/5) * 5
        ty = abs(ty)
        note.parm("ty").set(ty)



def notes_align_frames() :
    print("note_align_frames")


#####################
#####################


def camera_set_ortho(toggle) :
    pane = "IKOON_3_music.dual_scene.world"
    if toggle == True :
        script = "viewtype -t ortho_front " + pane
        hou.hscript(script)
    else :
        script = "viewtype -t perspective " + pane
        hou.hscript(script)
    

def camera_get_LRY() :
    pane_net, pane_parm, pane_scene = panes_music()

    camera = pane_scene.curViewport().defaultCamera()
    translation  = camera.translation()
    width  = camera.orthoWidth()
    left   = translation[0] - width/2
    right  = translation[0] + width/2
    y      = translation[1]
    return left, right, y


def camera_set_LRY(left, right, y) :
    pane_net, pane_parm, pane_scene = panes_music()
    # pane_scene.curViewport().frameBoundingBox(bbox)
    # setPivot does not translate the camera

    camera = pane_scene.curViewport().defaultCamera()
    x      = (left + right) / 2
    y      = y
    z      = camera.translation()[2]
    width  = right-left
    translation  = (x, y, z)
    camera.setTranslation(translation)
    camera.setOrthoWidth(width)


#####################
#####################



def camera_scope_playrange() :
    left         = hou.playbar.playbackRange()[0];
    right        = hou.playbar.playbackRange()[1];
    track_active = track_item_active_node()
    y            = track_active.parm("ty").eval()

    camera_set_LRY(left,right,y)



def camera_scope_track_active() :
    track          = track_item_active_node()
    left, right, y = track_item_bbox_LRY(track)

    camera_set_LRY(left,right,y)



def camera_scope_track_all() :
    tracks = list(  _node_tracks.children()  )
    l_all  = []
    r_all  = []
    y_all  = []
    for track in tracks :
        l, r, y = track_item_bbox_LRY(track)
        l_all.append(l)
        r_all.append(r)
        y_all.append(y)

    left  = min(l_all)
    right = max(r_all)
    y     = numpy.mean(y_all)

    camera_set_LRY(left,right,y)



#####################
#####################


def timeline_playrange_from_camera() :
    left, right, y = camera_get_LRY()
    play_start = math.floor(left);
    play_end   = math.ceil(right);
    hou.playbar.setPlaybackRange( play_start, play_end )


def timeline_jump_bar(direction) :
    node   = hou.node("/obj/music/bargrid/bar_main_points_array")
    geo    = node.geometry()
    frames = geo.intListAttribValue("array")
    frame  = round(  hou.frame()  )

    # --- after AE effects ---#
    # print frames
    # --- after AE effects ---#

    if direction > 0 :
        index = bisect.bisect_right(frames,frame)
    if direction < 0 :
        index = bisect.bisect_left(frames,frame) -1 

    bar = frames[index]
    hou.setFrame(bar)
    

def timeline_click_time() :
    position = pane_scene_selectpositions(1)[0]
    frame    = position[0]
    hou.setFrame(frame)



#####################
#####################


def span_edit() :
    span  = track_item_active_node().node("span")
    span.setGenericFlag(hou.nodeFlag.Selectable,True)
    span.setSelected(True,clear_all_selected=True)
    pane = wf_selection.pane_linkGroup( hou.paneTabType.SceneViewer )
    pane.setCurrentState("pose")
    span.setGenericFlag(hou.nodeFlag.Selectable,False)


def span_scope_notes(track) :
    span           = track.node("span")
    notes_GEO_zoom = track.node("vex/GEO_zoom").geometry()

    if len(   notes_GEO_zoom.points()   )>0 :
        notes_left   = notes_GEO_zoom.boundingBox().minvec()[0]
        notes_right  = notes_GEO_zoom.boundingBox().maxvec()[0]
        sizex        = notes_right - notes_left
        centerx      = (notes_right + notes_left) / 2

        span.parm("sizex").set(sizex)
        span.parm("centerx").set(centerx)


def span_scope_camera(track) :
    span           = track.node("span")
    left, right, y = camera_get_LRY()

    sizex        = right - left
    centerx      = (left + right ) / 2
    span.parm("sizex").set(sizex)
    span.parm("centerx").set(centerx)


#####################
#####################

def reload_source_music(node) :
    file_node = node.node("chopnet/file")
    file_node.parm("reload").pressButton()


def print_music_properties(node) :

    file_node = node.node("chopnet/OUT")

    # .wav first sample is 0
    # .wav last  sample is [1]-[0]
    # last length is [1]-[0] + 1
    sampleRange    = file_node.sampleRange()[1] - file_node.sampleRange()[0]  +  1
    samplesToFrame = file_node.samplesToFrame(sampleRange)
    samplesToTime  = file_node.samplesToTime(sampleRange)
    sampleRate     = file_node.sampleRate()

    print("\n\n-------------- audio --------------")
    print("set the track_length_seconds to:")
    print("samplesToTime()      " , str(samplesToTime) , " seconds")
    print("---------------------------------------")
    print("sampleRange()        " , str(file_node.sampleRange()))
    print("samplesToFrame()     " , str(samplesToFrame))
    print("sampleRate()         " , str(sampleRate))