# Rig Control Builder

Tool to quickly create shape controls for rig joints.<br> 
Lets you parent constraint controls under each other or create quick pole vectors controls.

<img width=600px src="https://github.com/SlyCodePanda/Maya-Tools/blob/master/rigControlBuilder/screenCap.JPG" />

Nice TODOs
------
* Add colour picker to change the shapes colour.
* Give option to add to new layer.
* Add more shapes (arrow, star, sphere, etc..)

Important TODOs
------
* Clean up un-necessary code.
* Add ability for user to set naming format.
* Fix unique naming issue.

Usage
------
```
import rigControlBuilder as rcb
reload(rcb)
rcb.controlBuilder().show()
```
