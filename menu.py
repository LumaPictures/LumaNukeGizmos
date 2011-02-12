# *****************************************************************************
# NOTE: in order for this to work, you must ALSO install the included init.py;
# the installation instructions for it are essentially identical...
# *****************************************************************************
#
# To use this file, copy it as 'menu.py' to a directory on your plugin path.
# By default, the plugin path is (taken from the nuke manual):
#
# Linux:
#  /users/login name/.nuke
#  /usr/local/Nuke6.0v6/plugins
# Mac OS X:
#  /Users/login name/.nuke
#  /Applications/Nuke6.0v6/Nuke6.0v6.app/Contents/MacOS/plugins
# Windows:
#  In the .nuke directory, which can be found under the directory pointed to
#  by the HOME environment variable. If this variable is not set (which is
#  common), the .nuke directory will be under the folder specified by the
#  USERPROFILE environment variable - which is generally of the form:
#    drive letter:\Documents and Settings\login name\      (Windows XP)
#        or
#    drive letter:\Users\login name\                       (Windows Vista)
#
# If there is already a 'menu.py' at that location, open it in your favorite
# text editor, and add the contents of this file to the end of it.
#
# Once installed, this script will allow you to create subfolders within the
# same directory it resides in (or in the directory pointed at by the
# NUKE_GIZMO_PATH environment variable, if it is defined, or you may provide
# a custom directory by editing the CUSTOM_GIZMO_LOCATION, below), and have gizmos
# within those subfolders automatically available in nuke from the menu (or submenu)
# of the same name.
#
# Ie, if your directory structure looks like this:
#
# /basePluginDir
#     menu.py
#     /Images
#         Rainbow.gizmo
#     /MyCustomMenu
#         /SubMenu
#             MakeAwesome.gizmo
#
# ...then when you clicked on the 'Image' menu, there would be an additional
# item at the end to create a 'Rainbow' node.  Additionally, there would
# be a new top-level menu, 'MyCustomMenu', which would have a 'SubMenu', which
# would have an entry to create a 'MakeAwesome' node.

if __name__ == '__main__':
  # Just in case they didn't use the supplied init.py
  gizManager = globals().get('gizManager', None)
  if gizManager is None:
      print 'Problem finding GizmoPathManager - check that init.py was setup correctly'
  else:
      gizManager.addGizmoMenuItems()
      # Don't need it no more...
      del gizManager
