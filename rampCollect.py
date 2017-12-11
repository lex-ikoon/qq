node = hou.selectedNodes()[0]
parms = node.parms()

string = '''
ramp_preset = []
ramp_basis = []
ramp_keys = []
ramp_values = []

'''

for parm in parms:
    if parm.parmTemplate().type() == hou.parmTemplateType.Ramp:
    
        #parm is Ramp
        parmName = parm.name()
        orig_ramp = parm.eval()

        basis = orig_ramp.basis()
        keys = orig_ramp.keys()
        values = orig_ramp.values()

        string = string + "ramp_preset.append( '%s' )" % parmName  + "\n"
        string = string + "ramp_basis.append( %s ) " % (basis,) + "\n"
        string = string + "ramp_keys.append( %s ) " % (keys,) + "\n"
        string = string + "ramp_values.append( %s ) " % (values,) + "\n"
        string = string + "\n"


string = string.replace( "rampBasis." , "hou.rampBasis." )

print string