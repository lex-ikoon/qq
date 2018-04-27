import re
import hou
import wf_network_ui_ramp_lib
import wf_selected

def node_global () :
    color = hou.color(0.0, 0.0, 0.0)
    path = "/obj/global"
    name = "global"
    
    if hou.node(path) :
        existed = 1
        return hou.node(path)
    else :
        existed = 0
        node_global = hou.node("/obj").createnode('null',name)
        node_global.movetogoodposition()
        node_global.setuserdata("nodeshape", "circle")
        node_global.setcolor(color)
        return node_global


def node_parent (node) :
    return node.parent()


def opmultiparm_ramp (node_channel, node_source, ramp_name, color) :

    rel_path = node_channel.relativePathTo(node_source)

    hscript  = 'opmultiparm '
    hscript +=  node_channel.path()
    hscript +=  ' "' + ramp_name + '#pos"    "' + rel_path + '/' + ramp_name + '#pos"     '
    hscript +=  ' "' + ramp_name + '#interp" "' + rel_path + '/' + ramp_name + '#interp"  '

    if not color:
        hscript +=  ' "' + ramp_name + '#value"  "' + rel_path + '/' + ramp_name + '#value"   '
    else:
        hscript +=  ' "' + ramp_name + '#cr"     "' + rel_path + '/' + ramp_name + '#cr"      ' 
        hscript +=  ' "' + ramp_name + '#cg"     "' + rel_path + '/' + ramp_name + '#cg"      '
        hscript +=  ' "' + ramp_name + '#cb"     "' + rel_path + '/' + ramp_name + '#cb"      '         

    hou.hscript(hscript)



def parm_ref_parm_ramp (node_channel, node_source, ramp_name) :

    ramp_source  = node_source.parm(ramp_name)
    ramp_channel = node_channel.parm(ramp_name)
    ramp_channel.set(ramp_source, None, False)

    template = ramp_source.parmTemplate().parmType()
    color = template == hou.rampParmType.Color

    keys   = ramp_source.eval().keys()

    if color :
        parms = ["pos","interp","cr","cg","cb"]
    else :
        parms = ["pos","interp","value"]

    for i in xrange(len(keys)) :
        for parm in parms :
            parm_source        =  node_source.parm(ramp_name + str(i + 1) + parm)
            parm_channel       = node_channel.parm(ramp_name + str(i + 1) + parm)
            parm_channel.set(parm_source, None, False)

    opmultiparm_ramp (node_channel, node_source, ramp_name, color)



def parm_ref_parm (node_channel, node_source, parm_name, parm_type) :

    if   parm_type == "rampfloat" or parm_type == "rampcolor" :
        parm_ref_parm_ramp(node_channel, node_source, parm_name)

    elif parm_type == "vector" :
        for dim in ["x","y","z"] :
            parm_source  = node_source.parm(parm_name + dim)
            parm_channel = node_channel.parm(parm_name + dim)
            parm_channel.set(parm_source, None, False)

    elif parm_type == "color" :
        for dim in ["r","g","b"] :
            parm_source  = node_source.parm(parm_name + dim)
            parm_channel = node_channel.parm(parm_name + dim)
            parm_channel.set(parm_source, None, False)

    else :
        parm_source  = node_source.parm(parm_name)
        parm_channel = node_channel.parm(parm_name)
        parm_channel.set(parm_source, None, False)



