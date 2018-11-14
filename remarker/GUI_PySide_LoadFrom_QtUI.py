import maya.cmds as cmds
import maya.mel as mel
from PySide2 import QtCore, QtWidgets
import time

from . import loadUiWidget


class PyQtMayaWindow(QtWidgets.QMainWindow):

    def __init__(self):

        #self.app = QtWidgets.QApplication.instance()
        self.MainWindow = loadUiWidget.loadUiWidget().loadUiWidget('/home/chi/maya/scripts/tool/remarker/resource/main.ui')
        #self.MainWindow = self.loadUiWidget('/home/chi/maya/scripts/tool/cameraShaker/resource/main.ui')

        self.init_UI()
        self.SignalSlotLinker()

        #print ("isChecked"+str(self.checkBox.isChecked() ) )
        #print ("isChecked"+str(self.checkBox2.isChecked() ) )


    # ----------------------------------------------- run & show -----------------------------------------------
    def run(self):

        self.MainWindow.show()
        #self.app.exec_()

    def show(self):
        self.MainWindow.show()

    # ----------------------------------------------- init UI stuf -----------------------------------------------
    def init_UI(self):
        self.btn = self.getUIElement(QtWidgets.QPushButton,"pushButton")
        self.lineEdit = self.getUIElement(QtWidgets.QLineEdit,"lineEdit")
        self.lineEdit2 = self.getUIElement(QtWidgets.QLineEdit,"lineEdit_2")
        self.lineEdit3 = self.getUIElement(QtWidgets.QLineEdit,"lineEdit_3")

        self.lineEdit4 = self.getUIElement(QtWidgets.QLineEdit,"lineEdit_4")
        self.lineEdit5 = self.getUIElement(QtWidgets.QLineEdit,"lineEdit_5")

        self.textEdit = self.getUIElement(QtWidgets.QTextEdit,"textEdit")


        self.btn2 = self.getUIElement(QtWidgets.QPushButton,"pushButton_2")



    def SignalSlotLinker(self):

        self.btn.clicked.connect( self.slot1)

        self.btn2.clicked.connect( self.addNote)




    # ----------------------------------------------- slot function -----------------------------------------------
    def slot1(self):

        self.load_camera_setting()
        self.lineEdit.setText(self.cam)
        print(self.cam)
        print("QQ")


    def load_camera_setting(self):

        self.cam = self.getCamName()
        if self.cam == "":
            print("fk")



    def updateLineEdit(self):
        ""

    # ----------------------------------------------- get func -----------------------------------------------
    def getCamName(self):

        camSel = ''.join(cmds.ls(sl=True) )

        return camSel


    def getRelShape(self,ele):
        camShape = ''.join(cmds.listRelatives(ele)[0] )
        return camShape

    def getUIElement(self,type,element):
        return self.MainWindow.findChild(type, element)

    # ----------------------------------------------- tool func -----------------------------------------------


    def addNote(self):
        self.setting()
        self.addWord()
        self.addPlane()
        self.groupWordPlane()

        self.addCurve()
        self.groupAllNoteStuff()

        self.setAlwaysFaceCamera()

    def setting(self):
        self.margin_w=float(self.lineEdit2.text())
        self.margin_h=float(self.lineEdit3.text())
        self.plane_content=self.textEdit.toPlainText()

        self.fontSize=float(self.lineEdit4.text())
        self.fontDepth=float(self.lineEdit5.text())
        self.extrudeDivisions=1
        self.extrudeDistance=self.fontDepth

        #self.contentShape
        #self.content


    def addPlane(self):

        self.plane_w=self.margin_w*2+(self.contentbb[3]-self.contentbb[0])
        self.plane_h=self.margin_h*2+(self.contentbb[4]-self.contentbb[1])

        #plane
        self.plane=cmds.polyPlane(sx=1, sy=1, w=self.plane_w, h=self.plane_h)
        cmds.setAttr(self.plane[0] + '.translateZ', self.plane_h/2)

        cmds.refresh()

    def addWord(self):

        # word init
        mel.eval("typeCreateText")
        self.contentShape = ''.join(cmds.ls(sl=True))
        self.content = cmds.listRelatives(self.contentShape, p=True)
        cmds.refresh()

        # word setting
        cmds.setAttr('type' + self.contentShape[len(self.contentShape) - 1:] + '.fontSize', self.fontSize)
        cmds.setAttr('typeExtrude' + self.contentShape[len(self.contentShape) - 1:] + '.extrudeDivisions', self.extrudeDivisions)
        cmds.setAttr('typeExtrude' + self.contentShape[len(self.contentShape) - 1:] + '.extrudeDistance', self.extrudeDistance)

        self.contentbb_t = cmds.xform(self.content, q=True, bb=True)


        # word content
        content_hex = self.transform_utf8_hex(self.plane_content)
        cmds.setAttr('type' + self.contentShape[len(self.contentShape) - 1:] + '.textInput', content_hex, type='string')

        cmds.refresh()

        # word content
        self.contentbb = cmds.xform(self.content, q=True, bb=True)
        self.word_half_w=(self.contentbb[3]-self.contentbb[0])/2
        self.word_half_h=(self.contentbb[4]-self.contentbb[1])/2

        cmds.setAttr(self.content[0] + '.rx', -90)
        cmds.setAttr(self.content[0] + '.translateY', 0.01)
        cmds.setAttr(self.content[0] + '.translateX', self.word_half_w*-1)
        #cmds.setAttr(self.content[0] + '.translateZ', (self.contentbb_t[4] - self.contentbb_t[1]) / 2 + self.plane_h/2)
        cmds.setAttr(self.content[0] + '.translateZ', (self.contentbb_t[4] - self.contentbb_t[1]) / 2 + self.margin_h)
        cmds.refresh()

    def groupWordPlane(self):
        self.group=cmds.group(self.content[0], self.plane[0], n='note')
        cmds.setAttr(self.group + '.rx', 90)

        cmds.setAttr(self.group + '.translateZ', self.plane_h/2*-1)

    def addCurve(self):

        self.curve = cmds.curve(d=1, p=[(0, 0, 0), (0, 0, 0)])
        c0 = self.curve + ".ep[0]"
        self.locator0 = cmds.pointCurveConstraint(c0, rpo=True, ch=True, w=1)
        c1 = self.curve + ".ep[1]"
        self.locator1 = cmds.pointCurveConstraint(c1, rpo=True, ch=True, w=1)


        cmds.xform( self.locator0,cp=True )
        cmds.xform( self.locator1,cp=True )

        #WordPlane and locator1 parent
        note = cmds.xform(self.group, q=True, bb=True)
        cmds.xform(self.locator1, t=((note[0] + note[3]) / 2, note[1]-1 , (note[2] + note[5]) / 2))

        #t_object and locator0 parent
        t_object = cmds.xform(self.lineEdit.text(), q=True, bb=True)
        cmds.xform(self.locator0, t=((t_object[0] + t_object[3]) / 2, (t_object[4] + 1), (t_object[2] + t_object[5]) / 2))



        #cmds.xform(self.group, t=((t_object[0] + t_object[3]) / 2, (t_object[4] + 1), (t_object[2] + t_object[5]) / 2))

    def groupAllNoteStuff(self):
        self.group=cmds.group(self.group, self.plane[0], self.curve, self.locator0, self.locator1, n='noteG')

        cmds.parentConstraint(self.group, self.locator1, w=1, mo=1)
        cmds.parentConstraint(self.lineEdit.text(), self.locator0, w=1, mo=1)

    def setAlwaysFaceCamera(self):
        cameraName = cmds.camera()
        cmds.parentConstraint(cameraName, self.group, st=["x", "y", "z"], w=1)



    def transform_utf8_hex(self,str):
        return " ".join("{:02x}".format(ord(c)) for c in str)



if __name__ == '__main__':

    pyQtWindow=PyQtMayaWindow()

    pyQtWindow.run()


