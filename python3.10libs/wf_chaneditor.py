import hou
import wf_selection

def scope_timedependent_container () :

    expr_list = [
        "bezier()",
        "constant()",
        "cubic()",
        "cycle()",
        "cyclet()",
        "ease()",
        "easein()",
        "easeinp()",
        "easeout()",
        "easeoutp()",
        "easep()",
        "linear()",
        "match()",
        "matchin()",
        "matchout()",
        "quintic()",
        "repeat()",
        "repeatt()",
        "spline()",
        "vmatch()",
        "vmatchin()",
        "vmatchout()"
        ]
    
    for node in hou.selectedNodes() :
        for child in node.allSubChildren() :
            if not child.isInsideLockedHDA() :
                parms = child.parms()
                for parm in parms:
                    keys = parm.keyframes()
                    if keys != ():
                        key = keys[0]
                        if key.expression() in expr_list :
                            parm.setScope(1)








    # container = wf_selection.container()
    # nodes = container.allSubChildren()
    # for node in nodes:
    #     if not node.isInsideLockedHDA():
    #         parms = node.parms()
    #         for parm in parms:
    #             if parm.isTimeDependent():
    #                 parm.setScope(1)

