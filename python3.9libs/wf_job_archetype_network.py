import hou
import json


def ue_export_settings (node) :
    # import imp ; import wf_job_archetype_network ; imp.reload(wf_job_archetype_network) ; node = kwargs["node"] ; wf_job_archetype_network.ue_export_settings(node)


    # ------------ contents -------------
    # job rangex rangey
    # job fps
    # camera resx, resy
    # camera tx, ty, tz, rx, ry, rz, 
    # camera focal distance, aperture


    # ------- sequence settings ----------
    cam_node = node.parm("job_camera").evalAsNode()
    rangex   = node.parm("job_rangex").evalAsString()
    rangey   = node.parm("job_rangey").evalAsString()
    fps      = hou.text.expandString("$FPS")


    # -------    camera TRS    ----------
    # Houdini uses a Y-up right handed coordinate system
    # Unreal  uses a Z-up left handed coordinate system.

    tx = cam_node.parm("tx").eval()
    ty = cam_node.parm("ty").eval()
    tz = cam_node.parm("tz").eval()
    rx = cam_node.parm("rx").eval()
    ry = cam_node.parm("ry").eval()
    rz = cam_node.parm("rz").eval()


    #----    camera UE coordinates  ------
   
    sampleVector = [tx,ty,tz]
    
    # rotation_degrees = 90
    # rotation_radians = np.radians(rotation_degrees)
    # rotation_axis    = np.array([0, 0, 1])
    
    # rotation_vector = rotation_radians * rotation_axis
    # rotation        = R.from_rotvec(rotation_vector)
    # rotated_vector  = rotation.apply(sampleVector)
 
    # print(rotated_vector)
    
    # --------- camera lens ------------





    # --------- camera json ------------

    json_content = {}
    json_content['level_settings'] = {
        'resx': cam_node.parm("resx").evalAsString(),
        'resy': cam_node.parm("resy").evalAsString(),
        'tx'  : cam_node.parm("tx").evalAsString(),
        'ty'  : cam_node.parm("ty").evalAsString(),
        'tz'  : cam_node.parm("tz").evalAsString(),
        'rx'  : cam_node.parm("rx").evalAsString(),
        'ry'  : cam_node.parm("ry").evalAsString(),
        'rz'  : cam_node.parm("rz").evalAsString()
    }


    # ------------ path ----------------

    hip_name = hou.text.expandString("$HIPNAME")
    hip_name = hip_name.split(" ")[0]
    cam_name = node.parm("job_camera").evalAsNode().name()
    job_name = node.name()

    # ------------ path ----------------

    json_path_seq = "Q:/_engine/_json/settings/seq." + hip_name + "." + job_name + ".json"
    json_path_cam = "Q:/_engine/_json/settings/cam." + hip_name + "." + cam_name + ".json"

    # ---------- write files -------------


    with open(json_path_seq, "w") as outfile_seq: 
        json.dump(json_content, outfile_seq, indent=2)
    outfile_seq.close()

    with open(json_path_cam, "w") as outfile_cam: 
        json.dump(json_content, outfile_cam, indent=2)
    outfile_cam.close()









def ue_filemark_to_create_level (node) :
    # import imp ; import wf_job_archetype_network ; imp.reload(wf_job_archetype_network) ; node = kwargs["node"] ; wf_job_archetype_network.ue_filemark_to_create_level(node)


    # ------------ path ----------------

    json_content = {}
    json_content['level_settings'] = {
        'create': 'yes',
    }



    # ------------ path ----------------

    hip_name = hou.text.expandString("$HIPNAME")
    hip_name = hip_name.split(" ")[0]
    job_name = node.name()

    # ------------ path ----------------

    json_path_mark = "Q:/_engine/_json/create/create." + hip_name + "." + job_name + ".json"

    # ---------- write files -------------


    with open(json_path_mark, "w") as outfile_mark: 
        json.dump(json_content, outfile_mark, indent=2)
    outfile_mark.close()

    # ----------    ---     ------------
