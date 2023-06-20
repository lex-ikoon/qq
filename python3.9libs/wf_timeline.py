import os
import hou
import math
import bisect
import toolutils
import wf_selection


#####################
###     resim     ###
#####################


def sim_solver_valid (node) :

    if "solver" in node.type().name() or "dopnet" in node.type().name() and node.isInsideLockedHDA() == False :
        return True
    else:
        return False



def sim_solver () :

    # workaround because houdini feature (ID# 122908)

    # ----------------------------
    # for display & inputs
    try:
        display = wf_selection.parmnode_obj().displayNode()
        for i in range(64):
            if sim_solver_valid(display) :
                return display
            else :
                display = display.input(0)
    except:
        pass


    # ----------------------------
    # for selected & parents 
    try:
        selected = wf_selection.parmnode()
        for i in range(8):
            if sim_solver_valid(selected) :
                return selected
            else :
                selected = selected.parent()
    except:
        pass

    # ----------------------------
    # dopnet
    if hou.currentDopNet() != None :
        return hou.currentDopNet()




# return the current dopnet node
def sim_dopnet () :
    dopnet         = sim_solver()
    try:
        cache_on       = dopnet.parm("explicitcache").eval()
        cache_name     = dopnet.parm("explicitcachename").rawValue()
        cache_substeps = dopnet.parm("substep").eval()
        cache_start    = dopnet.parm("startframe").eval()
        cache_spacing  = dopnet.parm("explicitcachecheckpointspacing").eval()
    except:
        cache_on       = 0
        cache_name     = None
        cache_substeps = 1
        cache_start    = 1
        cache_spacing  = 1

    return [dopnet, cache_on, cache_name, cache_substeps, cache_start, cache_spacing]



# list of all $SF that may be cached with current dopnet settings
# and list of appropriate $F frames
def sim_cache_framelists() :
    dopnet, cache_on, cache_name, cache_substeps, cache_start, cache_spacing = sim_dopnet()
    framerange_end = hou.playbar.frameRange()[1]

    candidate_sf = 0
    candidate_f  = cache_start
    list_sf      = [candidate_sf]
    list_f       = [candidate_f]

    while candidate_f <= framerange_end :
        candidate_sf  += cache_spacing
        candidate_f   = math.floor((candidate_sf-1) / cache_substeps) + cache_start
        list_sf.append(candidate_sf) 
        list_f.append (candidate_f) 

    return list_sf, list_f


# find the given frame's precedent cached $F
def sim_cache_precedent_index ( frame ) :
    list_sf, list_f = sim_cache_framelists()
    precedent_index = bisect.bisect_right(list_f,frame)
    precedent_index = max (precedent_index - 1, 0)
    return precedent_index


# delete the .sim cache files in the playrange
# but don't delete the first one, we want to built on it
def sim_cache_delete_playrange () :
    dopnet, cache_on, cache_name, cache_substeps, cache_start, cache_spacing = sim_dopnet()
    hou.cd(dopnet.path()) # to expandString() correctly
    list_sf, list_f = sim_cache_framelists()
    index = 1 + sim_cache_precedent_index(  hou.playbar.playbackRange()[0]  )

    candidate_frames = list_sf[index:]
    
    # try to delete the files, if they exist
    for frame in candidate_frames :
        file_path = cache_name.replace("$SF",str(frame))
        file_path = hou.expandString(file_path)
        file_path = file_path.replace("*","_")

        if file_path.endswith(".sim") :
            try :
                os.remove(file_path)
            except :
                # frame was not cached
                pass


# hotkey: F5
# reset the sim
def sim_cache_reset (set_frame) :
    dopnet, cache_on, cache_name, cache_substeps, cache_start, cache_spacing = sim_dopnet()
    # print (dopnet, cache_on, cache_name, cache_substeps, cache_start, cache_spacing)

    if cache_on:
        # delete .sim files
        message = "Delete .sim files in playback range? \n\n" + str(dopnet.path())
        if hou.ui.displayMessage(message, buttons=("OK", "Cancel")) == 0:
            sim_cache_delete_playrange()

    try:
        dopnet.parm("resimulate").pressButton()
    except:
        pass

    try:
        dopnet.parm("resetsim").pressButton()
    except:
        pass

    wf_selection.parmnode().cook(force=True)
    hou.setCurrentDopNet(dopnet)

    if set_frame :
        hou.setFrame(hou.playbar.playbackRange()[0]) 




