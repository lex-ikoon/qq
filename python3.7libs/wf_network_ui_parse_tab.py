import hou
import os
import subprocess
import re
import pickle
import wf_selection


def tab_vex_edit (node) :
    editor       = hou.getenv("wf_editor")
    sourcefile   = node.userData("sourcefile")
    sourceline   = node.userData("sourceline")
    arg = sourcefile + '":' + sourceline
    print(arg)
    subprocess.call([editor, "--goto", arg], shell=True)
    # subprocess.call(editor, shell=True)
    # subprocess.call(["C:/Users/info/AppData/Local/Programs/Microsoft VS Code/Code.exe", "--goto", "Q:\_packages\wf_workflow\vex_src\dim_coord_fill\dimension.vfl"], shell=True) 
    



def tab_vex_indent (snippet, leading_spaces) :
    indented = ""
    lines    = snippet.split('\n')

    for (i, line) in enumerate(lines) :
        if i > 0 :
            line = " " * leading_spaces + line

        indented = indented + line + '\n'

    return indented



def tab_vex_paste (index) :

    # read files
    #------------------------------------------------------------
    path_VEX_db      = hou.getenv("wf_path") + "/vex_src/_db/"
    path_snippets    = path_VEX_db + "tab_vex_snippets.db"
    path_nodenames   = path_VEX_db + "tab_vex_nodenames.db"
    path_sourcefiles = path_VEX_db + "tab_vex_sourcefiles.db"
    path_sourcelines = path_VEX_db + "tab_vex_sourcelines.db"
    
    with open(  path_snippets  ,    'rb') as f:
        snippets    = pickle.load(f)
    with open(  path_nodenames  ,   'rb') as f:
        nodenames   = pickle.load(f)
    with open(  path_sourcefiles  , 'rb') as f:
        sourcefiles = pickle.load(f)
    with open(  path_sourcelines  , 'rb') as f:
        sourcelines = pickle.load(f)

    snippet    = snippets[index]
    nodename   = nodenames[index]
    sourcefile = sourcefiles[index]
    sourceline = sourcelines[index]


    # search for qw in current node
    #------------------------------------------------------------
    current_node = wf_selection.parmnode()
    found = -1
    for parm in current_node.parms() :
        parm_string = parm.evalAsString()

        # found in parm
        if parm_string.find("qw") > -1 :

            # indent the snippet
            for line in parm_string.split('\n') :
                if line.find("qw") > -1 :
                    leading_spaces = len(line) - len(line.lstrip())
                    snippet        = tab_vex_indent(snippet, leading_spaces)

            parm_string = parm_string.replace("qw",snippet)
            parm.set(parm_string)
            found = 1
            

    # create node
    #------------------------------------------------------------
    if found < 0 :
        import wf_network_utils
        node_create = wf_network_utils.create_node("attribwrangle")
        node_create.setName(nodename, unique_name=True)
        node_create.parm("snippet").set(snippet)
        node_create.setUserData("sourcefile", sourcefile)
        node_create.setUserData("sourceline", str(sourceline))



    

def create_vex_shelf () :

    # read files
    #------------------------------------------------------------
    path_VEX_db    = hou.getenv("wf_path") + "/vex_src/_db/"
    path_snippets  = path_VEX_db + "tab_vex_snippets.db"
    path_nodenames = path_VEX_db + "tab_vex_nodenames.db"
    path_toolnames = path_VEX_db + "tab_vex_toolnames.db"

    print (path_snippets)

    with open(path_snippets, 'rb') as f:
        snippets  = pickle.load(f)
    with open(path_nodenames, 'rb') as f:
        nodenames = pickle.load(f)
    with open(path_toolnames, 'rb') as f:
        toolnames = pickle.load(f)

    shelf = ""

    # .shelf --- header
    #-----------------------------------------------------------------------------------------------------------------
    shelf += """<?xml version="1.0" encoding="UTF-8"?>\n<shelfDocument>
  <!-- DON'T EDIT THIS FILE, IT GETS OVERWRITTEN BY A SCRIPT  -->
  <!--     python3.7libs\wf_network_ui_parse_tab.py           -->
  <toolshelf name="wf_vex" label="wf_vex">
    """

    # .shelf --- LOOP membername
    #-----------------------------------------------------------------------------------------------------------------
    membertools = ""
    for toolname in toolnames :
        membertools += "\n"
        membertools += '        <memberTool name="'
        membertools += toolname
        membertools += '"/>'
    shelf += membertools + "\n"

    # .shelf --- mid
    #-----------------------------------------------------------------------------------------------------------------
    shelf += "</toolshelf>\n\n"


    # .shelf --- LOOP name 
    #-----------------------------------------------------------------------------------------------------------------

    tools = ""
    for (index, toolname) in enumerate(toolnames) :
        tools += '  <tool name="' + toolname + '" label="' + toolname + '" icon="PLASMA_App">\n'
        tools += '    <toolMenuContext name="network"><contextNetType>SOP</contextNetType><contextNetType>DOP</contextNetType></toolMenuContext>\n'
        tools += '    <script scriptType="python"><![CDATA[import wf_network_ui_parse_tab\nwf_network_ui_parse_tab.tab_vex_paste(' + str(index) + ')]]></script>\n'
        tools += '  </tool>\n\n'
    shelf += tools + "\n"

    # .shelf --- footer
    #-----------------------------------------------------------------------------------------------------------------
    shelf += "</shelfDocument>"
    
    # write file
    #-----------------------------------------------------------------------------------------------------------------
    path_shelf = hou.getenv("wf_path") + "/toolbar/wf_vex.shelf"
    file_shelf = open( path_shelf, 'w')
    file_shelf.write(shelf)
    file_shelf.close()



