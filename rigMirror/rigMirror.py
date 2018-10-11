from maya import cmds

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
        self.controls = cmds.ls(sl=True)

        self.mirrorControls()

    # Class functions
    # Takes in an object and gives it a new name whether you are creating a left or right duplicate of it.
    def getNewSideName(self, object):
        oldName = str(object)
        newName = oldName.replace(self.curSide, self.newSide)

        return newName

    # Get all the controls and their groups on one side of the rig and mirror them to the other side.
    def mirrorControls(self):
        # Iterate through all the controls and their groups and duplicate them
        for control in self.controls:
            # Get the group and the control in it.
            ctrlName = str(control)
            ctrlGrps = cmds.listRelatives(ctrlName, parent=True)
            transX = cmds.getAttr(ctrlGrps[0] + ".translateX")
            transY = cmds.getAttr(ctrlGrps[0] + ".translateY")
            transZ = cmds.getAttr(ctrlGrps[0] + ".translateZ")

            # Duplicate groups and controls
            duplicate = cmds.duplicate(ctrlGrps[0], name=self.getNewSideName(ctrlGrps[0]))
            # Mirror the duplicate to other side.
            cmds.xform(duplicate[0], t=(-transX, transY, transZ))

    # Get all the connections and store them in connections dictionary. Then set up connections on the other side.
    def mirrorConnections(self):
        pass
        # Look at mirrorJoint() command