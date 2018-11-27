from maya import cmds
import pymel.core as pm

'''
Steps for creating control.
1. Create shape.
2. Orient the shape in the right axis using xform.
3. Group the control to itself and rename.
4. Select shape control group and the joint it is going to control and parent them.
5. Zero out translations and rotations on group.
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
    height = 400
    width = 400

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
        pass

    # Close the Renamer window.
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

        cmds.text(label="Orientation: ", align='left', w=textWidth)


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

        shapeType = pm.radioButtonGrp('shapeType_Btn', q=True, sl=True)
        newShapes = []

        print(str(self.joints))

        # Create controls for all the joints depending on which radio button is selected.
        for joint in self.joints:
            if shapeType == 1:
                name = joint.split('_')[0] + "_ctrl"
                newShapes.append(self.pickShape('Circle', name))
            elif shapeType == 2:
                name = joint.split('_')[0] + "_ctrl"
                newShapes.append(self.pickShape('Box', name))


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
