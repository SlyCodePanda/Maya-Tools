from maya import cmds

'''
    Order of steps to take when using this tool :
        STEP 1 : Mirror FK
        STEP 2 : Mirror IK
        STEP 3 : Mirror Pole Vector
'''

# A class that holds all functions for mirroring a rig.
class rigMirror(object):
    # Class variables

    curSide = ""
    newSide = ""
    scale = ""

    # FK
    FK_connections = {}
    FK_controls = []
    FK_dupControls = []

    joints = []
    dupJoints = []

    # POLE VECTOR
    poleVector = []
    dupPoleVector = []

    # IK
    ikHandle = []
    dupIkHandle = []
    IK_controls = []
    IK_dupControls = []

    # Initializer function.
    def __init__(self, curSide, newSide, scale):
        # Get the current built side naming convention and the new side naming convention.
        self.curSide = curSide
        self.newSide = newSide
        # Get what axis we are mirroring along.
        self.scale = scale

    ################################
    # BASIC HELPER FUNCTIONS
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
    # MAIN MIRROR FUNCTIONS
    ################################

    # Mirror the FK rig (joints and controls)
    def mirrorFK(self):
        # Get the rig controls based on user selection.
        self.FK_controls = cmds.ls(sl=True, et="transform")
        self.joints = cmds.ls(sl=True, dag=True, type="joint")

        print("FK_controls : " + str(self.FK_controls))
        print("joints : " + str(self.joints))

        # Duplicate and mirror rig controls from one side to the other.
        self.mirrorControls("FK")
        # Duplicate and mirror joints from one side to the other.
        self.mirrorJoints("FK")

    # Mirror the IK rig (joints and controls)
    def mirrorIK(self):
        # Get the IK joints, IK handle, and hand/foot control from user selection.
        self.ikHandle = cmds.ls(sl=True, dag=True, type="ikHandle")
        self.IK_controls = cmds.ls(sl=True, et="transform")
        self.joints = cmds.ls(sl=True, dag=True, type="joint")

        # Duplicate and mirror rig controls from one side to the other.
        self.mirrorControls("IK")

        # Duplicate and mirror joints from one side to the other.
        self.mirrorJoints("IK")

        # Duplicate and mirror Ik handle.
        self.mirrorIKhandle()

    ################################
    # MIRROR HELPER FUNCTIONS
    ################################

    def mirrorControls(self, type):
        # Duplicate top level group in hierarchy and rename it for new side.
        if type == "FK":
            dup = cmds.duplicate(self.FK_controls[0], name=self.getNewSideName(self.FK_controls[0]))
        elif type == "IK":
            dup = cmds.duplicate(self.IK_controls[0], name=self.getNewSideName(self.IK_controls[0]))
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
                # Adding new duplicated controls to global list 'dupControls'.
                if type == "FK":
                    self.FK_dupControls.append(newName)
                elif type == "IK":
                    self.IK_dupControls.append(newName)

        # Create a temporary group to use to scale the group in -1 along the X axis.
        # May add functionality to choose which axis to scale across later.
        group = cmds.group(dup[0], name="ctrls_mirrorGrp")
        cmds.xform(group, os=True, piv=[0, 0, 0])
        # Depending on what scale was chosen by user, depends which direction it will be scaled in
        if self.scale == "X":
            cmds.scale(-1, 1, 1, group)
        elif self.scale == "Y":
            cmds.scale(1, -1, 1, group)
        elif self.scale == "Z":
            cmds.scale(1, 1, -1, group)
        cmds.ungroup("ctrls_mirrorGrp")

    # Duplicates and mirrors the skeleton (joints).
    def mirrorJoints(self, type):
        # Duplicate top level joint in hierarchy and rename it for new side.
        # If there are no joints selected, return out of function and do nothing.

        if self.joints:
            if self.scale == "X":
                self.dupJoints = cmds.mirrorJoint(self.joints[0], mirrorYZ=True, mirrorBehavior=True,
                                       sr=[self.curSide, self.newSide])
            # TODO : Add other axis to list for scaling (Y, Z)
        else:
            return
        constraints = []
        joints = []
        ctrls = []

        # Add duplicated controls to new list (without the groups).
        if type == "FK":
            for i in range(len(self.FK_dupControls)):
                if not self.isGroup(self.FK_dupControls[i]):
                    ctrls.append(self.FK_dupControls[i])

        elif type == "IK":
            for i in range(len(self.IK_dupControls)):
                if not self.isGroup(self.IK_dupControls[i]):
                    ctrls.append(self.IK_dupControls[i])

        print("CTRLS : " + str(ctrls) )

        # Add old parent constraints from the duplicates list to new list, and add joints to another new list.
        for i in range(len(self.dupJoints)):
            if cmds.objectType(self.dupJoints[i]) == "parentConstraint":
                constraints.append(self.dupJoints[i])
            else:
                joints.insert(0, self.dupJoints[i])

        # If FK, parent constraint new side controls to right new joints.
        if type == "FK":
            for i in range(len(ctrls)):
                curJoint = joints[i]
                oldCon = constraints[i]
                # Remove old constraint and add new one for new side.
                cmds.parentConstraint(curJoint, oldCon, edit=True, rm=True)
                cmds.parentConstraint(ctrls[i], curJoint, mo=True)

    # Mirror the pole vector.
    def mirrorPoleVector(self):
        # Duplicated selected pole vector control
        self.poleVector = cmds.ls(sl=True)
        self.dupPoleVector = cmds.duplicate(self.poleVector, name=self.getNewSideName(self.poleVector[0]))
        topGrp = self.dupPoleVector[0]
        topGrp.replace(topGrp[-1], "")

        children = cmds.listRelatives(topGrp, children=True, ad=True, type="transform", f=True)

        # Go through children list and rename them to the other side.
        for i in range(len(children)):
            if cmds.objectType(children[i]) != 'joint':
                name = children[i].split("|")[-1]
                newName = cmds.rename(children[i], self.getNewSideName(name))
                # Adding new duplicated controls to global list 'dupControls'.
                self.dupPoleVector.append(newName)


        # Create a temporary group to use to scale the group in -1 along the X axis.
        group = cmds.group(self.dupPoleVector[0], name="ctrls_mirrorGrp")
        cmds.xform(group, os=True, piv=[0, 0, 0])
        if self.scale == "X":
            cmds.scale(-1, 1, 1, group)
        elif self.scale == "Y":
            cmds.scale(1, -1, 1, group)
        elif self.scale == "Z":
            cmds.scale(1, 1, -1, group)
        cmds.ungroup("ctrls_mirrorGrp")

        # Pole vector constraint new pole vector control to new ikhandle
        # Get original pole vector shape node.
        pvChildren = cmds.listRelatives(self.poleVector, children=True, ad=True, type="transform", f=True)
        child = pvChildren[0].split("|")[-1]
        # Get the original pv shape's constraints.
        pvCon = cmds.listConnections(str(child), type="poleVectorConstraint", d=True, s=False)[0]
        # Get the IK
        Lf_ik = cmds.listConnections(pvCon, type="ikHandle")[0]

        if Lf_ik:
            Rt_ik = self.getNewSideName(str(Lf_ik))
            Rt_pv = self.dupPoleVector[-1]
            cmds.poleVectorConstraint(str(Rt_pv), str(Rt_ik))

        #pvConstraint = cmds.listConnections(str(self.poleVector[0]), d=True, s=False, type="poleVectorConstraint")[0]
        #conType = cmds.objectType(pvConstraint)
        # if pvConstraint:
        #     print("PV CONSTRAINT FOUND")
        #cmds.poleVectorConstraint(str(self.dupPoleVector[0]), str(self.dupIkHandle))

    # Mirror IK handle.
    def mirrorIKhandle(self):
        # Strip out any non-joints from the dupJoints list.
        self.dupJoints = cmds.ls(self.dupJoints, type="joint")

        # Joints to use for the ikhandle. THROW AWAY.
        topJoint = self.dupJoints[0]
        bottomJoint = self.dupJoints[-1]

        # Create new ikhandle and change the targets from left shoulder and wrist to right shoulder and wrist.
        cmds.ikHandle(self.getNewSideName(self.ikHandle[0]), e=True, sj=self.dupJoints[0], ee=self.dupJoints[-1])

        # point constraint IK handle to to foot/hand ctrl. (ik then foot/hand selection order)
        ik = cmds.ls(self.getNewSideName(self.ikHandle[0]))[0]
        ctrl = self.IK_dupControls[0]
        cmds.pointConstraint(ctrl, ik)


