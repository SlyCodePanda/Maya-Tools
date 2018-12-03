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
* Add more error messaging.

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
    height = 120
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
        cmds.textField("xOrient", edit=True, text=0)
        cmds.textField("yOrient", edit=True, text=0)
        cmds.textField("zOrient", edit=True, text=0)

        cmds.textField("xScale", edit=True, text=1)
        cmds.textField("yScale", edit=True, text=1)
        cmds.textField("zScale", edit=True, text=1)

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
        cmds.optionMenu("shapeType_optionMenu", label='Shape Type')
        cmds.menuItem(label='Circle')
        cmds.menuItem(label='Box')
        cmds.menuItem(label='Sphere')
        cmds.menuItem(label='Diamond')

        cmds.setParent('..')

        # Set shape scale.
        cmds.rowLayout(numberOfColumns=4)
        cmds.text(label="Scale: ", align='left', w=textWidth)
        cmds.textField("xScale", ann="X-axis", text=1, w=textWidth)
        cmds.textField("yScale", ann="Y-axis", text=1, w=textWidth)
        cmds.textField("zScale", ann="Z-axis", text=1, w=textWidth)


        cmds.setParent('..')

        # Set shape orientation.
        cmds.rowLayout(numberOfColumns=4)
        cmds.text(label="Orientation: ", align='left', w=textWidth)
        cmds.textField("xOrient", ann="X-axis", text=0, w=textWidth)
        cmds.textField("yOrient", ann="Y-axis", text=0, w=textWidth)
        cmds.textField("zOrient", ann="Z-axis", text=0, w=textWidth)

        cmds.setParent('..')

        # Select whether this control is a singular control, a pole vector or you want to parent them under each other.
        cmds.rowLayout(numberOfColumns=4)
        cmds.radioButtonGrp('parentAndPole_radiobuttonGrp', numberOfRadioButtons=3, cw=[1, 120], select=1,
                         labelArray3=['Singular Control', 'Parent Controls', 'Pole Vector'])

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

        # Return an error if there are no joints selected.
        if not self.joints:
            cmds.error("Please select joint(s) to creates shapes for.")
            return

        # Gets the type of shape we want to create.
        shapeType = pm.optionMenu('shapeType_optionMenu', q=True, sl=True)
        # List of new shapes created.
        newShapes = []

        # Dictionaries
        jointShapes = OrderedDict()
        jointGroups = {}

        # List of items that will be used to group under each other.
        controlAndGroup = []

        # TODO : Need to figure out a way to only allow for unique names to be created.

        # Create controls for all the joints depending on which radio button is selected.
        for joint in self.joints:

            # If item in the joints list is not a joint, return an error.
            if not cmds.objectType(joint, isType="joint"):
                cmds.error("The list of joints you have selected contains a non-joint.")
                return
            
            name = joint + "_ctrl"

            # Checks if this control should be a pole vector naming convention.
            if cmds.radioButtonGrp('parentAndPole_radiobuttonGrp', q=True, sl=True) == 3:
                name = joint.split('_')[0] + "_poleVector_ctrl"
                if cmds.objExists(name):
                    cmds.select(name)
                    # Generate a new name based off of old obj.
                    newName = cmds.rename(name + "_#")
                    cmds.rename(name)
                    print(newName)
                    name = newName

            # Check if name already exists, if it does rename it with a unique number on the end.
            elif cmds.objExists(name):
                cmds.select(name)
                # Generate a new name based off of old obj.
                newName = cmds.rename(name+"_#")
                cmds.rename(name)
                print(newName)
                name = newName

            print("The Name is : " + name)
            self.pickShape(shapeType, name)
            newShapes.append(name)
            jointShapes.update({joint : name})
            print("jointShapes : " + str(jointShapes))
            print("newShapes : " + str(newShapes))

        # New way of creation that allows for renaming properly if already exists.
        # for joint in self.joints:
        #     name = joint + "_ctrl"
        #
        #     if cmds.objExists(name):
        #         cmds.select(name)
        #         # Generate a new name based off of old obj.
        #         newName = cmds.rename(name+"_#")
        #         cmds.rename(name)
        #         print(newName)
        #         return
        #     else:
        #         self.pickShape(shapeType, name)
        #         newShapes.append(name)
        #         jointShapes.update({joint : name})

        # Set Orientations.
        xOri = float(cmds.textField("xOrient", q=True, text=True))
        yOri = float(cmds.textField("yOrient", q=True, text=True))
        zOri = float(cmds.textField("zOrient", q=True, text=True))

        for shape in newShapes:
            cmds.setAttr(shape + '.rotateX', xOri)
            cmds.setAttr(shape + '.rotateY', yOri)
            cmds.setAttr(shape + '.rotateZ', zOri)

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
        if cmds.radioButtonGrp('parentAndPole_radiobuttonGrp', q=True, sl=True) == 2:
            for index in range(len(controlAndGroup)):
                if self.isGroup(controlAndGroup[index]) and index != len(controlAndGroup)-1:
                    cmds.parent(controlAndGroup[index], controlAndGroup[index+1])

            # Parent constraint control to joints IF checkbox is on.
            for key, value in jointShapes.items():
                cmds.parentConstraint(value, key)

    ########################
    # Helper functions
    ########################

    # Returns the right curve based on the shape name passed, also names it according to name passed.
    def pickShape(self, shape, name):
        if shape == 1:
            # Circle shape control.
            circle = pm.circle(n=name, nr=[0, 1, 0])
            return circle
        elif shape == 2:
            # Box/cube shape control.
            box = pm.curve(n=name, d=1,
                              p=[(1, 1, 1), (1, 1, -1), (-1, 1, -1), (-1, 1, 1), (1, 1, 1), (1, -1, 1),
                                 (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1), (1, -1, -1),
                                 (-1, -1, -1), (-1, -1, 1), (-1, 1, 1), (-1, -1, 1), (1, -1, 1)],
                              k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
            return box
        elif shape == 3:
            sphere = cmds.sphere(name=name, po=0)
            return sphere
        elif shape == 4:
            diamond = pm.curve(name=name, d=1, p=[(0, 1, 0), (-1, 0.00278996, 6.18172e-08), (0, 0, 1), (0, 1, 0),
                                       (1, 0.00278996, 0), (0, 0, 1), (1, 0.00278996, 0), (0, 0, -1), (0, 1, 0),
                                       (0, 0, -1), (-1, 0.00278996, 6.18172e-08), (0, -1, 0), (0, 0, -1),
                                       (1, 0.00278996, 0),(0, -1, 0),(0, 0, 1)],
                               k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
            return diamond


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