def parm_create (node, type, name, label) :

    if type == "integer" :
        new_template = hou.IntParmTemplate(name, name, 1)

    if type == "toggle" :
        new_template = hou.ToggleParmTemplate(name, name)

    if type == "float" :
        new_template = hou.FloatParmTemplate(name, name, 1)

    if type == "vector" :
        new_template = hou.FloatParmTemplate(name, name, 3)
        new_template.setLook(hou.parmLook.Regular)

    if type == "color" :
        new_template = hou.FloatParmTemplate(name, name, 3)
        new_template.setNamingScheme(hou.parmNamingScheme.RGBA)
        new_template.setLook(hou.parmLook.ColorSquare)

    if type == "string" : 
        new_template = hou.StringParmTemplate(name, name, 1)
        new_template.setStringType(hou.stringParmType.Regular)

    if type == "file" : 
        new_template = hou.StringParmTemplate(name, name, 1)
        new_template .setStringType(hou.stringParmType.FileReference)

    if type == "node" : 
        new_template = hou.StringParmTemplate(name, name, 1)
        new_template.setStringType(hou.stringParmType.NodeReference)

    if type == "separator" : 
        new_template = hou.SeparatorParmTemplate(name)

    if type == "label" : 
        new_template = hou.LabelParmTemplate(name, label, [label], False, True)

    if type == "rampfloat" : 
        new_template = hou.RampParmTemplate(name, name, hou.rampParmType.Float)
        new_template.setShowsControls(False)

    if type == "rampcolor" : 
        new_template = hou.RampParmTemplate(name, name, hou.rampParmType.Color)
        new_template.setShowsControls(False)
            
    try :
        ptg = node.parmTemplateGroup()
        ptg.addParmTemplate(new_template)
        node.setParmTemplateGroup( ptg )
        existed = 0

    except:
        existed = 1



def parm_update (node, type, name, default, min, max, hidden, join, ramplib) :

    ptg = node.parmTemplateGroup()
    parmedit = ptg.find( name )
    
    if type == "integer" :
        try:
            parmedit.setDefaultValue(  [int(default)] )
            parmedit.setMinValue    (   int(min)     )
            parmedit.setMaxValue    (   int(max)     )
        except:
            pass

    if type == "toggle" :
        try:
            parmedit.setDefaultValue(  int(default) )
        except:
            pass
            
    if type == "float" :
        try:
            parmedit.setDefaultValue(  [float(default)] )
            parmedit.setMinValue    (   float(min)     )
            parmedit.setMaxValue    (   float(max)     )
        except:
            pass
            
    if hidden  : parmedit.hide(True)
    if join    : parmedit.setJoinWithNext( True )

    if ramplib :
        ramp_preset, ramp_basis, ramp_keys, ramp_values = wf_network_ui_ramp_lib.ramp_lib()
        try:
            i = ramp_preset.index(ramplib)
            newRamp = hou.Ramp(ramp_basis[i], ramp_keys[i], ramp_values[i])
            node.setParms({name:newRamp})
        except:
            # comment is "color" or "glob" or anything else
            pass

        
    ptg.replace( name, parmedit )
    node.setParmTemplateGroup( ptg )



