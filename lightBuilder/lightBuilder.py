'''
LightBuilder.py
Functions :
    1. Allows you to create, save, and use pre-built lighting setups. e.g 'Clear Day', 'Overcast', 'Night', etc.
    2. Allows you to edit lights currently in the scene. e.g turn them off, edit colour, etc.

To run:
    Place script in script folder of Maya and run the following in the Script Editor window:
        import lightBuilder as lb
        reload(lb)
        lb.LightBuilder().show()

Note:
    Trying to avoid using pymel as my workplace does not allow for use of that module.
'''

# TODO : Convert the script to use QtWidget.

from maya import cmds
from maya import OpenMayaUI as omui
import Qt
from Qt import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
from functools import partial


def getMayaMainWindow():
    '''
    Get the maya main window as a QMainWindow instance
    '''
    # We are using OpenMayaUI API to get a reference to Maya's MainWindow.
    win = omui.MQtUtil_mainWindow()
    # Then we use the wrapInstance method to convert it to something python can understand (QMainWindow).
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)
    return ptr


class LightBuilder(QtWidgets.QWidget):
    # A nested dictionary of lights that we can build based on the lights option menu create above.
    lights = {1: {'Area Light': partial(cmds.shadingNode, 'areaLight', asLight=True)},
              2: {"Ambient Light": cmds.ambientLight},
              3: {"Directional Light": cmds.directionalLight},
              4: {"Point Light": cmds.pointLight},
              5: {"Spot Light": cmds.spotLight},
              6: {"Volume Light": partial(cmds.shadingNode, 'volumeLight', asLight=True)}
              }

    def __init__(self):
        '''
        Initialize the window.
        '''

        parent = QtWidgets.QDialog(parent=getMayaMainWindow())
        parent.setObjectName('lightBuilder')
        parent.setWindowTitle('Light Builder')

        layout = QtWidgets.QVBoxLayout(parent)

        # Now that we have our parent, we need to send it to the QWidgets initialization method.
        super(LightBuilder, self).__init__(parent=parent)

        # We call our buildUI method to construct our UI.
        self.buildUI()
        # Now we can tell it to populate with widgets for every light.
        #self.populate()

        # We then add ourself to our parents layout.
        self.parent().layout().addWidget(self)

        parent.show()

    def populate(self):
        pass


    ########################
    # UI functions
    ########################

    windowName = "LightBuilder"
    height = 500
    width = 500

    # def show(self):
    #     # If a window named "LightBuilder" already exists, delete the UI.
    #     if cmds.window(self.windowName, query=True, exists=True):
    #         cmds.deleteUI(self.windowName)
    #
    #     # Create the window, build the UI, then show the window.
    #     self.window = cmds.window(self.windowName, w=self.width, h=self.height, mnb=False, mxb=False, sizeable=False)
    #     self.buildUI()
    #     cmds.showWindow()
    #     cmds.setFocus(self.windowName)

    def buildUI(self):
        # Sizing variables.
        text_width = 90
        optionMenu_width = 200
        button_height = 20
        scroll_width = 490
        scroll_height = 350
        lowerButtons_width = 200

        layout = QtWidgets.QGridLayout(self)

        # Presets.
        self.Presets_label = QtWidgets.QLabel('Presets')
        layout.addWidget(self.Presets_label, 0, 0, 1, 1)
        self.Presets_comboBox = QtWidgets.QComboBox()
        layout.addWidget(self.Presets_comboBox, 0, 0, 1, 2)
        self.Presets_comboBox.addItem('...')

        # cmds.separator() # Does the separator appear in Maya 2018??
        #
        # cmds.setParent('..')
        # cmds.columnLayout(h=20) # Spacing.
        # cmds.setParent('..')
        #
        # # Create light.
        # cmds.rowLayout(numberOfColumns=3,  columnWidth3=(100, 75, 150))
        # cmds.optionMenu("lights_optionMenu", label='Create Light', w=optionMenu_width)
        # cmds.menuItem(label='Area Light')
        # cmds.menuItem(label='Ambient Light')
        # cmds.menuItem(label='Directional Light')
        # cmds.menuItem(label='Point Light')
        # cmds.menuItem(label='Spot Light')
        # cmds.menuItem(label='Volume Light')
        # cmds.button("buildPreset_button", label="Create", align='right', h=button_height, command=self.createLight)

        # Build up lights combo box from the dictionary of lights.
        self.lights_comboBox = QtWidgets.QComboBox()
        for key1, value1 in self.lights.items():
            for key2, value2 in value1.items():
                self.lights_comboBox.addItem(key2)

        layout.addWidget(self.lights_comboBox, 1, 1, 1, 1)

        #
        # cmds.setParent('..')
        #
        # # Scroll area.
        # cmds.rowLayout(numberOfColumns=1)
        # cmds.scrollField("sceneLights_scrollField", w=scroll_width, h=scroll_height, ed=False)
        # cmds.scrollField("sceneLights_scrollField", e=True, it="Visible")
        #
        # cmds.setParent('..')
        #
        # # Save and Reset buttons.
        # cmds.rowLayout(numberOfColumns=2)
        # cmds.button("SavePreset_button", label="Save", h=button_height, w=lowerButtons_width)
        # cmds.button("Reset_button", label="Reset", h=button_height, w=lowerButtons_width, bgc=(1, 0.2, 0.2))

    ########################
    # Builder functions
    ########################

    def createLight(self, *args):

        # Currently selected light from the lights option menu (range from 1-6).
        light = cmds.optionMenu("lights_optionMenu", q=True, sl=True)
        # Print the currently selected light.
        print(lights[light]['Type'])
        # Create the light.
        lights[light]['Command']()





