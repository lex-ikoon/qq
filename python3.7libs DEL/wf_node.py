#import hou



def lastDescendant (self) :

    while 
    try :
        last_descendant = node.outputs()[0]
    except :
        last_descendant = node


    if last_descendant == node :
        return node
    else :
        return lastDescendant(last_descendant)

        
hou.Node.lastDescendant() = lastDescendant()



def func(my_list, z):

    if z == len(my_list):
        return something
    else:
        # do something else
        return func(my_list, z+1)