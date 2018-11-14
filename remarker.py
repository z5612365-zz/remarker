#run this on maya python script
from tool.remarker.remarker import GUI_PySide_LoadFrom_QtUI as gui

reload(gui)
cameraShaker = gui.PyQtMayaWindow()
cameraShaker.run()

