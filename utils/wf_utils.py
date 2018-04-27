from shutil import copyfile


root       = "C:/Users/info/OneDrive/Documents/houdini16.5/"
git        = "_git/qq/"

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
    dst = root + git + file + "/wf_" + file + ".py"
    if file == "network_ui_ramp_lib" :
        dst = root + git + "network_ui/wf_" + file + ".py"
    copyfile(src, dst)

    # readme
    src = root + src_readme + "wf_" + file + ".md"
    dst = root + git + file + "/readme.md"
    if file == "network_ui_ramp_lib" :
        dst = root + git + "network_ui/readme_ramp_lib.md"
    copyfile(src, dst)

    # shelf
    if file == "network_ui_ramp_lib" :
        file = "network_ui"
    src = root + src_shelf + "wf_" + file + ".shelf"
    dst = root + git + file + "/wf_" + file + ".shelf"
    copyfile(src, dst)
