import re
import hou
import wf_selection

def ramp_lib_get() :
    node = wf_selection.parmnode()
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



def ramp_lib() :

    ramp_preset = []
    ramp_basis = []
    ramp_keys = []
    ramp_values = []

    ###################

    ramp_preset.append( 'quad' )
    ramp_basis.append( (hou.rampBasis.MonotoneCubic, hou.rampBasis.MonotoneCubic, hou.rampBasis.MonotoneCubic, hou.rampBasis.MonotoneCubic) ) 
    ramp_keys.append( (0.0, 0.15000000596046448, 0.8500000238418579, 1.0) ) 
    ramp_values.append( (0.0, 1.0, 1.0, 0.0) ) 

    ramp_preset.append( 'ends' )
    ramp_basis.append( (hou.rampBasis.MonotoneCubic, hou.rampBasis.MonotoneCubic, hou.rampBasis.MonotoneCubic, hou.rampBasis.MonotoneCubic, hou.rampBasis.MonotoneCubic, hou.rampBasis.MonotoneCubic) ) 
    ramp_keys.append( (0.0, 0.10000000149011612, 0.20000000298023224, 0.800000011920929, 0.8999999761581421, 1.0) ) 
    ramp_values.append( (0.0, 1.0, 0.0, 0.0, 1.0, 0.0) ) 

    ramp_preset.append( 'sparkle' )
    ramp_basis.append( (hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant, hou.rampBasis.Constant) ) 
    ramp_keys.append( (0.0, 0.011058451607823372, 0.03238546475768089, 0.046603474766016006, 0.056872036308050156, 0.06319115310907364, 0.09557662159204483, 0.12243285775184631, 0.13349130749702454, 0.1548183262348175, 0.17772512137889862, 0.2195892632007599, 0.24802528321743011, 0.2606635093688965, 0.28278040885925293, 0.2898894250392914, 0.3151658773422241, 0.3428120017051697, 0.3649289011955261, 0.36966824531555176, 0.40205371379852295, 0.44312795996665955, 0.5094786882400513, 0.5165876746177673, 0.5394944548606873, 0.5616113543510437, 0.6279621124267578, 0.6327013969421387, 0.6714060306549072, 0.6832543611526489, 0.7930489778518677, 0.8214849829673767, 0.8925750255584717, 0.9028435945510864, 0.9958626627922058, 1.0) ) 
    ramp_values.append( (1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.990338146686554, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.9951691031455994, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0) ) 

    ramp_preset.append( 'bounce' )
    ramp_basis.append( (hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier) ) 
    ramp_keys.append( (0.0, 0.136274516582489, 0.30000001192092896, 0.3700000047683716, 0.48137253522872925, 0.5882353186607361, 0.7137255072593689, 0.772549033164978, 0.8303921818733215, 0.8990195989608765, 0.936274528503418, 0.9637255072593689, 1.0) ) 
    ramp_values.append( (1.0, 0.9427083134651184, 0.5690000057220459, 0.0, 0.34200000762939453, 0.34200000762939453, 0.0, 0.07800000160932541, 0.07800000160932541, 0.0, 0.024000000208616257, 0.024000000208616257, 0.0) ) 

    ramp_preset.append( 'spring' )
    ramp_basis.append( (hou.rampBasis.BSpline, hou.rampBasis.BSpline, hou.rampBasis.BSpline, hou.rampBasis.BSpline, hou.rampBasis.BSpline, hou.rampBasis.BSpline, hou.rampBasis.BSpline, hou.rampBasis.BSpline, hou.rampBasis.BSpline) ) 
    ramp_keys.append( (0.0, 0.15000000596046448, 0.30000001192092896, 0.44999998807907104, 0.550000011920929, 0.6700000166893005, 0.75, 0.8500000238418579, 1.0) ) 
    ramp_values.append( (0.0, 1.149999976158142, 0.09000000357627869, 0.75, 0.3499999940395355, 0.5799999833106995, 0.4699999988079071, 0.5, 0.5) ) 

    #######################

    ramp_preset.append( 'up' )
    ramp_basis.append( (hou.rampBasis.Linear, hou.rampBasis.Linear) ) 
    ramp_keys.append( (0.0, 1.0) ) 
    ramp_values.append( (0.0, 1.0) ) 

    ramp_preset.append( 'up_r' )  # was up_in
    ramp_basis.append( (hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier) ) 
    ramp_keys.append( (0.0, 0.5, 0.949999988079071, 1.0) ) 
    ramp_values.append( (0.0, 0.0, 0.0, 1.0) ) 

    ramp_preset.append( 'up_l' )  # was up_out
    ramp_basis.append( (hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier) ) 
    ramp_keys.append( (0.0, 0.05000000074505806, 0.5, 1.0) ) 
    ramp_values.append( (0.0, 1.0, 1.0, 1.0) ) 

    ramp_preset.append( 'up_rl' ) # was up_inout
    ramp_basis.append( (hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier) ) 
    ramp_keys.append( (0.0, 0.44999998807907104, 0.550000011920929, 1.0) ) 
    ramp_values.append( (0.0, 0.0, 1.0, 1.0) ) 

    ramp_preset.append( 'up_lr' ) # was up_outin
    ramp_basis.append( (hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier) ) 
    ramp_keys.append( (0.0, 0.10000000149011612, 0.8999999761581421, 1.0) ) 
    ramp_values.append( (0.0, 1.0, 0.0, 1.0) ) 

    ########################

    ramp_preset.append( 'dn' )
    ramp_basis.append( (hou.rampBasis.Linear, hou.rampBasis.Linear) ) 
    ramp_keys.append( (0.0, 1.0) ) 
    ramp_values.append( (1.0, 0.0) ) 

    ramp_preset.append( 'dn_r' ) # was dn_in
    ramp_basis.append( (hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier) ) 
    ramp_keys.append( (0.0, 0.5, 0.949999988079071, 1.0) ) 
    ramp_values.append( (1.0, 1.0, 1.0, 0.0) ) 

    ramp_preset.append( 'dn_l' ) # was dn_out
    ramp_basis.append( (hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier) ) 
    ramp_keys.append( (0.0, 0.05000000074505806, 0.5, 1.0) ) 
    ramp_values.append( (1.0, 0.0, 0.0, 0.0) ) 

    ramp_preset.append( 'dn_rl' ) # was dn_inout
    ramp_basis.append( (hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier) ) 
    ramp_keys.append( (0.0, 0.44999998807907104, 0.550000011920929, 1.0) ) 
    ramp_values.append( (1.0, 1.0, 0.0, 0.0) ) 

    ramp_preset.append( 'dn_lr' ) # was dn_outin
    ramp_basis.append( (hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier) ) 
    ramp_keys.append( (0.0, 0.10000000149011612, 0.8999999761581421, 1.0) ) 
    ramp_values.append( (1.0, 0.0, 1.0, 0.0) ) 

    ##########################

    ramp_preset.append( 'tri' )
    ramp_basis.append( (hou.rampBasis.Linear, hou.rampBasis.Linear, hou.rampBasis.Linear) ) 
    ramp_keys.append( (0.0, 0.5, 1.0) ) 
    ramp_values.append( (0.0, 1.0, 0.0) ) 

    ramp_preset.append( 'tri_rl' )
    ramp_basis.append( (hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier) ) 
    ramp_keys.append( (0.0, 0.25, 0.44999998807907104, 0.5, 0.550000011920929, 0.75, 1.0) ) 
    ramp_values.append( (0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0) ) 

    ramp_preset.append( 'tri_lr' )
    ramp_basis.append( (hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier) ) 
    ramp_keys.append( (0.0, 0.10000000149011612, 0.4000000059604645, 0.5, 0.6000000238418579, 0.8999999761581421, 1.0) ) 
    ramp_values.append( (0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0) ) 

    ramp_preset.append( 'tri_rllr' )
    ramp_basis.append( (hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier, hou.rampBasis.Bezier) ) 
    ramp_keys.append( (0.0, 0.23999999463558197, 0.25999999046325684, 0.5, 0.7400000095367432, 0.7599999904632568, 1.0) ) 
    ramp_values.append( (0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0) ) 

    return ramp_preset, ramp_basis, ramp_keys, ramp_values