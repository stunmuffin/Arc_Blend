# ##### BEGIN GPL LICENSE BLOCK #####
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
# ##### END GPL LICENSE BLOCK #####

# ----------------------------------------------
# Define Addon info
# ----------------------------------------------
bl_info = {
    "name": "Arc Blend Tools",
    "author": "Stun Muffin (KB)",
    "version": (0, 5, 0),
    "blender": (3, 20, 0),
    "location": "View3d >Tool> Arc Blend",
    "support": "COMMUNITY",
    "category": "Development",
    "description": "Free opensource Blender add-on to help with your models",
}

# Import statements
import bpy

from . import AB_Asset_Browser
from . import AB_Camera
from . import AB_Create
from . import AB_Modify
from . import Vertex_Edit_Panel
from . import Themes_Panel
from . import Modelling_Panel
from . import AB_Scatter
from . import AB_Proxy
from . import AB_Light
from . import AB_Material
from . import AB_Color_Picker
from . import AB_Wall
from . import AB_MaterialManagement

# Check Blender version
if bpy.app.version >= (4, 1, 0):
    from . import AB_Shade_Auto_Smooth

# ------------------------------------------------------------------------------
# REGISTRATION AREA

def register():
    # Register all modules
    AB_Asset_Browser.register()
    AB_Camera.register()
    AB_Create.register()
    AB_Modify.register()
    Vertex_Edit_Panel.register()
    Themes_Panel.register()
    Modelling_Panel.register()
    AB_Scatter.register()
    AB_Proxy.register()
    AB_Light.register()
    AB_Material.register()
    AB_Color_Picker.register()
    AB_Wall.register()
    AB_MaterialManagement.register()

    # Register Shade Auto Smooth if Blender version is compatible
    if bpy.app.version >= (4, 1, 0):
        AB_Shade_Auto_Smooth.register()

def unregister():
    # Unregister all modules
    AB_Asset_Browser.unregister()
    AB_Camera.unregister()
    AB_Create.unregister()
    AB_Modify.unregister()
    Vertex_Edit_Panel.unregister()
    Themes_Panel.unregister()
    Modelling_Panel.unregister()
    AB_Scatter.unregister()
    AB_Proxy.unregister()
    AB_Light.unregister()
    AB_Material.unregister()
    AB_Color_Picker.unregister()
    AB_Wall.unregister()
    AB_MaterialManagement.unregister()

    # Unregister Shade Auto Smooth if Blender version is compatible
    if bpy.app.version >= (4, 1, 0):
        AB_Shade_Auto_Smooth.unregister()

# ------------------------------------------------------------------------------

if __name__ == "__main__":
    register()
