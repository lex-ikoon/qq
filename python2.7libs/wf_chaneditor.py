import hou
import wf_selection

def scope_timedependent_container () :
    container = wf_selection.container()
    nodes = container.allSubChildren()
    for node in nodes:
        if not node.isInsideLockedHDA():
            parms = node.parms()
            for parm in parms:
                if parm.isTimeDependent():
                    parm.setScope(1)