def line_parse (node, line, linenum) :

    name    = None
    label   = None
    type    = None
    default = None
    min     = None
    max     = None
    hidden  = None
    join    = None
    ramplib = None

    ##################
    ###### type ######
    ##################

    chi         = re.findall('chi\([\"\'](\w+)[\'\"]',line)
    chf         = re.findall('chf\([\"\'](\w+)[\'\"]',line)
    chv         = re.findall('chv\([\"\'](\w+)[\'\"]',line)
    chs         = re.findall('chs\([\"\'](\w+)[\'\"]',line)
    chramp      = re.findall('chramp\(\"(\w+)\"', line)
    chlabel     = re.findall('\/\/\# *(.+)', line)
    chseparator = re.findall("\/\/\-\-\-", line)
    chcolor     = re.findall('\/\/.*color',line)
    chtoggle    = re.findall('\/\/.*toggle',line)
    chfile      = re.findall('\/\/.*file',line)
    chnode      = re.findall('\/\/.*node',line)


    if chi                : type = "integer"     ; name = chi[0]                   ; label = name
    if chi and chtoggle   : type = "toggle"      ; name = chi[0]                   ; label = name
    if chf                : type = "float"       ; name = chf[0]                   ; label = name
    if chv                : type = "vector"      ; name = chv[0]                   ; label = name
    if chv and chcolor    : type = "color"       ; name = chv[0]                   ; label = name
    if chs                : type = "string"      ; name = chs[0]                   ; label = name
    if chs and chfile     : type = "file"        ; name = chs[0]                   ; label = name
    if chs and chnode     : type = "node"        ; name = chs[0]                   ; label = name
    if chseparator        : type = "separator"   ; name = "separ" + str(linenum)   ; label = name
    if chlabel            : type = "label"       ; name = "label" + str(linenum)   ; label = re.sub("[^0-9a-zA-Z\. ]+", "_", chlabel[0])
    if chramp             : type = "rampfloat"   ; name = chramp[0]                ; label = name
    if chramp and chcolor : type = "rampcolor"   ; name = chramp[0]                ; label = name

    if name      :
        # check if already referenced
        if name.startswith( "../" ) or name.startswith( "/obj/" ) : name == None

    if name      : parm_create (node, type, name, label)

    ##################
    ###### spec ######
    ##################

    parm_join    = re.findall('\/\/.*join',line)
    parm_hide    = re.findall('\/\/.*hide',line)
    ramplib      = re.findall('chramp\(.*\/\/.*?(\w+)',line)
    defminmax    = re.findall("\/\/ *([+-]?\d+\.?\d*?|\.\d+) +in +([+-]?\d+\.?\d*?|\.\d+) +to +([+-]?\d+\.?\d*|\.\d+)",line)
    if parm_join :    join = True
    if parm_hide :  hidden = True
    if ramplib   : ramplib = ramplib[0]
    if defminmax :
        default  = defminmax[0][0]
        min      = defminmax[0][1]
        max      = defminmax[0][2]

    if name      : parm_update (node, type, name, default, min, max, hidden, join, ramplib)

    ###################
    ###  reference  ###
    ###################

    ref_parent    = re.findall('\/\/.*parent',line)
    ref_global    = re.findall('\/\/.*global',line)

    
    if ref_parent and name :
        node_channel = node
        node_source  = node_parent(node)
        parm_create   (node_source, type, name, label)
        parm_update   (node_source, type, name, default, min, max, hidden, join, ramplib)
        parm_ref_parm (node_channel, node_source, name, type)

        node.setUserData("nodeshape", "chevron_down")
        node.setColor(hou.Color(0.95, 0.27, 0.27))

        line = line.replace('"' + name + '"', '"../' + name + '"')


    if ref_global and name :
        node_channel = node
        node_source  = node_global()
        parm_create   (node_source, type, name, label)
        parm_update   (node_source, type, name, default, min, max, hidden, join, ramplib)
        parm_ref_parm (node_channel, node_source, name, type)

        node.setUserData("nodeshape", "chevron_down")
        node.setColor(hou.Color(0.95, 0.27, 0.27))

        line = line.replace('"' + name + '"', '"/obj/global/' + name + '"')

    return line



