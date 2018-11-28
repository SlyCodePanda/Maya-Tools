from maya import cmds
import pymel.core as pm

'''
Steps for creating control.
1. Create shape. X
2. Orient the shape in the right axis using setattr. X
3. Group the control to itself and rename. X
4. Select shape control group and the joint it is going to control and parent them. X
5. Zero out translations and rotations on group. X
6. Un-parent joint and control group.
'''


# Create controls for selected joints.
class controlBuilder(object):

    def __init__(self):
        pass

    ########################
    # UI functions
    ########################

    windowName = "RigControlBuilder"
    scriptName = 'controlBuilder'
    height = 80
    width = 400
    xVal = 0
    yVal = 0
    zVal = 0

    def show(self):
        # If a window named "RigControlBuilder" already exists, delete the UI.
        if cmds.window(self.windowName, query=True, exists=True):
            cmds.deleteUI(self.windowName)

        # Create the window, build the UI, then show the window.
        self.window = cmds.window(self.windowName, w=self.width, h=self.height, mnb=False, mxb=False, sizeable=False)
        self.buildUI()
        cmds.showWindow()
        cmds.setFocus(self.windowName)

    # Reset all text fields.
    def reset(self, *args):
        cmds.textField("xOrient", edit=True, text=0)
        cmds.textField("yOrient", edit=True, text=0)
        cmds.textField("zOrient", edit=True, text=0)

    # Close the window.
    def close(self, *args):
        cmds.deleteUI(self.windowName)

    def buildUI(self):
        textWidth = 80
        buttonWidth = 197

        cmds.setParent(self.window)

        # Main layout.
        mainColumnLayout = cmds.columnLayout(w=self.width, h=self.height)

        # Set shape type.
        cmds.rowLayout(numberOfColumns=3)
        cmds.text(label="Shape type: ", align='left', w=textWidth)
        pm.radioButtonGrp("shapeType_Btn", labelArray2=('Circle', 'Box'), numberOfRadioButtons=2,
                          columnWidth3=[50, 50, 50], select=1)

        cmds.setParent('..')

        # Set shape orientation.
        cmds.rowLayout(numberOfColumns=4)
        cmds.text(label="Orientation: ", align='left', w=textWidth)
        self.xVal = cmds.textField("xOrient", ann="X-axis", text=0, w=textWidth)
        self.yVal = cmds.textField("yOrient", ann="Y-axis", text=0, w=textWidth)
        self.zVal = cmds.textField("zOrient", ann="Z-axis", text=0, w=textWidth)

        cmds.setParent('..')

        # Create shape.
        cmds.rowLayout(numberOfColumns=2)
        pm.button(label="Create", align='right', command=self.createShapes, width=buttonWidth)
        pm.button(label="Reset", align='right', command=self.reset, width=buttonWidth)


    ########################
    # Builder functions
    ########################

    def createShapes(self, *args):
        # Get selected joint(s)
        self.joints = cmds.ls(sl=True)

        # Gets the type of shape we want to create.
        shapeType = pm.radioButtonGrp('shapeType_Btn', q=True, sl=True)
        # List of new shapes created.
        newShapes = []

        jointShapes = {}
        jointGroups = {}

        print(str(self.joints))

        # Create controls for all the joints depending on which radio button is selected.
        for joint in self.joints:
            if shapeType == 1:
                name = joint.split('_')[0] + "_ctrl"
                self.pickShape('Circle', name)
                newShapes.append(name)
                jointShapes.update({joint : name})
            elif shapeType == 2:
                name = joint.split('_')[0] + "_ctrl"
                self.pickShape('Box', name)
                newShapes.append(name)
                jointShapes.update({joint: name})

        # Set Orientations.
        self.xVal = float(cmds.textField("xOrient", q=True, text=True))
        self.yVal = float(cmds.textField("yOrient", q=True, text=True))
        self.zVal = float(cmds.textField("zOrient", q=True, text=True))

        for shape in newShapes:
            cmds.setAttr(shape + '.rotateX', self.xVal)
            cmds.setAttr(shape + '.rotateY', self.yVal)
            cmds.setAttr(shape + '.rotateZ', self.zVal)

        # Group and rename.
        for key, value in jointShapes.items():
            cmds.group(value, n=value + 'Grp')
            jointGroups.update({key : value + 'Grp'})

        # Parent, zero out translations and rotations, and un-parent.
        for key, value in jointGroups.items():
            cmds.parent(value, key)
            cmds.setAttr(value + '.translateX', 0)
            cmds.setAttr(value + '.translateY', 0)
            cmds.setAttr(value + '.translateZ', 0)
            cmds.setAttr(value + '.rotateX', 0)
            cmds.setAttr(value + '.rotateY', 0)
            cmds.setAttr(value + '.rotateZ', 0)
            cmds.parent(value, world=True)

    def pickShape(self, shape, name):
        if shape == 'Circle':
            # Circle shape control.
            circle = pm.circle(n=name, nr=[0, 1, 0])
            return circle
        elif shape == 'Box':
            # Box/cube shape control.
            box = pm.curve(n=name, d=1,
                              p=[(1, 1, 1), (1, 1, -1), (-1, 1, -1), (-1, 1, 1), (1, 1, 1), (1, -1, 1),
                                 (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1), (1, -1, -1),
                                 (-1, -1, -1), (-1, -1, 1), (-1, 1, 1), (-1, -1, 1), (1, -1, 1)],
                              k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
            return box

