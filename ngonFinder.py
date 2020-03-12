import maya.cmds

"""
Looks at the selected mesh and selects any faces that are ngons
(has more than 4 edges on a face/more than 2 triangles making up the face).

refs used:
https://stackoverflow.com/questions/32428452/selecting-faces-in-a-list-maya-python
"""


def analyzeFace(faces):
    """
    Looks through the obj faces given and selects all the ngons in the list.
    :param faces: faces we want to look through for ngons.
    :return: Returns 'None' if no ngons are found.
    """
    # Expand compacted face name into a list of face names.
    facesList = maya.cmds.filterExpand(faces, sm=34)
    ngonCount = 0
    ngonFaces = []

    # Clear selection.
    maya.cmds.select(cl=True)

    # Select face and check the number of tris.
    for face in facesList:
        maya.cmds.select(face, add=True)
        numOfTris = maya.cmds.polyEvaluate(tc=True)
        # deselect face.
        maya.cmds.select(face, d=True)

        if numOfTris > 2:
            ngonCount += 1
            ngonFaces.append(face)

    # If list is empty (no ngons) return None.
    if len(ngonFaces) == 0:
        objName = facesList[0].split('.')[0]
        print "No ngons found on ", objName
        return None

    # Select the faces in the ngon list.
    [maya.cmds.select(face, add=True, af=True) for face in ngonFaces]

    print "NGons found: ", ngonCount


def run():
    selObj = maya.cmds.ls(selection=True)

    if len(selObj) > 1:
        maya.cmds.warning("Please only select one object.")
        return None

    faces = maya.cmds.ls('%s.f[*]' % selObj[0])
    print "Object Name: ", selObj[0]
    analyzeFace(faces)

