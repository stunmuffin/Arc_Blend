# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
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

import random
import sys
import os

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





# ------------------------------------------------------------------------------
# REGISTRATION AREA

def register():
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



def unregister():
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


# ------------------------------------------------------------------------------

if __name__ == "__main__":
    register()
