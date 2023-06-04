import hou

if hou.isUIAvailable() == True:
    import hdefereval
    import wf_ui_panetab

    # executeDeferred, because we have to wait for the UI
    hdefereval.executeDeferred(lambda: wf_ui_panetab.panetab_restore(True, False))