'''
LightBuilder.py
Functions :
    1. Allows you to create, save, and use pre-built lighting setups. e.g 'Clear Day', 'Overcast', 'Night', etc.
    2. Allows you to edit lights currently in the scene. e.g turn them off, edit colour, etc.

To run:
    Place script in script folder of Maya and run the following in the Script Editor window:
        import lightBuilder as lb
        reload(lb)
        lb.LightBuilder().show()

Note:
    Trying to avoid using pymel as my workplace does not allow for use of that module.
'''

# TODO : Convert the script to use QtWidget.

from maya import cmds
from maya import OpenMayaUI as omui
import Qt
from Qt import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
from functools import partial


def getMayaMainWindow():
    '''
    Get the maya main window as a QMainWindow instance
    '''
    # We are using OpenMayaUI API to get a reference to Maya's MainWindow.
    win = omui.MQtUtil_mainWindow()
    # Then we use the wrapInstance method to convert it to something python can understand (QMainWindow).
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)
    return ptr


class LightBuilder(QtWidgets.QWidget):
    # A nested dictionary of lights that we can build based on the lights option menu create above.
    lights = {1: {'Area Light': partial(cmds.shadingNode, 'areaLight', asLight=True)},
              2: {"Ambient Light": cmds.ambientLight},
              3: {"Directional Light": cmds.directionalLight},
              4: {"Point Light": cmds.pointLight},
              5: {"Spot Light": cmds.spotLight},
              6: {"Volume Light": partial(cmds.shadingNode, 'volumeLight', asLight=True)}
              }

    def __init__(self):
        '''
        Initialize the window.
        '''

        parent = QtWidgets.QDialog(parent=getMayaMainWindow())
        parent.setObjectName('lightBuilder')
        parent.setWindowTitle('Light Builder')

        layout = QtWidgets.QVBoxLayout(parent)

        # Now that we have our parent, we need to send it to the QWidgets initialization method.
        super(LightBuilder, self).__init__(parent=parent)

        # We call our buildUI method to construct our UI.
        self.buildUI()
        # Now we can tell it to populate with widgets for every light.
        #self.populate()

        # We then add ourself to our parents layout.
        self.parent().layout().addWidget(self)

        parent.show()

    def populate(self):
        pass

    ########################
    # UI functions
    ########################

    windowName = "LightBuilder"
    height = 500
    width = 500

    def buildUI(self):
        layout = QtWidgets.QGridLayout(self)

        # Presets.
        presets_label = QtWidgets.QLabel('Presets')
        layout.addWidget(presets_label, 0, 0, 1, 1)

        self.Presets_comboBox = QtWidgets.QComboBox()
        self.Presets_comboBox.addItem('...')
        layout.addWidget(self.Presets_comboBox, 0, 1, 1, 1)

        presets_button = QtWidgets.QPushButton('Build')
        layout.addWidget(presets_button, 0, 2, 1, 1)

        # Separator.
        # TODO : Work out how to do separators in PyQt.

        # Build up lights combo box from the dictionary of lights.
        lights_label = QtWidgets.QLabel('Create Light')
        layout.addWidget(lights_label, 1, 0, 1, 1)

        self.lights_comboBox = QtWidgets.QComboBox()
        for key1, value1 in self.lights.items():
            for key2, value2 in value1.items():
                self.lights_comboBox.addItem(key2)
        layout.addWidget(self.lights_comboBox, 1, 1, 1, 1)

        createLight_button = QtWidgets.QPushButton('Create')
        layout.addWidget(createLight_button, 1, 2, 1, 1)

        # Scroll Box.
        scrollWidget = QtWidgets.QWidget()
        scrollWidget.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.scrollLayout = QtWidgets.QVBoxLayout(scrollWidget)

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(scrollWidget)
        layout.addWidget(scrollArea, 2, 0, 1, 3)

        # Save and Reset.
        save_button = QtWidgets.QPushButton('Save')
        layout.addWidget(save_button, 3, 0, 1, 1)

        reset_button = QtWidgets.QPushButton('Reset')
        layout.addWidget(reset_button, 3, 2, 1, 1)

    ########################
    # Builder functions
    ########################

    # Creates a light based on the selection of the lights combobox.
    def createLight(self, *args):
        # Currently selected light from the lights option menu (range from 1-6).
        light = cmds.optionMenu("lights_optionMenu", q=True, sl=True)
        # Print the currently selected light.
        print(lights[light]['Type'])
        # Create the light.
        lights[light]['Command']()





