# -------------------------
# contents of the wf_hda.py

import hou
import hdefereval

def extract(node) :
    def extract_hda(hda_node) :
        label = "Extract HDA: " + str(hda_node.type().name())
        with hou.undos.group(label):
            hda_node.extractAndDelete()

    hdefereval.executeDeferred(lambda: extract_hda(node) )

# -------------------------
# OnCreated scipt in the Type Properties:
# import wf_hda
# wf_hda.extract(  kwargs["node"]  )





# reload(wf_hda)