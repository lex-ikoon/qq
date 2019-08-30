import hou

import wf_selection
reload(wf_selection)

import wf_sceneview
reload(wf_sceneview)

import wf_music
reload(wf_music)

import wf_network_parm
reload(wf_network_parm)

import wf_timeline
reload(wf_timeline)

import wf_network_connection
reload(wf_network_connection)

def cursor_over_music() :
    if wf_selection.cursor_linkGroup() == hou.paneLinkType.Group3 :
        return True
    else:
        return False

#####################
#####################




def hotkey_z () :
    if cursor_over_music() :
        wf_music.camera_scope_track_active()
    else :
        wf_sceneview.frame_selected()


def hotkey_z_shift () :
    if cursor_over_music() :
        wf_music.camera_scope_track_all()
    else :
        wf_sceneview.frame_all()


def hotkey_f_alt () :
    if cursor_over_music() :
        wf_music.timeline_playrange_from_camera()
    else :
        wf_timeline.playrange_from_name()



def hotkey_j () :
    if cursor_over_music() :
        wf_music.camera_scope_playrange()
    else :
        pass


#####################
#####################

def hotkey_left_ctrl_shift () :
    wf_music.timeline_jump_bar(-1)


def hotkey_right_ctrl_shift () :
    wf_music.timeline_jump_bar(1)



#####################
#####################



def hotkey_pgup() :
    if cursor_over_music() :
        wf_music.tracks_activate(1)
    else :
        wf_network_connection.selection_go([0,1])



def hotkey_pgdn() :
    if cursor_over_music() :
        wf_music.tracks_activate(-1)
    else :
        wf_network_connection.selection_go([0,-1])



def hotkey_pgup_shift() :
    print "music"

    
def hotkey_pgdp_shift() :
    print "music"


def hotkey_pgup_ctrl() :
    print "music"
    # select tracks


def hotkey_pgdn_ctrl() :
    print "music"
    # select track

#####################
#####################


def hotkey_enter_alt() :
    if cursor_over_music() :
        wf_music.span_edit()
    else :
        pass



def hotkey_enter_ctrl_shift() :
    # no hotkey yet
    # make it global
    if cursor_over_music() :
        wf_music.note_create()
    else :
        pass


#####################
#####################


def hotkey_del_ctrl() :
    if cursor_over_music() :
        wf_music.tracks_visualize_toggle("spectrum")
    else :
        wf_network_parm.flag_bypass()


def hotkey_ins() :
    if cursor_over_music() :
        wf_music.tracks_visualize_toggle("arrays")
    else :
        wf_network_parm.flag_display()


def hotkey_ins_shift() :
    if cursor_over_music() :
        wf_music.timeline_click_time()
    else :
        wf_network_connection.create_by_y()


def hotkey_ins_ctrl() :
    if cursor_over_music() :
        wf_music.tracks_visualize_toggle("clones")
    else :
        wf_network_parm.flag_bypass()


def hotkey_ins_ctrl_shift () :
    if cursor_over_music() :
        wf_music.tracks_visualize_toggle("bpm")
    else :
        wf_network_parm.flag_bypass()


