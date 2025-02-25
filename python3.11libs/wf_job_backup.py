def copypaste_ptg_folder( which_folder, insert_before_folder, node_src, node_dst ) :

    ptg_dst = node_dst.parmTemplateGroup()
    ptg_src = node_src.parmTemplateGroup()

    # remove target folder if already exists
    try:
        ptg_dst.remove(  ptg_dst.findFolder( which_folder )  )
        node_dst.setParmTemplateGroup(ptg_dst)
    except:
        pass
    
    # find and insert the folder, set PTG
    cargo    = ptg_src.findFolder( which_folder )
    location = ptg_dst.findFolder( insert_before_folder )
    # :) debug in 20.5.487 
    # print ("cargo: ")
    # print (cargo)
    # print ("location: ")
    # print (location)
    # ptg_dst.insertBefore( 0 , cargo )
    ptg_dst.insertBefore( location , cargo )
    node_dst.setParmTemplateGroup(ptg_dst)


:::::::::::::::::DEBUG::::::::::::


def copypaste_ptg_folder( which_folder, insert_before_folder, node_src, node_dst ) :

node_src = hou.node('/obj/rivet1')
node_dst = hou.node('/obj/geo1')

ptg_src = node_src.parmTemplateGroup()
ptg_dst = node_dst.parmTemplateGroup()

which_folder = "Rivet"
insert_before_folder = "Transform"

cargo    = ptg_src.findFolder( which_folder )
location = ptg_dst.findFolder( insert_before_folder )

print(cargo)
print(location)

    # ptg_dst.insertBefore( location , cargo )
    # node_dst.setParmTemplateGroup(ptg_dst)

