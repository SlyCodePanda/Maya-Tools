from maya import cmds
import pymel.core as pm
from collections import OrderedDict

'''
Steps taken to create control(s).
1. Create shape.
2. Orient the shape in the right axis using setattr.
3. Group the control to itself and rename.
4. Select shape control group and the joint it is going to control and parent them.
5. Zero out translations and rotations on group.
6. Un-parent joint and control group.
7. Parent controls under each-other if checkbox is set to True.
8. Parent constraint joints to controls.

# TODOs
* Add ability for user to set naming format?
* Clean up un-necessary code.
* Fix unique naming issue.
* Have it so you can only select one of the checkboxes at a time.

# Nice TODOs
* Add colour picker to change the shapes colour.
* Give option to add to new layer.
* Add more shapes (arrow, star, etc..)
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
    height = 100
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
        textWidth = 90
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

        # Set shape scale.
        cmds.rowLayout(numberOfColumns=4)
        cmds.text(label="Scale: ", align='left', w=textWidth)
        self.xVal = cmds.textField("xScale", ann="X-axis", text=1, w=textWidth)
        self.yVal = cmds.textField("yScale", ann="Y-axis", text=1, w=textWidth)
        self.zVal = cmds.textField("zScale", ann="Z-axis", text=1, w=textWidth)


        cmds.setParent('..')

        # Set shape orientation.
        cmds.rowLayout(numberOfColumns=4)
        cmds.text(label="Orientation: ", align='left', w=textWidth)
        cmds.textField("xOrient", ann="X-axis", text=0, w=textWidth)
        cmds.textField("yOrient", ann="Y-axis", text=0, w=textWidth)
        cmds.textField("zOrient", ann="Z-axis", text=0, w=textWidth)

        cmds.setParent('..')

        # Select whether you want to parent the chain of controls and their groups.
        cmds.rowLayout(numberOfColumns=3)
        cmds.checkBox('parentControls_checkBox', label="Parent controls under each other")

        # Select whether the control we are building is intended as a Pole Vector control.
        cmds.checkBox('poleVector_checkBox', label="Pole Vector")

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
        #cmds.selectPref(tso=True)
        self.joints = cmds.ls(sl=True)

        # Gets the type of shape we want to create.
        shapeType = pm.radioButtonGrp('shapeType_Btn', q=True, sl=True)
        # List of new shapes created.
        newShapes = []

        # Dictionaries
        jointShapes = OrderedDict()
        jointGroups = {}

        # List of items that will be used to group under each other.
        controlAndGroup = []

        print("LIST OF JOINTS SELECTED : " + str(self.joints))

        # TODO : Need to figure out a way to only allow for unique names to be created.

        # Create controls for all the joints depending on which radio button is selected.
        # Currently outputs an error when trying to create multiple controls at the same joint.
        for joint in self.joints:
            print("CUR JOINT : " + joint)
            if shapeType == 1:
                #name = joint.split('_')[1] + "_ctrl"
                name = joint + "_ctrl"

                # Checks if this control should be a pole vector naming convention.
                if cmds.checkBox('poleVector_checkBox', q=True, value=True):
                    name = joint.split('_')[0] + "_poleVector_ctrl"

                # Check if name already exists.
                elif cmds.objExists(name):
                    cmds.error(name + " : Trying to create a shape with the same name."
                                      "Please change the name of previously built shape..")
                    return

                self.pickShape('Circle', name)
                newShapes.append(name)
                jointShapes.update({joint : name})

            elif shapeType == 2:
                #name = joint.split('_')[1] + "_ctrl"
                name = joint + "_ctrl"

                # Checks if this control should be a pole vector naming convention.
                if cmds.checkBox('poleVector_checkBox', q=True, value=True):
                    name = joint.split('_')[0] + "_poleVector_ctrl"

                # Check if name already exists.
                elif cmds.objExists(name):
                    cmds.error(name + " : Trying to create a shape with the same name."
                                      "Please change the name of previously built shape..")
                    return

                self.pickShape('Box', name)
                newShapes.append(name)
                jointShapes.update({joint: name})

        # Set Orientations.
        self.xVal = float(cmds.textField("xOrient", q=True, text=True))
        self.yVal = float(cmds.textField("yOrient", q=True, text=True))
        self.zVal = float(cmds.textField("zOrient", q=True, text=True))

        for shape in newShapes:
            if self.xVal != 0.0:
                cmds.setAttr(shape + '.rotateX', self.xVal)
            elif self.yVal != 0.0:
                cmds.setAttr(shape + '.rotateY', self.yVal)
            elif self.zVal != 0.0:
                cmds.setAttr(shape + '.rotateZ', self.zVal)

        # Set Scale.
        xScale = float(cmds.textField("xScale", q=True, text=True))
        yScale = float(cmds.textField("yScale", q=True, text=True))
        zScale = float(cmds.textField("zScale", q=True, text=True))

        for shape in newShapes:
            cmds.setAttr(shape + '.scaleX', xScale)
            cmds.setAttr(shape + '.scaleY', yScale)
            cmds.setAttr(shape + '.scaleZ', zScale)

        # Group and rename.
        for key, value in jointShapes.items():
            cmds.group(value, n=value + 'Grp')
            jointGroups.update({key : value + 'Grp'})
            # Add the control and it's group to a list in the order that we will need to group them.
            controlAndGroup.insert(0, value +'Grp')
            controlAndGroup.insert(0, value)

        # Check list of group and control items.
        print("Control and Group Pairs")
        print(controlAndGroup)

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

        # Parent controls and groups under each other.
        # Iterate through the list and group the items up the chain IF the checkbox is on.
        if cmds.checkBox('parentControls_checkBox', q=True, value=True):
            for index in range(len(controlAndGroup)):
                if self.isGroup(controlAndGroup[index]) and index != len(controlAndGroup)-1:
                    print("Group " + controlAndGroup[index] + " to " + controlAndGroup[index+1])
                    cmds.parent(controlAndGroup[index], controlAndGroup[index+1])

            # Parent constraint control to joints IF checkbox is on.
            print("Control and Joint Pairs : ")
            print(jointShapes)
            for key, value in jointShapes.items():
                cmds.parentConstraint(value, key)

    ########################
    # Helper functions
    ########################

    # Returns the right curve based on the shape name passed, also names it according to name passed.
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

    # Returns True if node is a group, False otherwise.
    def isGroup(self, node):
        if cmds.nodeType(node) != "transform":
            return False

        children = cmds.listRelatives(node, children=True)

        if children is None:
            return True

        for child in children:
            if cmds.nodeType(child) != 'transform':
                return False
        else:
            return True
