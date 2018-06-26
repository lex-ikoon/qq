*This repository is described here: http://lex.ikoon.cz*

*I hope that some of the Python or VEX functions will help you. Some of them are mine, some of them are collected and I [THANK YOU](http://lex.ikoon.cz/thanks/) very much, all the authors and great community. I could not do this without you. I will record a video description asap.*
&nbsp;  
&nbsp;  

# files and folders 

#### toolbar
- this folder contains:
    - one **shelf set** (`wf__set.shelf`)
    - twelve shelves (`wf_chaneditor.shelf`, `wf_render.shelf`, etc.)
- each shelve contains tools, and each tool calls a specific function
- some of the tools have their hotkey, other are accessible by the TAB menu
&nbsp;  
&nbsp;  
&nbsp;  
#### python2.7libs
- this folder contains python functions
- here is described what each function does: 
  - http://lex.ikoon.cz/network_parm
  - http://lex.ikoon.cz/network_ui
  - etc.
- this folder is **necessary** for the shelf (toolbar) to work
&nbsp;  
&nbsp;  
&nbsp;  
#### vex
- this folder contains:
  - `uber.vfl` - a source for "uber parse" as described here: http://lex.ikoon.cz/vex-uber-parse
  - `qq.vfl` - library of custom functions, to be #included in a wrangle
  - `triggers.db` - library of triggers, more described here: http://lex.ikoon.cz/vex-ui-markup
  - `snippets.db` - library of snippets
  - `helpcard.txt` - just a helpcard
- this folder is **not** necessary for the shelf to work
&nbsp;  
&nbsp;  
&nbsp;  
#### Houdini.keymap.overrides
- this file is set of my custom hotkeys
- You probably dont want to import the file 1:1 as it is. I recommend you to look inside the file and check it.
- this folder is **not** necessary for the shelf to work
&nbsp;  
&nbsp;  
&nbsp;  
#### PARMmenu.xml
- this file customizes the Parameter context menu (right click on any Parameter)
- this folder is **not** necessary for the shelf to work
&nbsp;  
&nbsp;  
&nbsp;  
# instalation
- copy the files (which you really want) into `$HOUDINI_USER_PREF_DIR`
- on Windows it is typically `C:\Users\your_user_name\Documents\houdini16.5`
- restart Houdini
- if you copied the `toolbar` and `python2.7libs` folder, you can enable the shelf as in this gif (`Shelf Sets > workflow__set`)

![enable-shelf](http://lex.ikoon.cz/images/install/enable-shelf.gif)
