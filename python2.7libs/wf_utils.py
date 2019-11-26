from shutil import copyfile
import mistune


def xml_for_wordpress ():

    dir_root = "C:/Users/info/OneDrive/Documents/houdini16.5/"
    dir_blog = "_blog/"
    dir_md   = "python2.7libs/md/" 
    dir_py   = "python2.7libs/" 

    py_begin = '''<h2>source code</h2>
    the following code is maintained also on my <a href="https://github.com/lex-ikoon/qq">github</a><br>
    <a href="http://lex.ikoon.cz/thanks">thank you, great people</a>, I couldn't do this without you.
    <pre class="EnlighterJSRAW" data-enlighter-language="null">'''
    py_end = '</pre>'

    files = []
    ids   = []
    files.append("blog_dim_coord_distort_fill") ; ids.append(66)
    files.append("blog_midi_to_animation")      ; ids.append(69)
    files.append("blog_thanks")                 ; ids.append(48)
    files.append("blog_vex_uber_parse")         ; ids.append(15)
    files.append("blog_vex_ui_markup")          ; ids.append(63)
    files.append("blog_workflow")               ; ids.append(72)
    files.append("wf_chaneditor")               ; ids.append(49)
    files.append("wf_network_connection")       ; ids.append(122)
    files.append("wf_network_kwargs")           ; ids.append(125)
    files.append("wf_network_layout")           ; ids.append(117)
    files.append("wf_network_parm")             ; ids.append(108)
    files.append("wf_network_ui")               ; ids.append(111)
    files.append("wf_network_ui_ramp_lib")      ; ids.append(114)
    files.append("wf_network_utils")            ; ids.append(128)
    files.append("wf_render")                   ; ids.append(134)
    files.append("wf_sceneview")                ; ids.append(131)
    files.append("wf_selection")                ; ids.append(137)
    files.append("wf_timeline")                 ; ids.append(140)
    files.append("wf_utils")                    ; ids.append(143)
    files.append("wf_midi")                     ; ids.append(152)


    for file in files :

        # py
        path_md   = dir_root + dir_md   + file + ".md"
        path_html = dir_root + dir_blog + file + ".html"
        path_py   = dir_root + dir_py   + file + ".py"
        
        file_mark = open( path_md )
        file_html = open( path_html, 'w' )

        data_mark = file_mark.read()
        data_html = mistune.markdown(data_mark,hard_wrap=True)


        if file.startswith('wf_') :
            file_py   = open( path_py   )
            data_py   = file_py.read()
            data_html = data_html + py_begin
            data_html = data_html + data_py
            data_html = data_html + py_end

        file_html.write(data_html)


    xml_begin = '<?xml version="1.0" encoding="UTF-8" ?><channel>'
    xml_end   = '</channel>'
    xml_data  = xml_begin

    for (filenum, file) in enumerate(files):
        path_html = dir_root + dir_blog + file + ".html"
        file_html = open( path_html )
        data_html = file_html.read()
        data_html = data_html.replace('<![CDATA[','<glitch to preview CDATA in CDATA ![CDATA[')
        data_html = data_html.replace(']]>',']<glitch to preview CDATA in CDATA]>')
        xml_data += '<item><id>' + str(ids[filenum]) + '</id>'
        xml_data += '<content><![CDATA[' + data_html + ']]></content></item>'

    xml_data += xml_end
    path_xml = "C:\Users\info\Desktop\export.xml"
    file_xml = open( path_xml, 'w' )
    file_xml.write(xml_data)    




def collect_for_github() :

    #################################
    #####     copy files     ########
    #################################

    from shutil import copyfile

    root       = "Q:/_houdini17.5/"
    git        = "_git/qq/"

    src_py     = "python2.7libs/"
    src_shelf  = "toolbar/"
        
    files = []
    files.append ("_set")
    files.append ("hotkeys")
    files.append ("chaneditor")
    files.append ("midi")
    files.append ("music")
    files.append ("network_connection")
    files.append ("network_kwargs")
    files.append ("network_layout")
    files.append ("network_parm")
    files.append ("network_ui")
    files.append ("network_ui_ramp_lib")
    files.append ("network_utils")
    files.append ("render")
    files.append ("rigging")
    files.append ("sceneview")
    files.append ("selection")
    files.append ("timeline")
    files.append ("utils")


    for file in files :

        # py
        try :
            src = root + src_py + "wf_" + file + ".py"
            dst = root + git + src_py   + "wf_" + file + ".py"
            copyfile(src, dst)
        except :
            pass

        # shelf
        try :
            src = root + src_shelf + "wf_" + file + ".shelf"
            dst = root + git + src_shelf + "/wf_" + file + ".shelf"
            copyfile(src, dst)
        except :
            pass


    #################################
    #####     vex and other    ######
    #################################

    files_src = []
    files_dst = []

    files_src.append ("Q:/_houdini17.5/vex/include/helpcard.txt")
    files_dst.append ("Q:/_houdini17.5/_git/qq/vex/include/helpcard.txt")

    files_src.append ("Q:/_houdini17.5/vex/include/qq.vfl")
    files_dst.append ("Q:/_houdini17.5/_git/qq/vex/include/qq.vfl")

    files_src.append ("Q:/_houdini17.5/vex/include/snippets.db")
    files_dst.append ("Q:/_houdini17.5/_git/qq/vex/include/snippets.db")

    files_src.append ("Q:/_houdini17.5/vex/include/triggers.db")
    files_dst.append ("Q:/_houdini17.5/_git/qq/vex/include/triggers.db")

    files_src.append ("Q:/_houdini17.5/vex/include/uber.vfl")
    files_dst.append ("Q:/_houdini17.5/_git/qq/vex/include/uber.vfl")

    files_src.append ("Q:/_houdini17.5/PARMmenu.xml")
    files_dst.append ("Q:/_houdini17.5/_git/qq/PARMmenu.xml")

    files_src.append ("C:/Users/info/OneDrive/Documents/houdini17.5/Houdini.keymap.overrides")
    files_dst.append ("Q:/_houdini17.5/_git/qq/Houdini.keymap.overrides")



    for counter, file in enumerate(files_src):
        try :
            src = file
            dst = files_dst[counter]
            copyfile(src, dst)
        except :
            pass
