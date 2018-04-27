import hou
import PyTake2

def start () :
    pane = hou.ui.curDesktop().paneTabOfType(hou.paneTabType.IPRViewer)
    pane.killRender()
    pane.startRender()


def kill () :
    pane = hou.ui.curDesktop().paneTabOfType(hou.paneTabType.IPRViewer)
    pane.killRender()


def take_from_name () :
    for node in hou.selectedNodes():
        name = node.name()
        new_take = PyTake2.Take(name)
        new_take.includeDisplayFlag(node)
        PyTake2.returnToMainTake()