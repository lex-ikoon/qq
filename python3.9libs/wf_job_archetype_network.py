import hou
import json
# import math
# import numpy




# def rotation_matrix(axis, theta):
#     """
#     Return the rotation matrix associated with counterclockwise rotation about
#     the given axis by theta radians.
#     """
#     axis = numpy.asarray(axis)
#     axis = axis / math.sqrt(numpy.dot(axis, axis))
#     a    = math.cos(theta / 2.0)

#     b, c, d = -axis * math.sin(theta / 2.0)
#     aa, bb, cc, dd = a * a, b * b, c * c, d * d
#     bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    
#     return numpy.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
#                      [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
#                      [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])



def ue_export_settings (node) :
    # import imp ; import wf_job_archetype_network ; imp.reload(wf_job_archetype_network) ; node = kwargs["node"] ; wf_job_archetype_network.ue_export_settings(node)


    # ------------ contents -------------
    # job rangex rangey
    # job fps
    # camera resx, resy
    # camera tx, ty, tz, rx, ry, rz, 
    # camera focus_distance 
    # camera focal_length


    # -------   camera node ----------
    cam_node = node.parm("job_camera").evalAsNode()

    # -------   camera TRS    ----------

    tx = cam_node.parm("tx").eval()
    ty = cam_node.parm("ty").eval()
    tz = cam_node.parm("tz").eval()
    rx = cam_node.parm("rx").eval()
    ry = cam_node.parm("ry").eval()
    rz = cam_node.parm("rz").eval()


    #---------  camera UE coordinates  ------
    # Houdini uses a Y-up right handed coordinate system
    # Unreal  uses a Z-up left handed coordinate system.
    # Houdini   0 0   5      0   0     0
    # Unreal    0 500 0      0   0    -90

    # Houdini   0 0   -5     0   180  0
    # Unreal    0 -500 0     0   0    90


    # Houdini   5   0 0      0 -270  0
    # Unreal    500 0 0      0   0 -180


    # position
    ue_tx = 100 * tx
    ue_ty = 100 * tz
    ue_tz = 100 * ty


    # rotation
    
    cam_UP_axis       = [0, 1, 0]
    cam_matrix        = cam_node.worldTransform()
    cam_UP_world      = hou.Vector3(hou.Vector4(tuple(cam_UP_axis) + (0.0,)) * cam_matrix)

    turn_90_around_UP = hou.hmath.buildRotateAboutAxis(cam_UP_world, 90)
    cam_matrix_cam    = cam_matrix * turn_90_around_UP

    quat_H = hou.Quaternion(cam_matrix_cam)
    # tests:
    # quat_H = hou.Quaternion(hou.hmath.buildRotate((45, 0, 0), "yxz"))

    x      = quat_H[0]
    y      = quat_H[1]
    z      = quat_H[2]
    w      = quat_H[3]

    quat_UE  = hou.Quaternion(x, z, -y, w)
    euler_UE = quat_UE.extractEulerRotates()

    ue_rx = euler_UE[0]
    ue_ry = euler_UE[1]
    ue_rz = euler_UE[2]



    # print(euler_UE)
    # turn_90_around_X  = hou.hmath.buildRotateAboutAxis(hou.Vector3(1, 0, 0), 90)
    # scale_Z           = hou.hmath.buildScale(1, 1, -1)
    # cam_matrix_rotated = cam_matrix_cam * turn_90_around_X
    # cam_matrix_scaled  = cam_matrix_rotated * scale_Z
    # print (hou.Matrix4.extractRotates(cam_matrix_scaled))

    # --------- focal length --------------
    
    ue_resx         = cam_node.parm("resx").eval()
    ue_resy         = cam_node.parm("resy").eval()
    focal_length    = cam_node.parm("focal").eval()
    resx            = cam_node.parm("aperture").eval()
    ratio           = resx / focal_length
    ue_focal_length = ue_resx / ratio


    # --------- focus distance ------------

    focus_distance    = cam_node.parm("focus").eval()
    ue_focus_distance = focus_distance * 100


    # --------- camera json ------------

    json_content = {}
    json_content['level_settings'] = {

        # --------- camera sensor ------------

        'focus_distance': ue_focus_distance,
        'focal_length'  : ue_focal_length,
        'resx'          : ue_resx,
        'resy'          : ue_resy,

        # --------- sequencer  ------------

        'rangex': node.parm("job_rangex").evalAsString(),
        'rangey': node.parm("job_rangey").evalAsString(),
        'fps'   : hou.text.expandString("$FPS"),

        # --------- cam coordinates  ---------

        'tx'  : ue_tx,
        'ty'  : ue_ty,
        'tz'  : ue_tz,
        'rx'  : ue_rx,
        'ry'  : ue_ry,
        'rz'  : ue_rz
    }


    # ------------ path ----------------

    hip_name = hou.text.expandString("$HIPNAME")
    hip_name = hip_name.split(" ")[0]
    cam_name = node.parm("job_camera").evalAsNode().name()
    job_name = node.name()

    # ------------ path ----------------

    json_path_seq = "Q:/_engine/_json/settings/seq." + hip_name + "." + job_name + ".json"
    # json_path_cam = "Q:/_engine/_json/settings/cam." + hip_name + "." + cam_name + ".json"

    # ---------- write files -------------


    with open(json_path_seq, "w") as outfile_seq: 
        json.dump(json_content, outfile_seq, indent=2)
    outfile_seq.close()

    # with open(json_path_cam, "w") as outfile_cam: 
    #     json.dump(json_content, outfile_cam, indent=2)
    # outfile_cam.close()








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
