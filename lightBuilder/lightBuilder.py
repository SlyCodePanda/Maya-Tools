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

from maya import cmds
from maya import OpenMayaUI as omui
import Qt
from Qt import QtWidgets, QtCore, QtGui
from Qt.QtCore import Signal
from shiboken2 import wrapInstance
from functools import partial
import logging


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
    # A dictionary of lights paired with their command to create them.
    lights = {"Area Light": partial(cmds.shadingNode, 'areaLight', asLight=True),
              "Ambient Light": cmds.ambientLight,
              "Directional Light": cmds.directionalLight,
              "Point Light": cmds.pointLight,
              "Spot Light": cmds.spotLight,
              "Volume Light": partial(cmds.shadingNode, 'volumeLight', asLight=True)
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
        for lightType in sorted(self.lights):
            self.lights_comboBox.addItem(lightType)
        layout.addWidget(self.lights_comboBox, 1, 1, 1, 1)

        createLight_button = QtWidgets.QPushButton('Create')
        createLight_button.clicked.connect(self.createLight)
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
        lightSelected = self.lights_comboBox.currentText()
        print('Creating a ' + lightSelected)
        self.lights[lightSelected]()

        # Add light widget to UI.
        self.addLight(lightSelected)

    # This function will create a light widget for the given light to add it to the UI.
    def addLight(self, light):
        # First we create the LightWidget.
        widget = LightWidget(light)
        # We add it to the scrollLayout.
        self.scrollLayout.addWidget(widget)
        # Then we connect the onSolo signal from the widget to our onSolo method.
        widget.onSolo.connect(self.onSolo)

    def onSolo(self, value):
        # This function will isolate a single light.

        # First we find all our children who are LightWidgets.
        lightWidgets = self.findChildren(LightWidget)

        # We'll loop through the list to perform our logic.
        for widget in lightWidgets:
            # Every signal lets us know who sent it that we can query with sender()
            # So for every widget we check if its the sender.
            if widget != self.sender():
                # If it's not the widget, we'll disable it.
                widget.disableLight(value)


class LightWidget(QtWidgets.QWidget):
    """
        A Basic controller for controlling lights
        to display it, give it the name of a light like so
        ui = LightWidget('directionalLight1')
        ui.show()
    """

    # This is our solo signal.
    # We are creating our own signal for other Qt objects to connect to.
    # Qt demands that we make the signal here so it knows what the class looks like.
    onSolo = Signal(bool)

    def __init__(self, light):
        # Our init function takes the name of a light.

        # We then call the init from QWidget to make sure that our object is initialized properly.
        super(LightWidget, self).__init__()

        # Then we store the pyMel node on this class.
        self.light = light
        # Finally we call the buildUI method.
        self.buildUI()

    def buildUI(self):
        layout = QtWidgets.QGridLayout(self)

        

        # Now this is a weird Qt thing where we tell it the kind of sizing we want it respect.
        # We are saying that the widget should never be larger than the maximum space it needs.
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)







