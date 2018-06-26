import re
import hou

def node_data (node_app, prefix) :

    node_con      = node_app.parent()
    path_con      = node_con.path()
    name_app      = node_app.name()
    name_app_done = re.findall('.*app\_(.*)',name_app)

    if not name_app_done :
        name_app = prefix + "app_" + name_app
        node_app.setName(name_app)

    name_dat  = name_app.replace("app_", "dat_")
    path_dat  = path_con + "/" + name_dat
    node_dat  = hou.node(path_dat)

    if node_dat :
        existed = 1
    else :
        existed = 0
        node_dat = node_con.createNode('attribwrangle',name_dat)
        posx = node_app.position()[0] + 3
        posy = node_app.position()[1] + 0
        node_dat.setPosition( [posx,posy] )
        node_dat.parm("class").set("detail")
    
    return node_dat


def snippet_preview (parms) :
    snippet  = '\n'
    snippet += 'qqinc\n'
    snippet += '// delete one of those:\n'
    snippet += 'qqpreview_int\n'
    snippet += 'qqpreview_float \n'
    snippet += '\n'
    for parm in parms :
        snippet += 'fi@' + parm.name() + '\n' 
    return snippet



def snippet_reference (parms) :
    snippet = '\n'
    for parm in parms :
        snippet += 'qq@f.' + parm.name() + '\n' 
    return snippet



def parm_ref_appdat (node_app, node_dat, parm_name) :
    expression        = 'detail("../' + node_dat.name() + '","' + parm_name + '",0)'
    parm              = node_app.parm(parm_name)
    parm.setExpression(expression)


def parmmenu_pre (node_app, parms) :
    prefix    = 'PRE'
    node_dat  = node_data(node_app,prefix)
    snip_parm = node_dat.parm('snippet')
    snippet   = snip_parm.unexpandedString()
    snippet  += snippet_preview (parms)
    snip_parm.set(snippet)

    for parm in parms :
        parm_ref_appdat (node_app, node_dat, parm.name())


def parmmenu_ref (node_app, parms) :
    prefix    = 'REF'
    node_dat  = node_data(node_app,prefix)
    snip_parm = node_dat.parm('snippet')
    snippet   = snip_parm.unexpandedString()
    snippet  += snippet_reference (parms)
    snip_parm.set(snippet)

    for parm in parms :
        parm_ref_appdat (node_app, node_dat, parm.name())