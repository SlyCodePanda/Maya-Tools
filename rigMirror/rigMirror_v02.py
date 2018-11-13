from maya import cmds

# Base class for building UI.
class BaseWindow(object):
    windowName = "BaseWIndow"

    def show(self):
        if cmds.window(self.windowName, query=True, exists=True):
            cmds.deleteUI(self.windowName)

        cmds.window(self.windowName)
        self.buildUI()
        cmds.showWindow()

    def buildUI(self):
        pass

    def reset(self, *args):
        pass

    def close(self, *args):
        cmds.deleteUI(self.windowName)

# A class that holds all functions for mirroring a rig.
class rigMirror(BaseWindow):
    # Class variables
    selection = []

    FK_joints = []
    IK_joints = []

    FK_constraints = []
    IK_constraints = []
    polevector = []

    controls = []

    ikHandle = []

    curSide = ""
    newSide = ""
    scale = ""

    # Initializer function.
    def __init__(self, curSide, newSide, scale):
        # Get the current built side naming convention and the new side naming convention.
        self.curSide = curSide
        self.newSide = newSide
        # Get what axis we are mirroring along.
        self.scale = scale

        # Get selection.
        self.selection = cmds.ls(sl=True, dag=True)
        print(str(self.selection))

        # Get FK and IK joints.
        self.getFKjoints()
        self.getIKjoints()

        # Get controls.
        self.getControls()

        # Get IKHandle.
        self.getIKhandle()

        # Get IK and FK constraints.
        self.getFKconstraints()
        self.getIKconstraints()

        # Get pole vector.
        self.getPoleVector()

    ################################
    # BASIC HELPER FUNCTIONS
    ################################

    # Takes in an object and gives it a new name whether you are creating a left or right duplicate of it.
    def getNewSideName(self, object):
        oldName = str(object)
        newName = oldName.replace(self.curSide, self.newSide)

        return newName

    # Checks if node is a group.
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

    # Returns true if passed object is apart of the FK rig (joints and controls).
    def isFK(self, object):
        if "FK" in object or "fk" in object:
            return True
        else:
            return False

    # Returns true if passed object is apart of the IK rig (joints, controls, and ikHandle).
    def isIK(self, object):
        if "IK" in object or "ik" in object:
            return True
        else:
            return False

    # Check if object is a constraint of some kind (other than pole vector).
    def isConstraint(self, node):
        if cmds.objectType(node, isType="parentConstraint"):
            return True
        elif cmds.objectType(node, isType="pointConstraint"):
            return True
        elif cmds.objectType(node, isType="scaleConstraint"):
            return True
        elif cmds.objectType(node, isType="aimConstraint"):
            return True
        else:
            return False

    ################################
    # GET FUNCTIONS
    ################################

    # Get FK joint chain.
    def getFKjoints(self):
        # Iterate through selection list and find the joints with FK naming conventions.
        for each in self.selection:
            # Check if object in list is apart of FK chain.
            if self.isFK(each):
                # Check if FK item is a joint.
                if cmds.objectType(each, isType="joint"):
                    self.FK_joints.append(each)

        print("FK Joints : " + str(self.FK_joints))

    # Get IK joint chain.
    def getIKjoints(self):
        # Iterate through selection list and find the joints with FK naming conventions.
        for each in self.selection:
            # Check if object in list is apart of FK chain.
            if self.isIK(each):
                # Check if FK item is a joint.
                if cmds.objectType(each, isType="joint"):
                    self.IK_joints.append(each)

        print("IK Joints : " + str(self.IK_joints))

    # Get controls.
    def getControls(self):
        controlGroups = []

        # Get the control groups.
        for each in self.selection:
            if cmds.objectType(each, isType="transform") and self.isGroup(each):
                controlGroups.append(each)

        print("Groups : " + str(controlGroups))

        # Get children of control groups.
        for each in controlGroups:
            children = cmds.listRelatives(each, children=True, type="transform")
            self.controls.append(children[0])

        print("Controls : " + str(self.controls))

    # Get ikHandle.
    def getIKhandle(self):
        for each in self.selection:
            if cmds.objectType(each, isType="ikHandle"):
                self.ikHandle.append(each)

        print("IKHandle : " + str(self.ikHandle))

    # Get FK constraints.
    def getFKconstraints(self):
        for each in self.selection:
            # Check if object in list is apart of FK chain.
            if self.isFK(each):
                # Check if object is a constraint.
                if self.isConstraint(each):
                    self.FK_constraints.append(each)

        print("FK Constraints : " + str(self.FK_constraints))

    # Get IK constraints.
    def getIKconstraints(self):
        for each in self.selection:
            # Check if object in list is apart of IK chain.
            if self.isIK(each):
                # Check if object is a constraint.
                if self.isConstraint(each):
                    self.IK_constraints.append(each)

        print("IK Constraints : " + str(self.IK_constraints))

    # Get pole vector.
    def getPoleVector(self):
        for each in self.selection:
            if cmds.objectType(each, isType="poleVectorConstraint"):
                self.polevector.append(each)

        print("Pole Vector : " + str(self.polevector))

    ################################
    # MIRROR FUNCTIONS
    ################################