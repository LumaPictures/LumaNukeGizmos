## Install instructions

1.	Copy the **menu.py** and **init.py** into your **.nuke** folder.
	If there is already an **init.py** or  **menu.py** at that location, open it in your favorite text editor, and add the contents of this **init.py** or **menu.py** to the end of your current **init.py** or **menu.py** respectively. 
2.	Copy the directories within the **Gizmos** folder directly into your **.nuke** folder
	Your directory structure will look similar to the following:
	<pre>
	.nuke/
		Channel/
		Draw/
		Filter/
		Image/
		Keyer/
		Merge/
		Transform/
		init.py
		menu.py
	</pre>
3.	Open Nuke.

## OR If you want to put the gizmos into a subdirectory

1.	Copy the contents of the **LumaNukeGizmos** package into your **.nuke** directory.
	If there is already an **init.py** or  **menu.py** at that location, open it in your favorite text editor, and add the contents of this **init.py** or **menu.py** to the end of your current **init.py** or **menu.py** respectively. 
	Your directory structure will look similar to the following:
	<pre>
	.nuke/
		Gizmos/
		init.py
		menu.py
	</pre>
2.	Open **init.py** and add a **CUSTOM_GIZMO_LOCATION** path.
3.	Replace **&lt;login name&gt;** with your login name in this example
	*	**Linux:**
		<pre>CUSTOM_GIZMO_LOCATION = r'/users/&lt;login name&gt;/.nuke/Gizmos'</pre>
	*	**OSX**
		<pre>CUSTOM_GIZMO_LOCATION = r'/Users/&lt;login name&gt;/.nuke/Gizmos'</pre>
	*	**Windows**
		<pre>CUSTOM_GIZMO_LOCATION = r'C:\Users\<login name>\.nuke\Gizmos'</pre>
		*If you are on Windows do not include a trailing slash!*
4.	Save **init.py** file and open Nuke.