def qq_expand () :
    ###################################################
    #######     qqr qqi qqf //  +  interface    #######
    ###################################################

    parm_pane = hou.ui.curDesktop().paneTabOfType(hou.paneTabType.Parm)
    node = parm_pane.currentNode()

    snippet = node.parm("snippet")
    actualcode = snippet.unexpandedString()
    lines = actualcode.split('\n')

    for line in lines:
        found = 0
        if line.startswith("qqf."):
            qq,var = line.split('.')
            newline = 'float ' + var + ' = chf("' + var + '"); // 0.5 in 0.0 to 1.0'
            found = 1
            
        if line.startswith("qqi."):
            qq,var = line.split('.')        
            newline = 'int ' + var + ' = chi("' + var + '"); // 1 in 0 to 10'
            found = 1
            
        if line.startswith("qqr."):
            qq,var = line.split('.')        
            newline = var + ' = chramp("' + var + '",' + var + '); //' + var
            found = 1

        if line.startswith("qqs."):
            qq,var = line.split('.')        
            newline = 'string ' + var + ' = chs("' + var + '"); // file node'
            found = 1

        if line.startswith("qqv."):
            qq,var = line.split('.')        
            newline = 'vector ' + var + ' = chv("' + var + '"); // color'
            found = 1

        if line.startswith("qq@f."):
            qq,var = line.split('.')
            newline = 'f@' + var + ' = chf("' + var + '"); // 0.5 in 0.0 to 1.0'
            found = 1

        if line.startswith("qq@i."):
            qq,var = line.split('.')
            newline = 'i@' + var + ' = chi("' + var + '"); // 1 in 0 to 10'
            found = 1

        if line.startswith("qq01."):
            qq,var = line.split('.')
            newline  = 'float new_min = chf("new_min"); // -1 in -10 to 10\n';
            newline += 'float new_max = chf("new_max"); //  1 in -10 to 10\n';
            newline += var + ' = fit01(' + var + ', new_min, new_max);';
            found = 1

            
        if line.startswith("qqx."):
            qq,var = line.split('.')
            if var.find("//") > 0 :
                # comment is defined
                var,comment = var.split('//')
                comment = " //"+comment
            else:
                comment = ""

            var = var.strip(" ")
            newline = '//----\n'
            newline += 'float ' + var + '_x = chf("' + var + '_x");' + comment + '\n'
            newline += 'float ' + var + '_y = chf("' + var + '_y");' + comment + '\n'
            newline += 'float ' + var + '_z = chf("' + var + '_z");' + comment + '\n'
            newline += 'vector  ' + var + ' = set(' + var + '_x, ' + var + '_y, ' + var + '_z);'   
            found = 1 

            
        if line.startswith("qqxx."):
            qq,var = line.split('.')
            if var.find("//") > 0 :
                # comment is defined
                var,comment = var.split('//')
                comment = " //"+comment
            else:
                comment = ""

            var = var.strip(" ")
            newline = '//----\n'
            newline += 'float ' + var + '_x_min = chf("' + var + '_x_min");' + comment + '\n'
            newline += 'float ' + var + '_x_max = chf("' + var + '_x_max");' + comment + '\n'
            newline += '//----\n'
            newline += 'float ' + var + '_y_min = chf("' + var + '_y_min");' + comment + '\n'
            newline += 'float ' + var + '_y_max = chf("' + var + '_y_max");' + comment + '\n'
            newline += '//----\n'
            newline += 'float ' + var + '_z_min = chf("' + var + '_z_min");' + comment + '\n'
            newline += 'float ' + var + '_z_max = chf("' + var + '_z_max");' + comment + '\n'

            newline += 'fit_xyz( '+ var + '_noise, ' + var + '_x_min, ' + var + '_x_max, ' + var + '_y_min, ' + var + '_y_max, ' + var + '_z_min, ' + var + '_z_max);'
            
            
            found = 1 
            
            
        if found:
            actualcode = actualcode.replace(line,newline,1) # only the first occurrence

    snippet.set(actualcode)

    ##############################################
    #######         read library         #########
    ##############################################

    import pickle

    path_shortcuts = hou.getenv("HOUDINI_USER_PREF_DIR") + "/vex/include/uber_qq_shortcuts.vfl"
    path_snippets  = hou.getenv("HOUDINI_USER_PREF_DIR") + "/vex/include/uber_qq_snippets.vfl"

    with open(path_shortcuts, 'r') as f:
        src = pickle.load(f)
        
    with open(path_snippets, 'r') as f:
        rep = pickle.load(f)


    ##############################################
    #######        replace library        ########
    ##############################################

    snippet = node.parm("snippet")
    actualcode = snippet.unexpandedString()
    index = 0
    for src_item in src:
        rep_item = rep[index]
        if src_item in actualcode:
            newcode = actualcode.replace(src_item,rep_item)
            snippet.set(newcode)
            actualcode = newcode
        index = index+1



def parm_generate () :
    node = wf_selected.parmnode()
    parm = node.parm("snippet")
    snippet = parm.unexpandedString()
    snippet_updated = ''
    lines = snippet.split('\n')

    for (linenum, line) in enumerate(lines):
        line_updated = line_parse (node, line, linenum)
        snippet_updated += line_updated
        if linenum < len(lines)-1 : snippet_updated += '\n'

    node.parm("snippet").set(snippet_updated)


def parm_clean () :
    node = wf_selected.parmnode()
    ptg = node.parmTemplateGroup()
    ptg.clear()
    node.setParmTemplateGroup(ptg)



