#import hou
#hou.appendSessionModuleSource('''hou.hscript("autosave on")''')

desktops_dict = dict((d.name(), d) for d in hou.ui.desktops())
desktops_dict['IKOON_1_left_bottom'].setAsCurrent()
desktops_dict['IKOON_4_left_top'].setAsCurrent()
desktops_dict['IKOON_5_center'].setAsCurrent()
desktops_dict['IKOON_6_right'].setAsCurrent()
## and this will be actual:
#desktops_dict['test'].setAsCurrent()


#hou.ui.desktop("test").findPaneTab("panetab7").pane().setSplitFraction(0.5)
#hou.ui.desktop("test").findPaneTab("panetab7").pane().setIsSplitMaximized(True)

#print "ok"