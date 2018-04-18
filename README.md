# Project Title

One Paragraph of project description goes here

```python
def node_global () :
    color = hou.Color(0.0, 0.0, 0.0)
    path = "/obj/global"
    name = "global"
    
    if hou.node(path) :
        existed = 1
        return hou.node(path)
    else :
        existed = 0
        node_global = hou.node("/obj").createNode('null',name)
        node_global.moveToGoodPosition()
        node_global.setUserData("nodeshape", "circle")
        node_global.setColor(color)
        return node_global
```