# hotkey: /
# trim the playback start to the playhead's precedent cached .sim file
def playrange_to_precedent () :
    list_sf, list_f = sim_cache_framelists()
    index = sim_cache_precedent_index(  hou.intFrame()  )

    frame_start = list_f[index]
    frame_end   = hou.playbar.playbackRange()[1]
    hou.playbar.setPlaybackRange( frame_start, frame_end )



# hotkeys: . ,
# add or remove one cached spacing in playrange
def playrange_extend_spacing (direction) :
    # list_sf, list_f = sim_cache_framelists()
    # index = sim_cache_precedent_index(  hou.playbar.playbackRange()[0]  )
    # index = max (index + direction, 0)

    # frame_start = list_f[index]
    # frame_end   = hou.playbar.playbackRange()[1]
    # hou.playbar.setPlaybackRange( frame_start, frame_end )

    if direction == -1 :
        frame_start = hou.frame()
        frame_end   = hou.playbar.playbackRange()[1]

    if direction == 1 :
        frame_end   = hou.playbar.playbackRange()[0]
        frame_start = hou.frame()


    hou.playbar.setPlaybackRange( frame_start, frame_end )



#####################
###   resim end   ###
#####################



def play_backward () :
    hou.playbar.stop()
    #if hou.playbar.isPlaying() :
    #    hou.playbar.stop()
    #else :
    #    hou.playbar.reverse()



def play_forward () :
    hou.playbar.play()



def play_scrub (multiplier) :
    import time
    from PySide2.QtGui import QCursor

    mouse_last = hou.getenv("mouse", "0")
    mouse_last = float(mouse_last)
    mouse_now = QCursor().pos()

    time_now = time.time()
    time_last = hou.getenv("time", "0")
    time_last = float(time_last)
    time_diff = time_now-time_last

    mouse_now = round(  mouse_now.x() / 10 )

    if time_diff > 0.1 :
        mouse_last = mouse_now


    ###########
    # skip by playrange
    range_mult = hou.playbar.playbackRange()[1] - hou.playbar.playbackRange()[0]
    range_mult = range_mult / 200


    skip = mouse_last - mouse_now
    skip = skip * multiplier
    if abs(skip) > 20 :
        skip = skip * 2

    skip = skip * range_mult
    ###########

    frame_now = hou.frame()
    frame_now = hou.frame() - skip
    frame_now = max(frame_now,hou.playbar.playbackRange()[0]) # first frame
    frame_now = min(frame_now,hou.playbar.playbackRange()[1]) # last frame
    frame_now = round(frame_now)
    hou.setFrame(frame_now)

    hou.putenv("mouse", str(mouse_now))
    hou.putenv("time", str(time_now))



def toggle_realtime () :
    hou.playbar.setRealTime(not hou.playbar.isRealTime())
    hou.playbar.setRealTimeSkipping(hou.playbar.isRealTime())




def toggle_manualupdate () :
    mode = hou.updateModeSetting().name()
    if mode == 'AutoUpdate':
        hou.setUpdateMode(hou.updateMode.Manual)
    if mode == 'Manual':
        hou.setUpdateMode(hou.updateMode.AutoUpdate)



def playrange_from_job () :


    def node_range( node ) :
        cont_start = node.parm("job_rangex").eval();
        cont_end   = node.parm("job_rangey").eval();
        hou.playbar.setPlaybackRange( cont_start, cont_end )
    

    # ----------------------------
    # selected has job_range
    try:
        node_range ( hou.selectedNodes()[0] )
        return
    except:
        pass 


    # ----------------------------
    # parent has job_range
    try:
        node_range ( hou.selectedNodes()[0].parent() )
        return
    except:
        pass 


    # ----------------------------
    # parent.parent has job_range
    try:
        node_range ( hou.selectedNodes()[0].parent().parent() )
        return
    except:
        globalstart  = hou.playbar.timelineRange()[0]
        globalend    = hou.playbar.timelineRange()[1]
        hou.playbar.setPlaybackRange( globalstart , globalend )
        pass 



