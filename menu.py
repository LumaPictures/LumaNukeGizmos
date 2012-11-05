'''
Notes
=====
This file is meant to be deployed alongside the included `init.py`, and invokes
the automatic menu item creation on the default `GizmoPathManager` instance.
Please see the docstring of the `init.py` for installation instructions and
further information.

Once installed, this script uses the default ``GizmoPathManager`` instance to
automatically build hierarchical menu structures and commands for any gizmo
files it locates by recursively searching its defined path(s). These menu
hierarchies will be structured to match the layout of the gizmo files on disk,
allowing for easy menu reorganization without any code changes.


Sample Folder Structure
-----------------------
$HOME
    .nuke
        Gizmos    <- $NUKE_GIZMO_PATH environment variable points here.
            Channel    <- Each directory will generate a submenu
                BumpNormals.gizmo    <- .gizmo files generate menu commands
                Colormatte.gizmo
                FacingRatio_v02.gizmo    <- '_v02' will be stripped
            Color
                ColorAnalyses.gizmo
            Draw
                AdvancedGrain.gizmo
            Transform
                ITransform.gizmo
            ...
            ...

This will produce a menu structure with menu commands generated from the gizmo
file names minus the extension and, if present, a version suffix matching the
form '_vxx'. So in the above example tree, the file 'FacingRatio_v02.gizmo'
will generate a menu command simply labeled 'FacingRatio'.

If directory names found in the search tree match any of Nuke's built-in menu
names (e.g. Color, Filter, Draw, etc.), the gizmo menu commands will be added
to them. Please note that currently, if the menu command matches the name of a
command that already exists, it will replace the existing item.


*Example gizmo names taken from Nukepedia.com
'''
if __name__ == '__main__':
    gizManager = globals().get('gizManager', None)
    if gizManager is None:
        print 'Problem finding GizmoPathManager - check that init.py was setup correctly'
    else:
        gizManager.addGizmoMenuItems()
        del gizManager
