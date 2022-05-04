import hdefereval
import wf_network_ui

# def functionToExecuteOnStartup():
#     wf_network_ui.panetab_restore(True)
# hdefereval.executeDeferred(functionToExecuteOnStartup)

hdefereval.executeDeferred(lambda: wf_network_ui.panetab_restore(True))
# hdefereval.executeDeferred(lambda: extract_hda(node) )