def validate_nodename(text):
    # thanks to Graham and Atom from odforce for this function
    # replace any illegal characters for node names here
    text = re.sub("[^0-9a-zA-Z\.]+", "_", text)
    text = text.replace("docs_", "")
    text = text.strip("_")
    return text



def validate_toolname(text):
    text = text.replace(  "'" , "&apos;" )
    text = text.replace(  '"' , "&quot;" )
    text = text.replace(  "&" , "&amp;"  )
    text = text.replace(  "<" , "&lt;"   )
    text = text.replace(  ">" , "&gt;"   )
    return text




def parse_tab_vex () :

    # init variables
    #------------------------------------------------------------
    toolname_prefix = "qw // "
    path_VEX_db      = hou.getenv("wf_path") + "/vex_src/_db/"
    path_VEX_vfl     = hou.getenv("wf_path") + "/vex_src/"


    # find files
    #------------------------------------------------------------
    vfl_paths = []

    for root, dirs, files in os.walk(path_VEX_vfl):
        for file in files:
            if file.endswith(".vfl"):
                vfl_path = os.path.join(root, file)
                vfl_paths.append(vfl_path)


    # separate snippets and descriptions
    #------------------------------------------------------------
    snippets    = []
    nodenames   = []
    sourcefiles = []
    sourcelines = []
    toolnames   = []
    
    for vfl_path in vfl_paths:

        vfl_file  = open( vfl_path )
        uber_data = vfl_file.read()
        blocks    = uber_data.split('///---------------------')

        for block in blocks:

            block                 = block.strip("-")
            lines                 = block.split('\n')
            line_num              = len(lines)
            line_with_description = -1

            for i, line in enumerate(lines) :
                if line.startswith("///") :
                    line_with_description = i

            if line_with_description > -1:

                # block is a valid definition
                # sourceline
                all_lines   = uber_data.split('\n')
                description = lines[line_with_description]
                for i, line in enumerate(all_lines) :
                    if line.startswith(description) :
                        sourceline = i + 1

                # description
                description = lines[line_with_description]
                description = description.lstrip("/ ")

                # snippet
                snippet = ""
                for i in range( line_with_description + 1 , len(lines) ) :
                    snippet += lines[i]
                    snippet += "\n"

                # nodename
                nodename = validate_nodename(description)

                # toolname
                toolname = validate_toolname(description)
                toolname = toolname_prefix + description

                # arrays
                snippets.append(snippet)
                nodenames.append(nodename)
                sourcefiles.append(vfl_path)
                sourcelines.append(sourceline)
                toolnames.append(toolname)


    # write to disk
    #------------------------------------------------------------
    # paths
    path_snippets    = path_VEX_db + "tab_vex_snippets.db"
    path_nodenames   = path_VEX_db + "tab_vex_nodenames.db"
    path_sourcefiles = path_VEX_db + "tab_vex_sourcefiles.db"
    path_sourcelines = path_VEX_db + "tab_vex_sourcelines.db"
    path_toolnames   = path_VEX_db + "tab_vex_toolnames.db"
    # files
    file_snippets    = open( path_snippets, 'wb')
    file_nodenames   = open( path_nodenames, 'wb')
    file_sourcefiles = open( path_sourcefiles, 'wb')
    file_sourcelines = open( path_sourcelines, 'wb')
    file_toolnames   = open( path_toolnames, 'wb')
    # write
    pickle.dump(snippets, file_snippets )
    pickle.dump(nodenames, file_nodenames )
    pickle.dump(sourcefiles, file_sourcefiles )
    pickle.dump(sourcelines, file_sourcelines )        
    pickle.dump(toolnames, file_toolnames )
    # close
    file_snippets.close()
    file_nodenames.close()
    file_sourcefiles.close()
    file_sourcelines.close()
    file_toolnames.close()

    create_vex_shelf()


