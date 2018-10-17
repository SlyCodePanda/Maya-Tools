from maya import cmds
import re

# A class that holds all functions for mirroring a rig.
class rigMirror(object):
    # Class variables
    connections = {}
    controls = []
    curSide = ""
    newSide = ""

    # Initializer function.
    def __init__(self, curSide, newSide):
        self.curSide = curSide
        self.newSide = newSide

        # Get the rig controls based on user selection.
        # Get both groups and any children.
        self.controls = cmds.ls(sl=True, dag=True, type="transform")

        print("CONTROLS : \n %s" % self.controls)

        self.mirrorControls()

    # Class functions

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
            name = children[i].split("|")[-1]
            cmds.rename(children[i], self.getNewSideName(name))

        # Create a temporary group to use to scale the group in -1 along the X axis.
        # May add functionality to choose which axis to scale across later.
        group = cmds.group(dup[0], name="ctrls_mirrorGrp")
        cmds.xform(group, os=True, piv=[0, 0, 0])
        cmds.scale(-1, 1, 1, group)
        cmds.ungroup("ctrls_mirrorGrp")

    # Duplicates and mirrors the skeleton (joints).
    def mirrorJoints(self):
        pass

    # Get all the connections and store them in connections dictionary. Then set up connections on the other side.
    def mirrorConnections(self):
        pass
        # Look at mirrorJoint() command