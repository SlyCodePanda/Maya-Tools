from maya import cmds

# A class that holds all functions for mirroring a rig.
class rigMirror(object):
    # Class variables
    connections = {}
    controls = []
    dupControls = []
    joints = []
    curSide = ""
    newSide = ""

    # Initializer function.
    def __init__(self, curSide, newSide):
        self.curSide = curSide
        self.newSide = newSide

        # Get the rig controls based on user selection.
        self.controls = cmds.ls(sl=True, dag=True, type="transform")
        self.joints = cmds.ls(sl=True, dag=True, type="joint")

        # Strip joints from controls list.
        for cur in self.controls:
            if cmds.objectType(cur) == "joint":
                self.controls.remove(cur)

        print("CONTROLS : \n" + str(self.controls))
        print("JOINTS : \n" + str(self.joints))

        # Duplicate and mirror rig controls from one side to the other.
        self.mirrorControls()
        # Duplicate and mirror joints from one side to the other.
        self.mirrorJoints()

    ################################
    # HELPER FUNCTIONS
    ################################

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

    # Takes in an object and gives it a new name whether you are creating a left or right duplicate of it.
    def getNewSideName(self, object):
        oldName = str(object)
        newName = oldName.replace(self.curSide, self.newSide)

        return newName

    ################################
    # MIRROR FUNCTIONS
    ################################

    def mirrorControls(self):
        # Duplicate top level group in hierarchy and rename it for new side.
        dup = cmds.duplicate(self.controls[0], name=self.getNewSideName(self.controls[0]))
        # Remove the '1' on the end of the duplicate.
        topGrp = dup[0]
        topGrp.replace(topGrp[-1], "")

        # Get children of the new duplicate top grp.
        children = cmds.listRelatives(topGrp, children=True, ad=True, type="transform", f=True)

        # Go through children list and rename them to the other side.
        for i in range(len(children)):
            if cmds.objectType(children[i]) != 'joint':
                name = children[i].split("|")[-1]
                newName = cmds.rename(children[i], self.getNewSideName(name))
                # Adding new duplicated controls to global list.
                self.dupControls.append(newName)

        # Create a temporary group to use to scale the group in -1 along the X axis.
        # May add functionality to choose which axis to scale across later.
        group = cmds.group(dup[0], name="ctrls_mirrorGrp")
        cmds.xform(group, os=True, piv=[0, 0, 0])
        cmds.scale(-1, 1, 1, group)
        cmds.ungroup("ctrls_mirrorGrp")

    # Duplicates and mirrors the skeleton (joints).
    def mirrorJoints(self):
        # Duplicate top level joint in hierarchy and rename it for new side.
        dup = cmds.mirrorJoint(self.joints[0], mirrorYZ=True, mirrorBehavior=True, sr=[self.curSide, self.newSide])
        constraints = []
        joints = []
        ctrls = []

        # Add duplicated controls to new list (without the groups).
        for i in range(len(self.dupControls)):
            if not self.isGroup(self.dupControls[i]):
                ctrls.append(self.dupControls[i])

        # Add old parent contraints from the duplicates list to new list, and add joints to another new list.
        for i in range(len(dup)):
            if cmds.objectType(dup[i]) == "parentConstraint":
                constraints.append(dup[i])
            else:
                joints.insert(0, dup[i])

        # Parent contraint new side controls to right new joints.
        for i in range(len(ctrls)):
             curJoint = joints[i]
             oldCon = constraints[i]
             # Remove old constraint and add new one for new side.
             cmds.parentConstraint(curJoint, oldCon, edit=True, rm=True)
             cmds.parentConstraint(ctrls[i], curJoint, mo=True)

    # Get all the connections and store them in connections dictionary. Then set up connections on the other side.
    def mirrorConnections(self):
        pass
        # Look at mirrorJoint() command