def qq_parse_uberfile () :

    import pickle

    path_VEX  = hou.getenv("HOUDINI_USER_PREF_DIR") + "/vex/include/"
    path_uber = path_VEX + "uber_qq__definitions.vfl"
    file_uber = open( path_uber )
    uber_data = file_uber.read()

    snippets    = []
    shortcuts   = []
    includes    = ""
    helplines   = ""

    blocks = uber_data.split('///------------------------------------------------------------------')

    for block in blocks:

        block = block.strip("-")
        lines = block.split('\n')
        line_num = len(lines)
        line_with_shortcut = -1

        for i, line in enumerate(lines) :
            if line.startswith("--") :
                line_with_shortcut = i

        if line_with_shortcut == -1 :
            # block is a headline
            # -------------------
            helplines += "----------------\n"

        else :
            # block is a definition
            # ---------------------
            snippet    = ""
            shortcut   = ""
            include    = ""        
            helpline   = ""        
            
            # snippet
            for i in range( 0 , line_with_shortcut ) :
                snippet += lines[i].lstrip("-")
                snippet += "\n"
            
            snippet = snippet.strip("\n")

            # include        
            if lines[line_with_shortcut].startswith("--dont") :
                #this definition is just a shortcut without function to be included
                pass
            else:    
                include += "//DON'T EDIT THIS FILE, IT GETS OVERWRITTEN BY A SCRIPT\n"
                for i in range( line_with_shortcut , len(lines) ) :
                    include += lines[i].lstrip("-")
                    include += "\n"

            # helpline
            helpline = lines[line_with_shortcut]
            helpline = helpline.lstrip("-")
            helpline = helpline.split(" ")[1]
            helpline = helpline.replace(" ", "")
            helpline = helpline.split("(")[0]

            # shortcut
            shortcut = "qq" + helpline

            snippets.append(snippet)
            shortcuts.append(shortcut)
            includes  += include  + "\n"
            helplines += helpline + "\n"

    # write to disk
    # paths
    path_includes  = path_VEX + "qq.vfl"
    path_shortcuts = path_VEX + "uber_qq_shortcuts.vfl"
    path_snippets  = path_VEX + "uber_qq_snippets.vfl"
    path_helpcard  = path_VEX + "uber_qq_helpcard.vfl"
    # files
    file_includes  = open( path_includes, 'w')
    file_shortcuts = open( path_shortcuts, 'w')
    file_snippets  = open( path_snippets, 'w')
    file_helpcard  = open( path_helpcard, 'w')
    # write
    pickle.dump(shortcuts, file_shortcuts)
    pickle.dump(snippets,  file_snippets )
    file_helpcard.write(helplines)
    file_includes.write(includes)


def names_counts_in (node, ptg) :
    names     = []
    counts    = []
    index     = -1
    for pt in ptg.parmTemplates() :
        if pt.type() == hou.parmTemplateType.Folder :
            if pt.folderType() == hou.folderType.Tabs :
                try:
                    name      = pt.name() + "1"
                    parm      = node.parm(name).eval()
                    names.append(pt.name())
                    counts.append(0)
                    index     = index+1
                except:
                    pass
                counts[index] = counts[index] + 1
               
    return names, counts

def folders_trygo (node, name, count, dir) :
    went = 0
    parm = node.parm(name+"1")
    actual = parm.eval()
    if dir > 0 :
        if actual < count-1:
            parm.set(actual+1)
            went = 1
  
    if dir < 0 :
        if actual > 0:
            parm.set(actual-1)
            went = 1

    return went    
    
def folders_tab_go (dir) :
    node = wf_selected.parmnode()
    A = node.parmTemplateGroup()
    A_names, A_counts = names_counts_in (node, A)

    for (iA,A_name) in enumerate(A_names) :

        A_went = 0
        B_went = 0
        C_went = 0
        
        A_actual = node.parm(A_name+"1").eval()
        A_count = A_counts[iA]
        pt_name = A_name 
        
        if A_actual > 0:
            pt_name += "_" + str(A_actual)
            
        B = node.parmTemplateGroup().find(pt_name)
        B_names, B_counts = names_counts_in (node, B)
        
        for (iB,B_name) in enumerate(B_names) :
            B_actual = node.parm(B_name+"1").eval()
            B_count = B_counts[iB]
            pt_name = B_name 
            if B_actual > 0:
                pt_name += "_" + str(B_actual)
                
            C = node.parmTemplateGroup().find(pt_name)
            C_names, C_counts = names_counts_in (node, C)
            
            for (iC,C_name) in enumerate(C_names):
                C_count = C_counts[iC]
                C_went = folders_trygo(node, C_name, C_count , dir)
                
                    
            if C_went == 0:
                B_went = folders_trygo(node, B_name, B_count , dir)


        if B_went == 0 and C_went == 0:
            A_went = folders_trygo(node, A_name, A_count , dir)