# To use this file, copy it as 'init.py' to a directory on your plugin path.
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
# If there is already a 'init.py' at that location, open it in your favorite
# text editor, and add the contents of this file to the end of it.
#
# Once installed, this script will add to the plugin path subfolders of the
# folder it resides in (or of directories pointed at by the NUKE_GIZMO_PATH
# environment variable, if it is defined... or you may provide a custom
# directory by editing the CUSTOM_GIZMO_LOCATION, below), and have gizmos within
# those subfolders automatically available in nuke
# 
# If in GUI mode, menu items for these subfolders may also be automatically
# created - see 'menu.py' for details.


# Example custom gizmo locations:

# Linux:
# CUSTOM_GIZMO_LOCATION = r'/users/<login name>/.nuke/Gizmos'

# Mac OS X:
# CUSTOM_GIZMO_LOCATION = r'/Users/<login name>/.nuke/Gizmos'

# Windows:
# CUSTOM_GIZMO_LOCATION = r'C:\Users\<login name>\.nuke\Gizmos'

# WARNING: on windows, do NOT end with a trailing slash... ie this is BAD:
# CUSTOM_GIZMO_LOCATION = r'C:\Users\<login name>\.nuke\Gizmos\'

CUSTOM_GIZMO_LOCATION = r''

import os
import re

import nuke

class GizmoPathManager(object):
    def __init__(self, exclude=r'^\.', searchPaths=None):
        '''Used to add folders within the gizmo folder(s) to the gizmo path
        
        exclude: a regular expression for folders / gizmos which should NOT be
            added; by default, excludes files / folders that begin with a '.'
            
        searchPaths: a list of paths to recursively search; if not given, it
            will use the NUKE_GIZMO_PATH environment variable; if that is
            not defined, it will use the directory in which this file resides;
            and if it cannot detect that, it will use the pluginPath 
        '''
        if isinstance(exclude, basestring):
            exclude = re.compile(exclude)
        self.exclude = exclude
        if searchPaths is None:
            searchPaths = os.environ.get('NUKE_GIZMO_PATH', '').split(os.pathsep)
            if not searchPaths:
                import inspect
                thisFile = inspect.getsourcefile(lambda: None)
                if thisFile:
                    searchPaths = [os.path.dirname(os.path.abspath(thisFile))]
                else:
                    searchPaths = list(nuke.pluginPath())
        self.searchPaths = searchPaths
        self.reset()
        
    @classmethod
    def canonical_path(cls, path):
        return os.path.normcase(os.path.normpath(os.path.realpath(os.path.abspath(path))))
        
    def reset(self):
        self._crawlData = {}
        
    def addGizmoPaths(self):
        '''Recursively search searchPaths for folders to add to the nuke
        pluginPath.
        '''
        self.reset()
        self._visited = set()
        for gizPath in self.searchPaths:
            self._recursiveAddGizmoPaths(gizPath, self._crawlData,
                                         foldersOnly=True)
            
    def _recursiveAddGizmoPaths(self, folder, crawlData, foldersOnly=False):
        # If we're in GUI mode, also store away data in _crawlDatato to be used
        # later by addGizmoMenuItems
        if not os.path.isdir(folder):
            return
        
        if nuke.GUI:
            if 'files' not in crawlData:
                crawlData['gizmos'] = []
            if 'dirs' not in crawlData:
                crawlData['dirs'] = {}

        # avoid an infinite loop due to symlinks...
        canonical_path = self.canonical_path(folder)
        if canonical_path in self._visited:
            return
        self._visited.add(canonical_path)
        
        for subItem in sorted(os.listdir(canonical_path)):
            if self.exclude and self.exclude.search(subItem):
                continue
            subPath = os.path.join(canonical_path, subItem)
            if os.path.isdir(subPath):
                nuke.pluginAppendPath(subPath)
                subData = {}
                if nuke.GUI:
                    crawlData['dirs'][subItem] = subData
                self._recursiveAddGizmoPaths(subPath, subData)
            elif nuke.GUI and (not foldersOnly) and os.path.isfile(subPath):
                name, ext = os.path.splitext(subItem)
                if ext == '.gizmo':
                    crawlData['gizmos'].append(name)
                    
    def addGizmoMenuItems(self, toolbar=None, defaultTopMenu=None):
        '''Recursively create menu items for gizmos found on the searchPaths.
        
        Only call this if you're in nuke GUI mode! (ie, from inside menu.py)
        
        toolbar - the toolbar to which to add the menus; defaults to 'Nodes'
        defaultTopMenu - if you do not wish to create new 'top level' menu items,
            then top-level directories for which there is not already a top-level
            menu will be added to this menu instead (which must already exist)
        '''        
        if not self._crawlData:
            self.addGizmoPaths()
            
        if toolbar is None:
            toolbar = nuke.menu("Nodes")
        elif isinstance(toolbar, basestring):
            toolbar = nuke.menu(toolbar)
        self._recursiveAddGizmoMenuItems(toolbar, self._crawlData,
                                         defaultSubMenu=defaultTopMenu,
                                         topLevel=True)
    
    def _recursiveAddGizmoMenuItems(self, toolbar, crawlData,
                                    defaultSubMenu=None, topLevel=False):
        for name in crawlData.get('gizmos', ()):
            niceName = name
            if niceName.find('_v')==len(name) - 4:
                niceName = name[:-4]
            toolbar.addCommand(niceName,"nuke.createNode('%s')" % name)
            
        for folder, data in crawlData.get('dirs', {}).iteritems():
            import sys
            subMenu = toolbar.findItem(folder)
            if subMenu is None:
                if defaultSubMenu:
                    subMenu = toolbar.findItem(defaultSubMenu)
                else:
                    subMenu = toolbar.addMenu(folder)
            self._recursiveAddGizmoMenuItems(subMenu, data)
                    
if __name__ == '__main__':
    if CUSTOM_GIZMO_LOCATION and os.path.isdir(CUSTOM_GIZMO_LOCATION):
        gizManager = GizmoPathManager(searchPaths=[CUSTOM_GIZMO_LOCATION])
    else:
        gizManager = GizmoPathManager()
    gizManager.addGizmoPaths()
    if not nuke.GUI:
        # We're not gonna need it anymore, cleanup...
        del gizManager
