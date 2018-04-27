import hou
import toolutils



def play_backward () :
    hou.playbar.stop()
    #if hou.playbar.isPlaying() :
    #    hou.playbar.stop()
    #else :
    #    hou.playbar.reverse()

def play_forward () :
    hou.playbar.play()

def play_scrub () :
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

    skip = mouse_last - mouse_now
    if abs(skip) > 20 :
        skip = skip * 2

    frame_now = hou.frame()
    frame_now = hou.frame() - skip
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


def framerange_from_name () :
    #local playback range
    start  = hou.playbar.playbackRange()[0]
    end    = hou.playbar.playbackRange()[1]
    actual = hou.intFrame;

    # global time range
    globalstart  = hou.playbar.timelineRange()[0]
    globalend    = hou.playbar.timelineRange()[1]

    # container name
    active_pane = toolutils.activePane(kwargs)
    if active_pane is not None and active_pane.type() == hou.paneTabType.NetworkEditor:
        containername = active_pane.pwd().name()
        
    if containername == "obj":
        # range from global
        cont_start = globalstart;
        cont_end   = globalend;

    else:
        # range from name
        name = containername.split("_")
        if len(name) == 3 :
            cont_start = float( name[1] )
            cont_end   = float( name[2] )
        else:
            cont_start = globalstart
            cont_end   = globalend
        
    # set range
    hou.playbar.setPlaybackRange( cont_start, cont_end )
