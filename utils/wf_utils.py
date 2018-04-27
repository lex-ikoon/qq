from shutil import copyfile


root       = "C:/Users/info/OneDrive/Documents/houdini16.5/"
git        = "qq/"

src_py     = "python2.7libs/"
src_readme = "python2.7libs/" 
src_shelf  = "toolbar/"

files = []
files.append ("chaneditor")
files.append ("network_connection")
files.append ("network_kwargs")
files.append ("network_layout")
files.append ("network_parm")
files.append ("network_ui")
files.append ("network_ui_ramp_lib")
files.append ("network_utils")
files.append ("render")
files.append ("sceneview")
files.append ("selected")
files.append ("timeline")
files.append ("utils")


for file in files :
    # py
    src = root + src_py + "wf_" + file + ".py"
    dst = root + git + file + "/" + file + ".py"

    copyfile(src, dst)