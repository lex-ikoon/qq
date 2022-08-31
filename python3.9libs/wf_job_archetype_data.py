import hou


def job_data_update_range_descriptiveparm (node) :
    # callback script:
    # import wf_job_archetype_data ; node = kwargs["node"] ; wf_job_archetype_data.job_data_update_range_descriptiveparm(node)
    if node.parm("job_range_single_file").eval() == 1:
        description = "- " + node.parm( "job_rangex").evalAsString() + " -"
    else :
        description = node.parm( "job_rangex").evalAsString() + " - " + node.parm("job_rangey").evalAsString()
    node.parm("job_range_descriptiveparm").set(description)


def job_data_rename(node) :
    print ("rename")
    # callback script:
    # import wf_job_archetype_data ; node = kwargs["node"] ; wf_job_archetype_data.job_data_rename(node)

    # geo_data
    # o_merged null
    # rs_rop
    # gl_rop
    pass
