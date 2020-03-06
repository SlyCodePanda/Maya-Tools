import maya.cmds

"""
Looks at the selected mesh and selects any faces that are ngons
(has more than 4 edges on a face).

https://stackoverflow.com/questions/32428452/selecting-faces-in-a-list-maya-python
"""


def analyzeFace(faces):
    """
    ahsdfkjasf
    :param faces:
    :return:
    """
    # Expand compacted face name into a list of face names.
    facesList = maya.cmds.filterExpand(faces, sm=34)
    ngonCount = 0

    # Clear selection.
    maya.cmds.select(cl=True)

    # Select face and check the number of tris.
    for face in facesList:
        maya.cmds.select(face, add=True)
        numOfTris = maya.cmds.polyEvaluate(tc=True)

        if numOfTris % 2 != 0:
            ngonCount += 1

        else:
            # deselect face.
            maya.cmds.select(face, d=True)

    print "NGons found: ", ngonCount


def run():
    selObjs = maya.cmds.ls(selection=True)

    for obj in selObjs:
        faces = maya.cmds.ls('%s.f[*]' % obj)
        print "Object Name: ", selObjs
        analyzeFace(faces)




