import maya.cmds as cmds

'''
Script to colour all the mesh inside a selected group.
NOTE: Does not work if you already have drawing overrides switched on.
'''

###################
# Helper Function #
###################

def get_colour_editor():
    """
    Opens a color editor.
    :return: returns the RGB value of the selected colour: [float, float, float]
             If nothing selected, return 'None'.
    """
    rgb_values = None

    # Build a colour editor and return values selected.
    cmds.colorEditor()
    if cmds.colorEditor(query=True, result=True):
        rgb_values = cmds.colorEditor(query=True, rgb=True)
        print 'RGB = ' + str(rgb_values)
    else:
        print 'Colour editor was closed'
        return None

    return rgb_values


#################
# Main Function #
#################

def colour_mesh():
    """
    Colours all the mesh and nurbsSurface object's wireframes in a selected
    group.
    :return: N/A
    """
    # Get mesh inside the selected group.
    sel_group = cmds.ls(sl=True, dag=True, type=['mesh','nurbsSurface'])
    print(sel_group)

    # If there are no mesh or nurbsSurface in the group.
    if not sel_group:
        cmds.warning("No mesh or nurbsSurface found in group.")
        return

    colour = get_colour_editor()

    try:
        # Set the colours of each of the mesh in selected group.
        for mesh in sel_group:
            # Make sure drawing overrides are on for each mesh.
            cmds.setAttr("%s.overrideEnabled" % mesh, 1)
            cmds.color(mesh, rgb=colour)
        # If colour editor was exited out of, do no try to change colour of mesh
        # Exit without error.
        if colour is None:
            return
    except TypeError:
        pass







