import random
import sys
from mathutils import Matrix, Vector
import time
import numpy as np
import math
from bpy.types import Menu
import bmesh
import bpy
from bl_ui.utils import PresetPanel
from bpy.types import Panel
bl_info = {
    "name": "Arc_Blend_Tools",
    "author": "Stun Muffin (KB)",
    "version": (0, 5, 0),
    "blender": (3, 20, 0),
    "location": "View3d >Tool> Arc Blend",
    "support": "COMMUNITY",
    "category": "Development",
    "description": "Free opensource Blender add-on to help with your models",
}

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option)any later version.
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
# ------------------------------------------------------------------------------
# INSTALL GUIDE
# Installation info
#
# Download file to your computer.
# In Blender go to Edit > Preferences > Addons
# Click install and select the file.
# Location "N"Panel

# ------------------------------------------------------------------------------
# ARC BLEND IMPORTS

# ------------------------------------------------------------------------------
# ARC BLEND PANEL


class arcblend (bpy.types.Panel):
    bl_label = "AB Create"
    bl_idname = "PT_ArcBlend"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"

    def draw(self, context):
        layout = self.layout

# ------------------------------------------------------------------------------
# MESH PANEL


class Add_Mesh (bpy.types.Panel):
    bl_label = "Mesh"
    bl_idname = "PT_AddMesh"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_ArcBlend"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Add Mesh")
        row = layout.row()
        row.operator("mesh.primitive_plane_add", icon="MESH_PLANE")
        row.operator("mesh.primitive_cube_add", icon="CUBE")
        row = layout.row()
        row.operator("mesh.primitive_circle_add", icon="MESH_CIRCLE")
        row.operator("mesh.primitive_uv_sphere_add", icon="MESH_UVSPHERE")
        row = layout.row()
        row.operator("mesh.primitive_ico_sphere_add", icon="MESH_ICOSPHERE")
        row.operator("mesh.primitive_cylinder_add", icon="MESH_CYLINDER")
        row = layout.row()
        row.operator("mesh.primitive_cone_add", icon="MESH_CONE")
        row.operator("mesh.primitive_torus_add", icon="MESH_TORUS")
        row = layout.row()
        row.operator("mesh.primitive_grid_add", icon="MESH_GRID")
        row.operator("mesh.primitive_monkey_add", icon="MESH_MONKEY")
        row = layout.row()

# ------------------------------------------------------------------------------
# CURVE PANEL


class Add_Curve (bpy.types.Panel):
    bl_label = "Curve"
    bl_idname = "PT_AddCurve"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_ArcBlend"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Add Curve")
        row = layout.row()
        row.operator("curve.primitive_bezier_curve_add", icon="CURVE_BEZCURVE")
        row.operator("curve.primitive_bezier_circle_add",
                     icon="CURVE_BEZCIRCLE")
        row = layout.row()
        row.operator("curve.primitive_nurbs_curve_add", icon="CURVE_NCURVE")
        row.operator("curve.primitive_nurbs_circle_add", icon="CURVE_NCIRCLE")
        row = layout.row()
        row.operator("curve.primitive_nurbs_path_add", icon="CURVE_PATH")
        row = layout.row()

# ------------------------------------------------------------------------------
# SURFACE PANEL----------------------------------------------------------------


class Add_Surface (bpy.types.Panel):
    bl_label = "Surface"
    bl_idname = "PT_AddSurface"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_ArcBlend"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Add Surface")
        row = layout.row()
        row.operator("surface.primitive_nurbs_surface_curve_add",
                     icon="SURFACE_NCURVE")
        row.operator("surface.primitive_nurbs_surface_circle_add",
                     icon="SURFACE_NCIRCLE")
        row = layout.row()
        row.operator("surface.primitive_nurbs_surface_surface_add",
                     icon="SURFACE_NSURFACE")
        row.operator("surface.primitive_nurbs_surface_cylinder_add",
                     icon="SURFACE_NCYLINDER")
        row = layout.row()
        row.operator("surface.primitive_nurbs_surface_sphere_add",
                     icon="SURFACE_NSPHERE")
        row.operator("surface.primitive_nurbs_surface_torus_add",
                     icon="SURFACE_NTORUS")
        row = layout.row()

# ------------------------------------------------------------------------------
# METABALL BUTTON "BALL"OPERATOR


class mball_ball (bpy.types.Operator):
    """Create Metaball : Ball"""
    bl_label = ""
    bl_idname = "object.button_mball_ball"

    def execute(self, context):
        bpy.ops.object.metaball_add(
            type='BALL', radius=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# METABALL BUTTON "CAPSULE"OPERATOR


class mball_capsule (bpy.types.Operator):
    """Create Metaball : Capsule"""
    bl_label = ""
    bl_idname = "object.button_mball_capsule"

    def execute(self, context):
        bpy.ops.object.metaball_add(
            type='CAPSULE', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# METABALL BUTTON "PLANE"OPERATOR


class mball_plane (bpy.types.Operator):
    """Create Metaball : Plane"""
    bl_label = ""
    bl_idname = "object.button_mball_plane"

    def execute(self, context):
        bpy.ops.object.metaball_add(
            type='PLANE', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# METABALL BUTTON "ELLIPSOID"OPERATOR


class mball_ellipsoid (bpy.types.Operator):
    """Create Metaball : Ellipsoid"""
    bl_label = ""
    bl_idname = "object.button_mball_ellipsoid"

    def execute(self, context):
        bpy.ops.object.metaball_add(
            type='ELLIPSOID', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# METABALL BUTTON "CUBE"OPERATOR


class mball_cube (bpy.types.Operator):
    """Create Metaball : Cube"""
    bl_label = ""
    bl_idname = "object.button_mball_cube"

    def execute(self, context):
        bpy.ops.object.metaball_add(
            type='CUBE', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# METABALL PANEL


class Add_Metaball (bpy.types.Panel):
    bl_label = "METABALL"
    bl_idname = "PT_AddMetaball"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_ArcBlend"

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        row = layout.row()
        col.label(text="ADD METABALL", icon="OUTLINER_OB_META")
        row = layout.row()
        row.operator("object.button_mball_ball", icon="META_BALL")
        row.operator("object.button_mball_capsule", icon="META_CAPSULE")
        row.operator("object.button_mball_plane", icon="META_PLANE")
        row.operator("object.button_mball_ellipsoid", icon="META_ELLIPSOID")
        row.operator("object.button_mball_cube", icon="META_CUBE")
        row = layout.row()

# ------------------------------------------------------------------------------
# ----------------------------------------------TEXT PANEL------------------------------------------------------


class Add_Text (bpy.types.Panel):
    bl_label = "Add Text"
    bl_idname = "PT_AddText"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_ArcBlend"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Add Text")
        row = layout.row()
        row.operator("object.text_add", icon="OUTLINER_OB_FONT")
        row = layout.row()

# ------------------------------------------------------------------------------
# ----------------------------------------------VOLUME PANEL----------------------------------------------------


class Add_Volume (bpy.types.Panel):
    bl_label = "Volume"
    bl_idname = "PT_AddVolume"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_ArcBlend"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Add Volume")
        row = layout.row()
        row.operator("object.volume_add", icon="VOLUME_DATA")
        row = layout.row()

# ------------------------------------------------------------------------------
# GREASE PENCIL "BLANK"OPERATOR


class grease_pencil_blank (bpy.types.Operator):
    """Add a Grease pencil object to the Scene: Blank"""
    bl_label = ""
    bl_idname = "object.button_grease_pencil_blank"

    def execute(self, context):
        bpy.ops.object.gpencil_add(align='WORLD', location=(
            0, 0, 0), scale=(1, 1, 1), type='LRT_SCENE')
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# GREASE PENCIL "STROKE"OPERATOR


class grease_pencil_stroke (bpy.types.Operator):
    """Add a Grease pencil object to the Scene : Stroke"""
    bl_label = ""
    bl_idname = "object.button_grease_pencil_stroke"

    def execute(self, context):
        bpy.ops.object.gpencil_add(align='WORLD', location=(
            0, 0, 0), scale=(1, 1, 1), type='STROKE')
        return {"FINISHED"}
# ------------------------------------------------------------------------------
# GREASE PENCIL "MONKEY"OPERATOR


class grease_pencil_monkey (bpy.types.Operator):
    """Add a Grease pencil object to the Scene : Monkey"""
    bl_label = ""
    bl_idname = "object.button_grease_pencil_monkey"

    def execute(self, context):
        bpy.ops.object.gpencil_add(align='WORLD', location=(
            0, 0, 0), scale=(1, 1, 1), type='MONKEY')
        return {"FINISHED"}
# ------------------------------------------------------------------------------
# GREASE PENCIL "SCENE LINE ART"OPERATOR


class grease_pencil_sla (bpy.types.Operator):
    """Add a Grease pencil object to the Scene: Scene Line Art"""
    bl_label = ""
    bl_idname = "object.button_grease_pencil_sla"

    def execute(self, context):
        bpy.ops.object.gpencil_add(align='WORLD', location=(
            0, 0, 0), scale=(1, 1, 1), type='LRT_SCENE')
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# GREASE PENCIL "COLLECTION LINE ART"OPERATOR


class grease_pencil_cla (bpy.types.Operator):
    """Add a Grease pencil object to the Scene : Collection Line Art"""
    bl_label = ""
    bl_idname = "object.button_grease_pencil_cla"

    def execute(self, context):
        bpy.ops.object.gpencil_add(align='WORLD', location=(
            0, 0, 0), scale=(1, 1, 1), type='LRT_COLLECTION')
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# GREASE PENCIL "OBJECT LINE ART"OPERATOR


class grease_pencil_ola (bpy.types.Operator):
    """Add a Grease pencil object to the Scene : Object Line Art"""
    bl_label = ""
    bl_idname = "object.button_grease_pencil_ola"

    def execute(self, context):
        bpy.ops.object.gpencil_add(align='WORLD', location=(
            0, 0, 0), scale=(1, 1, 1), type='LRT_OBJECT')
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# GREASE PENCIL PANEL


class Add_Grease_Pencil (bpy.types.Panel):
    bl_label = "GREASE PENCIL"
    bl_idname = "PT_AddGreasePencil"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_ArcBlend"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="ADD GREASE PENCIL", icon="GP_SELECT_STROKES")
        row = layout.row()
        row.operator("object.button_grease_pencil_blank", icon="EMPTY_AXIS")
        row.operator("object.button_grease_pencil_stroke", icon="STROKE")
        row.operator("object.button_grease_pencil_monkey", icon="MONKEY")
        row.operator("object.button_grease_pencil_sla", icon="SCENE_DATA")
        row.operator("object.button_grease_pencil_cla",
                     icon="OUTLINER_COLLECTION")
        row.operator("object.button_grease_pencil_ola", icon="OBJECT_DATA")
        row = layout.row()

# ------------------------------------------------------------------------------
# ARMATURE PANEL


class Add_Armature (bpy.types.Panel):
    bl_label = "Armature"
    bl_idname = "PT_AddArmature"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_ArcBlend"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Add Armature")
        row = layout.row()
        row.operator("object.armature_add", icon="OUTLINER_OB_ARMATURE")
        row = layout.row()

# ------------------------------------------------------------------------------
# LATTICE OPERATOR BUTTON


class lattice_button (bpy.types.Operator):
    """Add an Object to the scene"""
    bl_label = "Lattice"
    bl_idname = "object.button_lattice"

    def execute(self, context):
        bpy.ops.object.add(type='LATTICE', enter_editmode=False,
                           align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# LATTICE PANEL


class Add_Lattice (bpy.types.Panel):
    bl_label = "Lattice"
    bl_idname = "PT_AddLattice"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_ArcBlend"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Add Lattice")
        row = layout.row()
        row.operator("object.button_lattice", icon="OUTLINER_OB_LATTICE")
        row = layout.row()

# ------------------------------------------------------------------------------
# EMPTY PLAIN AXES BUTTON


class empty_plain_axes (bpy.types.Operator):
    """Add an empty object to the scene : Empty Plain Axes"""
    bl_label = "Plain Axes"
    bl_idname = "object.button_empty_plain_axes"

    def execute(self, context):
        bpy.ops.object.empty_add(
            type='PLAIN_AXES', radius=1, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# EMPTY ARROWS BUTTON


class empty_arrows (bpy.types.Operator):
    """Add an empty object to the scene : Arrows"""
    bl_label = "Arrows"
    bl_idname = "object.button_empty_arrows"

    def execute(self, context):
        bpy.ops.object.empty_add(
            type='ARROWS', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# EMPTY SINGLE ARROW BUTTON


class empty_single_arrow (bpy.types.Operator):
    """Add an empty object to the scene : Single Arrow"""
    bl_label = "Single Arrow"
    bl_idname = "object.button_empty_single_arrow"

    def execute(self, context):
        bpy.ops.object.empty_add(
            type='SINGLE_ARROW', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# EMPTY CIRCLE BUTTON


class empty_circle (bpy.types.Operator):
    """Add an empty object to the scene : Circle"""
    bl_label = "Circle"
    bl_idname = "object.button_empty_circle"

    def execute(self, context):
        bpy.ops.object.empty_add(
            type='CIRCLE', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# EMPTY CUBE BUTTON


class empty_cube (bpy.types.Operator):
    """Add an empty object to the scene : Cube"""
    bl_label = "Cube"
    bl_idname = "object.button_empty_cube"

    def execute(self, context):
        bpy.ops.object.empty_add(
            type='CUBE', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# EMPTY SPHERE BUTTON


class empty_sphere (bpy.types.Operator):
    """Add an empty object to the scene : Sphere"""
    bl_label = "Sphere"
    bl_idname = "object.button_empty_sphere"

    def execute(self, context):
        bpy.ops.object.empty_add(
            type='SPHERE', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# EMPTY CONE BUTTON


class empty_cone (bpy.types.Operator):
    """Add an empty object to the scene : Cone"""
    bl_label = "Cone"
    bl_idname = "object.button_empty_cone"

    def execute(self, context):
        bpy.ops.object.empty_add(
            type='CONE', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# EMPTY IMAGE BUTTON


class empty_image (bpy.types.Operator):
    """Add an empty object to the scene : Image"""
    bl_label = "Image"
    bl_idname = "object.button_empty_image"

    def execute(self, context):
        bpy.ops.object.empty_add(
            type='IMAGE', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# EMPTY PANEL


class Add_Empty (bpy.types.Panel):
    bl_label = "Empty"
    bl_idname = "PT_AddEmpty"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_ArcBlend"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Add Empty")
        row = layout.row()
        row.operator("object.button_empty_plain_axes", icon="EMPTY_AXIS")
        row.operator("object.button_empty_arrows", icon="EMPTY_ARROWS")
        row = layout.row()
        row.operator("object.button_empty_single_arrow",
                     icon="EMPTY_SINGLE_ARROW")
        row.operator("object.button_empty_circle", icon="MESH_CIRCLE")
        row = layout.row()
        row.operator("object.button_empty_cube", icon="CUBE")
        row.operator("object.button_empty_sphere", icon="SPHERE")
        row = layout.row()
        row.operator("object.button_empty_cone", icon="CONE")
        row.operator("object.button_empty_image", icon="IMAGE_DATA")
        row = layout.row()

# ------------------------------------------------------------------------------
# IMAGE PANEL


class Add_Image (bpy.types.Panel):
    bl_label = "Image"
    bl_idname = "PT_AddImage"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_ArcBlend"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        col = layout.column()
        row.label(text="Add Image")
        row = layout.row()
        row.operator("object.empty_add", icon="IMAGE_BACKGROUND")
        row = layout.row()
# ------------------------------------------------------------------------------
# LIGHT POINT BUTTON


class light_point (bpy.types.Operator):
    """Add a light object to the scene : Point Light"""
    bl_label = "Point Light"
    bl_idname = "object.button_light_point"

    def execute(self, context):

        bpy.ops.object.light_add(
            type='POINT', radius=1, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}
# ------------------------------------------------------------------------------
# LIGHT SUN BUTTON


class light_sun (bpy.types.Operator):
    """Add a light object to the scene : Sun"""
    bl_label = "Sun"
    bl_idname = "object.button_light_sun"

    def execute(self, context):
        bpy.ops.object.light_add(
            type='SUN', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# LIGHT SPOT BUTTON


class light_spot (bpy.types.Operator):
    """Add a light object to the scene : Spot Light"""
    bl_label = "Spot Light"
    bl_idname = "object.button_light_spot"

    def execute(self, context):
        bpy.ops.object.light_add(
            type='SPOT', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}
# ------------------------------------------------------------------------------
# LIGHT AREA BUTTON


class light_area (bpy.types.Operator):
    """Add a light object to the scene : Area Light"""
    bl_label = "Area Light"
    bl_idname = "object.button_light_area"

    def execute(self, context):
        bpy.ops.object.light_add(
            type='AREA', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# LIGHT PANEL


class Add_Light (bpy.types.Panel):
    bl_label = "Light"
    bl_idname = "PT_AddLight"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_ArcBlend"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = layout.column()
        row.label(text="Add Light")
        row = layout.row()
        row.operator("object.button_light_point", icon="LIGHT_POINT")
        row.operator("object.button_light_sun", icon="LIGHT_SUN")
        row = layout.row()
        row.operator("object.button_light_spot", icon="LIGHT_SPOT")
        row.operator("object.button_light_area", icon="LIGHT_AREA")
        row = layout.row()

# ------------------------------------------------------------------------------
# LIGHT PROBE REFLECTION CUBEMAP BUTTON


class light_probe_cubemap (bpy.types.Operator):
    """Add a light probe object to the scene : Cubemap"""
    bl_label = "Reflection Cubemap"
    bl_idname = "object.button_light_probe_cubemap"

    def execute(self, context):
        bpy.ops.object.lightprobe_add(
            type='CUBEMAP', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}
# ------------------------------------------------------------------------------
# LIGHT PROBE REFLECTION PLANE BUTTON


class light_probe_reflectionplane (bpy.types.Operator):
    """Add a light probe object to the scene : Cubemap"""
    bl_label = "Reflection Plane"
    bl_idname = "object.button_light_probe_reflectionplane"

    def execute(self, context):
        bpy.ops.object.lightprobe_add(
            type='PLANAR', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# LIGHT PROBE IRRADIENCE VOLUME BUTTON


class light_probe_irradiencevolume (bpy.types.Operator):
    """Add a light probe object to the scene : Cubemap"""
    bl_label = "Reflection Irradience Volume"
    bl_idname = "object.button_light_probe_irradiencevolume"

    def execute(self, context):
        bpy.ops.object.lightprobe_add(
            type='GRID', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# LIGHT PROBE PANEL


class Add_Light_Probe (bpy.types.Panel):
    bl_label = "Light Probe"
    bl_idname = "PT_AddLightProbe"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_ArcBlend"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = layout.column()
        row.label(text="Add Light Probe")
        row = layout.row()
        row.operator("object.button_light_probe_cubemap",
                     icon="LIGHTPROBE_CUBEMAP")
        row = layout.row()
        row.operator("object.button_light_probe_reflectionplane",
                     icon="LIGHTPROBE_PLANAR")
        row = layout.row()
        row.operator("object.button_light_probe_irradiencevolume",
                     icon="LIGHTPROBE_GRID")
        row = layout.row()

# ------------------------------------------------------------------------------
# ADD CAMERA BUTTON


class camera_normal (bpy.types.Operator):
    """Add a camera object to the scene"""
    bl_label = "Add Camera"
    bl_idname = "object.button_camera_normal"

    def execute(self, context):
        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(
            0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# CAMERA PANEL


class Add_Camera (bpy.types.Panel):
    bl_label = "Camera"
    bl_idname = "PT_AddCamera"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_ArcBlend"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = layout.column()
        row.label(text="Add Camera")
        row = layout.row()
        row.operator("object.button_camera_normal", icon="OUTLINER_OB_CAMERA")
        row = layout.row()

# ------------------------------------------------------------------------------
# ADD SPEAKER BUTTON


class speaker_button (bpy.types.Operator):
    """Add a speaker object to the scene"""
    bl_label = "Add Speaker"
    bl_idname = "object.button_speaker_button"

    def execute(self, context):
        bpy.ops.object.speaker_add(
            enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# SPEAKER PANEL


class Add_Speaker (bpy.types.Panel):
    bl_label = "Speaker"
    bl_idname = "PT_AddSpeaker"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_ArcBlend"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = layout.column()
        row.label(text="Add Speaker")
        row = layout.row()
        row.operator("object.button_speaker_button",
                     icon="OUTLINER_OB_SPEAKER")
        row = layout.row()

# ------------------------------------------------------------------------------
# FORCE FIELD "FORCE"BUTTON


class forcefield_force (bpy.types.Operator):
    """Add an empty object with a physics effector to the scene: Force"""
    bl_label = "Force"
    bl_idname = "object.button_forcefield_force"

    def execute(self, context):
        bpy.ops.object.effector_add(
            type='FORCE', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}
# ------------------------------------------------------------------------------
# FORCE FIELD "WIND"BUTTON


class forcefield_wind (bpy.types.Operator):
    """Add an empty object with a physics effector to the scene: Wind"""
    bl_label = "Wind"
    bl_idname = "object.button_forcefield_wind"

    def execute(self, context):
        bpy.ops.object.effector_add(
            type='WIND', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# FORCE FIELD "VORTEX"BUTTON


class forcefield_vortex (bpy.types.Operator):
    """Add an empty object with a physics effector to the scene: Vortex"""
    bl_label = "Vortex"
    bl_idname = "object.button_forcefield_vortex"

    def execute(self, context):
        bpy.ops.object.effector_add(
            type='VORTEX', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# FORCE FIELD "MAGNETİC"BUTTON


class forcefield_magnetic (bpy.types.Operator):
    """Add an empty object with a physics effector to the scene: Magnetic"""
    bl_label = "Magnetic"
    bl_idname = "object.button_forcefield_magnetic"

    def execute(self, context):
        bpy.ops.object.effector_add(
            type='MAGNET', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# FORCE FIELD "HARMONIC"BUTTON


class forcefield_harmonic (bpy.types.Operator):
    """Add an empty object with a physics effector to the scene: Harmonic"""
    bl_label = "Harmonic"
    bl_idname = "object.button_forcefield_harmonic"

    def execute(self, context):
        bpy.ops.object.effector_add(
            type='HARMONIC', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# FORCE FIELD "CHARGE"BUTTON


class forcefield_charge (bpy.types.Operator):
    """Add an empty object with a physics effector to the scene: Charge"""
    bl_label = "Charge"
    bl_idname = "object.button_forcefield_charge"

    def execute(self, context):
        bpy.ops.object.effector_add(
            type='CHARGE', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# FORCE FIELD "LENNARD JONES"BUTTON


class forcefield_lennardj (bpy.types.Operator):
    """Add an empty object with a physics effector to the scene: Lennard Jones"""
    bl_label = "Lennard Jones"
    bl_idname = "object.button_forcefield_lennardj"

    def execute(self, context):
        bpy.ops.object.effector_add(
            type='LENNARDJ', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# FORCE FIELD "TEXTURE"BUTTON


class forcefield_texture (bpy.types.Operator):
    """Add an empty object with a physics effector to the scene: Texture"""
    bl_label = "Texture"
    bl_idname = "object.button_forcefield_texture"

    def execute(self, context):
        bpy.ops.object.effector_add(
            type='TEXTURE', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# FORCE FIELD "CURVE GUIDE"BUTTON


class forcefield_curveguide (bpy.types.Operator):
    """Add an empty object with a physics effector to the scene: Curve Guide"""
    bl_label = "Curve Guide"
    bl_idname = "object.button_forcefield_curveguide"

    def execute(self, context):
        bpy.ops.object.effector_add(
            type='GUIDE', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# FORCE FIELD "BOID"BUTTON


class forcefield_boid (bpy.types.Operator):
    """Add an empty object with a physics effector to the scene: Boid"""
    bl_label = "Boid"
    bl_idname = "object.button_forcefield_boid"

    def execute(self, context):
        bpy.ops.object.effector_add(
            type='BOID', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# FORCE FIELD "TURBULANCE"BUTTON


class forcefield_turbulance (bpy.types.Operator):
    """Add an empty object with a physics effector to the scene: Turbulance"""
    bl_label = "Turbulance"
    bl_idname = "object.button_forcefield_turbulance"

    def execute(self, context):
        bpy.ops.object.effector_add(
            type='TURBULENCE', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# FORCE FIELD "DRAG"BUTTON


class forcefield_drag (bpy.types.Operator):
    """Add an empty object with a physics effector to the scene: Drag"""
    bl_label = "Drag"
    bl_idname = "object.button_forcefield_drag"

    def execute(self, context):
        bpy.ops.object.effector_add(
            type='DRAG', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# FORCE FIELD "FLUID FLOW"BUTTON


class forcefield_fluidflow (bpy.types.Operator):
    """Add an empty object with a physics effector to the scene: Fluid Flow"""
    bl_label = "Fluid Flow"
    bl_idname = "object.button_forcefield_fluidflow"

    def execute(self, context):
        bpy.ops.object.effector_add(
            type='FLUID', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# FORCE FIELD PANEL


class Add_Force_Field (bpy.types.Panel):
    bl_label = "Force Field"
    bl_idname = "PT_AddForcefield"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_ArcBlend"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = layout.column()
        row.label(text="Add Force Field")
        row = layout.row()
        row.operator("object.button_forcefield_force", icon="FORCE_FORCE")
        row.operator("object.button_forcefield_wind", icon="FORCE_WIND")
        row = layout.row()
        row.operator("object.button_forcefield_vortex", icon="FORCE_VORTEX")
        row.operator("object.button_forcefield_magnetic",
                     icon="FORCE_MAGNETIC")
        row = layout.row()
        row.operator("object.button_forcefield_harmonic",
                     icon="FORCE_HARMONIC")
        row.operator("object.button_forcefield_charge", icon="FORCE_CHARGE")
        row = layout.row()
        row.operator("object.button_forcefield_lennardj",
                     icon="FORCE_LENNARDJONES")
        row.operator("object.button_forcefield_texture", icon="FORCE_TEXTURE")
        row = layout.row()
        row.operator("object.button_forcefield_curveguide", icon="FORCE_CURVE")
        row.operator("object.button_forcefield_boid", icon="FORCE_BOID")
        row = layout.row()
        row.operator("object.button_forcefield_turbulance",
                     icon="FORCE_TURBULENCE")
        row.operator("object.button_forcefield_drag", icon="FORCE_DRAG")
        row = layout.row()
        row.operator("object.button_forcefield_fluidflow",
                     icon="FORCE_FLUIDFLOW")
        row = layout.row()

# ------------------------------------------------------------------------------
# COLLECTION INSTANCE "COLLECTION"BUTTON


class collection_instance_collection (bpy.types.Operator):
    """Add a Collection Instance : Collection"""
    bl_label = "Collection"
    bl_idname = "object.button_collection_instance_collection"

    def execute(self, context):
        bpy.ops.object.collection_instance_add(
            collection='Collection', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# COLLECTION PANEL


class Add_Collection_instance (bpy.types.Panel):
    bl_label = "Collection"
    bl_idname = "PT_AddCollectioninstance"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_ArcBlend"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = layout.column()
        row.label(text="Add Collection Instance")
        row = layout.row()
        row.operator("object.button_collection_instance_collection",
                     icon="OUTLINER_COLLECTION")
        row = layout.row()

# ------------------------------------------------------------------------------
# ARC BLEND MODIFIERS PANEL


class ArcBlendModifiers (bpy.types.Panel):
    bl_label = "AB Modify"
    bl_idname = "PT_ArcBlendModifiers"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"

    def draw(self, context):
        layout = self.layout

# ------------------------------------------------------------------------------
# EDGE LOOP OPERATOR


class loop_multiple_select (bpy.types.Operator):
    """Select a loop of connected edges by connection type"""
    bl_label = "Edge Loop"
    bl_idname = "object.button_loop_multiple_select"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.loop_multi_select(ring=False)
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# RING LOOP OPERATOR


class loop_multiple_select_ring (bpy.types.Operator):
    """Select a loop of connected edges by connection type"""
    bl_label = "Ring Loop"
    bl_idname = "object.button_loop_multiple_select_ring"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.loop_multi_select(ring=True)
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# SELECT LOOP OPERATOR


class loop_select (bpy.types.Operator):
    """Select region of faces inside of a selected loop of edges"""
    bl_label = "Loop to Region"
    bl_idname = "object.button_loop_select"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.loop_to_region(select_bigger=False)
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# SELECT BOUNDRY EDGES OPERATOR


class loop_select_boundry_faces (bpy.types.Operator):
    """Select boundary edges around the selected faces"""
    bl_label = "Select Boundry Edges"
    bl_idname = "object.button_loop_select_boundry_faces"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.region_to_loop()
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# MESH SEPERATE OPERATOR


class loop_mesh_seperate (bpy.types.Operator):
    """Separate selected geometry into a new mesh"""
    bl_label = "Seperate Selected Geometry"
    bl_idname = "object.button_loop_mesh_seperate"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.separate(type='SELECTED')
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# SHORTEST PATH PICK OPERATOR


class loop_mesh_shortest_path_pick (bpy.types.Operator):
    """Select shortest path between two selections"""
    bl_label = "Shortest Path Select"
    bl_idname = "object.button_loop_mesh_shortest_path_pick"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.shortest_path_select(edge_mode='SELECT', use_face_step=False,
                                          use_topology_distance=False, use_fill=False, skip=0, nth=1, offset=0)
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# MESH SPLİT OFF OPERATOR


class loop_mesh_split (bpy.types.Operator):
    """Split off selected geometry from connected unselected geometry"""
    bl_label = "Split Off Selected Geometry"
    bl_idname = "object.button_loop_mesh_split"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.split()
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# QUADS TO TRIOS OPERATOR


class loop_mesh_quads_convert_to_tris (bpy.types.Operator):
    """Triangulate selected faces"""
    bl_label = "Quads to Trios"
    bl_idname = "object.button_loop_mesh_quads_convert_to_tris"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.quads_convert_to_tris(
            quad_method='FIXED', ngon_method='BEAUTY')
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# TRIOS TO QUADS OPERATOR


class loop_mesh_tris_convert_to_quads (bpy.types.Operator):
    """Join triangles into quads"""
    bl_label = "Trios to Quads"
    bl_idname = "object.button_loop_mesh_tris_convert_to_quads"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.tris_convert_to_quads(face_threshold=0.698132, shape_threshold=0.698132,
                                           uvs=False, vcols=False, seam=False, sharp=False, materials=False)
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# FIND TRIOS OPERATOR


class loop_mesh_find_trios (bpy.types.Operator):
    """Select vertices or faces to find trios (3 sides)"""
    bl_label = "Find Trios"
    bl_idname = "object.button_loop_mesh_find_trios"

    def execute(self, context):
        if bpy.context.active_object:
            bpy.ops.object.mode_set(mode='EDIT', toggle=True)
        else:
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.select_face_by_sides(number=3, type='EQUAL', extend=True)
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# FIND QUADS OPERATOR


class loop_mesh_find_quads (bpy.types.Operator):
    """Select vertices or faces to find quads (4 sides)"""
    bl_label = "Find Quads"
    bl_idname = "object.button_loop_mesh_find_quads"

    def execute(self, context):
        if bpy.context.active_object:
            bpy.ops.object.mode_set(mode='EDIT', toggle=True)
        else:
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.select_face_by_sides(number=4, type='EQUAL', extend=True)
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# Loopm Menu PANEL


class Loop_Menu (bpy.types.Panel):
    bl_label = "Export Object Data"
    bl_idname = "PT_ArcBlendCreateBox"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_ArcBlendModifiers"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend
        layout.label(text="File Path : ")
        layout.prop(Arc_Blend, "filepath", text="")
        col = layout.column()
        col1 = col.column(align=True)
        col1.operator("object.button_loop_sde", text="Export Data")

        # col.operator("object.button_loop_idtm", text="Import Data to Mesh")

# ------------------------------------------------------------------------------
# SELECTED DATA EXPORT


class loop_sde(bpy.types.Operator):
    bl_label = "Export Data"
    bl_description = "Exports Selected Meshes All Data to .TXT File"
    bl_idname = "object.button_loop_sde"

    def execute(self, context):
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend
        filepath = bpy.context.scene.Arc_Blend.filepath
        abverts = bpy.context.active_object.data.vertices
        abedges = bpy.context.active_object.data.edges
        abfaces = bpy.context.active_object.data.polygons
        verts = []
        edges = []
        faces = []
        for vertex in abverts:
            verts.append(tuple(vertex.co))
        for edgs in abedges:
            edges.append(tuple(edgs.vertices))
        for face in abfaces:
            faces.append(tuple(face.vertices))
        file = open(filepath, 'w')
        file.writelines(str("verts="))
        file.write(str(""))
        file.writelines(str(verts))
        file.write(str("\n"))
        file.write(str("edges="))
        file.write(str(""))
        file.write(str(edges))
        file.write(str("\n"))
        file.write(str("faces="))
        file.write(str(""))
        file.write(str(faces))
        file.close()
        return {'FINISHED'}

# ------------------------------------------------------------------------------
# IMPORT DATA TO MESH
# WORK IN PROGRESS!!!


class loop_idtm(bpy.types.Operator):
    bl_label = "Import Data to Mesh"
    bl_description = "verts,edges and faces to mesh"
    bl_idname = "object.button_loop_idtm"

    def execute(self, context):
        scene = context.scene
        Arc_Blend = scene.Arc_Blend
        mesh = bpy.data.meshes.new("Mesh")
        obj = bpy.data.objects.new(mesh.name, mesh)
        col = bpy.data.collections.get("Collection")
        col.objects.link(obj)
        bpy.context.view_layer.objects.active = obj
        verts = []
        edges = []
        faces = []
        mesh.from_pydata(verts, edges, faces)
        return {'FINISHED'}

# WORK IN PROGRESS!!!
# ------------------------------------------------------------------------------
# TRANSFORM & EDİT PANEL


class modifier (bpy.types.Panel):
    bl_label = "Transform & Edit"
    bl_idname = "PT_Transform"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_ArcBlendModifiers"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        row = layout.row()

# ------------------------------------------------------------------------------
# OBJECT  PANEL


class transform_edit_object_panel (bpy.types.Panel):
    bl_label = "Object"
    bl_idname = "PT_Object_Transform"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_Transform"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        collection = context.collection
        scene = context.scene
        Arc_Blend = scene.Arc_Blend
        col = layout.column()
        if bpy.context.selected_objects != []:
            try:
                col.prop(obj, "name")
                col.prop(obj, "type")
                col.prop(obj, "active_material")
                col.prop(obj, "data")
                col.prop(obj, "parent")
                col.prop(obj, "parent_type")
            except (TypeError,KeyError):
                pass
            col.prop(Arc_Blend, "arc_blend_set_origin")
            col = layout.column()
            col.prop(Arc_Blend, "arc_blend_manuel_axis",
                     text="Set Origin to Manuel Axis:", icon="EMPTY_AXIS")
            if bpy.context.scene.Arc_Blend.arc_blend_manuel_axis:
                box1 = layout.box()
                box1.prop(Arc_Blend, "arc_blend_manuel_origin_x",
                          text="Origin X Level")
                box1.prop(Arc_Blend, "arc_blend_manuel_origin_y",
                          text="Origin Y Level")
                box1.prop(Arc_Blend, "arc_blend_manuel_origin",
                          text="Origin Z Level")
            else:
                pass
            col = layout.column()
            sub = col.row(align=True)
            sub.prop(Arc_Blend, "align_objects_xyz",
                     text="Align Objects", icon="OUTLINER_OB_POINTCLOUD")
            if bpy.context.scene.Arc_Blend.align_objects_xyz:
                box = layout.box()
                box.label(text="Align Objects (Fast): ")
                sub = box.row(align=True)
                sub.operator(
                    "object.button_transform_edit_object_align_x", text="X")
                sub.operator(
                    "object.button_transform_edit_object_align_y", text="Y")
                sub.operator(
                    "object.button_transform_edit_object_align_z", text="Z")
                sub.operator(
                    "object.button_transform_edit_object_align_bound", text="All")
                box.prop(Arc_Blend, "distribute_objects",
                         text="Distribute Objects ", icon="MOD_ARRAY")
                if bpy.context.scene.Arc_Blend.distribute_objects:
                    sub = box.column(align=True)
                    sub.label(text="Distribute Objects : ")
                    sub.prop(Arc_Blend, "distribute_x", text="X Copy : ")
                    sub.prop(Arc_Blend, "distribute_y", text="Y Copy : ")
                    # sub.prop(Arc_Blend, "distribute_z", text="Z Copy : ")
                    sub = box.column(align=True)
                    sub.label(text="Distribute Distance : ")
                    sub.prop(Arc_Blend, "distribute_distance_object_x",
                             text="X Distance : ")
                    sub.prop(Arc_Blend, "distribute_distance_object_y",
                             text="Y Distance : ")
                    # sub.prop(Arc_Blend, "distribute_distance_object_z", text="Z Distance : ")
                else:
                    pass
                box.prop(Arc_Blend, "proportional_align",
                         text="Proportional Align ", icon="ALIGN_JUSTIFY")
                if bpy.context.scene.Arc_Blend.proportional_align:
                    # col = layout.column()
                    box.label(text="Align Objects Distance : ")
                    sub = box.column(align=True)
                    sub.prop(Arc_Blend, "distance_object_x",
                             text="X Distance:")
                    sub.prop(Arc_Blend, "distance_object_y",
                             text="Y Distance:")
                    sub.prop(Arc_Blend, "distance_object_z",
                             text="Z Distance:")
                    # col = layout.column()
                    box.label(text="Align Objects Rotation : ")
                    sub = box.column(align=True)
                    sub.prop(Arc_Blend, "rotation_object_x",
                             text="X Rotation:")
                    sub.prop(Arc_Blend, "rotation_object_y",
                             text="Y Rotation:")
                    sub.prop(Arc_Blend, "rotation_object_z",
                             text="Z Rotation:")
                    # col = layout.column()
                    box.label(text="Align Objects Scale : ")
                    sub = box.column(align=True)
                    sub.prop(Arc_Blend, "scale_object_x", text="X Scale:")
                    sub.prop(Arc_Blend, "scale_object_y", text="Y Scale:")
                    sub.prop(Arc_Blend, "scale_object_z", text="Z Scale:")
            else:
                pass
            row = layout.row()
            row = layout.row(align=True)
            row.operator("object.shade_smooth")
            row.operator("object.shade_flat")
            row = layout.row()
            row = layout.row()
            sub = row.row(align=True)
            sub.scale_x = 1.5
            sub.label(text="Color : ")
            sub.scale_x = 4.6
            sub.prop(obj, "color", text="")
            row = layout.row()
            row = layout.row(align=True)
            row.operator(
                "object.button_transform_edit_object_randomize_colors", text="Randomize Colors")
            row.operator(
                "object.button_transform_edit_object_reset_colors", text="Reset Colors")
        else:
            pass
        col = layout.column()
        col.label(text="Turn ON/OFF Display Color : ")
        col.prop(Arc_Blend, "color_mode_display", text="", icon="FILE_REFRESH")
        col.label(text="Purge unused data objects : ")
        col.operator("object.button_transform_edit_object_purge", text="Purge")
        col = layout.column()

# ------------------------------------------------------------------------------
# RANDOMIZE COLOR OPERATOR


class transform_edit_object_randomize_colors (bpy.types.Operator):
    """Randomize colors to selected Objects """
    bl_label = ""
    bl_idname = "object.button_transform_edit_object_randomize_colors"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        selected = bpy.context.selected_objects
        color = bpy.context.object.color
        for i in selected:
            if i.type == "MESH":
                alpha = i.color[3]
                red = random.random()
                green = random.random()
                blue = random.random()
                i.color = (red, green, blue, alpha)
        return {"FINISHED"}
# ------------------------------------------------------------------------------
# RESET COLOR OPERATOR


class transform_edit_object_reset_colors (bpy.types.Operator):
    """Reset colors to selected Objects colors came from Color """
    bl_label = ""
    bl_idname = "object.button_transform_edit_object_reset_colors"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        selected = bpy.context.selected_objects
        color = bpy.context.object.color

        for i in selected:
            if i.type == "MESH":
                alpha = i.color[3]
                i.color = bpy.context.object.color

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# PURGE OPERATOR


class transform_edit_object_purge (bpy.types.Operator):
    """Purge All Un-Used  Data  """
    bl_label = ""
    bl_idname = "object.button_transform_edit_object_purge"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        bpy.ops.outliner.orphans_purge()
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# ALIGN OBJECTS X AXIS OPERATOR


class transform_edit_object_align_x (bpy.types.Operator):
    """Align Objects to Active Objects' X Axis"""
    bl_label = ""
    bl_idname = "object.button_transform_edit_object_align_x"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend
        selected = bpy.context.selected_objects
        active = bpy.context.active_object
        for i in selected:
            i.location.x = active.location.x
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# ALIGN OBJECTS Y AXIS OPERATOR


class transform_edit_object_align_y (bpy.types.Operator):
    """Align Objects to Active Objects' Y Axis"""
    bl_label = ""
    bl_idname = "object.button_transform_edit_object_align_y"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend
        selected = bpy.context.selected_objects
        active = bpy.context.active_object
        for i in selected:
            i.location.y = active.location.y
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# ALIGN OBJECTS Z AXIS OPERATOR


class transform_edit_object_align_z (bpy.types.Operator):
    """Align Objects to Active Objects' Z Axis"""
    bl_label = ""
    bl_idname = "object.button_transform_edit_object_align_z"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend
        selected = bpy.context.selected_objects
        active = bpy.context.active_object
        for i in selected:
            i.location.z = active.location.z
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# ALIGN OBJECTS BOUND OPERATOR


class transform_edit_object_align_bound (bpy.types.Operator):
    """Align objects with sequence.(Sort the selected objects)"""
    bl_label = ""
    bl_idname = "object.button_transform_edit_object_align_bound"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend
        selected = bpy.context.selected_objects
        active = bpy.context.active_object
        for i in range(1, len(selected)):
            selected[i].bound_box.data.location[0] = selected[i-1].bound_box.data.location[0] + \
                bpy.context.active_object.bound_box.data.dimensions[0]
            selected[i].bound_box.data.location[1] = selected[i -
                                                              1].bound_box.data.location[1]
            selected[i].bound_box.data.location[2] = selected[i -
                                                              1].bound_box.data.location[2]
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# TRANSFORM  PANEL


class transform (bpy.types.Panel):
    bl_label = "Transform"
    bl_idname = "PT_Transformpanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_Transform"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        row = layout.row()
        col = layout.column()
        if bpy.context.selected_objects != []:
            try:
                col.prop(obj, "location")
                col.prop(obj, "rotation_euler")
                col.prop(obj, "scale")
                col.prop(obj, "dimensions")
                row = layout.row()
            except (TypeError,KeyError):
                pass
        else:
            pass

# ------------------------------------------------------------------------------
# MODIFIER PANEL


class modifier_panel (bpy.types.Panel):
    bl_label = "Modifiers Panel"
    bl_idname = "PT_modifier_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_Transform"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        row = layout.row()

# ------------------------------------------------------------------------------
# MODIFY PANEL


class modify_panel (bpy.types.Panel):
    bl_label = "Modify"
    bl_idname = "PT_modify_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_modifier_panel"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        row = layout.row()

# ------------------------------------------------------------------------------
# ARRAY PANEL


class array_panel (bpy.types.Panel):
    bl_label = "Array"
    bl_idname = "PT_array_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_modify_panel"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend
        split = layout.split()
        if bpy.context.selected_objects != []:
            # layout.prop(Arc_Blend, "text_area")
            layout.prop(Arc_Blend, "fit_type_area")
            if Arc_Blend.fit_type_area == "FIXED_COUNT":
                layout.prop(Arc_Blend, "count_area")
                layout.prop(Arc_Blend, "y_axes_copy")
                layout.prop(Arc_Blend, "z_axes_copy")
            if Arc_Blend.fit_type_area == "FIT_LENGTH":
                layout.prop(Arc_Blend, "length_area")
                layout.prop(Arc_Blend, "y_axes_length")
                layout.prop(Arc_Blend, "z_axes_length")
            if Arc_Blend.fit_type_area == "FIT_CURVE":
                layout.prop(Arc_Blend, "curve_select")
            else:
                row = layout.row()
                col = layout.column()
                col.label(
                    text="-----------------------------------------------------------------")
                row = layout.row()
                row.operator("object.button_modifier_array", icon="MOD_ARRAY")
                row.operator(
                    "object.button_modifier_array_detail_executer", text="Result")
                row.operator("object.button_modifier_array_apply",
                             icon="CHECKMARK")
        else:
            pass

# ------------------------------------------------------------------------------
# ARRAY OPERATOR


class modifier_array (bpy.types.Operator):
    """Add a procedural operation/effect to the active object: Array"""
    bl_label = ""
    bl_idname = "object.button_modifier_array"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend
        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.ops.object.modifier_add(type='ARRAY')
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# OBJECT MODE CHANGE DISPLAY


def color_mode_display_upd(self, context):
    try:
        if bpy.context.scene.Arc_Blend.color_mode_display:
            bpy.context.space_data.shading.color_type = 'OBJECT'
        else:
            bpy.context.space_data.shading.color_type = 'MATERIAL'
    except ValueError:
        pass
    return None

# ------------------------------------------------------------------------------
# ORIGIN SET LOW
# Answer: https://blender.stackexchange.com/questions/42105/set-origin-to-bottom-center-of-multiple-objects


def origin_set_low_upd(ob, matrix=Matrix()):
    if bpy.context.scene.Arc_Blend.arc_blend_set_origin == 'origin_to_low':
        me = ob.data
        mw = ob.matrix_world
        local_verts = [matrix @ Vector(v[:])for v in ob.bound_box]
        o = sum(local_verts, Vector()) / 8
        o.z = min(v.z for v in local_verts)
        o = matrix.inverted() @ o
        me.transform(Matrix.Translation(-o))
        mw.translation = mw @ o
    return {"FINISHED"}

# ------------------------------------------------------------------------------
# ORIGIN SET HIGH
# I added to  max values :).


def origin_set_high_upd(ob, matrix=Matrix()):

    if bpy.context.scene.Arc_Blend.arc_blend_set_origin == 'origin_to_high':
        me = ob.data
        mw = ob.matrix_world
        local_verts = [matrix @ Vector(v[:])for v in ob.bound_box]
        o = sum(local_verts, Vector()) / 8
        o.z = max(v.z for v in local_verts)
        o = matrix.inverted() @ o
        me.transform(Matrix.Translation(-o))
        mw.translation = mw @ o
    return {"FINISHED"}

# ------------------------------------------------------------------------------
# ORIGIN SET MANUEL Z LEVEL


def origin_set_manuel_matrix(ob, matrix=Matrix()):
    me = ob.data
    mw = ob.matrix_world
    local_verts = [matrix @ Vector(v[:])for v in ob.bound_box]
    o = sum(local_verts, Vector()) / 8
    o.x = min(v.x for v in local_verts)+bpy.context.object.dimensions.x * \
        int(bpy.context.scene.Arc_Blend.arc_blend_manuel_origin_x)/100
    o.y = min(v.y for v in local_verts)+bpy.context.object.dimensions.y * \
        int(bpy.context.scene.Arc_Blend.arc_blend_manuel_origin_y)/100
    o.z = min(v.z for v in local_verts)+bpy.context.object.dimensions.z * \
        int(bpy.context.scene.Arc_Blend.arc_blend_manuel_origin)/100
    o = matrix.inverted() @ o
    me.transform(Matrix.Translation(-o))
    mw.translation = mw @ o
    return {"FINISHED"}

# ------------------------------------------------------------------------------
# ORIGIN SET MANUEL Z UPDATE


def origin_set_manuel_upd(self, context):
    if bpy.context.scene.Arc_Blend.arc_blend_manuel_origin >= 0 or bpy.context.scene.Arc_Blend.arc_blend_manuel_origin <0:
        for i in bpy.context.selected_objects:
            if i.type == 'MESH':
                ob = i
                origin_set_manuel_matrix(ob)
    return None

# ------------------------------------------------------------------------------
# ORIGIN SET MANUEL Y LEVEL


def origin_set_manuel_matrix_y(ob, matrix=Matrix()):
    me = ob.data
    mw = ob.matrix_world
    local_verts = [matrix @ Vector(v[:])for v in ob.bound_box]
    o = sum(local_verts, Vector()) / 8
    o.x = min(v.x for v in local_verts)+bpy.context.object.dimensions.x * \
        int(bpy.context.scene.Arc_Blend.arc_blend_manuel_origin_x)/100
    o.y = min(v.y for v in local_verts)+bpy.context.object.dimensions.y * \
        int(bpy.context.scene.Arc_Blend.arc_blend_manuel_origin_y)/100
    o.z = min(v.z for v in local_verts)+bpy.context.object.dimensions.z * \
        int(bpy.context.scene.Arc_Blend.arc_blend_manuel_origin)/100
    o = matrix.inverted() @ o
    me.transform(Matrix.Translation(-o))
    mw.translation = mw @ o
    return {"FINISHED"}

# ------------------------------------------------------------------------------
# ORIGIN SET MANUEL Y UPDATE


def origin_set_manuel_upd_y(self, context):

    if bpy.context.scene.Arc_Blend.arc_blend_manuel_origin_y >= 0 or bpy.context.scene.Arc_Blend.arc_blend_manuel_origin_y <0:
        for i in bpy.context.selected_objects:
            if i.type == 'MESH':
                ob = i
                origin_set_manuel_matrix_y(ob)
    return None

# ------------------------------------------------------------------------------
# ORIGIN SET MANUEL X LEVEL


def origin_set_manuel_matrix_x(ob, matrix=Matrix()):
    me = ob.data
    mw = ob.matrix_world
    local_verts = [matrix @ Vector(v[:])for v in ob.bound_box]
    o = sum(local_verts, Vector()) / 8
    o.x = min(v.x for v in local_verts)+bpy.context.object.dimensions.x * \
        int(bpy.context.scene.Arc_Blend.arc_blend_manuel_origin_x)/100
    o.y = min(v.y for v in local_verts)+bpy.context.object.dimensions.y * \
        int(bpy.context.scene.Arc_Blend.arc_blend_manuel_origin_y)/100
    o.z = min(v.z for v in local_verts)+bpy.context.object.dimensions.z * \
        int(bpy.context.scene.Arc_Blend.arc_blend_manuel_origin)/100
    o = matrix.inverted() @ o
    me.transform(Matrix.Translation(-o))
    mw.translation = mw @ o
    return {"FINISHED"}

# ------------------------------------------------------------------------------
# ORIGIN SET MANUEL X UPDATE


def origin_set_manuel_upd_x(self, context):
    if bpy.context.scene.Arc_Blend.arc_blend_manuel_origin_x >= 0 or bpy.context.scene.Arc_Blend.arc_blend_manuel_origin_x <0:
        for i in bpy.context.selected_objects:
            if i.type == 'MESH':
                ob = i
                origin_set_manuel_matrix_x(ob)
    return None

# ------------------------------------------------------------------------------
# OBJECT ORIGIN SET
# I use the blender's origin operators and converting to update mode. If enumProperty values change then
# automatically values runs the operator.


def object_set_origin_upd(self, context):
    if bpy.context.scene.Arc_Blend.arc_blend_set_origin == 'geometry_to_origin':
        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
    elif bpy.context.scene.Arc_Blend.arc_blend_set_origin == 'origin_to_geometry':
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    elif bpy.context.scene.Arc_Blend.arc_blend_set_origin == 'origin_to_3d_cursor':
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    elif bpy.context.scene.Arc_Blend.arc_blend_set_origin == 'origin_to_center_of_mass_center':
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
    elif bpy.context.scene.Arc_Blend.arc_blend_set_origin == 'origin_to_center_of_mass_volume':
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME')
    # This statement runs lowest level origins.
    elif bpy.context.scene.Arc_Blend.arc_blend_set_origin == 'origin_to_low':
        # This for loop include all selected objects.
        for i in bpy.context.selected_objects:
            # And this looking for mesh types. If you want to change.Look Blender's type.
            if i.type == 'MESH':
                ob = i
                origin_set_low_upd(ob)
    # This statement runs highest level origins.
    elif bpy.context.scene.Arc_Blend.arc_blend_set_origin == 'origin_to_high':
        for i in bpy.context.selected_objects:
            if i.type == 'MESH':
                ob = i
                origin_set_high_upd(ob)
    return None

# ------------------------------------------------------------------------------
# Scatter Update


def object_scatter_upd(self, context):
    try:
        if self.object_scatter:
            bpy.data.particles[bpy.context.object.particle_systems.data.particle_systems.active.settings.name].type = 'HAIR'
        else:
            bpy.data.particles[bpy.context.object.particle_systems.data.particle_systems.active.settings.name].type = 'EMITTER'
    except AttributeError:
        pass
    return None

# ------------------------------------------------------------------------------
# OBJECT ORIGIN SET
# I use the blender's origin operators and converting to update mode. If enumProperty values change then
# automatically values runs the operator.


def object_scatter_view_as_upd(self, context):
    if bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_none':
        bpy.data.particles[bpy.context.object.particle_systems.data.particle_systems.active.settings.name].render_type = 'NONE'
    elif bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_path':
        bpy.data.particles[bpy.context.object.particle_systems.data.particle_systems.active.settings.name].render_type = 'PATH'
    elif bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_object':
        bpy.data.particles[bpy.context.object.particle_systems.data.particle_systems.active.settings.name].render_type = 'OBJECT'
    elif bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_collection':
        bpy.data.particles[bpy.context.object.particle_systems.data.particle_systems.active.settings.name].render_type = 'COLLECTION'

# ------------------------------------------------------------------------------
# PAINT GROUP DEF


def object_scatter_paint_panel_upd(self, context):
    if bpy.context.scene.Arc_Blend.object_scatter_paint_panel:
        bpy.context.active_object.select_set(True)
        bpy.ops.paint.weight_paint_toggle()
    else:
        bpy.ops.paint.weight_paint_toggle()

# ------------------------------------------------------------------------------
# MODELLING EDIT MODE DEF


def modelling_edit_mode_upd(self, context):
    try:
        if bpy.context.scene.Arc_Blend.modelling_edit_mode:
            bpy.context.active_object.select_set(True)
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        else:
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    except (RuntimeError, AttributeError):
        pass

# ------------------------------------------------------------------------------
# MODELLING EDIT MODE VERTEX DEF


def modelling_edit_mode_auto_edge_loop_upd(self, context):
    # o = bpy.context.active_object
    # m = o.data
    # bm = bmesh.from_edit_mesh(m)
    # edge_lengths=[]
    # for e in bm.edges:
    #  if e.select:
    #        edge_lengths.append(e.calc_length())
    # n=len(edge_lengths)
    if bpy.context.scene.Arc_Blend.modelling_edit_mode_auto_edge_loop:
        bpy.ops.mesh.loop_multi_select(ring=False)
    else:
        pass

# ------------------------------------------------------------------------------
# ALIGN OBJECT X UPDATE


def distance_object_x_upd(self, context):
    selected = bpy.context.selected_objects
    active = bpy.context.active_object
    number_x = bpy.context.scene.Arc_Blend.distribute_x
    number_y = bpy.context.scene.Arc_Blend.distribute_y
    for i in range(1, len(selected)):
        selected[i].location.x = selected[i-1].location.x + \
            bpy.context.scene.Arc_Blend.distance_object_x

# ------------------------------------------------------------------------------
# ALIGN OBJECT Y UPDATE


def distance_object_y_upd(self, context):
    selected = bpy.context.selected_objects
    active = bpy.context.active_object
    number_x = bpy.context.scene.Arc_Blend.distribute_x
    number_y = bpy.context.scene.Arc_Blend.distribute_y
    for i in range(1, len(selected)):
        selected[i].location.y = selected[i-1].location.y + \
            bpy.context.scene.Arc_Blend.distance_object_y

# ------------------------------------------------------------------------------
# ALIGN OBJECT Z UPDATE


def distance_object_z_upd(self, context):
    selected = bpy.context.selected_objects
    active = bpy.context.active_object
    number_x = bpy.context.scene.Arc_Blend.distribute_x
    number_y = bpy.context.scene.Arc_Blend.distribute_y
    for i in range(1, len(selected)):
        selected[i].location.z = selected[i-1].location.z + \
            bpy.context.scene.Arc_Blend.distance_object_z

# ------------------------------------------------------------------------------
# ROTATION OBJECT X UPDATE


def rotation_object_x_upd(self, context):
    selected = bpy.context.selected_objects
    active = bpy.context.active_object
    for i in range(1, len(selected)):
        selected[i].rotation_euler[0] = selected[i-1].rotation_euler[0] + \
            bpy.context.scene.Arc_Blend.rotation_object_x

# ------------------------------------------------------------------------------
# ROTATION OBJECT Y UPDATE


def rotation_object_y_upd(self, context):
    selected = bpy.context.selected_objects
    active = bpy.context.active_object
    for i in range(1, len(selected)):
        selected[i].rotation_euler[1] = selected[i-1].rotation_euler[1] + \
            bpy.context.scene.Arc_Blend.rotation_object_y

# ------------------------------------------------------------------------------
# ROTATION OBJECT Z UPDATE


def rotation_object_z_upd(self, context):
    selected = bpy.context.selected_objects
    active = bpy.context.active_object
    for i in range(1, len(selected)):
        selected[i].rotation_euler[2] = selected[i-1].rotation_euler[2] + \
            bpy.context.scene.Arc_Blend.rotation_object_z

# ------------------------------------------------------------------------------
# SCALE OBJECT X UPDATE


def scale_object_x_upd(self, context):
    selected = bpy.context.selected_objects
    active = bpy.context.active_object
    for i in range(1, len(selected)):
        selected[i].scale[0] = selected[i-1].scale[0] + \
            bpy.context.scene.Arc_Blend.scale_object_x

# ------------------------------------------------------------------------------
# SCALE OBJECT Y UPDATE


def scale_object_y_upd(self, context):
    selected = bpy.context.selected_objects
    active = bpy.context.active_object
    for i in range(1, len(selected)):
        selected[i].scale[1] = selected[i-1].scale[1] + \
            bpy.context.scene.Arc_Blend.scale_object_y

# ------------------------------------------------------------------------------
# SCALE OBJECT Z UPDATE


def scale_object_z_upd(self, context):
    selected = bpy.context.selected_objects
    active = bpy.context.active_object
    for i in range(1, len(selected)):
        selected[i].scale[2] = selected[i-1].scale[2] + \
            bpy.context.scene.Arc_Blend.scale_object_z

# ------------------------------------------------------------------------------
# DISTRIBUTE DISTANCE OBJECT X UPDATE


def distribute_distance_object_x_upd(self, context):
    selected = bpy.context.selected_objects
    active = bpy.context.active_object
    quantity = len(bpy.context.selected_objects)
    # Number of elements
    number_x = bpy.context.scene.Arc_Blend.distribute_x
    number_y = bpy.context.scene.Arc_Blend.distribute_y
    # number_z = bpy.context.scene.Arc_Blend.distribute_z
    # Bound is distance of two elements
    bound_x = bpy.context.active_object.bound_box.data.dimensions[0]
    # Max distance of all elements
    # maximum_x = bound_x*quantity
    distance_x = bpy.context.scene.Arc_Blend.distribute_distance_object_x
    distance_y = bpy.context.scene.Arc_Blend.distribute_distance_object_y
    # distance_z = bpy.context.scene.Arc_Blend.distribute_distance_object_z
    try:
        for i in range(1, number_x):
            selected[i].location[0] = selected[i-1].location[0]+distance_x
    except IndexError:
        pass

# ------------------------------------------------------------------------------
# DISTRIBUTE DISTANCE OBJECT Y UPDATE


def distribute_distance_object_y_upd(self, context):
    selected = bpy.context.selected_objects
    active = bpy.context.active_object
    quantity = len(bpy.context.selected_objects)
    # Number of elements
    number_x = bpy.context.scene.Arc_Blend.distribute_x
    number_y = bpy.context.scene.Arc_Blend.distribute_y
    # number_z = bpy.context.scene.Arc_Blend.distribute_z
    # Bound is distance of two elements
    bound_x = bpy.context.active_object.bound_box.data.dimensions[0]
    # Max distance of all elements
    # maximum_x = bound_x*quantity
    distance_x = bpy.context.scene.Arc_Blend.distribute_distance_object_x
    distance_y = bpy.context.scene.Arc_Blend.distribute_distance_object_y
    # distance_z = bpy.context.scene.Arc_Blend.distribute_distance_object_z
    x_copy = distance_x
    y_copy = distance_y
    try:
        if number_x != 0:
            for i in range(number_x, number_x+number_y):
                selected[i].location[1] = selected[i-number_x].location[1]+ distance_y
        
        elif number_x == 0:
            for i in range(1, number_y):
                selected[i].location[1] = selected[i-1].location[1] + distance_y

    except IndexError:
        pass

# ------------------------------------------------------------------------------
# DISTRIBUTE DISTANCE OBJECT Z UPDATE


def distribute_distance_object_z_upd(self, context):
    selected = bpy.context.selected_objects
    active = bpy.context.active_object
    quantity = len(bpy.context.selected_objects)
    # Number of elements
    number_x = bpy.context.scene.Arc_Blend.distribute_x
    number_y = bpy.context.scene.Arc_Blend.distribute_y
    number_z = bpy.context.scene.Arc_Blend.distribute_z
    # Bound is distance of two elements
    bound_x = bpy.context.active_object.bound_box.data.dimensions[0]
    # Max distance of all elements
    # maximum_x = bound_x*quantity
    distance_x = bpy.context.scene.Arc_Blend.distribute_distance_object_x
    distance_y = bpy.context.scene.Arc_Blend.distribute_distance_object_y
    distance_z = bpy.context.scene.Arc_Blend.distribute_distance_object_z
    try:
        for i in range(number_x, number_x+number_z):
            selected[i].location[2] = selected[i-1].location[2]+distance_z
    except IndexError:
        pass

# ------------------------------------------------------------------------------
# DISTRIBUTE OBJECT X UPDATE


def distribute_x_upd(self, context):
    selected = bpy.context.selected_objects
    active = bpy.context.active_object
    quantity = len(bpy.context.selected_objects)
    # Number of elements
    number_x = bpy.context.scene.Arc_Blend.distribute_x
    number_y = bpy.context.scene.Arc_Blend.distribute_y
    # number_z = bpy.context.scene.Arc_Blend.distribute_z
    # Bound is distance of two elements
    bound_x = bpy.context.active_object.bound_box.data.dimensions[0]
    bound_y = bpy.context.active_object.bound_box.data.dimensions[1]
    bound_z = bpy.context.active_object.bound_box.data.dimensions[2]
    # Max distance of all elements
    # maximum_x = bound_x*quantity
    distance_x = bpy.context.scene.Arc_Blend.distribute_distance_object_x
    distance_y = bpy.context.scene.Arc_Blend.distribute_distance_object_y
    # distance_z = bpy.context.scene.Arc_Blend.distribute_distance_object_z

    try:
        for i in range(1, number_x):
            selected[i].location[2] = active.location[2]
            selected[i].location[1] = active.location[1]
            selected[i].location[0] = active.location[0] + i*distance_x
            
        for b in range(number_x, quantity):
            selected[b].location[0] = active.location[0]
            selected[b].location[1] = active.location[1]
            selected[b].location[2] = active.location[2]
    except IndexError:
        pass

# ------------------------------------------------------------------------------
# DISTRIBUTE OBJECT Y UPDATE


def distribute_y_upd(self, context):
    selected = bpy.context.selected_objects
    active = bpy.context.active_object
    # active = bpy.context.active_object.matrix_world.translation
    quantity = len(bpy.context.selected_objects)
    # Number of elements
    number_x = bpy.context.scene.Arc_Blend.distribute_x
    number_y = bpy.context.scene.Arc_Blend.distribute_y
    # number_z = bpy.context.scene.Arc_Blend.distribute_z
    # Bound is distance of two elements
    bound_x = bpy.context.active_object.bound_box.data.dimensions[0]
    bound_y = bpy.context.active_object.bound_box.data.dimensions[1]
    bound_z = bpy.context.active_object.bound_box.data.dimensions[2]
    # Max distance of all elements
    # maximum_x = bound_x*quantity
    distance_x = bpy.context.scene.Arc_Blend.distribute_distance_object_x
    distance_y = bpy.context.scene.Arc_Blend.distribute_distance_object_y
    # distance_z = bpy.context.scene.Arc_Blend.distribute_distance_object_z
    x_copy = distance_x
    y_copy = distance_y
    try:
        if number_x != 0:
            for i in range(number_x, number_x+number_y):
                selected[i].location[0] = selected[i-number_x].location[0]
                selected[i].location[1] = selected[i -
                                                   number_x].location[1]+y_copy
                selected[i].location[2] = selected[i-number_x].location[2]
            for b in range(number_x+number_y+number_x-1, quantity):
                selected[b].location[0] = active.location[0]
                selected[b].location[1] = active.location[1]
                selected[b].location[2] = active.location[2]
        elif number_x == 0:
            for i in range(1, number_y):
                selected[i].location[2] = active.location[2]
                selected[i].location[1] = active.location[1]+ i*distance_y
                selected[i].location[0] = active.location[0]
                
            for b in range(number_y, quantity):
                selected[b].location[0] = active.location[0]
                selected[b].location[1] = active.location[1]
                selected[b].location[2] = active.location[2]
    except IndexError:
        pass

# ------------------------------------------------------------------------------
# DISTRIBUTE OBJECT Z UPDATE


def distribute_z_upd(self, context):
    selected = bpy.context.selected_objects
    active = bpy.context.active_object
    quantity = len(bpy.context.selected_objects)
    # Number of elements
    number_x = bpy.context.scene.Arc_Blend.distribute_x
    number_y = bpy.context.scene.Arc_Blend.distribute_y
    number_z = bpy.context.scene.Arc_Blend.distribute_z
    # Bound is distance of two elements
    bound_x = bpy.context.active_object.bound_box.data.dimensions[0]
    bound_y = bpy.context.active_object.bound_box.data.dimensions[1]
    bound_z = bpy.context.active_object.bound_box.data.dimensions[2]
    # Max distance of all elements
    # maximum_x = bound_x*quantity
    try:
        if number_x == 0 and number_y == 0:
            for i in range(1, number_z):
                selected[i].location[0] = selected[i-1].location[0]
                selected[i].location[1] = selected[i-1].location[1]
                selected[i].location[2] = selected[i-1].location[2]+bound_z
            for b in range(number_z, quantity):
                selected[b].location[2] = active.location[2]
        elif number_x >= 1:
            for i in range(number_x, number_x+number_z):
                selected[i].location[0] = selected[i-number_x].location[0]
                selected[i].location[1] = selected[i-number_x].location[1]
                selected[i].location[2] = selected[i -
                                                   number_x].location[2]+bound_z
            for b in range(number_x+number_z, quantity):
                selected[b].location[2] = active.location[2]
        elif number_y >= 1:
            for i in range(number_y, number_y+number_z):
                selected[i].location[0] = selected[i-number_y].location[0]
                selected[i].location[1] = selected[i-number_y].location[1]
                selected[i].location[2] = selected[i -
                                                   number_y].location[2]+bound_z
            for b in range(number_y+number_z, quantity):
                selected[b].location[2] = active.location[2]
    except IndexError:
        pass

# ------------------------------------------------------------------------------
# DEF TOGGLE X-RAY


def toggle_xray_mode_upd(self, context):
    bpy.ops.view3d.toggle_xray()

# ------------------------------------------------------------------------------
# DEF CUTTER DISPLAY


def cutter_collection_viewport_upd(self, context):
    try:
        if bpy.context.scene.Arc_Blend.cutter_collection_viewport:
         bpy.data.collections["AB_Cutters_Collection"].hide_viewport=True
        else:
         bpy.data.collections["AB_Cutters_Collection"].hide_viewport=False
    except (TypeError,KeyError):
        pass

# ------------------------------------------------------------------------------
# DEF CUTTER RENDER


def cutter_collection_render_upd(self, context):
    try:
        if bpy.context.scene.Arc_Blend.cutter_collection_render:
            bpy.data.collections["AB_Cutters_Collection"].hide_render=True
        else:
            bpy.data.collections["AB_Cutters_Collection"].hide_render=False
    except (TypeError,KeyError):
        pass


# ------------------------------------------------------------------------------
# DEF CUTTER OBJECT COLLECTION VIEWPORT


def cutter_object_collection_viewport_upd(self, context):
    try:
        if bpy.context.scene.Arc_Blend.cutter_object_collection_viewport:
         bpy.data.collections["AB_Cutters_Object"].hide_viewport=True
        else:
         bpy.data.collections["AB_Cutters_Object"].hide_viewport=False
    except (TypeError,KeyError):
        pass

# ------------------------------------------------------------------------------
# DEF CUTTER OBJECT COLLECTION RENDER


def cutter_object_collection_render_upd(self, context):
    try:
        if bpy.context.scene.Arc_Blend.cutter_object_collection_render:
            bpy.data.collections["AB_Cutters_Object"].hide_render=True
        else:
            bpy.data.collections["AB_Cutters_Object"].hide_render=False
    except (TypeError,KeyError):
        pass

# ------------------------------------------------------------------------------
# ARRAY CLASS PROPERTYGROUP


class modifier_array_detail (bpy.types.PropertyGroup):
    # text_area: bpy.props.StringProperty(name="Text Area")#Text Area
    fit_type_area: bpy.props.EnumProperty(
        name="Fit Type",
        description="Fit Type",
        items=[("FIXED_COUNT", "Fixed Count", "Duplicate the object a certain number of times"), ("FIT_LENGTH",
                                                                                                  "Fit Length", "Generates enough copies to fit within the fixed length given by Length."), ]
    )
    count_area: bpy.props.IntProperty(
        name="X Copy",
        description="Count \nNumber of duplicates to make", soft_min=1, soft_max=1000, step=1)
    length_area: bpy.props.FloatProperty(
        name="X Length",
        description="Length \nLength to fit array within",
        soft_min=0, soft_max=1000)
    curve_select: bpy.props.FloatProperty(
        name="Curve Select",
        description="Length \nLength to fit array within",
        soft_min=0, soft_max=1000)
    # ----------RELATIVE OFFSET-----------------------------
    count_area_x: bpy.props.FloatProperty(
        name="X spacing:",
        description="Relative Offset Displacement \nThe size of the geometry will determine the distance between arrayed items",
        soft_min=1, soft_max=1000)
    count_area_y: bpy.props.FloatProperty(
        name="Y",
        description="Relative Offset Displacement \nThe size of the geometry will determine the distance between arrayed items",
        soft_min=1, soft_max=1000)
    count_area_z: bpy.props.FloatProperty(
        name="Z",
        description="Relative Offset Displacement \nThe size of the geometry will determine the distance between arrayed items",
        soft_min=1, soft_max=1000)
    # ----------RELATIVE OFFSET 2-----------------------------
    count_area_y2: bpy.props.FloatProperty(
        name="Y spacing:",
        description="Relative Offset Displacement \nThe size of the geometry will determine the distance between arrayed items",
        soft_min=1, soft_max=1000)
    # ----------RELATIVE OFFSET 3-----------------------------
    count_area_z2: bpy.props.FloatProperty(
        name="Z spacing",
        description="Relative Offset Displacement \nThe size of the geometry will determine the distance between arrayed items",
        soft_min=1, soft_max=1000)
    # ----------N Copy Y Axes  Fixed count----------------------------------
    y_axes_copy: bpy.props.IntProperty(
        name="Y Copy",
        description="Relative Offset Displacement \nThe size of the geometry will determine the distance between arrayed items",
        soft_min=0, soft_max=1000, step=1)
    # ----------N Copy Z Axes  Fixed count----------------------------------
    z_axes_copy: bpy.props.IntProperty(
        name="Z Copy",
        description="Relative Offset Displacement \nThe size of the geometry will determine the distance between arrayed items",
        soft_min=0, soft_max=1000, step=1)
    # ----------N Copy Y Axes  Fit Length----------------------------------
    y_axes_length: bpy.props.FloatProperty(
        name="Y Length",
        description="Relative Offset Displacement \nThe size of the geometry will determine the distance between arrayed items",
        soft_min=0, soft_max=1000, step=1)
    # ----------N Copy Z Axes  Fit Length----------------------------------
    z_axes_length: bpy.props.FloatProperty(
        name="Z Length",
        description="Relative Offset Displacement \nThe size of the geometry will determine the distance between arrayed items",
        soft_min=0, soft_max=1000, step=1)
    # ----------Relative Offset a----------------------------------
    relative_offset_a: bpy.props.BoolProperty(
        name="Hide X Arrays", default=True)
    relative_offset_b: bpy.props.BoolProperty(
        name="Hide Y Arrays", default=True)
    relative_offset_c: bpy.props.BoolProperty(
        name="Hide Z Arrays", default=True)
    # ----------File Path----------------------------------
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    # ----------Create a mesh----------------------------------
    verts_strings: bpy.props.StringProperty(
        name="verts",
        description="Enter All verts coordinates")
    edges_strings: bpy.props.StringProperty(
        name="edges",
        description="Enter All edges coordinates, if you want to blank, don't write anything")
    faces_strings: bpy.props.StringProperty(
        name="faces",
        description="Enter All faces coordinates, if you want to blank, don't write anything")
    # ----------Layer----------------------------------
    layer: bpy.props.IntProperty(
        name="Number of Faces",
        description="Number of Faces min=0, max=100000, default=5000",
        min=0, max=100000, default=5000)
    # Object Mode Change
    color_mode_display: bpy.props.BoolProperty(
        name="Color Mode", description="Changing Color Mode!", default=False, update=color_mode_display_upd)
    # Set Origins Change
    arc_blend_set_origin: bpy.props.EnumProperty(
        name="Set Origin",
        description="Set the object's origin, by either the moving the data, or set to center of data, or use 3D cursor ",
        items=[("geometry_to_origin", "Geometry to Origin", "Moves the model to the origin and this way the origin of the object will also be at the center of the object."),
               ("origin_to_geometry", "Origin to Geometry",
                "Generates enough copies to fit within the fixed length given by Length."),
               ("origin_to_3d_cursor", "Origin to 3D Cursor",
                "Moves the origin of the model to the position of the 3D cursor."),
               ("origin_to_center_of_mass_center", "Origin to Center of Mass (Surface)",
                "Moves the origin to the calculated center of mass of model (assuming the mesh has a uniform density)."),
               ("origin_to_center_of_mass_volume", "Origin to Center of Mass (Volume)",
                "Median Point Center, Bounding Box Center"),
               ("origin_to_low", "Origin to Lowest Level",
                "Moves the origin of the model to low and middle position (Multiple Objects Include)"),
               ("origin_to_high", "Origin to Highest Level",
                "Moves the origin of the model to High and middle position (Multiple Objects Include)"),
               ],
        update=object_set_origin_upd,
    )
    # Manuel Origin Change
    arc_blend_manuel_origin: bpy.props.IntProperty(
        name="Z level", soft_min=-100, soft_max=100, update=origin_set_manuel_upd, subtype="PERCENTAGE")
    arc_blend_manuel_origin_y: bpy.props.IntProperty(
        name="Y level", soft_min=-100, soft_max=100, update=origin_set_manuel_upd_y, subtype="PERCENTAGE")
    arc_blend_manuel_origin_x: bpy.props.IntProperty(
        name="X level", soft_min=-100, soft_max=100, update=origin_set_manuel_upd_x, subtype="PERCENTAGE")
    # ----------SET Origin Manuel Axis ON/OFF----------------------------------
    arc_blend_manuel_axis: bpy.props.BoolProperty(
        name="Set Origin of the Objects", default=False, description="Opens to manuel axis settings")
    # ----------SET Origin Manuel Axis ON/OFF----------------------------------
    object_scatter: bpy.props.BoolProperty(
        default=False, description="Object Scatter", update=object_scatter_upd)
    # Set Origins Change
    scatter_view_as: bpy.props.EnumProperty(
        name="Set Origin",
        description="Set the object's origin, by either the moving the data, or set to center of data, or use 3D cursor ",
        items=[("arc_blend_scatter_as_none", "None", "None", "X", 1),
               ("arc_blend_scatter_as_path", "Path",
                "Scatter as Path", "IPO_EASE_IN_OUT", 2),
               ("arc_blend_scatter_as_object", "Object",
                "Scatter as Object", "OUTLINER_OB_MESH", 3),
               ("arc_blend_scatter_as_collection", "Collection",
                "Scatter as Collection", "OUTLINER_COLLECTION", 4),
               ],
        update=object_scatter_view_as_upd,
    )
    # ----------Modellling Object to Edit Panel-----------------------------
    modelling_edit_mode: bpy.props.BoolProperty(
        name="Edit Mode", default=False, update=modelling_edit_mode_upd)
    # ----------Modellling Object Edit Panel Vertex Mode -----------------------------
    modelling_edit_mode_auto_edge_loop: bpy.props.BoolProperty(
        name="Vertex Mode", default=False, update=modelling_edit_mode_auto_edge_loop_upd,)
    # ----------Object Align Distance Panel Mode -----------------------------
    distance_object_x: bpy.props.FloatProperty(
        name="Distance Object X", soft_min=0, soft_max=100, update=distance_object_x_upd)
    distance_object_y: bpy.props.FloatProperty(
        name="Distance Object Y", soft_min=0, soft_max=100, update=distance_object_y_upd)
    distance_object_z: bpy.props.FloatProperty(
        name="Distance Object Z", soft_min=0, soft_max=100, update=distance_object_z_upd)
    # ----------Object Align Rotation Panel Mode -----------------------------
    rotation_object_x: bpy.props.FloatProperty(
        name="Rotation Object X", soft_min=0, soft_max=100, update=rotation_object_x_upd, subtype="ANGLE")
    rotation_object_y: bpy.props.FloatProperty(
        name="Rotation Object Y", soft_min=0, soft_max=100, update=rotation_object_y_upd, subtype="ANGLE")
    rotation_object_z: bpy.props.FloatProperty(
        name="Rotation Object Z", soft_min=0, soft_max=100, update=rotation_object_z_upd, subtype="ANGLE")
    # ----------Object Align Scale Panel Mode -----------------------------
    scale_object_x: bpy.props.FloatProperty(
        name="Scale Object X", soft_min=0, soft_max=100, update=scale_object_x_upd)
    scale_object_y: bpy.props.FloatProperty(
        name="Scale Object Y", soft_min=0, soft_max=100, update=scale_object_y_upd)
    scale_object_z: bpy.props.FloatProperty(
        name="Scale Object Z", soft_min=0, soft_max=100, update=scale_object_z_upd)
    # ----------Object Panel-----------------------------
    align_objects_xyz: bpy.props.BoolProperty(
        name="Align Objects", default=False, description="Opens to align objects settings")
    # ----------Proportional Align-----------------------------
    proportional_align: bpy.props.BoolProperty(
        name="Proportional Align : ", default=False)
    # ----------Distribute Align Distance Panel Mode -----------------------------
    distribute_distance_object_x: bpy.props.FloatProperty(
        name="Distance Object X", soft_min=0, soft_max=100, update=distribute_distance_object_x_upd)
    distribute_distance_object_y: bpy.props.FloatProperty(
        name="Distance Object Y", soft_min=0, soft_max=100, update=distribute_distance_object_y_upd)
    # distribute_distance_object_z: bpy.props.FloatProperty(name="Distance Object Z", soft_min=0, soft_max=100,update=distribute_distance_object_z_upd)
    # ----------Distribute Objects-----------------------------
    distribute_x: bpy.props.IntProperty(
        name="Distribute Object X", min=0, max=10000, update=distribute_x_upd)
    distribute_y: bpy.props.IntProperty(
        name="Distribute Object Y", min=0, max=10000, update=distribute_y_upd)
    # distribute_z: bpy.props.IntProperty(name = "Distribute Object Z", min = 0, max = 10000,update=distribute_z_upd)
    distribute_objects: bpy.props.BoolProperty(
        name="Distribute Objects : ", default=False)
    # ----------RELATIVE OFFSET Check Box-----------------------------
    hide_unhide_Relative_Offset: bpy.props.BoolProperty(
        name="X Factor : ", default=True)
    hide_unhide_Relative_Offset_Y: bpy.props.BoolProperty(
        name="Y Factor : ", default=True)
    hide_unhide_Relative_Offset_Z: bpy.props.BoolProperty(
        name="Z Factor : ", default=True)
    # ----------Paint Panel-----------------------------
    object_scatter_paint_panel: bpy.props.BoolProperty(
        name="Paint Vertex Groups", default=False, update=object_scatter_paint_panel_upd)
    # ----------Toggle X-ray-------------------------------
    toggle_xray_mode: bpy.props.BoolProperty(
        name="Z Factor : ", default=False, update=toggle_xray_mode_upd)
    # ----------MARKS-------------------------------
    marks_edit_geometry: bpy.props.BoolProperty(
        name="Marks and Clears ", default=False,)
    # ----------VIEW3D-------------------------------
    display_mode_view: bpy.props.BoolProperty(
        name="View3D", default=False)
    # ----------CUTTER-------------------------------    
    modelling_cutter: bpy.props.BoolProperty(
        name="Cutter", default=False)
    # ----------CUTTER COLLECTION--------------------   
    cutter_collection_viewport: bpy.props.BoolProperty(
        name="Viewport Display", default=False, update = cutter_collection_viewport_upd)
    cutter_collection_render: bpy.props.BoolProperty(
        name="Render Display", default=False, update = cutter_collection_render_upd)
    
    cutter_object_collection_viewport: bpy.props.BoolProperty(
        name="Viewport Display", default=False, update = cutter_object_collection_viewport_upd)
    cutter_object_collection_render: bpy.props.BoolProperty(
        name="Render Display", default=False, update = cutter_object_collection_render_upd)
    
# ------------------------------------------------------------------------------
# RELATIVE OFFSET


class Relative_Offset (bpy.types.Panel):
    bl_label = "Relative Offset"
    bl_idname = "PT_Relative_Offset"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_array_panel"  # Parent ID

    def draw(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend
        row = layout.row()
        col = layout.column()
        box = layout.box()
        if bpy.context.selected_objects != []:
            row.prop(Arc_Blend, "relative_offset_a")
            row.prop(Arc_Blend, "relative_offset_b")
            row.prop(Arc_Blend, "relative_offset_c")
            row = layout.row()
            box.prop(Arc_Blend, "hide_unhide_Relative_Offset")
            row = layout.row()
            box.prop(Arc_Blend, "hide_unhide_Relative_Offset_Y")
            box.prop(Arc_Blend, "hide_unhide_Relative_Offset_Z")
            if Arc_Blend.hide_unhide_Relative_Offset == True:
                # col.label(text="X Factor : ")
                box.prop(Arc_Blend, "count_area_x")
            else:
                False
            if Arc_Blend.hide_unhide_Relative_Offset_Y == True:
                # col.label(text="Y Factor : ")
                box.prop(Arc_Blend, "count_area_y2")
            else:
                False
            if Arc_Blend.hide_unhide_Relative_Offset_Z == True:
                # col.label(text="Z Factor : ")
                box.prop(Arc_Blend, "count_area_z2")
            else:
                False
        else:
            pass

# ------------------------------------------------------------------------------
# ARRAY APPLY OPERATOR


class modifier_array_apply (bpy.types.Operator):
    """Apply to Object : Arrays"""
    bl_label = ""
    bl_idname = "object.button_modifier_array_apply"

    def execute(self, context):
        layout = self.layout
        try:
            for obj in bpy.context.selected_objects:
                bpy.context.view_layer.objects.active = obj
                for modifier in obj.modifiers:
                    # Array Modifier Apply
                    if modifier.type == 'ARRAY':
                        try:
                            bpy.ops.object.modifier_apply(
                                modifier=modifier.name)
                        except (AttributeError, KeyError, RuntimeError):
                            bpy.ops.object.modifier_remove(modifier="Array")
        except (AttributeError, KeyError, RuntimeError):
            pass
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# ARRAY EXECUTER OPERATOR


class modifier_array_detail_executer (bpy.types.Operator):
    """Add a procedural operation/effect to the active object: Array"""
    bl_label = "OK"
    bl_idname = "object.button_modifier_array_detail_executer"

    def execute(self, context):
        scene = context.scene
        Arc_Blend = scene.Arc_Blend
        if Arc_Blend.fit_type_area == "FIXED_COUNT":
            bpy.context.object.modifiers["Array"].fit_type = 'FIXED_COUNT'
            # bpy.context.object.name = Arc_Blend.text_area
            bpy.context.object.modifiers["Array"].count = Arc_Blend.count_area
            bpy.context.object.modifiers["Array"].relative_offset_displace[0] = Arc_Blend.count_area_x
            bpy.context.object.modifiers["Array"].relative_offset_displace[1] = Arc_Blend.count_area_y
            bpy.context.object.modifiers["Array"].relative_offset_displace[2] = Arc_Blend.count_area_z
            bpy.context.object.modifiers["Array.001"].count = Arc_Blend.y_axes_copy
            bpy.context.object.modifiers["Array.001"].relative_offset_displace[0] = 0
            bpy.context.object.modifiers["Array.001"].relative_offset_displace[1] = Arc_Blend.count_area_y2
            bpy.context.object.modifiers["Array.002"].count = Arc_Blend.z_axes_copy
            bpy.context.object.modifiers["Array.002"].relative_offset_displace[2] = Arc_Blend.count_area_z2
            bpy.context.object.modifiers["Array.002"].relative_offset_displace[0] = 0
            bpy.context.object.modifiers["Array.002"].relative_offset_displace[1] = 0
            bpy.context.object.modifiers["Array"].use_relative_offset = Arc_Blend.relative_offset_a
            bpy.context.object.modifiers["Array.001"].use_relative_offset = Arc_Blend.relative_offset_b
            bpy.context.object.modifiers["Array.002"].use_relative_offset = Arc_Blend.relative_offset_c
        if Arc_Blend.fit_type_area == "FIT_LENGTH":
            bpy.context.object.modifiers["Array"].fit_type = 'FIT_LENGTH'
            # bpy.context.object.name = Arc_Blend.text_area
            bpy.context.object.modifiers["Array"].fit_length = Arc_Blend.length_area
            bpy.context.object.modifiers["Array.001"].fit_length = Arc_Blend.y_axes_length
            bpy.context.object.modifiers["Array.002"].fit_length = Arc_Blend.z_axes_length
            bpy.context.object.modifiers["Array"].relative_offset_displace[0] = Arc_Blend.count_area_x
            bpy.context.object.modifiers["Array"].relative_offset_displace[1] = Arc_Blend.count_area_y
            bpy.context.object.modifiers["Array"].relative_offset_displace[2] = Arc_Blend.count_area_z
            bpy.context.object.modifiers["Array.001"].count = Arc_Blend.y_axes_copy
            bpy.context.object.modifiers["Array.001"].relative_offset_displace[0] = 0
            bpy.context.object.modifiers["Array.001"].relative_offset_displace[1] = Arc_Blend.count_area_y2
            bpy.context.object.modifiers["Array.002"].count = Arc_Blend.z_axes_copy
            bpy.context.object.modifiers["Array.002"].relative_offset_displace[2] = Arc_Blend.count_area_z2
            bpy.context.object.modifiers["Array.002"].relative_offset_displace[0] = 0
            bpy.context.object.modifiers["Array.002"].relative_offset_displace[1] = 0
            bpy.context.object.modifiers["Array"].use_relative_offset = Arc_Blend.relative_offset_a
            bpy.context.object.modifiers["Array.001"].use_relative_offset = Arc_Blend.relative_offset_b
            bpy.context.object.modifiers["Array.002"].use_relative_offset = Arc_Blend.relative_offset_c
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# BEVEL PANEL


class bevel_panel (bpy.types.Panel):
    bl_label = "Bevel"
    bl_idname = "PT_bavel_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_modify_panel"  # Parent ID

    def draw(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        AB_Bevel = scene.AB_Bevel
        row = layout.row()
        col = layout.column()
        if bpy.context.selected_objects != []:
            layout.prop(AB_Bevel, "Width_Type_area")
            if AB_Bevel.Width_Type_area == 'OFFSET':
                layout.prop(AB_Bevel, "Amount_area")
            elif AB_Bevel.Width_Type_area == 'WIDTH':
                layout.prop(AB_Bevel, "Amount_area")
            elif AB_Bevel.Width_Type_area == 'DEPTH':
                layout.prop(AB_Bevel, "Amount_area")
            elif AB_Bevel.Width_Type_area == 'ABSOLUTE':
                layout.prop(AB_Bevel, "Amount_area")
            else:
                False
            if AB_Bevel.Width_Type_area == 'PERCENT':
                layout.prop(AB_Bevel, "Width_Percent_area")
            else:
                False
            layout.prop(AB_Bevel, "Segment_area")
            layout.label(text="Fixed Type")
            layout.prop(AB_Bevel, "Limit_Method_area")
            if AB_Bevel.Limit_Method_area == 'ANGLE':
                layout.prop(AB_Bevel, "Angle_area")
            else:
                False
            row = layout.row()
            col = layout.column()
            row = layout.row()
            col = layout.column()
            col.label(text="------------------Result Tab--------------------")
            row = layout.row()
            row.operator("object.button_modifier_bevel_v_button",
                         text="Vertices")
            row.operator("object.button_modifier_bevel_e_button", text="Edges")
            row = layout.row()
            row.operator("object.button_modifier_bevel_button",
                         icon="MOD_BEVEL")
            row.operator(
                "object.button_modifier_bevel_detail_executer", text="Result")
            row.operator("object.button_modifier_bevel_apply",
                         icon="CHECKMARK")
        else:
            pass

# ------------------------------------------------------------------------------
# BEVEL  BUTTON PANEL


class modifier_bevel_button (bpy.types.Operator):
    """Add a procedural operation/effect to the active object: Bevel"""
    bl_label = ""
    bl_idname = "object.button_modifier_bevel_button"

    def execute(self, context):
        scene = context.scene
        Arc_Blend = scene.Arc_Blend
        bpy.ops.object.modifier_add(type='BEVEL')
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# BEVEL VERTICES BUTTON PANEL


class modifier_bevel_v_button (bpy.types.Operator):
    """Affect edges or Vertices: Vertices"""
    bl_label = ""
    bl_idname = "object.button_modifier_bevel_v_button"

    def execute(self, context):
        scene = context.scene
        AB_Bevel = scene.AB_Bevel
        bpy.context.object.modifiers["Bevel"].affect = 'VERTICES'
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# BEVEL EDGES BUTTON PANEL


class modifier_bevel_e_button (bpy.types.Operator):
    """Affect edges or Vertices: Edges"""
    bl_label = ""
    bl_idname = "object.button_modifier_bevel_e_button"

    def execute(self, context):
        scene = context.scene
        object = context.object
        AB_Bevel = scene.AB_Bevel
        bpy.context.object.modifiers["Bevel"].affect = 'EDGES'
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# BEVEL APPLY OPERATOR


class modifier_bevel_apply (bpy.types.Operator):
    """Apply to Object : Bevels"""
    bl_label = ""
    bl_idname = "object.button_modifier_bevel_apply"

    def execute(self, context):
        layout = self.layout
        try:
            for obj in bpy.context.selected_objects:
                bpy.context.view_layer.objects.active = obj
                for modifier in obj.modifiers:
                    # Array Modifier Apply
                    if modifier.type == 'BEVEL':
                        try:
                            bpy.ops.object.modifier_apply(
                                modifier=modifier.name)
                        except (AttributeError, KeyError, RuntimeError):
                            bpy.ops.object.modifier_remove(modifier="Bevel")
        except (AttributeError, KeyError, RuntimeError):
            pass
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# BEVEL PROPERTYGROUP


class modifier_bevel_detail (bpy.types.PropertyGroup):
    # text_area: bpy.props.StringProperty(name="Text Area")#Text Area
    Width_Type_area: bpy.props.EnumProperty(
        name="Width Type: ",
        description="Width Type",
        items=[("OFFSET", "Offset", "What distance with measures: Offset \nAmount is offset of new edges from original"),
               ("WIDTH", "Width", "What distance with measures: Offset \nGenerates enough copies to fit within the fixed length given by Length."),
               ("DEPTH", "Depth", "What distance with measures: Offset \nValue is the perpendicular distance from the new bevel face to original edge."),
               ("PERCENT", "Percent", "What distance with measures: Offset \nThe percentage of the length of adjacent edge length that the new edges slide along."),
               ("ABSOLUTE", "Absolute", "What distance with measures: Offset \nThe exact distance along edges adjacent to the beveled edge. A difference from Offset is visible when the unbeveled edges attached to beveled edges meet at an angle besides a right angle."),
               ]
    )
    Amount_area: bpy.props.FloatProperty(
        name="Amount",
        description="Count \nNumber of duplicates to make",
        soft_min=0, soft_max=1000, subtype="DISTANCE")
    Segment_area: bpy.props.IntProperty(
        name="Segments",
        description="Length \nLength to fit array within",
        soft_min=0, soft_max=1000)
    Limit_Method_area: bpy.props.EnumProperty(
        name="Limit Method: ",
        description="Limit Method",
        items=[("NONE", "None", "No limit, all edges will be beveled."),
               ("ANGLE", "Angle", "Only bevels edges whose angle of adjacent face normals plus the defined Angle is less than 180 degrees. Intended to allow you to bevel only the sharp edges of an object without affecting its smooth surfaces."),
               ("WEIGHT", "Weight", "Use each edge’s bevel weight to determine the width of the bevel. When the bevel weight is 0.0, no bevel is applied. See here about adjusting bevel weights."),
               ("VGROUP", "Vertex Group", "Use weights from a vertex group to determine the width of the bevel. When the vertex weight is 0.0, no bevel is applied. An edge is only beveled if both of its vertices are in the vertex group. See here about adjusting vertex group weights."),
               ]
    )
    Angle_area: bpy.props.FloatProperty(
        name="Angle",
        description="Angle \nAngle above which to bevel edges",
        min=0, max=3.14159, subtype="ANGLE")
    Width_Percent_area: bpy.props.IntProperty(
        name="Width Percent",
        description="Width Percent \nBevel amount for percentage method",
        min=0, max=100, subtype="PERCENTAGE")

# ------------------------------------------------------------------------------
# BEVEL EXECUTER OPERATOR


class modifier_bevel_detail_executer (bpy.types.Operator):
    """See the Result. This button does not apply just sets the values and operations"""
    bl_label = "Result"
    bl_idname = "object.button_modifier_bevel_detail_executer"

    def execute(self, context):
        scene = context.scene
        AB_Bevel = scene.AB_Bevel
        if AB_Bevel.Width_Type_area == 'OFFSET':
            bpy.context.object.modifiers["Bevel"].offset_type = 'OFFSET'
            bpy.context.object.modifiers["Bevel"].width = AB_Bevel.Amount_area
            bpy.context.object.modifiers["Bevel"].segments = AB_Bevel.Segment_area
            bpy.context.object.modifiers["Bevel"].angle_limit = AB_Bevel.Angle_area
        if AB_Bevel.Width_Type_area == 'WIDTH':
            bpy.context.object.modifiers["Bevel"].offset_type = 'WIDTH'
            bpy.context.object.modifiers["Bevel"].width = AB_Bevel.Amount_area
            bpy.context.object.modifiers["Bevel"].segments = AB_Bevel.Segment_area
            bpy.context.object.modifiers["Bevel"].angle_limit = AB_Bevel.Angle_area
        if AB_Bevel.Width_Type_area == 'DEPTH':
            bpy.context.object.modifiers["Bevel"].offset_type = 'DEPTH'
            bpy.context.object.modifiers["Bevel"].width = AB_Bevel.Amount_area
            bpy.context.object.modifiers["Bevel"].segments = AB_Bevel.Segment_area
            bpy.context.object.modifiers["Bevel"].angle_limit = AB_Bevel.Angle_area
        if AB_Bevel.Width_Type_area == 'PERCENT':
            bpy.context.object.modifiers["Bevel"].offset_type = 'PERCENT'
            bpy.context.object.modifiers["Bevel"].width = AB_Bevel.Amount_area
            bpy.context.object.modifiers["Bevel"].segments = AB_Bevel.Segment_area
            bpy.context.object.modifiers["Bevel"].angle_limit = AB_Bevel.Angle_area
            bpy.context.object.modifiers["Bevel"].width_pct = AB_Bevel.Width_Percent_area
        if AB_Bevel.Width_Type_area == 'ABSOLUTE':
            bpy.context.object.modifiers["Bevel"].offset_type = 'ABSOLUTE'
            bpy.context.object.modifiers["Bevel"].width = AB_Bevel.Amount_area
            bpy.context.object.modifiers["Bevel"].segments = AB_Bevel.Segment_area
            bpy.context.object.modifiers["Bevel"].angle_limit = AB_Bevel.Angle_area
        if AB_Bevel.Limit_Method_area == 'NONE':
            bpy.context.object.modifiers["Bevel"].limit_method = 'NONE'
        if AB_Bevel.Limit_Method_area == 'ANGLE':
            bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'
        if AB_Bevel.Limit_Method_area == 'WEIGHT':
            bpy.context.object.modifiers["Bevel"].limit_method = 'WEIGHT'
        if AB_Bevel.Limit_Method_area == 'VGROUP':
            bpy.context.object.modifiers["Bevel"].limit_method = 'VGROUP'
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# GENERATE PANEL


class generate_panel (bpy.types.Panel):
    bl_label = "Generate"
    bl_idname = "PT_generate_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_modifier_panel"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        row = layout.row()

# ------------------------------------------------------------------------------
# DEFORM PANEL


class deform_panel (bpy.types.Panel):
    bl_label = "Deform"
    bl_idname = "PT_deform_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_modifier_panel"  # Parent ID

    def draw(self, context):
        layout = self.layout
        obj = context.object
        row = layout.row()

# ------------------------------------------------------------------------------
# PHYSICS PANEL


class physics_panel (bpy.types.Panel):
    bl_label = "Physics"
    bl_idname = "PT_dphysics_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_modifier_panel"  # Parent ID

    def draw(self, context):
        layout = self.layout
        obj = context.object
        row = layout.row()

# ------------------------------------------------------------------------------
# DISPLAY PANEL


class display_panel (bpy.types.Panel):
    bl_label = "Display Panel"
    bl_idname = "PT_display_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_Transform"  # Parent ID

    def draw(self, context):
        layout = self.layout
        obj = context.object
        space_data = context.space_data
        sdo = space_data.overlay
        row = layout.row()
        col = layout.column()
        if bpy.context.selected_objects != []:
            try:
                col.prop(obj, "display_type")
                col.prop(obj, "hide_viewport")
                col.prop(obj, "show_all_edges")
                col.prop(obj, "show_axis")
                col.prop(obj, "show_bounds")
                col.prop(obj, "display_bounds_type")
            except (TypeError,KeyError):
                pass
        else:
            pass
        col.prop(sdo, "show_wireframes")
        col.prop(sdo,  "show_stats")
        col.prop(sdo,  "show_face_orientation")
        row.operator("object.button_display_panel_show_xray", icon="XRAY")
        row.operator("object.button_display_panel_show_wireframe",
                     icon="SHADING_WIRE")
        row.operator("object.button_display_panel_show_solid",
                     icon="SHADING_SOLID")
        row.operator("object.button_display_panel_show_material",
                     icon="MATERIAL")
        row.operator("object.button_display_panel_show_rendered",
                     icon="SHADING_RENDERED")
        row = layout.row()
        row.prop(sdo, "show_axis_x")
        row.prop(sdo, "show_axis_y")
        row.prop(sdo, "show_axis_z")
        row = layout.row()
        col = layout.column()
        col.prop(sdo, "show_floor")
        row = layout.row()

# ------------------------------------------------------------------------------
# SHOW X-RAY OPERATOR


class display_panel_show_xray (bpy.types.Operator):
    """Show X-Ray"""
    bl_label = ""
    bl_idname = "object.button_display_panel_show_xray"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend
        bpy.ops.view3d.toggle_xray()
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# SHOW WIREFRAME OPERATOR


class display_panel_show_wireframe (bpy.types.Operator):
    """Show Wireframe"""
    bl_label = ""
    bl_idname = "object.button_display_panel_show_wireframe"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend
        bpy.context.space_data.shading.type = 'WIREFRAME'
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# SOLID DISPLAY OPERATOR


class display_panel_show_solid (bpy.types.Operator):
    """Show Solid Display"""
    bl_label = ""
    bl_idname = "object.button_display_panel_show_solid"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend
        bpy.context.space_data.shading.type = 'SOLID'
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# MATERIAL DISPLAY OPERATOR


class display_panel_show_material (bpy.types.Operator):
    """Show Material Preview"""
    bl_label = ""
    bl_idname = "object.button_display_panel_show_material"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend
        bpy.context.space_data.shading.type = 'MATERIAL'
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# RENDERED DISPLAY OPERATOR


class display_panel_show_rendered (bpy.types.Operator):
    """Show Rendered Preview"""
    bl_label = ""
    bl_idname = "object.button_display_panel_show_rendered"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend
        bpy.context.space_data.shading.type = 'RENDERED'
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# VERTEX EDİT PANEL


class edit_mode_vertex (bpy.types.Panel):
    bl_label = "Vertex Edit Panel"
    bl_idname = "PT_Vertex_Edit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        row = layout.row()
        col = layout.column()
        col.operator("object.button_edit_mode_add_vertex",
                     text="Add Single Vertex")
        col.label(text="Vertex Edit Panel")
        row = layout.row()
        col = layout.column()
        row = layout.row()
        row.operator("object.button_edit_mode_just_vertices",
                     text="Just Vertices")
        row.operator("object.button_edit_mode_just_edges", text="Just Edges")
        row = layout.row()
        row.operator("object.button_edit_mode_create_faces",
                     text="Create Faces")

# ------------------------------------------------------------------------------
# ADD SINGLE VERTEX OPERATOR


class edit_mode_add_vertex (bpy.types.Operator):
    """Add a Single Vertex in (0,0,0)location. And it creates 'AB_Vertex' to Scene Collection."""
    bl_label = ""
    bl_idname = "object.button_edit_mode_add_vertex"

    def execute(self, context):
        layout = self.layout
        scene = context.scene
        # make mesh
        vertices = [(0, 0, 0), ]
        edges = []
        faces = []
        new_mesh = bpy.data.meshes.new('Vertex')
        new_mesh.from_pydata(vertices, edges, faces)
        new_mesh.update()
        # make object from mesh
        new_object = bpy.data.objects.new('Vertex', new_mesh)
        # make collection
        try:
            collections_is = bpy.data.collections['AB_Vertex']
            collections_is.objects.link(new_object)
        except KeyError:
            new_collection = bpy.data.collections.new('AB_Vertex')
            bpy.context.scene.collection.children.link(new_collection)
            # add object to scene collection
            new_collection.objects.link(new_object)
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# BRIDGE VERTICES OPERATOR


class edit_mode_bridge_vertices (bpy.types.Operator):
    """Bridge selected Vertices..."""
    bl_label = ""
    bl_idname = "object.button_edit_mode_bridge_vertices"

    def execute(self, context):
        layout = self.layout
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.edge_face_add()
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# DELETE VERTICES OPERATOR


class edit_mode_delete_vertices (bpy.types.Operator):
    """Delete selected Vertices..."""
    bl_label = ""
    bl_idname = "object.button_edit_mode_delete_vertices"

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.delete(type='VERT')
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# JUST VERTICES OPERATOR


class edit_mode_just_vertices (bpy.types.Operator):
    """Leave the all Vertices to selected Object...(Removes all Edges and Faces leaves Vertices)"""
    bl_label = ""
    bl_idname = "object.button_edit_mode_just_vertices"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.delete(type='EDGE_FACE')
        bpy.ops.object.editmode_toggle()
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# JUST EDGES OPERATOR


class edit_mode_just_edges (bpy.types.Operator):
    """Leave the all Edges to selected Object...(Removes all  Faces leaves Edges and Vertices)"""
    bl_label = ""
    bl_idname = "object.button_edit_mode_just_edges"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.delete(type='ONLY_FACE')
        bpy.ops.object.editmode_toggle()
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# DEF ORDER
# Weights for order. Left>>Right Down>>Up


def order(vector):
    return vector[0]+200*vector[1]

# ------------------------------------------------------------------------------
# CREATE FACES OPERATOR


class edit_mode_create_faces (bpy.types.Operator):
    """Create points to Faces... (Work in Progress...Don't use so much!!!)"""
    bl_label = ""
    bl_idname = "object.button_edit_mode_create_faces"

    def execute(self, context):
        layout = self.layout
        scene = bpy.context.scene
        mesh_list = context.object.data.mesh_list
        index = context.object.data.list_index

        win = bpy.context.window
        scr = win.screen
        areas3d = [area for area in scr.areas if area.type == 'VIEW_3D']
        region = [
            region for region in areas3d[0].regions if region.type == 'WINDOW']
        override = {'window': win,
                    'screen': scr,
                    'area': areas3d[0],
                    'region': region,
                    'scene': bpy.context.scene,
                    }

        ob = bpy.context.object

        # ob.matrix_world.translation

        # List of vertices in any objects
        object_in_vertices = ob.data.vertices[:]

        object_in_vertices_co = []

        object_vertices_coordinates = []

        object_verts = []

        object_verts.sort(key=order)

        object_edges = []

        z = []

        face_list = []

        points_of_object = [ob.matrix_parent_inverse @
                            Vector(points)for points in object_in_vertices_co]

        # List of points' Vectors Coordinates every vectors append to "o"list
        for i in object_in_vertices:
            object_in_vertices_co.append(i.co)

        for b in object_in_vertices_co:
            object_vertices_coordinates.append(b.xyz)

        for c in object_vertices_coordinates:
            object_verts.append(c[:])

        points_count = len(object_verts)

        # For edges needs to 2 points to merge them
        for i in range(0, points_count):

            object_edges.append(i)

        for j in range(1, points_count+1):

            z.append(j)

        # list 2 type edge
        all_edges = list(zip(object_edges, z))

        all_edges.pop()

        # For faces needs to 3 points to merge them or needs to 2 edges
        for k in range(2, points_count+2):
            face_list.append(k)

        # list 3 type face
        all_faces = list(zip(object_edges, z, face_list))

        # Removing 2 last elements
        all_faces.pop()
        all_faces.pop()

        verts = object_verts
        edges = all_edges
        faces = all_faces

        # for i in range(0,len(object_verts)):
        ov = object_verts
        same_x0 = []
        same_y0 = []
        same_z0 = []
        same_xy = []
        same_zm = []
        same_zp = []

        # just same x loop
        same_x1 = []

        # just same y loop
        same_yy = []

        # just same y loop
        same_zz = []

        # just same x values are same
        just_same_x = []

        # just same y values are same
        just_same_y = []

        # just same z values are same
        just_same_z = []

        # just same xy values are same
        just_same_xy = []

        # just same xz values are same
        just_same_xz = []

        # just same yz values are same
        just_same_yz = []

        # just same xyz values are same
        just_same_xyz = []

        # Sphere formula is r is radius.
        # distance_two_points =math.sqrt((ov[i][0] -ov[i-1][0])** 2 + (ov[i][1] - ov[i-1][1])** 2 + (ov[i][2] - ov[i-1][2])** 2)#distance points

        # Let's Create Sphere formula  "r"is radius. And focus is (0,0,0)Origin and find all points.
        # ov[i][0]= X Coordinates and x on the surface points coordinate and x0 is origin x values =0,
        # ov[i][1]= Y Coordinates and y on the surface points coordinate and y0 is origin y values =0,
        # ov[i][2]= Z Coordinates and z on the surface points coordinate and z0 is origin z values =0
        # Sphere formula is r**2 = (x-xo)**2 + (y-y0)**2 + (z-z0)**2

        # Sphere_r= math.sqrt((ov[0][0]-0)**2 + (ov[0][1]-0)**2 + (ov[0][2]-0)**2)# Our r radius formula

        # this loop same x and z axis
        for i in range(0, len(object_verts)):
            distance_x = ov[i][0]
            distance_y = ov[i][1]
            distance_z = ov[i][2]

            just_same_x.append(distance_x)
            just_same_y.append(distance_y)
            just_same_z.append(distance_z)
            # Distance x and y
            just_same_xy.append(distance_x)
            just_same_xy.append(distance_y)
            # Distance x and z
            just_same_xz.append(distance_x)
            just_same_xz.append(distance_z)
            # Distance y and z
            just_same_yz.append(distance_y)
            just_same_yz.append(distance_z)
            # Distance x,y and z
            just_same_xyz.append(distance_x)
            just_same_xyz.append(distance_y)
            just_same_xyz.append(distance_z)
            if distance_x == 0:
                same_x0.append(i)

            if distance_y == 0:
                same_y0.append(i)

            if distance_z == 0:
                same_z0.append(i)

        just_same_x_values = list(set(just_same_x))
        just_same_y_values = list(set(just_same_y))
        just_same_z_values = list(set(just_same_z))

        just_same_xy_values = list(set(just_same_xy))

        just_same_xz_values = list(set(just_same_xz))

        just_same_yz_values = list(set(just_same_yz))

        just_same_xyz_values = list(set(just_same_xyz))
        same_x_level = []
        same_y_level = []
        same_z_level = []
        same_xy_level = []
        same_xz_level = []
        same_yz_level = []
        same_xyz_level = []
        for p in range(len(just_same_x_values)):
            same_x_level.append([])

        for p in range(len(just_same_y_values)):
            same_y_level.append([])

        for p in range(len(just_same_z_values)):
            same_z_level.append([])

        for p in range(len(just_same_xy_values)):
            same_xy_level.append([])

        for p in range(len(just_same_xz_values)):
            same_xz_level.append([])

        for p in range(len(just_same_yz_values)):
            same_yz_level.append([])

        for p in range(len(just_same_xyz_values)):
            same_xyz_level.append([])
        for i in range(0, len(object_verts)):
            distance_x = ov[i][0]
            distance_y = ov[i][1]
            distance_z = ov[i][2]
            for f in range(len(just_same_x_values)):
                if distance_x == just_same_x_values[f]:
                    same_x_level[f].append(i)

            for yy in range(len(just_same_y_values)):
                if distance_y == just_same_y_values[yy]:
                    same_y_level[yy].append(i)

            for zz in range(len(just_same_z_values)):
                if distance_z == just_same_z_values[zz]:
                    same_z_level[zz].append(i)

            for xy in range(len(just_same_xy_values)):
                if distance_x == just_same_xy_values[xy] or distance_y == just_same_xy_values[xy]:
                    same_xy_level[xy].append(i)

            for xz in range(len(just_same_xz_values)):
                if distance_x == just_same_xz_values[xz] or distance_z == just_same_xz_values[xz]:
                    same_xz_level[xz].append(i)

            for yz in range(len(just_same_yz_values)):
                if distance_y == just_same_yz_values[yz] or distance_z == just_same_yz_values[yz]:
                    same_yz_level[yz].append(i)

            for xyz in range(len(just_same_xyz_values)):
                if distance_x == just_same_xyz_values[xyz] and distance_y == just_same_xyz_values[xyz] and distance_z == just_same_xyz_values[xyz]:
                    same_xyz_level[xyz].append(i)
        # All same z values are faced
        obj = bpy.context.active_object
        for n in range(len(same_z_level)):
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(type="VERT")
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT')
            for m in same_z_level[n]:
                try:
                    obj.data.vertices[m].select = True
                except IndexError:
                    pass
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.edge_face_add()
            bpy.ops.object.editmode_toggle()
        # Select every level and create faces "This will work rectangeler elements..."
        obj = bpy.context.active_object
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        for p in range(1, len(obj.data.polygons)):
            obj.data.polygons[p-1].select = True
            obj.data.polygons[p].select = True
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.bridge_edge_loops()
        bpy.ops.object.editmode_toggle()
        # All same y values are faced
        #obj = bpy.context.active_object
        # for yyy in range(len(same_y_level)):
        #bpy.ops.object.mode_set(mode = 'EDIT')
        # bpy.ops.mesh.select_mode(type="VERT")
        #bpy.ops.mesh.select_all(action = 'DESELECT')
        #bpy.ops.object.mode_set(mode = 'OBJECT')
        # for y0 in same_y_level[yyy]:
        #obj.data.vertices[y0].select = True
        #bpy.ops.object.mode_set(mode = 'EDIT')
        # bpy.ops.mesh.edge_face_add()
        # bpy.ops.object.editmode_toggle()
        # All same x values are faced
        #obj = bpy.context.active_object
        # for xxx in range(len(same_x_level)):
        #bpy.ops.object.mode_set(mode = 'EDIT')
        # bpy.ops.mesh.select_mode(type="VERT")
        #bpy.ops.mesh.select_all(action = 'DESELECT')
        #bpy.ops.object.mode_set(mode = 'OBJECT')
        # for x0 in same_x_level[xxx]:
        #    obj.data.vertices[x0].select = True
        #bpy.ops.object.mode_set(mode = 'EDIT')
        # bpy.ops.mesh.edge_face_add()
        # bpy.ops.object.editmode_toggle()

        # All same xy values are faced
        #obj = bpy.context.active_object
        # for xy in range(len(same_xy_level)):
        #bpy.ops.object.mode_set(mode = 'EDIT')
        # bpy.ops.mesh.select_mode(type="VERT")
        #bpy.ops.mesh.select_all(action = 'DESELECT')
        #bpy.ops.object.mode_set(mode = 'OBJECT')
        # for xyxt in same_xy_level[xy]:
        #     obj.data.vertices[xyxt].select = True
        #bpy.ops.object.mode_set(mode = 'EDIT')
        # bpy.ops.mesh.edge_face_add()
        # bpy.ops.object.editmode_toggle()

        # All same xz values are faced
        #obj = bpy.context.active_object
        # for xz in range(len(same_xz_level)):
        #bpy.ops.object.mode_set(mode = 'EDIT')
        # bpy.ops.mesh.select_mode(type="VERT")
        #bpy.ops.mesh.select_all(action = 'DESELECT')
        #bpy.ops.object.mode_set(mode = 'OBJECT')
        # for xyxz in same_xz_level[xz]:
        #    obj.data.vertices[xyxz].select = True
        #bpy.ops.object.mode_set(mode = 'EDIT')
        # bpy.ops.mesh.edge_face_add()
        # bpy.ops.object.editmode_toggle()

        # All same yz values are faced
        #obj = bpy.context.active_object
        # for yz in range(len(same_yz_level)):
        #bpy.ops.object.mode_set(mode = 'EDIT')
        # bpy.ops.mesh.select_mode(type="VERT")
        #bpy.ops.mesh.select_all(action = 'DESELECT')
        #bpy.ops.object.mode_set(mode = 'OBJECT')
        # for xyyz in same_yz_level[yz]:
        #   obj.data.vertices[xyyz].select = True
        #bpy.ops.object.mode_set(mode = 'EDIT')
        # bpy.ops.mesh.edge_face_add()
        # bpy.ops.object.editmode_toggle()

        # All same xyz values are faced
        #obj = bpy.context.active_object
        # for xyz in range(len(same_xyz_level)):
        #bpy.ops.object.mode_set(mode = 'EDIT')
        # bpy.ops.mesh.select_mode(type="VERT")
        #bpy.ops.mesh.select_all(action = 'DESELECT')
        #bpy.ops.object.mode_set(mode = 'OBJECT')
        # for xyxyz in same_xyz_level[xyz]:
        #    obj.data.vertices[xyxyz].select = True
        #bpy.ops.object.mode_set(mode = 'EDIT')
        # bpy.ops.mesh.edge_face_add()
        # bpy.ops.object.editmode_toggle()

        # if distance_two_points <= i:

        #obj = bpy.context.active_object
        #bpy.ops.object.mode_set(mode = 'EDIT')
        # bpy.ops.mesh.select_mode(type="VERT")
        #bpy.ops.mesh.select_all(action = 'DESELECT')
        #bpy.ops.object.mode_set(mode = 'OBJECT')
        #obj.data.vertices[i].select = True
        #obj.data.vertices[i-1].select = True
        #bpy.ops.object.mode_set(mode = 'EDIT')
        # bpy.ops.mesh.edge_face_add()
        # bpy.ops.object.editmode_toggle()

        # for i in range(1,len(object_verts)):
        #ov = object_verts

        # if ov[i][0] == ov[i-1][0] :
        #obj = bpy.context.active_object
        #bpy.ops.object.mode_set(mode = 'EDIT')
        # bpy.ops.mesh.select_mode(type="VERT")
        #bpy.ops.mesh.select_all(action = 'DESELECT')
        #bpy.ops.object.mode_set(mode = 'OBJECT')
        #obj.data.vertices[i].select = True
        #obj.data.vertices[i-1].select = True
        #bpy.ops.object.mode_set(mode = 'EDIT')
        # bpy.ops.mesh.edge_face_add()
        # bpy.ops.object.editmode_toggle()

        # elif ov[i][1] == ov[i-1][1]:
        #obj = bpy.context.active_object
        #bpy.ops.object.mode_set(mode = 'EDIT')
        # bpy.ops.mesh.select_mode(type="VERT")
        #bpy.ops.mesh.select_all(action = 'DESELECT')
        #bpy.ops.object.mode_set(mode = 'OBJECT')
        #obj.data.vertices[i].select = True
        #obj.data.vertices[i-1].select = True
        #bpy.ops.object.mode_set(mode = 'EDIT')
        # bpy.ops.mesh.edge_face_add()
        # bpy.ops.object.editmode_toggle()

        # elif ov[i][2] == ov[i-1][2]:
        #obj = bpy.context.active_object
        #bpy.ops.object.mode_set(mode = 'EDIT')
        # bpy.ops.mesh.select_mode(type="VERT")
        #bpy.ops.mesh.select_all(action = 'DESELECT')
        #bpy.ops.object.mode_set(mode = 'OBJECT')
        #obj.data.vertices[i].select = True
        #obj.data.vertices[i-1].select = True
        #bpy.ops.object.mode_set(mode = 'EDIT')
        # bpy.ops.mesh.edge_face_add()
        # bpy.ops.object.editmode_toggle()

        return {'FINISHED'}

# ------------------------------------------------------------------------------
# THEMES PANEL


class Themes_Panel (bpy.types.Panel):
    bl_label = "AB Themes"
    bl_idname = "PT_Themes_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        row = layout.row()
        col = layout.column()
        col.operator("object.button_themes_panel_mak", text="Dark Theme")
        col.operator("object.button_themes_panel_white_chalk",
                     text="White Chalk Theme")
        col.operator("object.button_themes_panel_reset", text="Reset Theme")

# ------------------------------------------------------------------------------
# DARK THEME


class themes_panel_mak (bpy.types.Operator):
    """Dark Theme.Background "Black"Shows color object."""
    bl_label = ""
    bl_idname = "object.button_themes_panel_mak"

    def execute(self, context):
        bpy.context.space_data.shading.background_type = 'VIEWPORT'
        bpy.context.space_data.shading.light = 'STUDIO'
        bpy.context.space_data.shading.color_type = 'MATERIAL'
        bpy.context.space_data.overlay.show_floor = True
        bpy.context.space_data.overlay.show_axis_x = True
        bpy.context.space_data.overlay.show_axis_y = True
        bpy.context.space_data.overlay.show_axis_z = False
        bpy.context.space_data.overlay.show_wireframes = True
        bpy.context.space_data.shading.background_color = (0, 0, 0)
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# WHITE CHALK THEME


class themes_panel_white_chalk (bpy.types.Operator):
    """White Chalk Theme.Background "White"Shows white color object."""
    bl_label = ""
    bl_idname = "object.button_themes_panel_white_chalk"

    def execute(self, context):
        bpy.context.space_data.shading.background_type = 'VIEWPORT'
        bpy.context.space_data.shading.light = 'FLAT'
        bpy.context.space_data.shading.color_type = 'SINGLE'
        bpy.context.space_data.shading.show_object_outline = True
        bpy.context.space_data.shading.object_outline_color = (0, 0, 0)
        bpy.context.space_data.shading.single_color = (1, 1, 1)
        bpy.context.space_data.shading.object_outline_color = (0, 0, 0)
        bpy.context.space_data.overlay.show_wireframes = True
        bpy.context.space_data.overlay.show_floor = True
        bpy.context.space_data.overlay.show_axis_x = True
        bpy.context.space_data.overlay.show_axis_y = True
        bpy.context.space_data.overlay.show_axis_z = True
        bpy.context.space_data.shading.background_color = (1, 1, 1)
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# RESET THEME


class themes_panel_reset (bpy.types.Operator):
    """Reset Theme.(This theme sets the originals)"""
    bl_label = ""
    bl_idname = "object.button_themes_panel_reset"

    def execute(self, context):
        layout = self.layout

        bpy.context.space_data.shading.light = 'STUDIO'
        bpy.context.space_data.shading.studio_light = 'Default'
        bpy.context.space_data.shading.color_type = 'MATERIAL'
        bpy.context.space_data.shading.background_type = 'THEME'
        bpy.context.space_data.overlay.show_overlays = True
        bpy.context.space_data.shading.show_backface_culling = False
        bpy.context.space_data.shading.show_xray = False
        bpy.context.space_data.shading.show_shadows = False
        bpy.context.space_data.shading.show_cavity = False
        bpy.context.space_data.shading.use_dof = False
        bpy.context.space_data.shading.show_object_outline = True
        bpy.context.space_data.shading.object_outline_color = (0, 0, 0)
        bpy.context.space_data.shading.show_specular_highlight = True

        bpy.context.space_data.overlay.show_floor = True
        bpy.context.space_data.overlay.show_ortho_grid = True
        bpy.context.space_data.overlay.show_text = True
        bpy.context.space_data.overlay.show_cursor = True
        bpy.context.space_data.overlay.show_stats = False
        bpy.context.space_data.overlay.show_annotation = True

        bpy.context.space_data.overlay.show_extras = True
        bpy.context.space_data.overlay.show_bones = True
        bpy.context.space_data.overlay.show_relationship_lines = True
        bpy.context.space_data.overlay.show_outline_selected = True
        bpy.context.space_data.overlay.show_motion_paths = True
        bpy.context.space_data.overlay.show_object_origins = True
        bpy.context.space_data.overlay.show_object_origins_all = False

        bpy.context.space_data.overlay.show_wireframes = False
        bpy.context.space_data.overlay.show_face_orientation = False
        bpy.context.space_data.show_reconstruction = True
        bpy.context.space_data.show_camera_path = False
        bpy.context.space_data.show_bundle_names = False
        bpy.context.space_data.tracks_display_type = 'PLAIN_AXES'
        bpy.context.space_data.tracks_display_size = 0.2

        bpy.context.space_data.show_gizmo = True
        bpy.context.space_data.show_gizmo_navigate = True
        bpy.context.space_data.show_gizmo_tool = True
        bpy.context.space_data.show_gizmo_context = True
        bpy.context.scene.transform_orientation_slots[1].type = 'DEFAULT'
        bpy.context.space_data.show_gizmo_object_translate = False
        bpy.context.space_data.show_gizmo_object_rotate = False
        bpy.context.space_data.show_gizmo_object_scale = False
        bpy.context.space_data.show_gizmo_empty_image = True
        bpy.context.space_data.show_gizmo_empty_force_field = True
        bpy.context.space_data.show_gizmo_light_size = True
        bpy.context.space_data.show_gizmo_light_look_at = True
        bpy.context.space_data.show_gizmo_camera_lens = True
        bpy.context.space_data.show_gizmo_camera_dof_distance = True
        bpy.context.space_data.overlay.grid_scale = 1
        bpy.context.space_data.overlay.show_axis_x = True
        bpy.context.space_data.overlay.show_axis_y = True
        bpy.context.space_data.overlay.show_axis_z = False
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# MODELLING PANEL


class Modelling_Panel(bpy.types.Panel):
    bl_label = "AB Modelling"
    bl_idname = "PT_Modelling_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    
        
    def draw(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend
        
        
        
        col = layout.column()
        col.prop(Arc_Blend, "display_mode_view" , icon="VIEW3D")
        
        
        
        if bpy.context.scene.Arc_Blend.display_mode_view:
            box = layout.box()
            col = box.column()
            try:
                mesh= bpy.context.object.data
            except AttributeError:
                pass
            
            col.label(text="Perspective/Ortho Mode :")
            col.operator("view3d.view_persportho", text="Perspective/Orthographic")
            
            box.label(text="View3D Points:")
            row = box.row(align=True)
            row.operator("object.button_view_3d_top", text="Top (+Z)" )
            row.operator("object.button_view_3d_bottom", text="Bottom (-Z)")
            row= box.row(align=True)
            row.operator("object.button_view_3d_front", text="Front (-Y)")
            row.operator("object.button_view_3d_back", text="Back (+Y)")
            row= box.row(align=True)
            row.operator("object.button_view_3d_right", text="Right (+X)")
            row.operator("object.button_view_3d_left", text="Left (-X)")
       
        col = layout.column()
        col.prop(Arc_Blend, "modelling_cutter" , icon="UGLYPACKAGE")
        if bpy.context.scene.Arc_Blend.modelling_cutter:
            box = layout.box()
            try:
                mesh= bpy.context.object.data
            except AttributeError:
                pass
            
            col = box.column()
            col.label(text="Cutter Panel :")
            row = box.row(align=True)
            if bpy.context.active_object!= None:
             row.operator("object.button_cutter_box", text="Cutter Collection" )
             row.operator("object.button_cutter_box_object", text="Cutter Object" )
             row.operator("object.button_cutter_apply_modifier", text="", icon="CHECKMARK" )
            elif bpy.context.active_object == None:
              row.label(text="<<< Select/Create any Object >>>")  
            row = box.row(align=True)
            row.label(text="Auto Smooth")
            try:
                row.prop(mesh, "use_auto_smooth", text="")
                row.prop(mesh, "auto_smooth_angle", text="")
                row.prop_decorator(mesh, "auto_smooth_angle")
            except UnboundLocalError:
                pass
            col = box.column()
            col.label(text="Cutter Collection:")
            row = box.row(align=True)
            row.label(text="Collection :")
            row.prop(Arc_Blend, "cutter_collection_viewport" , icon="RESTRICT_VIEW_OFF")
            row.prop(Arc_Blend, "cutter_collection_render" , icon="RESTRICT_RENDER_OFF")
            row = box.row(align=True)
            row.label(text="Object :")
            row.prop(Arc_Blend, "cutter_object_collection_viewport" , icon="RESTRICT_VIEW_OFF")
            row.prop(Arc_Blend, "cutter_object_collection_render" , icon="RESTRICT_RENDER_OFF")
            
            
            
            col = box.column()
            col.label(text="Turn ON/OFF Display Color : ")
            
            col.prop(Arc_Blend, "color_mode_display", text="", icon="FILE_REFRESH")
            col.label(text="Purge unused data objects : ")
            col.operator("object.button_transform_edit_object_purge", text="Purge")
            row = box.row()
            try:
                sub = row.row(align=True)
                sub.scale_x = 1.5
                sub.label(text="Color : ")
                sub.scale_x = 4.6
                sub.prop(obj, "color", text="")
                row = box.row(align=True)
                row.operator(
                    "object.button_transform_edit_object_reset_colors", text="Reset Colors")
            except (TypeError,KeyError):
                pass
            #row.template_modifiers()
            
            
          
        col = layout.column()
        col.prop(Arc_Blend, "modelling_edit_mode",
                 text="Edit Mode", icon="EDITMODE_HLT")
                 
        col = layout.column(align=False)
        col.label(text="Object Selection Mode : ")

        
        if bpy.context.scene.Arc_Blend.modelling_edit_mode == False:
            box = layout.box()
            box.label(text="<<<<<Edit Mode is not Active!>>>>>")
        
        if bpy.context.scene.Arc_Blend.modelling_edit_mode == True:
            row1 = layout.row(align=True)
            row1.template_header_3D_mode()

            row1.prop(Arc_Blend, "toggle_xray_mode", text="", icon='XRAY')
            row1.prop(context.tool_settings, "use_mesh_automerge", text="")

            row1.scale_x = 2
            row1.scale_y = 2

# ------------------------------------------------------------------------------
# ENSURE COLECTION DEF

def ensure_collection(scene,collection_name) -> bpy.types.Collection:
            scene=bpy.context.scene
            try:
                new_collection = scene.collection.children[collection_name]
                bpy.data.collections['AB_Cutters_Collection'].color_tag="COLOR_01"
                #new_collection.objects.link(new_object)
            except KeyError:
                new_collection = bpy.data.collections.new(collection_name)
                scene.collection.children.link(new_collection)
                bpy.data.collections['AB_Cutters_Collection'].color_tag="COLOR_01"
                #new_collection.objects.link(new_object)
            try:
             return new_collection
            except KeyError:
                pass
# ------------------------------------------------------------------------------
# ENSURE COLECTION DEF

def ensure_collection_object(scene,collection_name) -> bpy.types.Collection:
            scene=bpy.context.scene
            try:
                new_collection = scene.collection.children[collection_name]
                bpy.data.collections['AB_Cutters_Object'].color_tag="COLOR_05"
                #new_collection.objects.link(new_object)
            except KeyError:
                new_collection = bpy.data.collections.new(collection_name)
                scene.collection.children.link(new_collection)
                bpy.data.collections['AB_Cutters_Object'].color_tag="COLOR_05"
                #new_collection.objects.link(new_object)
            try:
             return new_collection
            except KeyError:
                pass
# ------------------------------------------------------------------------------
# BOX CUTTER COLLECTION


class cutter_box(bpy.types.Operator):
    """Cutter: Makes boolean modifier > named "Cutter" > Collection Type operand > Collection > Solver Fast"""
    bl_label = ""
    bl_idname = "object.button_cutter_box"
    
        
    def execute(self, context):
        
        
        active = bpy.context.active_object    
        active.select_set(True)
        bpy.ops.object.modifier_add(type='BOOLEAN')
        active_mod = bpy.data.objects[bpy.context.active_object.name].modifiers.active.name
        bpy.ops.object.modifier_set_active(modifier=active_mod)
        bpy.context.object.modifiers[active_mod].name = "AB_Cutter_Collection"
        active_cutter = bpy.data.objects[bpy.context.active_object.name].modifiers.active.name
        bpy.ops.object.modifier_set_active(modifier=active_cutter)
        bpy.context.object.modifiers[active_cutter].operation = 'DIFFERENCE'
        bpy.context.object.modifiers[active_cutter].operand_type = 'COLLECTION'
        bpy.context.object.modifiers[active_cutter].solver = 'FAST'
        

        #bpy.ops.wm.tool_set_by_id(name="builtin.primitive_cube_add")
        active.select_set(True)
        
        #Creates Empty mesh data and exchange data's for cutter
        
        new_collection = ensure_collection(context.scene, "AB_Cutters_Collection")
        
        bpy.context.object.modifiers[active_cutter].collection = bpy.data.collections["AB_Cutters_Collection"]
        
        for i in bpy.data.collections['AB_Cutters_Collection'].objects:
            i.color = (1, 0.0252077, 0.021955, 0.342857)



        #bpy.context.object.modifiers[active_cutter].object = bpy.data.objects[active_cutter]

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# BOX CUTTER OBJECT


class cutter_box_object(bpy.types.Operator):
    """Cutter: Makes boolean modifier > named "AB_Cutter_Object" > Object Type operand > Object > Solver Fast"""
    bl_label = ""
    bl_idname = "object.button_cutter_box_object"
    
        
    def execute(self, context):
        new_collection = ensure_collection_object(context.scene, "AB_Cutters_Object")
        leng= len(bpy.data.collections['AB_Cutters_Object'].objects)
        
        for k in range(0,leng):
            active = bpy.context.active_object    
            active.select_set(True)
            bpy.ops.object.modifier_add(type='BOOLEAN')
            active_mod = bpy.data.objects[bpy.context.active_object.name].modifiers.active.name
            bpy.ops.object.modifier_set_active(modifier=active_mod)
            
            bpy.context.object.modifiers[active_mod].name = "AB_Cutter_Object"+ str(k)
            active_cutter = bpy.data.objects[bpy.context.active_object.name].modifiers.active.name
            bpy.ops.object.modifier_set_active(modifier=active_cutter)
            bpy.context.object.modifiers[active_cutter].operation = 'DIFFERENCE'
            bpy.context.object.modifiers[active_cutter].operand_type = 'OBJECT'
            bpy.context.object.modifiers[active_cutter].solver = 'FAST'
            

            #bpy.ops.wm.tool_set_by_id(name="builtin.primitive_cube_add")
            active.select_set(True)
            
            #Creates Empty mesh data and exchange data's for cutter
            
            
            
            bpy.context.object.modifiers[active_cutter].collection = bpy.data.collections["AB_Cutters_Object"]
            
        for i in range(0,leng) :
            bpy.context.object.modifiers["AB_Cutter_Object"+ str(i)].object = bpy.data.collections['AB_Cutters_Object'].objects[i]
            bpy.context.object.modifiers["AB_Cutter_Object"+ str(i)].object.color = (0.0517386, 0.70876, 1, 0.342857)

             
         

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# BOX CUTTER APPLY MODIFIER


class cutter_apply_modifier(bpy.types.Operator):
    """Apply all AB_Cutter (Boolean) modifier to Object"""
    bl_label = ""
    bl_idname = "object.button_cutter_apply_modifier"
    
        
    def execute(self, context):
        for obj in bpy.context.selected_objects:
                bpy.context.view_layer.objects.active = obj
                for modifier in obj.modifiers:
                    if modifier.type == 'BOOLEAN':
                            try:
                                bpy.ops.object.modifier_apply(modifier=modifier.name)
                            except (AttributeError, KeyError, RuntimeError):
                                bpy.ops.object.modifier_remove(modifier="Boolean")
        return {"FINISHED"}
      
# ------------------------------------------------------------------------------
# TOP VIEW OPERATOR


class view_3d_top(bpy.types.Operator):
    """Top View"""
    bl_label = ""
    bl_idname = "object.button_view_3d_top"

    def execute(self, context):
        bpy.ops.view3d.view_axis(type='TOP')
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# BOTTOM VIEW OPERATOR


class view_3d_bottom(bpy.types.Operator):
    """Bottom View"""
    bl_label = ""
    bl_idname = "object.button_view_3d_bottom"

    def execute(self, context):
        bpy.ops.view3d.view_axis(type='BOTTOM')
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# FRONT VIEW OPERATOR


class view_3d_front(bpy.types.Operator):
    """Front View"""
    bl_label = ""
    bl_idname = "object.button_view_3d_front"

    def execute(self, context):
        bpy.ops.view3d.view_axis(type='FRONT')
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# BACK VIEW OPERATOR


class view_3d_back(bpy.types.Operator):
    """Back View"""
    bl_label = ""
    bl_idname = "object.button_view_3d_back"

    def execute(self, context):
        bpy.ops.view3d.view_axis(type='BACK')
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# RIGHT VIEW OPERATOR


class view_3d_right(bpy.types.Operator):
    """Right View"""
    bl_label = ""
    bl_idname = "object.button_view_3d_right"

    def execute(self, context):
        bpy.ops.view3d.view_axis(type='RIGHT')
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# LEFT VIEW OPERATOR


class view_3d_left(bpy.types.Operator):
    """Right View"""
    bl_label = ""
    bl_idname = "object.button_view_3d_left"

    def execute(self, context):
        bpy.ops.view3d.view_axis(type='LEFT')
        return {"FINISHED"}
# ------------------------------------------------------------------------------
# VERTEX SELECTION PANEL


class Modelling_Panel_Vertex_Selection (bpy.types.Panel):
    bl_label = ""
    bl_idname = "Vertex_Selection"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_Modelling_Panel"

    def draw_header(self, context):

        layout = self.layout

        layout.label(text="Vertex Modify Selection", icon="VERTEXSEL")

    def draw(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        #row = layout.row()

        try:
            if bpy.context.tool_settings.mesh_select_mode[0] and bpy.context.active_object.mode == "EDIT":
                row = layout.row(align=True)
                row.operator("object.button_edit_mode_bridge_vertices",
                             text="New Edge/Face From Vertices", icon="MATPLANE")
                row.operator("object.button_edit_mode_delete_vertices",
                             text="Delete Vertices", icon="PANEL_CLOSE")

                row = layout.row(align=True)
                row.operator("object.button_vertex_selection_rip_vertex",
                             text="Vertex RIP (FAST)", icon="STICKY_UVS_VERT")
                row.operator("object.button_vertex_selection_merge_vertex_last",
                             text="Vertex Merge (LAST)", icon="PIVOT_CURSOR")

                row = layout.row(align=True)
                row.operator("MESH_OT_remove_doubles",
                             text="Vertex Merge (DISTANCE)", icon="CENTER_ONLY")
                row.operator("object.button_vertex_selection_dissolve_vertex",
                             text="Dissolve Vertex", icon="SHADERFX")

                row = layout.row(align=True)
                row.operator("object.button_loop_mesh_shortest_path_pick",
                             text="Shortest Path Select", icon="PARTICLE_POINT")
                row.operator("object.button_vertex_selection_connect_vertex_path",
                             text="Connect Vertex Path", icon="MOD_LENGTH")

                row = layout.row(align=True)
                row.operator("object.button_vertex_selection_create_vertices",
                             text="Create Vertices", icon="NORMALS_VERTEX")
                row.operator("object.button_vertex_selection_assign_vertex_group",
                             text="Assign Vertex Group", icon="GROUP_VERTEX")
                row = layout.row(align=True)
                row.operator(
                    "mesh.vertices_smooth", text="Smooth Vertices", icon="IPO_EASE_IN").factor = 0.5
                row.operator("mesh.select_axis",
                             text="Side of Active", icon="UV_ISLANDSEL")
                row = layout.row(align=True)
                row.operator("transform.vert_slide",
                             text="Vertex Slide", icon="TRACKING")
                #row.operator("object.button_vertex_selection_make_circle", text="Make Circle", icon="MESH_CIRCLE")

            else:
                pass
        except AttributeError:
            pass

# ------------------------------------------------------------------------------
# RIP VERTEX OPERATOR


class vertex_selection_make_circle (bpy.types.Operator):
    """Selected Vertices to make a circle"""
    bl_label = ""
    bl_idname = "object.button_vertex_selection_make_circle"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        mesh = bpy.context.object.data

        selected_verts = [v for v in mesh.vertices if v.select]

        cord_verts = []

        for i in selected_verts:
            cord_verts.append([i.co[0], i.co[1], i.index])

        length_list_cord = len(cord_verts)

        dimensions = []

        for a in range(0, length_list_cord):
            k = [0, 0]
            l_x = k[0]
            l_y = k[1]
            ind = cord_verts[a][2]
            x = cord_verts[a][0]
            y = cord_verts[a][1]

            g = math.sqrt(abs(x-l_x)) + math.sqrt(abs(y-l_y))

            dimensions.append(g)

        for b in range(0, len(dimensions)):
            d = 1
            k = [0, 0]
            l_x = k[0]
            l_y = k[1]
            x = 0
            y = 0
            math.sqrt(abs(x-l_x)) + math.sqrt(abs(y-l_y)) == 1

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# RIP VERTEX OPERATOR


class vertex_selection_rip_vertex (bpy.types.Operator):
    """Rip polygons and move the result"""
    bl_label = ""
    bl_idname = "object.button_vertex_selection_rip_vertex"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        if bpy.context.active_object.mode == "EDIT":
            bpy.ops.mesh.rip('INVOKE_DEFAULT')

        # bpy.ops.mesh.merge(type='LAST')

        return {"FINISHED"}
# ------------------------------------------------------------------------------
# MERGE VERTEX OPERATOR


class vertex_selection_merge_vertex_last (bpy.types.Operator):
    """Merge Selected Vertices"""
    bl_label = ""
    bl_idname = "object.button_vertex_selection_merge_vertex_last"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        if bpy.context.active_object.mode == "EDIT":
            try:
                bpy.ops.mesh.merge(type='LAST')
            except TypeError:
                pass

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# DISSOLVE VERTEX OPERATOR


class vertex_selection_dissolve_vertex (bpy.types.Operator):
    """Dissolve Vertices"""
    bl_label = ""
    bl_idname = "object.button_vertex_selection_dissolve_vertex"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        if bpy.context.active_object.mode == "EDIT":

            bpy.ops.mesh.dissolve_verts()

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# CONNECT VERTICES AS PATH OPERATOR


class vertex_selection_connect_vertex_path (bpy.types.Operator):
    """Connect vertices as path select minimum 2 vertices and try"""
    bl_label = ""
    bl_idname = "object.button_vertex_selection_connect_vertex_path"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        if bpy.context.active_object.mode == "EDIT":
            try:
                bpy.ops.mesh.vert_connect_path()
            except RuntimeError:
                pass

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# CREATE VERTICES OPERATOR


class vertex_selection_create_vertices (bpy.types.Operator):
    """Creates vertices on edges"""
    bl_label = ""
    bl_idname = "object.button_vertex_selection_create_vertices"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        if bpy.context.active_object.mode == "EDIT":

            bpy.ops.mesh.knife_tool(
                'INVOKE_DEFAULT', use_occlude_geometry=True,  only_selected=False, wait_for_input=True)

        return {"FINISHED"}
# ------------------------------------------------------------------------------
# ASIGN VERTEX GROUP OPERATOR


class vertex_selection_assign_vertex_group (bpy.types.Operator):
    """Assign the selected vertices to a new vertex group"""
    bl_label = ""
    bl_idname = "object.button_vertex_selection_assign_vertex_group"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        if bpy.context.active_object.mode == "EDIT":

            bpy.ops.object.vertex_group_assign_new()

        return {"FINISHED"}


# ------------------------------------------------------------------------------
# VERTEX GROUP PANEL

class Modelling_Panel_Vertex_Group_Panel (bpy.types.Panel):
    bl_label = ""
    bl_idname = "Vertex_Groups"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "Vertex_Selection"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    def draw_header(self, context):

        layout = self.layout

        layout.label(text="Vertex Groups", icon="GROUP_VERTEX")

    @classmethod
    def poll(cls, context):
        engine = context.engine
        obj = context.object
        return (obj and obj.type in {'MESH', 'LATTICE'} and (engine in cls.COMPAT_ENGINES))

    def draw(self, context):
        layout = self.layout

        ob = context.object
        group = ob.vertex_groups.active

        rows = 3
        if group:
            rows = 5

        row = layout.row()
        row.template_list("MESH_UL_vgroups", "", ob, "vertex_groups",
                          ob.vertex_groups, "active_index", rows=rows)

        col = row.column(align=True)

        col.operator("object.vertex_group_add", icon='ADD', text="")
        props = col.operator("object.vertex_group_remove",
                             icon='REMOVE', text="")
        props.all_unlocked = props.all = False

        col.separator()

        col.menu("MESH_MT_vertex_group_context_menu",
                 icon='DOWNARROW_HLT', text="")

        if group:
            col.separator()
            col.operator("object.vertex_group_move",
                         icon='TRIA_UP', text="").direction = 'UP'
            col.operator("object.vertex_group_move",
                         icon='TRIA_DOWN', text="").direction = 'DOWN'

        if (
                ob.vertex_groups and
                (ob.mode == 'EDIT' or
                 (ob.mode == 'WEIGHT_PAINT' and ob.type == 'MESH' and ob.data.use_paint_mask_vertex))
        ):
            row = layout.row()

            sub = row.row(align=True)
            sub.operator("object.vertex_group_assign", text="Assign")
            sub.operator("object.vertex_group_remove_from", text="Remove")

            sub = row.row(align=True)
            sub.operator("object.vertex_group_select", text="Select")
            sub.operator("object.vertex_group_deselect", text="Deselect")

            layout.prop(context.tool_settings,
                        "vertex_group_weight", text="Weight")

# ------------------------------------------------------------------------------
# MODIFY SELECTION PANEL


class Modelling_Panel_Modify_Selection (bpy.types.Panel):
    bl_label = ""
    bl_idname = "Modify_Selection"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_Modelling_Panel"

    def draw_header(self, context):

        layout = self.layout

        layout.label(text="Edge Modify Selection", icon="EDGESEL")

    def draw(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        #row = layout.row()

        try:
            # bpy.context.active_object.mode=="EDIT":
            if bpy.context.tool_settings.mesh_select_mode[1] and bpy.context.active_object.mode == "EDIT":
                row = layout.row(align=True)
                row.operator("object.button_loop_multiple_select",
                             text="Edge Loop", icon="PAUSE")
                row.operator("object.button_loop_multiple_select_ring",
                             text="Ring Loop", icon="SNAP_EDGE")
                row = layout.row(align=True)
                row.operator("object.button_modelling_edit_rotate_edges",
                             text="Rotate (CW)", icon="LOOP_FORWARDS")
                row.operator("mesh.edge_rotate", text="Rotate (CCW)",
                             icon="LOOP_BACK").use_ccw = True
                row = layout.row(align=True)
                row.operator("transform.edge_slide",
                             text="Edge Slide", icon="SNAP_MIDPOINT")
                props = row.operator("mesh.loopcut_slide",
                                     icon="PARTICLE_POINT")
                props.TRANSFORM_OT_edge_slide.release_confirm = False
                row.operator("mesh.offset_edge_loops_slide",
                             text="Offset Edge Slide", icon="PARTICLE_TIP")
                row3 = layout.row(align=True)
                row3.operator("object.button_loop_select",
                              text="Loop to Region", icon="HAND")
                row3.operator("object.button_loop_select_boundry_faces",
                              text="Outline", icon="PIVOT_BOUNDBOX")
                row = layout.row(align=True)
                row.operator("mesh.screw", text="Screw", icon="MOD_SCREW")
                row.operator("object.button_modelling_edit_edges_extrude",
                             text="Extrude", icon="FULLSCREEN_ENTER")
                row = layout.row(align=True)
                row.operator("object.button_modelling_edit_edges_collapse",
                             text="Collapse Edges", icon="FULLSCREEN_EXIT")
                row.operator("mesh.bridge_edge_loops",
                             text="Bridge Edge Loops", icon="COLLAPSEMENU")

                #col.operator("object.button_loop_auto_edge_loop", text="Auto Edge Loop")

            else:
                pass
        except AttributeError:
            pass


# ------------------------------------------------------------------------------
# GROW EDGE LOOP OPERATOR

class loop_grow_edge_select (bpy.types.Operator):
    """Expands the sub-object selection area outward in all available directions"""
    bl_label = ""
    bl_idname = "object.button_loop_grow_edge_select"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        bpy.ops.mesh.select_more()

        return {"FINISHED"}
# ------------------------------------------------------------------------------
# SHRINK EDGE LOOP OPERATOR


class loop_shrink_edge_select (bpy.types.Operator):
    """Reduces the sub-object selection area by deselecting the outer-most sub-objects"""
    bl_label = ""
    bl_idname = "object.button_loop_shrink_edge_select"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        bpy.ops.mesh.select_less()

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# AUTO EDGE LOOP OPERATOR


class loop_auto_edge_loop (bpy.types.Operator):
    """Reduces the sub-object selection area by deselecting the outer-most sub-objects"""
    bl_label = "Auto Edge Loop"
    bl_idname = "object.button_loop_auto_edge_loop"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        return {"FINISHED"}


# ------------------------------------------------------------------------------
# EDIT PANEL

class Modelling_Panel_Modify_Edit (bpy.types.Panel):
    bl_label = ""
    bl_idname = "PT_Modify_Edit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_Modelling_Panel"

    def draw_header(self, context):

        layout = self.layout

        layout.label(text="Edit Geometry", icon="MODIFIER")

    def draw(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        try:
            if bpy.context.active_object.mode == "EDIT":
                row = layout.row(align=True)
                row.operator("object.button_loop_grow_edge_select",
                             text="Grow", icon="ADD")
                row.operator("object.button_loop_shrink_edge_select",
                             text="Shrink", icon="REMOVE")
                row = layout.row(align=True)
                row.operator("object.button_modelling_edit_edges_connect",
                             text="Subdivide", icon="SHADING_WIRE")
                row.operator("mesh.unsubdivide",
                             text="Un-Subdivide", icon="MESH_CIRCLE")
                row1 = layout.row(align=True)
                row1.operator("object.button_modelling_edit_loop_cut",
                              text="Loop Cut", icon="MESH_UVSPHERE")
                row1.operator("object.button_modelling_edit_offset_edge_loop_cut",
                              text="Offset Edge Loop Cut", icon="MOD_THICKNESS")
                row2 = layout.row(align=True)
                row2.operator("object.button_modelling_edit_knife_cut",
                              text="Knife", icon="MOD_LINEART")
                row2.operator("object.button_modelling_edit_knife_bisect",
                              text="Bisect", icon="MOD_TRIANGULATE")
                row4 = layout.row(align=True)
                row4.operator("object.button_loop_mesh_shortest_path_pick",
                              text="Shortest Path Select", icon="DECORATE_DRIVER")
                row4.operator("mesh.fill_grid",
                              text="Magic Fill", icon="SHADERFX")
                row6 = layout.row(align=True)
                row6.operator("mesh.bevel", text="Bevel",
                              icon="MOD_BEVEL").affect = 'EDGES'
                row6.operator("mesh.knife_project", text="Knife Project", icon="VIEW_ORTHO")

                row7 = layout.row(align=True)
                row7.operator("object.button_loop_mesh_seperate",
                              text="Seperate Selected Geometry", icon="OUTLINER_OB_MESH")
                row7.operator("object.button_loop_mesh_split",
                              text="Split Off Selected Geometry", icon="MOD_EXPLODE")
                row = layout.row(align=True)
                row.operator("mesh.intersect")
                row.operator("mesh.intersect_boolean")
                row = layout.row(align=True)
                row.operator("object.button_modelling_edit_clean_mesh", text="Clean Mesh")

                row = layout.row(align=True)
                row.operator("transform.edge_crease", icon="BRUSH_CREASE")
                row.operator("transform.edge_bevelweight",
                             icon="MOD_VERTEX_WEIGHT")

                #col = layout.column()
                #col.label(text="Marks and Clears : ")
                box = layout.box()
                box.prop(Arc_Blend, "marks_edit_geometry",
                         icon="GREASEPENCIL", text="Marks and Clears")
                if bpy.context.scene.Arc_Blend.marks_edit_geometry == True:
                    col = box.column()
                    col.label(text="Marks and Clears :")
                    row = box.row(align=True)
                    row.operator("mesh.mark_seam",
                                 icon="OUTLINER_OB_CURVES").clear = False
                    row.operator("mesh.mark_seam", text="Clear Seam",
                                 icon="OUTLINER_DATA_CURVES").clear = True

                    row = box.row(align=True)
                    row.operator("mesh.mark_sharp", icon="SNAP_PERPENDICULAR")
                    row.operator("mesh.mark_sharp", text="Clear Sharp",
                                 icon="SNAP_MIDPOINT").clear = True
                    #row6.operator("object.button_modelling_edit_fill_sides", text="Align Edges")

                    row = box.row(align=True)
                    row.operator("mesh.mark_freestyle_edge",
                                 icon="HANDLE_FREE").clear = False
                    row.operator("mesh.mark_freestyle_edge",
                                 text="Clear Freestyle Edge", icon="HANDLE_VECTOR").clear = True

                col = layout.column()
                col.label(text="Mirror Selected Copy  :")
                row = layout.row(align=True)
                row.operator(
                    "object.button_modelling_edit_x_mirror", text="+X")
                row.operator(
                    "object.button_modelling_edit_y_mirror", text="+Y")
                row.operator(
                    "object.button_modelling_edit_z_mirror", text="+Z")
                row = layout.row(align=True)
                row.operator(
                    "object.button_modelling_edit_x_mirror_minus", text="-X")
                row.operator(
                    "object.button_modelling_edit_y_mirror_minus", text="-Y")
                row.operator(
                    "object.button_modelling_edit_z_mirror_minus", text="-Z")

                col = layout.column()
                col.label(text="Hide/Rev Selected/Unselected: ")
                row5 = layout.row(align=True)
                row5.operator("object.button_modelling_edit_hide_unselected",
                              text="Hide Unselected", icon="PMARKER")
                row5.operator("object.button_modelling_edit_hide_selected",
                              text="Hide Selected", icon="PMARKER_SEL")
                row5.operator("object.button_modelling_edit_reveal",
                              text="Reveal", icon="PMARKER_ACT")

                col = layout.column()
                col.label(text="Align Axis : ")
                row4 = layout.row(align=True)
                row4.operator(
                    "object.button_modelling_edit_orient_x", text="X", )
                row4.operator(
                    "object.button_modelling_edit_orient_y", text="Y", )
                row4.operator(
                    "object.button_modelling_edit_orient_z", text="Z", )

            else:
                pass

        except AttributeError:
            pass

# ------------------------------------------------------------------------------
# CLEAN MESH OPERATOR

class modelling_edit_clean_mesh (bpy.types.Operator):
    """Select and clean mesh"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_clean_mesh"

    def execute(self, context):
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles()
        bpy.ops.mesh.tris_convert_to_quads()
        bpy.ops.mesh.normals_make_consistent()
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# BEVEL OFFSET OPERATOR

class modelling_edit_rotate_edges (bpy.types.Operator):
    """Rotating an edge clockwise (CW)"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_rotate_edges"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        try:
            bpy.ops.mesh.edge_rotate(use_ccw=False)
        except RuntimeError:
            pass

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# LOOP CUT OPERATOR


class modelling_edit_loop_cut (bpy.types.Operator):
    """Loop Cut"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_loop_cut"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        bpy.ops.wm.tool_set_by_id(name="builtin.loop_cut")

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# OFFSET EDGE LOOP CUT OPERATOR


class modelling_edit_offset_edge_loop_cut (bpy.types.Operator):
    """Offset Edge Loop Cut"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_offset_edge_loop_cut"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        bpy.ops.wm.tool_set_by_id(name="builtin.offset_edge_loop_cut")

        return {"FINISHED"}
# ------------------------------------------------------------------------------
# KNIFE CUT OPERATOR


class modelling_edit_knife_cut (bpy.types.Operator):
    """Knife Tool"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_knife_cut"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                override = bpy.context.copy()
                override["space_data"] = area.spaces[0]
                override["area"] = area

                bpy.ops.mesh.knife_tool(
                    'INVOKE_DEFAULT', use_occlude_geometry=True,  only_selected=False, wait_for_input=True)

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# BISECT OPERATOR


class modelling_edit_knife_bisect (bpy.types.Operator):
    """Bisect Tool"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_knife_bisect"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                override = bpy.context.copy()
                override["space_data"] = area.spaces[0]
                override["area"] = area

                bpy.ops.wm.tool_set_by_id(override, name="builtin.bisect")

        return {"FINISHED"}


# ------------------------------------------------------------------------------
# COPY +X MIRROR OPERATOR

class modelling_edit_x_mirror (bpy.types.Operator):
    """Selected Verts/Edges or Faces Mirrors -X to +X Axis"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_x_mirror"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        bpy.ops.mesh.symmetrize(direction='NEGATIVE_X')

        return {"FINISHED"}
# ------------------------------------------------------------------------------
# COPY -X MIRROR OPERATOR


class modelling_edit_x_mirror_minus (bpy.types.Operator):
    """Selected Verts/Edges or Faces Mirrors +X to -X Axis"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_x_mirror_minus"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        bpy.ops.mesh.symmetrize(direction='POSITIVE_X')

        return {"FINISHED"}
# ------------------------------------------------------------------------------
# COPY +Y MIRROR OPERATOR


class modelling_edit_y_mirror (bpy.types.Operator):
    """Selected Verts/Edges or Faces Mirrors -Y to +Y Axis"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_y_mirror"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        bpy.ops.mesh.symmetrize(direction='NEGATIVE_Y')

        return {"FINISHED"}
# ------------------------------------------------------------------------------
# COPY -Y MIRROR OPERATOR


class modelling_edit_y_mirror_minus (bpy.types.Operator):
    """Selected Verts/Edges or Faces Mirrors +Y to -Y Axis"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_y_mirror_minus"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        bpy.ops.mesh.symmetrize(direction='POSITIVE_Y')

        return {"FINISHED"}
# ------------------------------------------------------------------------------
# COPY +Z MIRROR OPERATOR


class modelling_edit_z_mirror (bpy.types.Operator):
    """Selected Verts/Edges or Faces Mirrors -Z to +Z Axis"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_z_mirror"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        bpy.ops.mesh.symmetrize(direction='NEGATIVE_Z')

        return {"FINISHED"}
# ------------------------------------------------------------------------------
# COPY -Z MIRROR OPERATOR


class modelling_edit_z_mirror_minus (bpy.types.Operator):
    """Selected Verts/Edges or Faces Mirrors +Z to -Z Axis"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_z_mirror_minus"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        bpy.ops.mesh.symmetrize(direction='POSITIVE_Z')

        return {"FINISHED"}
# ------------------------------------------------------------------------------
# FILL SIDES OPERATOR


class modelling_edit_fill_sides (bpy.types.Operator):
    """Align Edges (Select loop and select one edge for referance (WIP)"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_fill_sides"

    def execute(self, context):
        layout = self.layout

        ob = context.object
        me = ob.data
        bm = bmesh.from_edit_mesh(me)

        edge_lengths = []

        for e in bm.edges:
            if e.select:
                edge_lengths.append(e.calc_length())
                #x= e.co.x
                #y= e.co.y
                #z= e.co.z

        sumz = sum(edge_lengths)

        setting = list(sorted(edge_lengths))

        scale = setting[-1]/setting[0]

        bpy.ops.transform.resize(value=(float(scale), float(scale), float(scale)), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
                                 mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

        return {"FINISHED"}


# ------------------------------------------------------------------------------
# HIDE UNSELECTED OPERATOR

class modelling_edit_hide_unselected (bpy.types.Operator):
    """Hide Unselected vert/edge or faces"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_hide_unselected"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        bpy.ops.mesh.hide(unselected=True)

        return {"FINISHED"}
# ------------------------------------------------------------------------------
# HIDE SELECTED OPERATOR


class modelling_edit_hide_selected (bpy.types.Operator):
    """Hide Selected vert/edge or faces"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_hide_selected"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        bpy.ops.mesh.hide(unselected=False)

        return {"FINISHED"}
# ------------------------------------------------------------------------------
# REVEAL OPERATOR


class modelling_edit_reveal (bpy.types.Operator):
    """Reveal hiding vert/edge or faces"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_reveal"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        bpy.ops.mesh.reveal(select=True)

        return {"FINISHED"}


# ------------------------------------------------------------------------------
# ORIENT X AXIS OPERATOR

class modelling_edit_orient_x (bpy.types.Operator):
    """Align X Axis selected all vertices,edges or faces"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_orient_x"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                override = bpy.context.copy()
                override["space_data"] = area.spaces[0]
                override["area"] = area

                bpy.ops.transform.resize(value=(0, 1, 1),
                                         orient_type='GLOBAL',
                                         orient_matrix=(
                                             (1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                         orient_matrix_type='GLOBAL',
                                         constraint_axis=(True, True, True),
                                         mirror=True, use_proportional_edit=False,
                                         proportional_edit_falloff='RANDOM',
                                         proportional_size=0.001,
                                         use_proportional_connected=False,
                                         use_proportional_projected=False)

        return {"FINISHED"}
# ------------------------------------------------------------------------------
# ORIENT Y AXIS OPERATOR


class modelling_edit_orient_y (bpy.types.Operator):
    """Align Y Axis selected all vertices,edges or faces"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_orient_y"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                override = bpy.context.copy()
                override["space_data"] = area.spaces[0]
                override["area"] = area

                bpy.ops.transform.resize(value=(1, 0, 1),
                                         orient_type='GLOBAL',
                                         orient_matrix=(
                                             (1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                         orient_matrix_type='GLOBAL',
                                         constraint_axis=(True, True, True),
                                         mirror=True, use_proportional_edit=False,
                                         proportional_edit_falloff='RANDOM',
                                         proportional_size=0.001,
                                         use_proportional_connected=False,
                                         use_proportional_projected=False)

        return {"FINISHED"}


# ------------------------------------------------------------------------------
# ORIENT Z AXIS OPERATOR

class modelling_edit_orient_z (bpy.types.Operator):
    """Align Z Axis selected all vertices,edges or faces"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_orient_z"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                override = bpy.context.copy()
                override["space_data"] = area.spaces[0]
                override["area"] = area

                bpy.ops.transform.resize(value=(1, 1, 0),
                                         orient_type='GLOBAL',
                                         orient_matrix=(
                                             (1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                         orient_matrix_type='GLOBAL',
                                         constraint_axis=(True, True, True),
                                         mirror=True, use_proportional_edit=False,
                                         proportional_edit_falloff='RANDOM',
                                         proportional_size=0.001,
                                         use_proportional_connected=False,
                                         use_proportional_projected=False)

        return {"FINISHED"}


# ------------------------------------------------------------------------------
# EDIT EDGES PANEL

class Modelling_Panel_Modify_Edit_Faces (bpy.types.Panel):
    bl_label = ""
    bl_idname = "PT_Modify_Edit_Faces"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_Modelling_Panel"

    def draw_header(self, context):

        layout = self.layout

        layout.label(text="Face Modify Selection", icon="FACESEL")

    def draw(self, context):
        layout = self.layout
        obj = context.object

        try:
            # bpy.context.active_object.mode=="EDIT":
            if bpy.context.tool_settings.mesh_select_mode[2] and bpy.context.active_object.mode == "EDIT":
                row = layout.row(align=True)
                row.operator(
                    "object.button_modelling_edit_faces_extrude", text="Face", icon="MESH_CUBE")
                row.operator("object.button_modelling_edit_faces_extrude_normals",
                             text="Normal", icon="ORIENTATION_NORMAL")
                row.operator("object.button_modelling_edit_faces_extrude_individual",
                             text="Individual", icon="IMGDISPLAY")

                row = layout.row(align=True)
                row.operator("object.button_modelling_edit_faces_inset",
                             text="Inset Face", icon="CLIPUV_DEHLT")
                row.operator("mesh.poke", text="Poke", icon="SNAP_NORMAL")
                row = layout.row(align=True)
                row.operator("object.button_modelling_edit_faces_triangulate",
                             text="Triangulate", icon="MOD_TRIANGULATE")
                row.operator("object.button_modelling_edit_faces_tris_to_quads",
                             text="Tris to Quads", icon="MATPLANE")
                row = layout.row(align=True)
                row.operator("mesh.solidify", text="Solidify",
                             icon="MOD_SOLIDIFY")
                row.operator("mesh.wireframe", text="Wireframe",
                             icon="MOD_WIREFRAME")
                row = layout.row(align=True)
                row.operator("object.button_modelling_edit_faces_flip_normals", text="Flip(N)",
                             icon="NORMALS_FACE")
                row.operator("object.button_modelling_edit_faces_recalculate_outside", text="Recalculate Outside(N)",
                             icon="ORIENTATION_NORMAL")

                # col=layout.column(align=True)

            else:
                pass

        except AttributeError:
            pass

# ------------------------------------------------------------------------------
# FLIP NORMALS OPERATOR


class modelling_edit_faces_flip_normals(bpy.types.Operator):
    """Flip Normals"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_faces_flip_normals"

    def execute(self, context):
        bpy.ops.mesh.flip_normals()
        return {"FINISHED"}
    
# ------------------------------------------------------------------------------
# RECALCULATE OUTSIDE OPERATOR


class modelling_edit_faces_recalculate_outside(bpy.types.Operator):
    """Reaclculate Outside (Normals)"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_faces_recalculate_outside"

    def execute(self, context):
        bpy.ops.mesh.normals_make_consistent(inside=False)
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# EXTRUDE FACES OPERATOR


class modelling_edit_faces_extrude(bpy.types.Operator):
    """Face Extrude"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_faces_extrude"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        bpy.ops.view3d.edit_mesh_extrude_move_normal()

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# EXTRUDE NORMAL FACES OPERATOR


class modelling_edit_faces_extrude_normals (bpy.types.Operator):
    """Face Extrude Normal"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_faces_extrude_normals"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        bpy.ops.view3d.edit_mesh_extrude_move_shrink_fatten()

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# EXTRUDE INDIVIDUAL FACES OPERATOR


class modelling_edit_faces_extrude_individual (bpy.types.Operator):
    """Face Extrude Individual"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_faces_extrude_individual"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        bpy.ops.mesh.extrude_faces_move("INVOKE_DEFAULT",
                                        MESH_OT_extrude_faces_indiv={
                                            "mirror": False},
                                        TRANSFORM_OT_shrink_fatten={"value": 0, "use_even_offset": False, "mirror": False, "use_proportional_edit": False, "proportional_edit_falloff": 'SMOOTH', "proportional_size": 1, "use_proportional_connected": False, "use_proportional_projected": False, "snap": False, "snap_target": 'CLOSEST', "snap_point": (0, 0, 0), "snap_align": False, "snap_normal": (0, 0, 0), "release_confirm": False, "use_accurate": False})

        return {"FINISHED"}
# ------------------------------------------------------------------------------
# INSET FACES OPERATOR


class modelling_edit_faces_inset (bpy.types.Operator):
    """Face Inset"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_faces_inset"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        bpy.ops.mesh.inset("INVOKE_DEFAULT")

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# POKE FACES OPERATOR


class modelling_edit_faces_poke (bpy.types.Operator):
    """Poke Faces"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_faces_poke"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        bpy.ops.mesh.poke(offset=0, use_relative_offset=True,
                          center_mode='MEDIAN')

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# TRIANGULATE FACES OPERATOR


class modelling_edit_faces_triangulate (bpy.types.Operator):
    """Triangulate Faces"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_faces_triangulate"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        bpy.ops.mesh.quads_convert_to_tris(
            quad_method='BEAUTY', ngon_method='BEAUTY')

        return {"FINISHED"}
# ------------------------------------------------------------------------------
# TRIS TO QUADS FACES OPERATOR


class modelling_edit_faces_tris_to_quads (bpy.types.Operator):
    """Triangulate Faces"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_faces_tris_to_quads"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        bpy.ops.mesh.tris_convert_to_quads()

        return {"FINISHED"}
# ------------------------------------------------------------------------------
# SOLIDIFY FACES OPERATOR


class modelling_edit_faces_solidify (bpy.types.Operator):
    """Triangulate Faces"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_faces_solidify"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        bpy.ops.mesh.solidify("INVOKE_DEFAULT")

        return {"FINISHED"}
# ------------------------------------------------------------------------------
# WIREFRAME FACES OPERATOR


class modelling_edit_faces_wireframe (bpy.types.Operator):
    """Triangulate Faces"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_faces_wireframe"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        bpy.ops.mesh.wireframe("INVOKE_DEFAULT")

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# EDGE CONNECT OPERATOR


class modelling_edit_edges_connect (bpy.types.Operator):
    """Subdivide Edges/Faces"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_edges_connect"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        bpy.ops.mesh.subdivide()

        return {"FINISHED"}


# ------------------------------------------------------------------------------
# EXTRUDE OPERATOR


class modelling_edit_edges_extrude (bpy.types.Operator):
    """Extrude"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_edges_extrude"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        Arc_Blend = scene.Arc_Blend

        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                override = bpy.context.copy()
                override["space_data"] = area.spaces[0]
                override["area"] = area

                bpy.ops.wm.tool_set_by_id(
                    override, name="builtin.extrude_region")

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# COLLAPSE EDGES OPERATOR


class modelling_edit_edges_collapse (bpy.types.Operator):
    """Collapse Edge or Edges"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_edges_collapse"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene

        bpy.ops.mesh.delete_edgeloop(use_face_split=True)

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# COLLAPSE EDGES OPERATOR


class modelling_edit_edges_collapse (bpy.types.Operator):
    """Collapse Edge or Edges"""
    bl_label = ""
    bl_idname = "object.button_modelling_edit_edges_collapse"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene

        bpy.ops.mesh.delete_edgeloop(use_face_split=True)

        return {"FINISHED"}


# ------------------------------------------------------------------------------
# PROXY PANEL

class Proxy_Panel (bpy.types.Panel):
    bl_label = "AB Proxy"
    bl_idname = "PT_Proxy_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        mesh = true_mesh_data(obj)
        Arc_Blend = scene.Arc_Blend
        ui = bpy.ops.ui
        main = layout.column()

        main.label(text="Proxy Panel:", icon="FILE_3D")

        # define two rows
        row = main.row()
        col1 = row.column()
        col2 = row.column()

        # draw template
        template = col1.column()
        try:
            template.template_list(
                "proxy_panel_object_list", "", mesh, "mesh_list", mesh, "list_index", rows=2)
        except (TypeError,AttributeError):
            pass
        template.scale_y = 1.1

        # draw side bar
        col2.separator(factor=0)
        #
        add = col2.column(align=True)
        AB_ADD = add.operator(
            "object.button_proxy_panel_add_objects", icon='ADD', text="")
        AB_ADD.add = "ADD"
        try:
            AB_ADD.mesh_name = mesh.name
        except AttributeError:
            pass

        #
        rem = col2.column(align=True)
        AB_REMOVE = rem.operator(
            "object.button_proxy_panel_remove_objects", icon='REMOVE', text="")
        AB_REMOVE.remove = "REMOVE"
        try:
            AB_REMOVE.mesh_name = mesh.name
        except AttributeError:
            pass

        col2.column_flow(columns=3, align=True)

        #
        rem = col2.column(align=True)
        rem.operator("object.button_proxy_panel_list_makes_parents",
                     icon='LINKED', text="")

        #
        rem = col2.column(align=True)
        rem.operator("object.button_proxy_panel_list_clear_parents",
                     icon='UNLINKED', text="")

        #
        rem = col2.column(align=True)
        rem.operator("object.button_proxy_panel_list_select_same_collection",
                     icon='OUTLINER_COLLECTION', text="")

        #
        rem = col2.column(align=True)
        rem.operator(
            "object.button_proxy_panel_list_apply_all_modifiers", icon='CHECKMARK', text="")

        col = layout.column()
        try:
            col.prop(obj,  "proxy_item_obj", icon="FILE_3D",
                     text="Active Object : ")
        except (AttributeError, TypeError):
            pass
        col.enabled = False

        col = layout.column()
        col.operator("object.button_edit_mode_add_vertex",
                     text="Add Empty Mesh")

        if bpy.context.selected_objects != []:
            row = layout.row(align=True)
            row.scale_x = 1
            row.label(text="Number of Faces:")
            row.scale_x = 1.5
            row.prop(Arc_Blend, "layer", text="")
            layout.operator(
                "object.button_proxy_panel_remeshx_result", text="Remesh")
            layout.operator(
                "object.button_proxy_panel_convertto_point_cloud", text="Point Cloud")
            layout.operator(
                "object.button_proxy_panel_convertto_hull_geometry", text="Convex Hull")
            layout.operator(
                "object.button_proxy_panel_convertto_bound_box", text="Bounding Box")

        else:
            pass


# ------------------------------------------------------------------------------
# REMESH APPLY OPERATOR


class proxy_panel_remeshx_result (bpy.types.Operator):
    """Remesh it.All data layers keeps in program"""
    bl_label = ""
    bl_idname = "object.button_proxy_panel_remeshx_result"

    def execute(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene

        bpy.ops.object.duplicate()
        x = f'{int(bpy.context.scene.Arc_Blend.layer)}'
        bpy.context.active_object.data.name = "AB_Object_" + str(x)
        bpy.context.active_object.name = "AB_Object_Remesh"

        bpy.context.object.data.remesh_mode = 'QUAD'
        bpy.context.object.data.use_remesh_preserve_paint_mask = False
        bpy.context.object.data.use_remesh_preserve_sculpt_face_sets = False
        bpy.ops.object.quadriflow_remesh(
            target_faces=int(bpy.context.scene.Arc_Blend.layer))

        time.sleep(1)
        bpy.ops.object.delete()

        return {"FINISHED"}
# ------------------------------------------------------------------------------
# CONVERT TO POINTS OPERATOR


class proxy_panel_convertto_point_cloud (bpy.types.Operator):
    """Mesh to Points"""
    bl_label = ""
    bl_idname = "object.button_proxy_panel_convertto_point_cloud"

    def execute(self, context):
        layout = self.layout
        scene = bpy.context.scene
        mesh_list = context.object.data.mesh_list
        index = context.object.data.list_index

        win = bpy.context.window
        scr = win.screen
        areas3d = [area for area in scr.areas if area.type == 'VIEW_3D']
        region = [
            region for region in areas3d[0].regions if region.type == 'WINDOW']
        override = {'window': win,
                    'screen': scr,
                    'area': areas3d[0],
                    'region': region,
                    'scene': bpy.context.scene,
                    }

        bpy.ops.object.duplicate()
        bpy.context.active_object.data.name = "AB_Point_Cloud"
        bpy.context.active_object.name = "AB_Point_Cloud"

        bpy.ops.object.mode_set(mode='EDIT', toggle=False)

        bpy.ops.mesh.select_all(action='SELECT')

        bpy.ops.mesh.delete(type='EDGE_FACE')
        bpy.ops.object.editmode_toggle()

        bpy.ops.object.delete()

        return {"FINISHED"}


# ------------------------------------------------------------------------------
# CONVERT TO HULL GEOMETRY OPERATOR


class proxy_panel_convertto_hull_geometry (bpy.types.Operator):
    """Mesh to Convex Hull Geometry"""
    bl_label = ""
    bl_idname = "object.button_proxy_panel_convertto_hull_geometry"

    def execute(self, context):
        layout = self.layout
        scene = bpy.context.scene
        mesh_list = context.object.data.mesh_list
        index = context.object.data.list_index

        win = bpy.context.window
        scr = win.screen
        areas3d = [area for area in scr.areas if area.type == 'VIEW_3D']
        region = [
            region for region in areas3d[0].regions if region.type == 'WINDOW']
        override = {'window': win,
                    'screen': scr,
                    'area': areas3d[0],
                    'region': region,
                    'scene': bpy.context.scene,
                    }

        bpy.ops.object.duplicate()
        bpy.context.active_object.data.name = "AB_Convex_Hull"
        bpy.context.active_object.name = "AB_Convex_Hull"

        bpy.ops.object.mode_set(mode='EDIT', toggle=False)

        bpy.ops.mesh.select_all(action='SELECT')

        bpy.ops.mesh.convex_hull()

        bpy.ops.object.editmode_toggle()

        bpy.ops.object.delete()

        return {"FINISHED"}


# ------------------------------------------------------------------------------
# BOUNDING BOX Def


def bounding_box_display_upd(self, context):

    if self.bounding_box_display == True:
        return_one_time(self.id_data, self.proxy_ui_index,
                        "bounding_box_display")

    bpy.context.object.data = bpy.data.meshes[f"{bpy.context.active_object.name}"]

    return {"FINISHED"}


# ------------------------------------------------------------------------------
# BOUNDING BOX GEOMETRY OPERATOR


class proxy_panel_convertto_bound_box (bpy.types.Operator):
    """Mesh to Bounding Box Geometry"""
    bl_label = ""
    bl_idname = "object.button_proxy_panel_convertto_bound_box"

    def execute(self, context):
        layout = self.layout
        scene = bpy.context.scene
        mesh_list = context.object.data.mesh_list
        index = context.object.data.list_index

        win = bpy.context.window
        scr = win.screen
        areas3d = [area for area in scr.areas if area.type == 'VIEW_3D']
        region = [
            region for region in areas3d[0].regions if region.type == 'WINDOW']
        override = {'window': win,
                    'screen': scr,
                    'area': areas3d[0],
                    'region': region,
                    'scene': bpy.context.scene,
                    }

        o = []
        ob = bpy.context.active_object

        ob.matrix_world.translation  # or .to_translation()

        bbox_corners = [ob.matrix_parent_inverse @
                        Vector(corner)for corner in ob.bound_box]
        # bbox_corners = [ob.matrix_world * Vector(corner)for corner in ob.bound_box]  # Use this in V2.79 or older

        verts = []
        edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 4), (4, 5),
                 (5, 6), (6, 7), (1, 5), (2, 6), (3, 7)]
        faces = [(0, 1, 2, 3), (1, 5, 6, 2), (0, 1, 5, 4),
                 (3, 2, 6, 7), (0, 4, 7, 3), (4, 5, 6, 7)]
        o = []

        for i in bbox_corners:
            o.append(i.xyz)

        # sorting min to max
        # o.sort()

        for b in o:
            verts.append(b[:])

        name_object = f"{bpy.context.active_object.name}"
        new_mesh = bpy.data.meshes.new(name_object + "_Bound_Box")
        new_mesh.from_pydata(verts, edges, faces)

        return {"FINISHED"}


# ------------------------------------------------------------------------------
# PROXY OBJECT LIST


class proxy_panel_object_list(bpy.types.UIList):
    """UI Proxy List"""

    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_propname, index):

        scene = context.scene
        row = layout.row(align=True)

        sub = row.row(align=True)
        sub.scale_x = 2

        sub.prop(item, "proxy_item", text='', icon="FILE_3D")

        sub = row.row(align=True)
        sub.scale_x = 1.1
        sub.enabled = bool(item.proxy_item)
        sub.prop(item, "proxy_display", text='',
                 icon='RESTRICT_VIEW_OFF' if item.proxy_display else 'RESTRICT_VIEW_ON')

        sub = row.row(align=True)
        sub.scale_x = 0.3
        sub.prop(item, "name", text="", icon="RADIOBUT_ON", emboss=False)
        sub.enabled = False

        #sub.prop(item,"proxy_render_frame",text='', icon='RESTRICT_RENDER_OFF'if item.proxy_render_frame else'RESTRICT_RENDER_ON')


# ------------------------------------------------------------------------------
# ADD OBJECT TO LIST


class proxy_panel_add_objects (bpy.types.Operator):
    """Add a new item to the list"""

    bl_label = ""
    bl_idname = "object.button_proxy_panel_add_objects"

    #mesh_name= bpy.props.StringProperty()
    #mesh_n = "Untitled"
    #mesh_name = bpy.context.object.data.name
    #mesh_name = ""

    add: bpy.props.StringProperty()
    mesh_name: bpy.props.StringProperty()

    def execute(self, context):
        try:
            mesh = bpy.data.meshes[self.mesh_name]
            index = mesh.list_index

            if self.add == 'ADD':

                item = mesh.mesh_list.add()

                item.name = mesh.name

                item.proxy_ui_index = len(mesh.mesh_list)

                mesh.list_index = len(mesh.mesh_list)-1

                fill_original_pointer(mesh)

        except (AttributeError, KeyError):
            pass

        return {'FINISHED'}
# ------------------------------------------------------------------------------
# DELETE OBJECT FROM LIST


class proxy_panel_remove_objects (bpy.types.Operator):
    """Remove item from the list"""

    bl_label = ""
    bl_idname = "object.button_proxy_panel_remove_objects"

    remove: bpy.props.StringProperty()
    mesh_name: bpy.props.StringProperty()

    def execute(self, context):
        try:
            mesh = bpy.data.meshes[self.mesh_name]
            index = mesh.list_index

            if self.remove == 'REMOVE':

                mesh.list_index -= 1
                mesh.mesh_list.remove(index)
                clean_original_pointer()
                # maybe user deleted active boolean

        except (AttributeError, KeyError):
            pass

        return {'FINISHED'}


# ------------------------------------------------------------------------------
# DEFINES
def find_instances(mesh_data):
    """Finds the instances"""
    r = []
    for o in bpy.data.objects:
        if (o.type == 'MESH'):
            if true_mesh_data(o) == mesh_data:
                r.append(o)
    return r


def fill_original_pointer(mesh_data):
    """Pointer filled first active object"""

    for ob in find_instances(mesh_data):
        # if ui list not empty but pointer is -> fill pointer
        if (len(ob.data.mesh_list) > 0) and (not ob.proxy_item_obj):
            ob.proxy_item_obj = mesh_data
    return None


def clean_original_pointer():
    """Clean original pointer"""

    for ob in bpy.data.objects:
        if ob.type == 'MESH':
            # if ui list empty but pointer original full -> restore and clean
            if (ob.proxy_item_obj) and (len(ob.proxy_item_obj.mesh_list) == 0):
                if ob.data != ob.proxy_item_obj:
                    ob.data = ob.proxy_item_obj
                ob.proxy_item_obj = None
    return None


def true_mesh_data(obj):
    """Original Mesh Data"""
    try:
        if obj.proxy_item_obj:
            return obj.proxy_item_obj
        else:
            return obj.data
    except AttributeError:
        pass


def return_one_time(mesh, active_idx, prop_api):
    """Returning once per elements"""
    AB_list = mesh.mesh_list

    for i in AB_list:
        if i.proxy_ui_index != active_idx:
            exec(f"i.{prop_api}= False")
    return None


def proxy_item_upd(self, context):
    if not self.proxy_item:
        self.proxy_render_frame = self.proxy_display = False
    return None


def proxy_display_upd(self, context):

    if self.proxy_display == True:
        return_one_time(self.id_data, self.proxy_ui_index, "proxy_display")

    selected_objects = bpy.context.selected_objects

    if len(selected_objects) > 1:
        try:
            for i in range(0, len(selected_objects)):
                o = []

                disp_list = list(
                    bpy.data.meshes[f"{bpy.context.active_object.proxy_item_obj.name}"].mesh_list)

                for j in disp_list:

                    o.append(j.proxy_display)

                    true_count = sum(o)

                if true_count == 1:

                    selected_objects[i].data = bpy.data.meshes[self.proxy_item.name]

                # if proxy_display is off than active objects change to first object
                elif true_count == 0:

                    selected_objects[i].data = bpy.data.meshes[
                        f"{bpy.context.active_object.proxy_item_obj.name}"]

        except AttributeError:
            pass

    elif len(selected_objects) <= 1:

        try:
            for i in range(0, len(bpy.data.meshes[f"{bpy.context.active_object.proxy_item_obj.name}"].mesh_list)):
                o = []

                disp_list = list(
                    bpy.data.meshes[f"{bpy.context.active_object.proxy_item_obj.name}"].mesh_list)

                # All list item append to "o"list and count the "True"
                for j in disp_list:

                    o.append(j.proxy_display)

                    true_count = sum(o)

                # if proxy_display is on than selected objects change
                if true_count == 1:

                    bpy.context.object.data = bpy.data.meshes[self.proxy_item.name]

                # if proxy_display is off than active objects change to first object
                elif true_count == 0:

                    bpy.context.object.data = bpy.data.meshes[
                        f"{bpy.context.active_object.proxy_item_obj.name}"]

        except AttributeError:
            pass

    return None

# def proxy_render_frame_upd(self, context):


#        if self.proxy_render_frame == True:return_one_time(self.id_data, self.proxy_ui_index, "proxy_render_frame")

#        return None


# ------------------------------------------------------------------------------
# PROXY PROPERTY GROUP

class proxy_panel_list_item(bpy.types.PropertyGroup):

    id: bpy.props.IntProperty()
    object: bpy.props.PointerProperty(
        name="Object",
        type=bpy.types.Object,)

    # Name of the items in the list
    name: bpy.props.StringProperty(description="Object Name",)
    # Random props in the lists
    proxy_ui_index: bpy.props.IntProperty(description='UI List Index',)
    proxy_item: bpy.props.PointerProperty(
        type=bpy.types.Mesh, description='Mesh Name', update=proxy_item_upd)
    proxy_display: bpy.props.BoolProperty(
        default=False, description="Display in Viewport", update=proxy_display_upd)
    #proxy_render_frame : bpy.props.BoolProperty(default=False,description="Show in Render",update=proxy_render_frame_upd)
    bound_box_display: bpy.props.BoolProperty(
        default=False, description="Display in Viewport", update=bounding_box_display_upd)

    def copy(self):
        self.object = self.id_data.copy()
        self.name = self.object.name
        return self.object

    def add(self, ob):
        self.object = ob
        self.name = ob.name
        return self.object

# ------------------------------------------------------------------------------
# MAKE PARENT


class proxy_panel_list_makes_parents(bpy.types.Operator):
    """Make Parent Active Object!"""

    bl_label = ""
    bl_idname = "object.button_proxy_panel_list_makes_parents"

    def execute(self, context):
        try:
            bpy.ops.object.parent_set(type='OBJECT')

        except (AttributeError, KeyError, RuntimeError):
            pass

        return {"FINISHED"}
# ------------------------------------------------------------------------------
# CLEAR PARENT


class proxy_panel_list_clear_parents(bpy.types.Operator):
    """Clear Parent Active Object!"""

    bl_label = ""
    bl_idname = "object.button_proxy_panel_list_clear_parents"

    def execute(self, context):
        try:

            bpy.ops.object.parent_clear(type='CLEAR')

        except (AttributeError, KeyError, RuntimeError):
            pass

        return {"FINISHED"}
# ------------------------------------------------------------------------------
# SELECT SAME COLLECTION


class proxy_panel_list_select_same_collection(bpy.types.Operator):
    """Select Same Collection Objects!"""

    bl_label = ""
    bl_idname = "object.button_proxy_panel_list_select_same_collection"

    def execute(self, context):
        try:

            bpy.ops.object.select_grouped(type='COLLECTION')

        except (AttributeError, KeyError, RuntimeError):
            pass

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# APPLY MODIFIERS OBJECT


class proxy_panel_list_apply_all_modifiers(bpy.types.Operator):
    """Apply all modifiers!"""

    bl_label = ""
    bl_idname = "object.button_proxy_panel_list_apply_all_modifiers"

    def execute(self, context):
        try:

            for obj in bpy.context.selected_objects:
                bpy.context.view_layer.objects.active = obj
                for modifier in obj.modifiers:

                    # Array Modifier Apply
                    if modifier.type == 'ARRAY':
                        try:
                            bpy.ops.object.modifier_apply(
                                modifier=modifier.name)

                        except (AttributeError, KeyError, RuntimeError):

                            bpy.ops.object.modifier_remove(modifier="Array")

                    # Bevel Modifier Apply
                    elif modifier.type == 'BEVEL':
                        try:
                            bpy.ops.object.modifier_apply(
                                modifier=modifier.name)

                        except (AttributeError, KeyError, RuntimeError):

                            bpy.ops.object.modifier_remove(modifier="Bevel")

                    # Boolean Modifier Apply
                    elif modifier.type == 'BOOLEAN':
                        try:
                            bpy.ops.object.modifier_apply(
                                modifier=modifier.name)

                        except (AttributeError, KeyError, RuntimeError):

                            bpy.ops.object.modifier_remove(modifier="Boolean")

                    # Build Modifier Apply
                    elif modifier.type == 'BUILD':

                        try:
                            bpy.ops.object.modifier_apply(
                                modifier=modifier.name)

                        except (AttributeError, KeyError, RuntimeError):

                            bpy.ops.object.modifier_remove(modifier="Build")

                    # Decimate Modifier Apply
                    elif modifier.type == 'DECIMATE':

                        try:
                            bpy.ops.object.modifier_apply(
                                modifier=modifier.name)

                        except (AttributeError, KeyError, RuntimeError):

                            bpy.ops.object.modifier_remove(modifier="Decimate")

                    # Edge Split Modifier Apply
                    elif modifier.type == 'EDGE_SPLIT':

                        try:
                            bpy.ops.object.modifier_apply(
                                modifier=modifier.name)

                        except (AttributeError, KeyError, RuntimeError):

                            bpy.ops.object.modifier_remove(
                                modifier="EdgeSplit")

                    # Nodes Modifier Apply
                    elif modifier.type == 'NODES':

                        try:
                            bpy.ops.object.modifier_apply(
                                modifier=modifier.name)

                        except (AttributeError, KeyError, RuntimeError):

                            bpy.ops.object.modifier_remove(
                                modifier="GeometryNodes")

                    # Mask Modifier Apply
                    elif modifier.type == 'MASK':

                        try:
                            bpy.ops.object.modifier_apply(
                                modifier=modifier.name)

                        except (AttributeError, KeyError, RuntimeError):

                            bpy.ops.object.modifier_remove(modifier="Mask")

                    # Mirror Modifier Apply
                    elif modifier.type == 'MIRROR':
                        try:
                            bpy.ops.object.modifier_apply(
                                modifier=modifier.name)

                        except (AttributeError, KeyError, RuntimeError):

                            bpy.ops.object.modifier_remove(modifier="Mirror")

                    # Multiresolution Modifier Apply
                    elif modifier.type == 'MULTIRES':
                        try:
                            bpy.ops.object.modifier_apply(
                                modifier=modifier.name)

                        except (AttributeError, KeyError, RuntimeError):

                            bpy.ops.object.modifier_remove(modifier="Multires")

                    # Remesh Modifier Apply
                    elif modifier.type == 'REMESH':
                        try:
                            bpy.ops.object.modifier_apply(
                                modifier=modifier.name)

                        except (AttributeError, KeyError, RuntimeError):

                            bpy.ops.object.modifier_remove(modifier="Remesh")

                    # Screw Modifier Apply
                    elif modifier.type == 'SCREW':
                        try:
                            bpy.ops.object.modifier_apply(
                                modifier=modifier.name)

                        except (AttributeError, KeyError, RuntimeError):

                            bpy.ops.object.modifier_remove(modifier="Screw")

                    # Skin Modifier Apply
                    elif modifier.type == 'SKIN':
                        try:
                            bpy.ops.object.modifier_apply(
                                modifier=modifier.name)

                        except (AttributeError, KeyError, RuntimeError):

                            bpy.ops.object.modifier_remove(modifier="Skin")

                    # Solidify Modifier Apply
                    elif modifier.type == 'SOLIDIFY':
                        try:
                            bpy.ops.object.modifier_apply(
                                modifier=modifier.name)

                        except (AttributeError, KeyError, RuntimeError):

                            bpy.ops.object.modifier_remove(modifier="Solidify")

                    # Subsurf Modifier Apply
                    elif modifier.type == 'SUBSURF':
                        try:
                            bpy.ops.object.modifier_apply(
                                modifier=modifier.name)

                        except (AttributeError, KeyError, RuntimeError):

                            bpy.ops.object.modifier_remove(
                                modifier="Subdivision")

                    # Triangulate Modifier Apply
                    elif modifier.type == 'TRIANGULATE':
                        try:
                            bpy.ops.object.modifier_apply(
                                modifier=modifier.name)

                        except (AttributeError, KeyError, RuntimeError):

                            bpy.ops.object.modifier_remove(
                                modifier="Triangulate")

                    # Volume to Mesh Modifier Apply
                    elif modifier.type == 'VOLUME_TO_MESH':
                        try:
                            bpy.ops.object.modifier_apply(
                                modifier=modifier.name)

                        except (AttributeError, KeyError, RuntimeError):

                            bpy.ops.object.modifier_remove(
                                modifier="Volume to Mesh")

                    # Weld to Mesh Modifier Apply
                    elif modifier.type == 'WELD':
                        try:
                            bpy.ops.object.modifier_apply(
                                modifier=modifier.name)

                        except (AttributeError, KeyError, RuntimeError):

                            bpy.ops.object.modifier_remove(modifier="Weld")

                    # Wireframe to Mesh Modifier Apply
                    elif modifier.type == 'WIREFRAME':
                        try:
                            bpy.ops.object.modifier_apply(
                                modifier=modifier.name)

                        except (AttributeError, KeyError, RuntimeError):

                            bpy.ops.object.modifier_remove(
                                modifier="Wireframe")

        except (AttributeError, KeyError, RuntimeError):
            pass

        return {"FINISHED"}

# ------------------------------------------------------------------------------
# SCATTER def PANEL


def particle_panel_enabled(context, psys):
    if psys is None:
        return True
    phystype = psys.settings.physics_type
    if psys.settings.type in {'EMITTER', 'REACTOR'} and phystype in {'NO', 'KEYED'}:
        return True
    else:
        return (psys.point_cache.is_baked is False) and (not psys.is_edited) and (not context.particle_system_editable)


def particle_panel_poll(cls, context):
    psys = context.particle_system
    engine = context.engine
    settings = 0

    if psys:
        settings = psys.settings
    elif isinstance(context.space_data.pin_id, bpy.types.ParticleSettings):
        settings = context.space_data.pin_id

    if not settings:
        return False

    return (settings.is_fluid is False) and (engine in cls.COMPAT_ENGINES)


def particle_get_settings(context):
    if context.particle_system:
        return context.particle_system.settings
    elif isinstance(context.space_data.pin_id, bpy.types.ParticleSettings):
        return context.space_data.pin_id
    return None


# ------------------------------------------------------------------------------
# SCATTER OBJECT LIST DEFINES

def find_modifier(ob, psys):
    for md in ob.modifiers:
        if md.type == 'PARTICLE_SYSTEM':
            if md.particle_system == psys:
                return md
    return None


# ------------------------------------------------------------------------------
# SCATTER OBJECT LIST


class scatter_panel_object_list(bpy.types.UIList):
    """UI Scatter List"""

    def draw_item(self, _context, layout, data, item, icon, _active_data, _active_propname, _index, _flt_flag):
        ob = data
        psys = item

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            md = find_modifier(ob, psys)
            row = layout.row(align=True)

            row.prop(psys, "name", text="",
                     emboss=False, icon="STICKY_UVS_LOC")
            if md:
                row.prop(
                    md,
                    "show_viewport",
                    emboss=False,
                    icon_only=True,
                )
                row.prop(
                    md,
                    "show_render",
                    emboss=False,
                    icon_only=True,
                )

        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon="STICKY_UVS_LOC")

    # def draw_item(self, context, layout, data, item, icon, active_data,
     #             active_propname, index):

        #scene = context.scene
        #row = layout.row(align=True)

        # sub=row.row(align=True)
        #sub.scale_x = 2

        #sub.prop(item,"scatter_item",text='', icon="STICKY_UVS_LOC")

        # sub=row.row(align=True)
        #sub.scale_x = 1.1
        #sub.enabled = bool(item.scatter_item)
        #sub.prop(item,"scatter_display",text='', icon='RESTRICT_VIEW_OFF'  if item.scatter_display else'RESTRICT_VIEW_ON')

        # sub=row.row(align=True)
        #sub.scale_x = 0.3
        #sub.prop(item,"name", text="", icon="RADIOBUT_ON", emboss=False)
        # sub.enabled=False

        #sub.prop(item,"proxy_render_frame",text='', icon='RESTRICT_RENDER_OFF'if item.proxy_render_frame else'RESTRICT_RENDER_ON')


# ------------------------------------------------------------------------------
# SCATTER PANEL

class Scatter_Panel (bpy.types.Panel):
    bl_label = "AB Scatter"
    bl_idname = "PT_Scatter_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    def draw(self, context):
        layout = self.layout
        ob = context.object
        scene = context.scene
        mesh = scatter_true_mesh_data(ob)
        Arc_Blend = scene.Arc_Blend
        ui = bpy.ops.ui
        main = layout.column()
        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass

        main.label(text="Scatter Panel : ", icon="STICKY_UVS_LOC")

        # define two rows
        row = main.row()
        col1 = row.column()
        col2 = row.column()

        # draw template
        template = col1.column()
        try:
            template.template_list("scatter_panel_object_list", "particle_systems", ob, "particle_systems",
                                   ob.particle_systems, "active_index", rows=3)
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass
        template.scale_y = 1.1

        # draw side bar
        col2.separator(factor=0)
        #
        add = col2.column(align=True)
        AB_ADD = add.operator(
            "object.particle_system_add", icon='ADD', text="")

        #
        rem = col2.column(align=True)
        AB_REMOVE = rem.operator(
            "object.particle_system_remove", icon='REMOVE', text="")

        col2.column_flow(columns=3, align=True)

        #
        rem = col2.column(align=True)
        rem.operator("object.button_proxy_panel_list_makes_parents",
                     icon='LINKED', text="")

        #
        rem = col2.column(align=True)
        rem.operator("object.button_proxy_panel_list_clear_parents",
                     icon='UNLINKED', text="")

        #
        rem = col2.column(align=True)
        rem.operator("object.button_proxy_panel_list_select_same_collection",
                     icon='OUTLINER_COLLECTION', text="")

        #
        rem = col2.column(align=True)
        rem.operator(
            "object.button_proxy_panel_list_apply_all_modifiers", icon='CHECKMARK', text="")

        col = layout.column()

        col = layout.column()
        col.prop(Arc_Blend, "object_scatter",
                 text="Object Scatter", icon="STICKY_UVS_LOC")
        try:
            if bpy.context.scene.Arc_Blend.object_scatter == True:

                # Emission
                col.prop(part, "count")
                col.prop(psys, "seed")
                col.prop(part, "hair_length", text="Object Lengths")
                # Viewport Display
                col.prop(part, "display_percentage",
                         slider=True, text="Amount")
                col.prop(context.object, "show_instancer_for_viewport",
                         text="Show Instancer", icon="STICKY_UVS_DISABLE")
                col.operator("object.button_scatter_panel_make_real_objects",
                             text="Make Instances Real", icon="OUTLINER_OB_MESH")

        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass


# ------------------------------------------------------------------------------
# ADD OBJECT TO LIST SCATTER


class scatter_panel_make_real_objects (bpy.types.Operator):
    """Make Instances Real"""

    bl_label = ""
    bl_idname = "object.button_scatter_panel_make_real_objects"

    def execute(self, context):
        bpy.ops.object.duplicates_make_real()

        return {'FINISHED'}

# ------------------------------------------------------------------------------
# SCATTER VIEW AS PANEL


class Scatter_Panel_Scatter_As (bpy.types.Panel):
    bl_label = ""
    bl_idname = "PT_Scatter_Panel_Scatter_As"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_Scatter_Panel"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    @classmethod
    def poll(cls, context):
        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass
        return bpy.context.scene.Arc_Blend.object_scatter == True

    def draw_header(self, context):

        layout = self.layout

        layout.label(text="Scatter As", icon="STICKY_UVS_LOC")

    def draw(self, context):
        layout = self.layout
        ob = context.object
        scene = context.scene
        mesh = scatter_true_mesh_data(ob)
        Arc_Blend = scene.Arc_Blend
        ui = bpy.ops.ui
        main = layout.column()
        layout.use_property_split = False

        col = layout.column()

        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active

            if bpy.context.scene.Arc_Blend.object_scatter == True:

                # Render
                col.prop(Arc_Blend, "scatter_view_as", text="Render Type")

                if bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_object' or bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_collection':

                    col = layout.column(align=False)
                    col.prop(part, "particle_size", text="Scale")
                    col.prop(part, "size_random", slider=True,
                             text="Scale Randomness")

                if bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_path':
                    col.prop(part, "material_slot", text="Material")
                    col.prop(psys, "parent", text="Coordinate System")

        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass

# ------------------------------------------------------------------------------
# SCATTER PAINT PANEL


class Scatter_Panel_Paint_Panel (bpy.types.Panel):
    bl_label = ""
    bl_idname = "PT_Scatter_Panel_Paint_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_Scatter_Panel"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    @classmethod
    def poll(cls, context):
        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass
        return bpy.context.scene.Arc_Blend.object_scatter == True

    def draw_header(self, context):

        layout = self.layout

        layout.label(text="Paint Panel", icon="BRUSHES_ALL")

    def draw(self, context):
        layout = self.layout
        ob = context.object
        scene = context.scene
        mesh = scatter_true_mesh_data(ob)
        Arc_Blend = scene.Arc_Blend
        ui = bpy.ops.ui
        #main = layout.column()
        layout.use_property_split = False

        #col = layout.column()
        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active

            layout.prop(Arc_Blend, "object_scatter_paint_panel",
                        text="PAINT", icon="BRUSHES_ALL")
            col = layout.column()
            row = col.row(align=True)
            sub = row.row(align=True)
            sub.use_property_decorate = False
            sub.prop_search(psys, "vertex_group_density", ob,
                            "vertex_groups", text="Density")
            row.prop(psys, "invert_vertex_group_density",
                     text="", toggle=True, icon='ARROW_LEFTRIGHT')

        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass

# ------------------------------------------------------------------------------
# SCATTER ROTATION PANEL


class Scatter_Panel_Rotation_Panel (bpy.types.Panel):
    bl_label = ""
    bl_idname = "PT_Scatter_Panel_Rotation_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_Scatter_Panel"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    @classmethod
    def poll(cls, context):
        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass
        return bpy.context.scene.Arc_Blend.object_scatter == True

    def draw_header(self, context):

        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            psys = bpy.context.object.particle_systems.active

            layout = self.layout

            layout.prop(part, "use_rotations", text="Rotation",
                        icon="ORIENTATION_GIMBAL")

        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass

    def draw(self, context):
        layout = self.layout
        ob = context.object
        scene = context.scene
        mesh = scatter_true_mesh_data(ob)
        Arc_Blend = scene.Arc_Blend
        ui = bpy.ops.ui
        #main = layout.column()
        layout.use_property_split = False

        #col = layout.column()
        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active

            layout.use_property_split = False

            main = layout.column()

            main.prop(part, "rotation_mode")
            row1 = layout.row()
            row1.label(text="Randomize : ")
            row1.scale_x = 2
            row1.prop(part, "rotation_factor_random", slider=True, text="")

            col = layout.column()
            row2 = layout.row()
            row2.label(text="Phase : ")
            row2.scale_x = 2
            row2.prop(part, "phase_factor", slider=True, text="")

            col = layout.column()
            row3 = layout.row()
            row3.label(text="Rndm Phase : ")
            row3.scale_x = 2
            row3.prop(part, "phase_factor_random", text="", slider=True)

            if part.type != 'HAIR':
                col.prop(part, "use_dynamic_rotation")
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass


# ------------------------------------------------------------------------------
# SCATTER OBJECT PANEL

class Scatter_Panel_Object (bpy.types.Panel):
    bl_label = ""
    bl_idname = "PT_Scatter_Panel_Object"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_Scatter_Panel_Scatter_As"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    @classmethod
    def poll(cls, context):
        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass
        return bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_object'

    def draw_header(self, context):

        layout = self.layout

        layout.label(text="Object", icon="OUTLINER_OB_MESH")

    def draw(self, context):
        layout = self.layout
        ob = context.object
        scene = context.scene
        mesh = scatter_true_mesh_data(ob)
        Arc_Blend = scene.Arc_Blend
        ui = bpy.ops.ui
        main = layout.column()
        layout.use_property_split = False

        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active

            if bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_object':

                col = layout.column()

                col.prop(part, "instance_object",
                         text="Instance", icon="STICKY_UVS_LOC")
                sub = col.column()
                sub.prop(part, "use_global_instance",
                         text="Global Coordinates")
                sub.prop(part, "use_rotation_instance", text="Object Rotation")
                sub.prop(part, "use_scale_instance", text="Object Scale")

        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass
# ------------------------------------------------------------------------------
# SCATTER COLLECTION PANEL


class Scatter_Panel_Collection (bpy.types.Panel):
    bl_label = ""
    bl_idname = "PT_Scatter_Panel_Collection"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_Scatter_Panel_Scatter_As"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    @classmethod
    def poll(cls, context):
        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass
        return bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_collection'

    def draw_header(self, context):

        layout = self.layout

        layout.label(text="Collection", icon="OUTLINER_COLLECTION")

    def draw(self, context):
        layout = self.layout
        ob = context.object
        scene = context.scene
        mesh = scatter_true_mesh_data(ob)
        Arc_Blend = scene.Arc_Blend
        ui = bpy.ops.ui
        main = layout.column()
        layout.use_property_split = False

        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active

            col = layout.column()

            if bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_collection':
                col.prop(part, "instance_collection",
                         text="Instance Collection")
                col.prop(part, "use_whole_collection")
                sub = col.column()
                sub.active = (part.use_whole_collection is False)
                sub.prop(part, "use_collection_pick_random")
                sub.prop(part, "use_global_instance",
                         text="Global Coordinates")
                sub.prop(part, "use_rotation_instance", text="Object Rotation")
                sub.prop(part, "use_scale_instance", text="Object Scale")
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass


# ------------------------------------------------------------------------------
# SCATTER COLLECTION USE COUNT PANEL

class Scatter_Panel_Collection_Use_Count (bpy.types.Panel):
    bl_label = ""
    bl_idname = "PT_Scatter_Panel_Collection_Use_Count"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_Scatter_Panel_Collection"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass
        return bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_collection'

    def draw_header(self, context):

        layout = self.layout

        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active

            part = bpy.context.object.particle_systems.data.particle_systems.active.settings

            layout.active = not part.use_whole_collection

            layout.prop(part, "use_collection_count",
                        text="Proportion (Elements)", icon="OUTLINER_COLLECTION")
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass

    def draw(self, context):
        layout = self.layout
        ob = context.object
        scene = context.scene
        mesh = scatter_true_mesh_data(ob)
        Arc_Blend = scene.Arc_Blend
        ui = bpy.ops.ui
        main = layout.column()
        layout.use_property_split = False

        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass

        col = layout.column()

        try:
            layout.active = part.use_collection_count and not part.use_whole_collection

            row = layout.row()
            row.template_list("UI_UL_list", "particle_instance_weights", part, "instance_weights",
                              part, "active_instanceweight_index")

            col = row.column()
            sub = col.row()
            subsub = sub.column(align=True)
            subsub.operator("particle.dupliob_copy", icon='ADD', text="")
            subsub.operator("particle.dupliob_remove", icon='REMOVE', text="")
            subsub.operator("particle.dupliob_move_up",
                            icon='TRIA_UP', text="")
            subsub.operator("particle.dupliob_move_down",
                            icon='TRIA_DOWN', text="")
            subsub.separator()
            subsub.operator("particle.dupliob_refresh",
                            icon='FILE_REFRESH', text="")

            weight = part.active_instanceweight
            if weight:
                row = layout.row()
                row.prop(weight, "count")
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass


# ------------------------------------------------------------------------------
# SCATTER EXTRA PANEL

class Scatter_Panel_Extra (bpy.types.Panel):
    bl_label = ""
    bl_idname = "PT_Scatter_Panel_Extra"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_Scatter_Panel_Scatter_As"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    @classmethod
    def poll(cls, context):
        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass
        return bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_object' or bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_collection'

    def draw_header(self, context):

        layout = self.layout

        layout.label(text="Extra", icon="SETTINGS")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False

        col = layout.column()
        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active

            if bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_object' or bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_collection':

                col.prop(part, "use_parent_particles", text="Parent Particles")
                col.prop(part, "show_unborn", text="Unborn")
                col.prop(part, "use_dead", text="Dead")

        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass

# ------------------------------------------------------------------------------
# ADD OBJECT TO LIST SCATTER


class scatter_panel_add_objects (bpy.types.Operator):
    """Add a new item to the list"""

    bl_label = ""
    bl_idname = "object.button_scatter_panel_add_objects"

    add: bpy.props.StringProperty()
    scatter_mesh_name: bpy.props.StringProperty()

    def execute(self, context):
        try:
            mesh = bpy.data.meshes[self.scatter_mesh_name]
            index = mesh.scatter_list_index

            if self.add == 'ADD':

                item = mesh.scatter_mesh_list.add()

                item.name = mesh.name

                item.scatter_ui_index = len(mesh.scatter_mesh_list)

                mesh.scatter_list_index = len(mesh.scatter_mesh_list)-1

                scatter_fill_original_pointer(mesh)

        except (AttributeError, KeyError):
            pass

        return {'FINISHED'}
# ------------------------------------------------------------------------------
# DELETE OBJECT FROM LIST


class scatter_panel_remove_objects (bpy.types.Operator):
    """Remove item from the list"""

    bl_label = ""
    bl_idname = "object.button_scatter_panel_remove_objects"

    remove: bpy.props.StringProperty()
    scatter_mesh_name: bpy.props.StringProperty()

    def execute(self, context):
        try:
            mesh = bpy.data.meshes[self.scatter_mesh_name]
            index = mesh.scatter_list_index
            if self.remove == 'REMOVE':
                mesh.scatter_list_index -= 1
                mesh.scatter_mesh_list.remove(index)
                scatter_clean_original_pointer()
                # maybe user deleted active boolean
        except (AttributeError, KeyError):
            pass

        return {'FINISHED'}

# ------------------------------------------------------------------------------
# DEFINES


def scatter_find_instances(scatter_mesh_data):
    """Finds the instances"""
    r = []
    for o in bpy.data.objects:
        if (o.type == 'MESH'):
            if scatter_true_mesh_data(o) == scatter_mesh_data:
                r.append(o)
    return r


def scatter_fill_original_pointer(scatter_mesh_data):
    """Pointer filled first active object"""

    for ob in scatter_find_instances(scatter_mesh_data):
        # if ui list not empty but pointer is -> fill pointer
        if (len(ob.data.scatter_mesh_list) > 0) and (not ob.scatter_item_obj):
            ob.scatter_item_obj = scatter_mesh_data
    return None


def scatter_clean_original_pointer():
    """Clean original pointer"""

    for ob in bpy.data.objects:
        if ob.type == 'MESH':
            # if ui list empty but pointer original full -> restore and clean
            if (ob.scatter_item_obj) and (len(ob.scatter_item_obj.scatter_mesh_list) == 0):
                if ob.data != ob.scatter_item_obj:
                    ob.data = ob.scatter_item_obj
                ob.scatter_item_obj = None
    return None


def scatter_true_mesh_data(obj):
    """Original Mesh Data"""
    try:
        if obj.scatter_item_obj:
            return obj.scatter_item_obj
        else:
            return obj.data
    except AttributeError:
        pass


def scatter_return_one_time(mesh, active_idx, prop_api):
    """Returning once per elements"""
    AB_list = mesh.scatter_mesh_list
    for i in AB_list:
        if i.scatter_ui_index != active_idx:
            exec(f"i.{prop_api}= False")
    return None


def scatter_item_upd(self, context):
    if not self.scatter_item:
        self.scatter_render_frame = self.scatter_display = False
    return None


def scatter_display_upd(self, context):
    if self.scatter_display == True:
        scatter_return_one_time(
            self.id_data, self.scatter_ui_index, "scatter_display")
    bpy.data.particles["AB_Scatter"].type = 'HAIR'
    bpy.data.particles["AB_Scatter"].render_type = 'OBJECT'
    bpy.data.particles["AB_Scatter"].instance_object = bpy.data.objects["Cube"]

    return None

# ------------------------------------------------------------------------------
# SCATTER PROPERTY GROUP


class scatter_panel_list_item(bpy.types.PropertyGroup):
    id: bpy.props.IntProperty()
    object: bpy.props.PointerProperty(
        name="Object",
        type=bpy.types.Object,)

    # Name of the items in the list
    name: bpy.props.StringProperty(description="Object Name")
    # Random props in the lists
    scatter_ui_index: bpy.props.IntProperty(description='UI List Index')
    scatter_item: bpy.props.PointerProperty(
        type=bpy.types.Mesh, description='Mesh Name', update=scatter_item_upd)
    scatter_display: bpy.props.BoolProperty(
        default=False, description="Display in Viewport", update=scatter_display_upd)

    def copy(self):
        self.object = self.id_data.copy()
        self.name = self.object.name
        return self.object

    def add(self, ob):
        self.object = ob
        self.name = ob.name
        return self.object

# ------------------------------------------------------------------------------
# CAMERA PANEL

class Camera_Panel (bpy.types.Panel):
    bl_label = "AB Camera"
    bl_idname = "PT_Camera_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    
    

    def draw(self, context):
        layout = self.layout
        ob = context.object
        scene = context.scene
        cam = context.scene.camera

        
        col = layout.column()
        row = layout.row()
        
        col.label(text="Camera Panel :" , icon="CAMERA_DATA")
        col.operator("object.button_camera_panel_add_camera_view", text="Add Camera to View", icon="OUTLINER_OB_CAMERA")
        
        # draw template
        col1 = row.column()
        col2 = row.column()
        template = col1
        template.template_list("camera_panel_list", "camera_list", scene, "camera_list",
                                   scene, "camera_list_index", rows=3)
        
        template.scale_y = 1.1
        

        # draw side bar
        col.separator(factor=0)
        #
        add = col2.column(align=True)
        AB_ADD = add.operator(
            "object.button_camera_panel_add_camera", icon='ADD', text="")
        AB_ADD.add = "ADD"
        try:
            AB_ADD.camera_name = cam.name
        except AttributeError:
            pass


        #
        rem = col2.column(align=True)
        AB_REMOVE = rem.operator(
            "object.button_camera_panel_remove_camera", icon='REMOVE', text="")
        AB_REMOVE.rem = "REMOVE"
        try:
            AB_REMOVE.camera_name = cam.name
        except AttributeError:
            pass

        col.column_flow(columns=3, align=True)

        

# ------------------------------------------------------------------------------
# ADD CAMERA TO VIEW OPERATOR

class camera_panel_add_camera_view (bpy.types.Operator):
    bl_label = "Add Camera"
    bl_idname = "object.button_camera_panel_add_camera_view"
 

    def execute(self, context):
        
        bpy.context.scene.camera = None
        #bpy.ops.object.camera_add()
        bpy.ops.object.camera_add()
        bpy.context.object.data.name = bpy.context.object.name

        #for i in bpy.context.view_layer.objects:
        #    if i.type=="CAMERA":
        #        print(i)

        bpy.ops.view3d.camera_to_view()
        bpy.context.scene.camera = None
        bpy.ops.view3d.object_as_camera()

        return {'FINISHED'}

# ------------------------------------------------------------------------------
# CAMERA LIST


class camera_panel_list(bpy.types.UIList):
    """UI Camera List"""

    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_propname, index):

        scene = context.scene
        row = layout.row(align=True)

        sub = row.row(align=True)
        sub.scale_x = 2

        sub.prop(item, "camera_item", text='', icon="OUTLINER_OB_CAMERA")

        sub = row.row(align=True)
        sub.scale_x = 1.1
        sub.enabled = bool(item.camera_item)
        sub.prop(item, "camera_display", text='',
                 icon='RESTRICT_VIEW_OFF' if item.camera_display else 'RESTRICT_VIEW_ON')
        
        
        
        sub.operator("object.button_lock_camera_to_object", icon="VIEWZOOM")
        
        
        
        sub = row.row(align=True)
        sub.scale_x = 0.3
        sub.prop(item, "name", text="", icon="LAYER_ACTIVE", emboss=False)
        sub.enabled = False

        #sub.prop(item,"proxy_render_frame",text='', icon='RESTRICT_RENDER_OFF'if item.proxy_render_frame else'RESTRICT_RENDER_ON')


# ------------------------------------------------------------------------------
# ADD CAMERA TO LIST


class camera_panel_add_camera (bpy.types.Operator):
    """Add a new item to the list"""

    bl_label = ""
    bl_idname = "object.button_camera_panel_add_camera"
    
    add: bpy.props.StringProperty()
    camera_name: bpy.props.StringProperty()

    def execute(self, context):
        scene = bpy.context.scene
 
        camera =  bpy.data.objects[self.camera_name]
        index = scene.camera_list_index
        
        item = scene.camera_list.add()

        item.name = camera.name

        item.camera_ui_index = len(scene.camera_list)

        scene.camera_list_index = len(scene.camera_list) - 1


        return {'FINISHED'}
# ------------------------------------------------------------------------------
# DELETE OBJECT FROM LIST


class camera_panel_remove_camera (bpy.types.Operator):
    """Remove item from the list"""

    bl_label = ""
    bl_idname = "object.button_camera_panel_remove_camera"

    rem: bpy.props.StringProperty()
    camera_name: bpy.props.StringProperty()

    def execute(self, context):
        scene = bpy.context.scene

        camera = bpy.data.objects[self.camera_name]
        index = scene.camera_list_index

        scene.camera_list_index -= 1
        scene.camera_list.remove(index)
 
        return {'FINISHED'}
# ------------------------------------------------------------------------------
# DEF CAMERA
def camera_return_one_time(mesh, active_idx, prop_api):
    """Returning once per elements"""
    scene= bpy.context.scene
    AB_list = scene.camera_list
    for i in AB_list:
        if i.camera_ui_index != active_idx:
            exec(f"i.{prop_api}= False")
    return None


def camera_display_upd(self, context):
    
    if self.camera_display == True:
        camera_return_one_time(self.id_data, self.camera_ui_index, "camera_display")
        len_cam=len(bpy.context.scene.camera_list)
        for i in range(0,len_cam):
            a = bpy.context.scene.camera_list[i].camera_item.name
            b = bpy.context.scene.camera_list[i].camera_display
            if b == True:
                bpy.context.active_object.select_set(False)
                bpy.context.scene.camera = bpy.data.objects[a]
                bpy.context.view_layer.objects.active = bpy.data.objects[a]
                bpy.context.object.select_set(True)

                try:
                    if bpy.context.active_object.type== 'CAMERA':
                        for area in bpy.context.screen.areas:
                            if area.type == 'VIEW_3D':
                                area.spaces[0].region_3d.view_perspective = 'CAMERA'
                                break
                except AttributeError:
                    pass
                    #try:
                        #bpy.ops.view3d.camera_to_view()
                    #except RuntimeError:
                    #    pass
                else:
                    pass
                #bpy.ops.view3d.object_as_camera()
            #if i.['camera_display'] == 1:

# ------------------------------------------------------------------------------
# Lock camera


class lock_camera_to_object(bpy.types.Operator):
    """Lock the Camera to the Selected Objects!"""

    bl_label = ""
    bl_idname = "object.button_lock_camera_to_object"

    def execute(self, context):
        
        bpy.context.space_data.lock_camera = True
        bpy.ops.view3d.camera_to_view_selected()
        bpy.context.space_data.lock_camera = False

        return {"FINISHED"}


# ------------------------------------------------------------------------------
# CAMERA PROPERTY GROUP


class camera_panel_list_item(bpy.types.PropertyGroup):
    id: bpy.props.IntProperty()
    camera: bpy.props.PointerProperty(name="Camera",type=bpy.types.Camera)

    # Name of the items in the list
    name: bpy.props.StringProperty(description="Object Name")
    # Random props in the lists
    camera_ui_index: bpy.props.IntProperty(description='UI List Index')
    camera_item: bpy.props.PointerProperty(type=bpy.types.Camera, description='Camera Name')
    camera_display: bpy.props.BoolProperty(default=False, description="Display in Viewport", update=camera_display_upd)
    
   

    def copy(self):
        self.camera = self.id_data.copy()
        self.name = self.camera.name
        return self.camera

    def add(self, cam):
        self.camera = cam
        self.name = cam.name
        return self.camera
# ------------------------------------------------------------------------------
# VIEW LOCK

class data_context_camera_lock(Panel):
    bl_label = "View Lock"
    bl_idname = "data_context_camera_lock"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_Camera_Panel"
   
    
    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        view = context.space_data

        col = layout.column(align=True)
        sub = col.column()
        sub.active = bool(view.region_3d.view_perspective != 'CAMERA' or view.region_quadviews)

        sub.prop(view, "lock_object")
        lock_object = view.lock_object
        if lock_object:
            if lock_object.type == 'ARMATURE':
                sub.prop_search(
                    view, "lock_bone", lock_object.data,
                    "edit_bones" if lock_object.mode == 'EDIT'
                    else "bones",
                    text="Bone",
                )

        col = layout.column(heading="Lock", align=True)
        if not lock_object:
            col.prop(view, "lock_cursor", text="To 3D Cursor")
        col.prop(view, "lock_camera", text="Camera to View")
# ------------------------------------------------------------------------------
# CAMERA AREA

class data_context_camera(bpy.types.Panel):
    bl_label = "Camera Settings"
    bl_idname = "data_context_camera"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "PT_Camera_Panel"
   
        
    def draw(self, context):
        layout = self.layout

    

# ------------------------------------------------------------------------------
# CAMERA LENS

class data_context_camera_lens(bpy.types.Panel):
    bl_label = "Lens"
    bl_idname = "data_context_camera_lens"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "data_context_camera"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    
   
   
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        try:
            cam = context.scene.camera.data
            layout.prop(cam, "type")
            col = layout.column()
            col.separator()

            if cam.type == 'PERSP':
                if cam.lens_unit == 'MILLIMETERS':
                    col.prop(cam, "lens")
                elif cam.lens_unit == 'FOV':
                    col.prop(cam, "angle")
                col.prop(cam, "lens_unit")

            elif cam.type == 'ORTHO':
                col.prop(cam, "ortho_scale")

            elif cam.type == 'PANO':
                engine = context.engine
                if engine == 'CYCLES':
                    ccam = cam.cycles
                    col.prop(ccam, "panorama_type")
                    if ccam.panorama_type == 'FISHEYE_EQUIDISTANT':
                        col.prop(ccam, "fisheye_fov")
                    elif ccam.panorama_type == 'FISHEYE_EQUISOLID':
                        col.prop(ccam, "fisheye_lens", text="Lens")
                        col.prop(ccam, "fisheye_fov")
                    elif ccam.panorama_type == 'EQUIRECTANGULAR':
                        sub = col.column(align=True)
                        sub.prop(ccam, "latitude_min", text="Latitude Min")
                        sub.prop(ccam, "latitude_max", text="Max")
                        sub = col.column(align=True)
                        sub.prop(ccam, "longitude_min", text="Longitude Min")
                        sub.prop(ccam, "longitude_max", text="Max")
                    elif ccam.panorama_type == 'FISHEYE_LENS_POLYNOMIAL':
                        col.prop(ccam, "fisheye_fov")
                        col.prop(ccam, "fisheye_polynomial_k0", text="K0")
                        col.prop(ccam, "fisheye_polynomial_k1", text="K1")
                        col.prop(ccam, "fisheye_polynomial_k2", text="K2")
                        col.prop(ccam, "fisheye_polynomial_k3", text="K3")
                        col.prop(ccam, "fisheye_polynomial_k4", text="K4")

                elif engine in {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}:
                    if cam.lens_unit == 'MILLIMETERS':
                        col.prop(cam, "lens")
                    elif cam.lens_unit == 'FOV':
                        col.prop(cam, "angle")
                    col.prop(cam, "lens_unit")

            col = layout.column()
            col.separator()

            sub = col.column(align=True)
            sub.prop(cam, "shift_x", text="Shift X")
            sub.prop(cam, "shift_y", text="Y")

            col.separator()
            sub = col.column(align=True)
            sub.prop(cam, "clip_start", text="Clip Start")
            sub.prop(cam, "clip_end", text="End")
        except AttributeError:
            pass
# ------------------------------------------------------------------------------
# CAMERA DOF

class data_context_camera_dof(bpy.types.Panel):
    bl_label = "Depth of Field"
    bl_idname = "data_context_camera_dof"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "data_context_camera"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    def draw_header(self, context):
        cam = context.scene.camera.data
        dof = cam.dof
        self.layout.prop(dof, "use_dof", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        cam = context.scene.camera.data
        dof = cam.dof
        layout.active = dof.use_dof

        col = layout.column()
        col.prop(dof, "focus_object", text="Focus on Object")
        sub = col.column()
        sub.active = (dof.focus_object is None)
        sub.prop(dof, "focus_distance", text="Focus Distance")
# ------------------------------------------------------------------------------
# CAMERA DOF APERTURE

class data_context_camera_dof_aperture(bpy.types.Panel):
    bl_label = "Aperture"
    bl_idname = "data_context_camera_dof_aperture"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "data_context_camera_dof"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    
    

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        cam = context.scene.camera.data
        dof = cam.dof
        layout.active = dof.use_dof

        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)

        col = flow.column()
        col.prop(dof, "aperture_fstop")

        col = flow.column()
        col.prop(dof, "aperture_blades")
        col.prop(dof, "aperture_rotation")
        col.prop(dof, "aperture_ratio")
        


# ------------------------------------------------------------------------------
# CAMERA 


class CAMERA_PT_presets(PresetPanel, Panel):
    bl_label = "Camera Presets"
    preset_subdir = "camera"
    preset_operator = "script.execute_preset"
    preset_add_operator = "camera.preset_add"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    
class data_context_camera_camera(bpy.types.Panel):
    bl_label = "Camera"
    bl_idname = "data_context_camera_camera"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "data_context_camera"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    def draw_header_preset(self, _context):
        CAMERA_PT_presets.draw_panel_header(self.layout)
        

    def draw(self, context):
        layout = self.layout

        cam = context.scene.camera.data

        layout.use_property_split = True

        col = layout.column()
        col.prop(cam, "sensor_fit")

        if cam.sensor_fit == 'AUTO':
            col.prop(cam, "sensor_width", text="Size")
        else:
            sub = col.column(align=True)
            sub.active = cam.sensor_fit == 'HORIZONTAL'
            sub.prop(cam, "sensor_width", text="Width")

            sub = col.column(align=True)
            sub.active = cam.sensor_fit == 'VERTICAL'
            sub.prop(cam, "sensor_height", text="Height")       
 
# ------------------------------------------------------------------------------
# SAFE AREAS
class SAFE_AREAS_PT_presets(PresetPanel, Panel):
    bl_label = "Camera Presets"
    preset_subdir = "safe_areas"
    preset_operator = "script.execute_preset"
    preset_add_operator = "safe_areas.preset_add"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

class data_context_camera_safe_areas(bpy.types.Panel):
    bl_label = "Safe Areas"
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "data_context_camera"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    def draw_header(self, context):
        cam = context.scene.camera.data

        self.layout.prop(cam, "show_safe_areas", text="")

    def draw_header_preset(self, _context):
        SAFE_AREAS_PT_presets.draw_panel_header(self.layout)

    def draw(self, context):
        layout = self.layout
        safe_data = context.scene.safe_areas
        camera = context.scene.camera.data

        layout.use_property_split = True

        layout.active = camera.show_safe_areas

        col = layout.column()

        sub = col.column()
        sub.prop(safe_data, "title", slider=True)
        sub.prop(safe_data, "action", slider=True)


class data_context_camera_safe_areas_center_cut(bpy.types.Panel):
    bl_label = "Center-Cut Safe Areas"
    bl_parent_id = "data_context_camera_safe_areas"
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    def draw_header(self, context):
        cam = context.scene.camera.data

        layout = self.layout
        layout.active = cam.show_safe_areas
        layout.prop(cam, "show_safe_center", text="")

    def draw(self, context):
        layout = self.layout
        safe_data = context.scene.safe_areas
        camera = context.scene.camera.data

        layout.use_property_split = True

        layout.active = camera.show_safe_areas and camera.show_safe_center

        col = layout.column()
        col.prop(safe_data, "title_center", slider=True)
        col.prop(safe_data, "action_center", slider=True)
        
# ------------------------------------------------------------------------------
# SAFE AREAS        
        
class data_context_camera_background_image(bpy.types.Panel):
    bl_label = "Background Images"
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "data_context_camera"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    def draw_header(self, context):
        cam = context.scene.camera.data

        self.layout.prop(cam, "show_background_images", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        cam = context.scene.camera.data
        use_multiview = context.scene.render.use_multiview

        col = layout.column()
        col.operator("view3d.background_image_add", text="Add Image")

        for i, bg in enumerate(cam.background_images):
            layout.active = cam.show_background_images
            box = layout.box()
            row = box.row(align=True)
            row.prop(bg, "show_expanded", text="", emboss=False)
            if bg.source == 'IMAGE' and bg.image:
                row.prop(bg.image, "name", text="", emboss=False)
            elif bg.source == 'MOVIE_CLIP' and bg.clip:
                row.prop(bg.clip, "name", text="", emboss=False)
            elif bg.source and bg.use_camera_clip:
                row.label(text="Active Clip")
            else:
                row.label(text="Not Set")

            row.prop(
                bg,
                "show_background_image",
                text="",
                emboss=False,
                icon='RESTRICT_VIEW_OFF' if bg.show_background_image else 'RESTRICT_VIEW_ON',
            )

            row.operator("view3d.background_image_remove", text="", emboss=False, icon='X').index = i

            if bg.show_expanded:
                row = box.row()
                row.prop(bg, "source", expand=True)

                has_bg = False
                if bg.source == 'IMAGE':
                    row = box.row()
                    row.template_ID(bg, "image", open="image.open")
                    if bg.image is not None:
                        box.template_image(bg, "image", bg.image_user, compact=True)
                        has_bg = True

                        if use_multiview:
                            box.prop(bg.image, "use_multiview")

                            column = box.column()
                            column.active = bg.image.use_multiview

                            column.label(text="Views Format:")
                            column.row().prop(bg.image, "views_format", expand=True)

                            sub = column.box()
                            sub.active = bg.image.views_format == 'STEREO_3D'
                            sub.template_image_stereo_3d(bg.image.stereo_3d_format)

                elif bg.source == 'MOVIE_CLIP':
                    box.prop(bg, "use_camera_clip", text="Active Clip")

                    column = box.column()
                    column.active = not bg.use_camera_clip
                    column.template_ID(bg, "clip", open="clip.open")

                    if bg.clip:
                        column.template_movieclip(bg, "clip", compact=True)

                    if bg.use_camera_clip or bg.clip:
                        has_bg = True

                    column = box.column()
                    column.active = has_bg
                    column.prop(bg.clip_user, "use_render_undistorted")
                    column.prop(bg.clip_user, "proxy_render_size")

                if has_bg:
                    col = box.column()
                    col.prop(bg, "alpha", slider=True)
                    col.row().prop(bg, "display_depth", expand=True)

                    col.row().prop(bg, "frame_method", expand=True)

                    row = box.row()
                    row.prop(bg, "offset")

                    col = box.column()
                    col.prop(bg, "rotation")
                    col.prop(bg, "scale")

                    col = box.column(heading="Flip")
                    col.prop(bg, "use_flip_x", text="X")
                    col.prop(bg, "use_flip_y", text="Y")


# ------------------------------------------------------------------------------
# VIEWPORT DISPLAY



class data_context_camera_display(bpy.types.Panel):
    bl_label = "Viewport Display"
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "data_context_camera"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        cam = context.scene.camera.data

        col = layout.column(align=True)

        col.prop(cam, "display_size", text="Size")

        col = layout.column(heading="Show")
        col.prop(cam, "show_limits", text="Limits")
        col.prop(cam, "show_mist", text="Mist")
        col.prop(cam, "show_sensor", text="Sensor")
        col.prop(cam, "show_name", text="Name")

        col = layout.column(align=False, heading="Passepartout")
        col.use_property_decorate = False
        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(cam, "show_passepartout", text="")
        sub = sub.row(align=True)
        sub.active = cam.show_passepartout
        sub.prop(cam, "passepartout_alpha", text="")
        row.prop_decorator(cam, "passepartout_alpha")


class data_context_camera_display_composition_guides(bpy.types.Panel):
    bl_label = "Composition Guides"
    bl_parent_id = "data_context_camera_display"
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        cam = context.scene.camera.data

        layout.prop(cam, "show_composition_thirds")

        col = layout.column(heading="Center", align=True)
        col.prop(cam, "show_composition_center")
        col.prop(cam, "show_composition_center_diagonal", text="Diagonal")

        col = layout.column(heading="Golden", align=True)
        col.prop(cam, "show_composition_golden", text="Ratio")
        col.prop(cam, "show_composition_golden_tria_a", text="Triangle A")
        col.prop(cam, "show_composition_golden_tria_b", text="Triangle B")

        col = layout.column(heading="Harmony", align=True)
        col.prop(cam, "show_composition_harmony_tri_a", text="Triangle A")
        col.prop(cam, "show_composition_harmony_tri_b", text="Triangle B")

# ------------------------------------------------------------------------------
# REGISTERATION AREA


def register():
    bpy.utils.register_class(arcblend)
    bpy.utils.register_class(Add_Mesh)
    bpy.utils.register_class(Add_Curve)
    bpy.utils.register_class(Add_Surface)
    bpy.utils.register_class(Add_Metaball)
    bpy.utils.register_class(Add_Text)
    bpy.utils.register_class(Add_Volume)
    bpy.utils.register_class(Add_Grease_Pencil)
    bpy.utils.register_class(Add_Armature)
    bpy.utils.register_class(Add_Lattice)
    bpy.utils.register_class(Add_Empty)
    bpy.utils.register_class(Add_Image)
    bpy.utils.register_class(Add_Light)
    bpy.utils.register_class(Add_Light_Probe)
    bpy.utils.register_class(Add_Camera)
    bpy.utils.register_class(Add_Speaker)
    bpy.utils.register_class(Add_Force_Field)
    bpy.utils.register_class(Add_Collection_instance)
    bpy.utils.register_class(ArcBlendModifiers)
    bpy.utils.register_class(modifier)
    bpy.utils.register_class(transform_edit_object_panel)
    bpy.utils.register_class(transform_edit_object_align_x)
    bpy.utils.register_class(transform_edit_object_align_y)
    bpy.utils.register_class(transform_edit_object_align_z)
    bpy.utils.register_class(transform_edit_object_align_bound)
    bpy.utils.register_class(transform_edit_object_purge)
    bpy.utils.register_class(transform)
    bpy.utils.register_class(modifier_panel)
    bpy.utils.register_class(modify_panel)
    bpy.utils.register_class(array_panel)
    bpy.utils.register_class(modifier_array)
    bpy.utils.register_class(modifier_array_detail)
    bpy.utils.register_class(modifier_array_detail_executer)
    bpy.utils.register_class(modifier_array_apply)
    bpy.utils.register_class(Relative_Offset)
    bpy.types.Scene.Arc_Blend = bpy.props.PointerProperty(
        type=modifier_array_detail)
    bpy.utils.register_class(bevel_panel)
    bpy.utils.register_class(modifier_bevel_button)
    bpy.utils.register_class(modifier_bevel_v_button)
    bpy.utils.register_class(modifier_bevel_e_button)
    bpy.utils.register_class(modifier_bevel_detail)
    bpy.utils.register_class(modifier_bevel_detail_executer)
    bpy.utils.register_class(modifier_bevel_apply)
    bpy.types.Scene.AB_Bevel = bpy.props.PointerProperty(
        type=modifier_bevel_detail)
    bpy.utils.register_class(generate_panel)
    bpy.utils.register_class(deform_panel)
    bpy.utils.register_class(physics_panel)
    bpy.utils.register_class(display_panel)
    bpy.utils.register_class(Loop_Menu)
    bpy.utils.register_class(loop_multiple_select)
    bpy.utils.register_class(loop_multiple_select_ring)
    bpy.utils.register_class(loop_select)
    bpy.utils.register_class(loop_select_boundry_faces)
    bpy.utils.register_class(loop_mesh_seperate)
    bpy.utils.register_class(loop_mesh_shortest_path_pick)
    bpy.utils.register_class(loop_mesh_split)
    bpy.utils.register_class(modelling_edit_clean_mesh)
    bpy.utils.register_class(loop_mesh_tris_convert_to_quads)
    bpy.utils.register_class(loop_mesh_quads_convert_to_tris)
    bpy.utils.register_class(loop_mesh_find_trios)
    bpy.utils.register_class(loop_mesh_find_quads)
    bpy.utils.register_class(loop_sde)
    bpy.utils.register_class(loop_idtm)
    bpy.utils.register_class(mball_ball)
    bpy.utils.register_class(mball_capsule)
    bpy.utils.register_class(mball_plane)
    bpy.utils.register_class(mball_ellipsoid)
    bpy.utils.register_class(mball_cube)
    bpy.utils.register_class(grease_pencil_blank)
    bpy.utils.register_class(grease_pencil_stroke)
    bpy.utils.register_class(grease_pencil_monkey)
    bpy.utils.register_class(grease_pencil_sla)
    bpy.utils.register_class(grease_pencil_cla)
    bpy.utils.register_class(grease_pencil_ola)
    bpy.utils.register_class(lattice_button)
    bpy.utils.register_class(empty_plain_axes)
    bpy.utils.register_class(empty_arrows)
    bpy.utils.register_class(empty_single_arrow)
    bpy.utils.register_class(empty_circle)
    bpy.utils.register_class(empty_cube)
    bpy.utils.register_class(empty_sphere)
    bpy.utils.register_class(empty_cone)
    bpy.utils.register_class(empty_image)
    bpy.utils.register_class(light_point)
    bpy.utils.register_class(light_sun)
    bpy.utils.register_class(light_spot)
    bpy.utils.register_class(light_area)
    bpy.utils.register_class(light_probe_cubemap)
    bpy.utils.register_class(light_probe_reflectionplane)
    bpy.utils.register_class(light_probe_irradiencevolume)
    bpy.utils.register_class(camera_normal)
    bpy.utils.register_class(speaker_button)
    bpy.utils.register_class(forcefield_force)
    bpy.utils.register_class(forcefield_wind)
    bpy.utils.register_class(forcefield_vortex)
    bpy.utils.register_class(forcefield_magnetic)
    bpy.utils.register_class(forcefield_harmonic)
    bpy.utils.register_class(forcefield_charge)
    bpy.utils.register_class(forcefield_lennardj)
    bpy.utils.register_class(forcefield_texture)
    bpy.utils.register_class(forcefield_curveguide)
    bpy.utils.register_class(forcefield_boid)
    bpy.utils.register_class(forcefield_turbulance)
    bpy.utils.register_class(forcefield_drag)
    bpy.utils.register_class(forcefield_fluidflow)
    bpy.utils.register_class(collection_instance_collection)
    bpy.utils.register_class(edit_mode_vertex)
    bpy.utils.register_class(edit_mode_add_vertex)
    bpy.utils.register_class(edit_mode_bridge_vertices)
    bpy.utils.register_class(edit_mode_delete_vertices)
    bpy.utils.register_class(edit_mode_just_vertices)
    bpy.utils.register_class(edit_mode_just_edges)
    bpy.utils.register_class(edit_mode_create_faces)
    bpy.utils.register_class(transform_edit_object_randomize_colors)
    bpy.utils.register_class(transform_edit_object_reset_colors)
    bpy.utils.register_class(display_panel_show_xray)
    bpy.utils.register_class(display_panel_show_wireframe)
    bpy.utils.register_class(display_panel_show_solid)
    bpy.utils.register_class(display_panel_show_material)
    bpy.utils.register_class(display_panel_show_rendered)
    bpy.utils.register_class(Themes_Panel)
    bpy.utils.register_class(themes_panel_mak)
    bpy.utils.register_class(themes_panel_white_chalk)
    bpy.utils.register_class(themes_panel_reset)
    bpy.utils.register_class(Modelling_Panel)
    bpy.utils.register_class(cutter_box)
    bpy.utils.register_class(cutter_box_object)
    
    bpy.utils.register_class(cutter_apply_modifier)
    
    
    
    
    
    bpy.utils.register_class(view_3d_top)
    bpy.utils.register_class(view_3d_bottom)
    bpy.utils.register_class(view_3d_front)
    bpy.utils.register_class(view_3d_back)
    bpy.utils.register_class(view_3d_right)
    bpy.utils.register_class(view_3d_left)
    
    
    bpy.utils.register_class(Modelling_Panel_Vertex_Selection)
    bpy.utils.register_class(vertex_selection_make_circle)
    bpy.utils.register_class(vertex_selection_rip_vertex)
    bpy.utils.register_class(vertex_selection_merge_vertex_last)
    bpy.utils.register_class(vertex_selection_dissolve_vertex)
    bpy.utils.register_class(vertex_selection_connect_vertex_path)
    bpy.utils.register_class(vertex_selection_create_vertices)
    bpy.utils.register_class(vertex_selection_assign_vertex_group)
    bpy.utils.register_class(Modelling_Panel_Vertex_Group_Panel)
    bpy.utils.register_class(Modelling_Panel_Modify_Selection)
    bpy.utils.register_class(loop_grow_edge_select)
    bpy.utils.register_class(loop_shrink_edge_select)
    bpy.utils.register_class(loop_auto_edge_loop)
    bpy.utils.register_class(Modelling_Panel_Modify_Edit_Faces)
    bpy.utils.register_class(modelling_edit_faces_flip_normals)
    bpy.utils.register_class(modelling_edit_faces_recalculate_outside)
    bpy.utils.register_class(modelling_edit_faces_extrude)
    bpy.utils.register_class(modelling_edit_faces_inset)
    bpy.utils.register_class(modelling_edit_faces_extrude_normals)
    bpy.utils.register_class(modelling_edit_faces_extrude_individual)
    bpy.utils.register_class(modelling_edit_faces_poke)
    bpy.utils.register_class(modelling_edit_faces_triangulate)
    bpy.utils.register_class(modelling_edit_faces_tris_to_quads)
    bpy.utils.register_class(modelling_edit_faces_solidify)
    bpy.utils.register_class(modelling_edit_faces_wireframe)
    bpy.utils.register_class(modelling_edit_edges_connect)
    bpy.utils.register_class(modelling_edit_edges_extrude)
    bpy.utils.register_class(modelling_edit_edges_collapse)
    bpy.utils.register_class(Modelling_Panel_Modify_Edit)
    bpy.utils.register_class(modelling_edit_loop_cut)
    bpy.utils.register_class(modelling_edit_rotate_edges)
    bpy.utils.register_class(modelling_edit_offset_edge_loop_cut)
    bpy.utils.register_class(modelling_edit_knife_cut)
    bpy.utils.register_class(modelling_edit_knife_bisect)
    bpy.utils.register_class(modelling_edit_x_mirror)
    bpy.utils.register_class(modelling_edit_x_mirror_minus)
    bpy.utils.register_class(modelling_edit_y_mirror)
    bpy.utils.register_class(modelling_edit_y_mirror_minus)
    bpy.utils.register_class(modelling_edit_z_mirror)
    bpy.utils.register_class(modelling_edit_z_mirror_minus)
    bpy.utils.register_class(modelling_edit_fill_sides)
    bpy.utils.register_class(modelling_edit_hide_unselected)
    bpy.utils.register_class(modelling_edit_hide_selected)
    bpy.utils.register_class(modelling_edit_reveal)
    bpy.utils.register_class(modelling_edit_orient_x)
    bpy.utils.register_class(modelling_edit_orient_y)
    bpy.utils.register_class(modelling_edit_orient_z)
    bpy.utils.register_class(Proxy_Panel)
    bpy.utils.register_class(proxy_panel_remeshx_result)
    bpy.utils.register_class(proxy_panel_convertto_point_cloud)
    bpy.utils.register_class(proxy_panel_object_list)
    bpy.utils.register_class(proxy_panel_add_objects)
    bpy.utils.register_class(proxy_panel_remove_objects)
    bpy.utils.register_class(proxy_panel_list_item)
    bpy.utils.register_class(proxy_panel_list_makes_parents)
    bpy.utils.register_class(proxy_panel_list_clear_parents)
    bpy.utils.register_class(proxy_panel_list_select_same_collection)
    bpy.utils.register_class(proxy_panel_list_apply_all_modifiers)
    bpy.utils.register_class(proxy_panel_convertto_hull_geometry)
    bpy.utils.register_class(proxy_panel_convertto_bound_box)
    # Scene
    # bpy.types.Scene.proxy_item = bpy.props.PointerProperty(type=bpy.types.Mesh,description='Original Mesh-Data name')
    # Object
    bpy.types.Object.proxy_item_obj = bpy.props.PointerProperty(
        type=bpy.types.Mesh, description='Original Mesh-Data name')
    # Mesh
    bpy.types.Mesh.mesh_list = bpy.props.CollectionProperty(
        type=proxy_panel_list_item)
    bpy.types.Mesh.list_index = bpy.props.IntProperty(
        name="Index for mesh_list", default=0)
    # bpy.types.Mesh.proxy_item = bpy.props.PointerProperty(type=bpy.types.Mesh,description='Original Mesh-Data name')
    bpy.utils.register_class(Scatter_Panel)
    bpy.utils.register_class(scatter_panel_make_real_objects)
    bpy.utils.register_class(scatter_panel_object_list)
    bpy.utils.register_class(scatter_panel_add_objects)
    bpy.utils.register_class(scatter_panel_remove_objects)
    bpy.utils.register_class(scatter_panel_list_item)
    bpy.utils.register_class(Scatter_Panel_Scatter_As)
    bpy.utils.register_class(Scatter_Panel_Paint_Panel)
    bpy.utils.register_class(Scatter_Panel_Rotation_Panel)
    bpy.utils.register_class(Scatter_Panel_Object)
    bpy.utils.register_class(Scatter_Panel_Collection)
    bpy.utils.register_class(Scatter_Panel_Collection_Use_Count)
    bpy.utils.register_class(Scatter_Panel_Extra)
    # Object
    bpy.types.Object.scatter_item_obj = bpy.props.PointerProperty(type=bpy.types.Mesh, description='Original Mesh-Data name')
    # Mesh
    bpy.types.Mesh.scatter_mesh_list = bpy.props.CollectionProperty(type=scatter_panel_list_item)
    bpy.types.Mesh.scatter_list_index = bpy.props.IntProperty(
        name="Index for scatter_mesh_list", default=0)
        
     
        
        
    bpy.utils.register_class(Camera_Panel)
    bpy.utils.register_class(camera_panel_add_camera_view)
    bpy.utils.register_class(camera_panel_list)   
    bpy.utils.register_class(camera_panel_add_camera)
    bpy.utils.register_class(camera_panel_remove_camera)
    bpy.utils.register_class(camera_panel_list_item)
    
    
    # Scene
    bpy.types.Scene.camera_list = bpy.props.CollectionProperty(type=camera_panel_list_item)
    bpy.types.Scene.camera_list_index = bpy.props.IntProperty(name="Index for camera_list", default=0)
    
    bpy.utils.register_class(data_context_camera_lock)
    bpy.utils.register_class(data_context_camera)
    bpy.utils.register_class(data_context_camera_lens)
    bpy.utils.register_class(data_context_camera_dof)
    bpy.utils.register_class(data_context_camera_dof_aperture)
    bpy.utils.register_class(data_context_camera_camera)
    bpy.utils.register_class(data_context_camera_safe_areas)
    bpy.utils.register_class(data_context_camera_safe_areas_center_cut)
    bpy.utils.register_class(data_context_camera_background_image)
    bpy.utils.register_class(data_context_camera_display)
    bpy.utils.register_class(data_context_camera_display_composition_guides)
    bpy.utils.register_class(lock_camera_to_object)
 
    
    
    
   

def unregister():
    # Unregister for Blender
    bpy.utils.unregister_class(arcblend)
    bpy.utils.unregister_class(Add_Mesh)
    bpy.utils.unregister_class(Add_Curve)
    bpy.utils.unregister_class(Add_Surface)
    bpy.utils.unregister_class(Add_Metaball)
    bpy.utils.unregister_class(Add_Text)
    bpy.utils.unregister_class(Add_Volume)
    bpy.utils.unregister_class(Add_Grease_Pencil)
    bpy.utils.unregister_class(Add_Armature)
    bpy.utils.unregister_class(Add_Lattice)
    bpy.utils.unregister_class(Add_Empty)
    bpy.utils.unregister_class(Add_Image)
    bpy.utils.unregister_class(Add_Light)
    bpy.utils.unregister_class(Add_Light_Probe)
    bpy.utils.unregister_class(Add_Camera)
    bpy.utils.unregister_class(Add_Speaker)
    bpy.utils.unregister_class(Add_Force_Field)
    bpy.utils.unregister_class(Add_Collection_instance)
    bpy.utils.unregister_class(ArcBlendModifiers)
    bpy.utils.unregister_class(modifier)
    bpy.utils.unregister_class(transform_edit_object_panel)
    bpy.utils.unregister_class(transform_edit_object_align_x)
    bpy.utils.unregister_class(transform_edit_object_align_y)
    bpy.utils.unregister_class(transform_edit_object_align_z)
    bpy.utils.unregister_class(transform_edit_object_align_bound)
    bpy.utils.unregister_class(transform_edit_object_purge)
    bpy.utils.unregister_class(transform)
    bpy.utils.unregister_class(modifier_panel)
    bpy.utils.unregister_class(modify_panel)
    bpy.utils.unregister_class(array_panel)
    bpy.utils.unregister_class(modifier_array)
    bpy.utils.unregister_class(modifier_array_detail)
    bpy.utils.unregister_class(modifier_array_detail_executer)
    bpy.utils.unregister_class(modifier_array_apply)
    bpy.utils.unregister_class(Relative_Offset)
    del bpy.types.Scene.Arc_Blend
    bpy.utils.unregister_class(bevel_panel)
    bpy.utils.unregister_class(modifier_bevel_button)
    bpy.utils.unregister_class(modifier_bevel_v_button)
    bpy.utils.unregister_class(modifier_bevel_e_button)
    bpy.utils.unregister_class(modifier_bevel_detail)
    bpy.utils.unregister_class(modifier_bevel_detail_executer)
    bpy.utils.unregister_class(modifier_bevel_apply)
    del bpy.types.Scene.AB_Bevel
    bpy.utils.unregister_class(generate_panel)
    bpy.utils.unregister_class(deform_panel)
    bpy.utils.unregister_class(physics_panel)
    bpy.utils.unregister_class(display_panel)
    bpy.utils.unregister_class(Loop_Menu)
    bpy.utils.unregister_class(loop_multiple_select)
    bpy.utils.unregister_class(loop_multiple_select_ring)
    bpy.utils.unregister_class(loop_select)
    bpy.utils.unregister_class(loop_select_boundry_faces)
    bpy.utils.unregister_class(loop_mesh_seperate)
    bpy.utils.unregister_class(loop_mesh_shortest_path_pick)
    bpy.utils.unregister_class(loop_mesh_split)
    bpy.utils.unregister_class(modelling_edit_clean_mesh)
    bpy.utils.unregister_class(loop_mesh_tris_convert_to_quads)
    bpy.utils.unregister_class(loop_mesh_quads_convert_to_tris)
    bpy.utils.unregister_class(loop_mesh_find_trios)
    bpy.utils.unregister_class(loop_mesh_find_quads)
    bpy.utils.unregister_class(loop_sde)
    bpy.utils.unregister_class(loop_idtm)
    bpy.utils.unregister_class(mball_ball)
    bpy.utils.unregister_class(mball_capsule)
    bpy.utils.unregister_class(mball_plane)
    bpy.utils.unregister_class(mball_ellipsoid)
    bpy.utils.unregister_class(mball_cube)
    bpy.utils.unregister_class(grease_pencil_blank)
    bpy.utils.unregister_class(grease_pencil_stroke)
    bpy.utils.unregister_class(grease_pencil_monkey)
    bpy.utils.unregister_class(grease_pencil_sla)
    bpy.utils.unregister_class(grease_pencil_cla)
    bpy.utils.unregister_class(grease_pencil_ola)
    bpy.utils.unregister_class(lattice_button)
    bpy.utils.unregister_class(empty_plain_axes)
    bpy.utils.unregister_class(empty_arrows)
    bpy.utils.unregister_class(empty_single_arrow)
    bpy.utils.unregister_class(empty_circle)
    bpy.utils.unregister_class(empty_cube)
    bpy.utils.unregister_class(empty_sphere)
    bpy.utils.unregister_class(empty_cone)
    bpy.utils.unregister_class(empty_image)
    bpy.utils.unregister_class(light_point)
    bpy.utils.unregister_class(light_sun)
    bpy.utils.unregister_class(light_spot)
    bpy.utils.unregister_class(light_area)
    bpy.utils.unregister_class(light_probe_cubemap)
    bpy.utils.unregister_class(light_probe_reflectionplane)
    bpy.utils.unregister_class(light_probe_irradiencevolume)
    bpy.utils.unregister_class(camera_normal)
    bpy.utils.unregister_class(speaker_button)
    bpy.utils.unregister_class(forcefield_force)
    bpy.utils.unregister_class(forcefield_wind)
    bpy.utils.unregister_class(forcefield_vortex)
    bpy.utils.unregister_class(forcefield_magnetic)
    bpy.utils.unregister_class(forcefield_harmonic)
    bpy.utils.unregister_class(forcefield_charge)
    bpy.utils.unregister_class(forcefield_lennardj)
    bpy.utils.unregister_class(forcefield_texture)
    bpy.utils.unregister_class(forcefield_curveguide)
    bpy.utils.unregister_class(forcefield_boid)
    bpy.utils.unregister_class(forcefield_turbulance)
    bpy.utils.unregister_class(forcefield_drag)
    bpy.utils.unregister_class(forcefield_fluidflow)
    bpy.utils.unregister_class(collection_instance_collection)
    bpy.utils.unregister_class(edit_mode_vertex)
    bpy.utils.unregister_class(edit_mode_add_vertex)
    bpy.utils.unregister_class(edit_mode_bridge_vertices)
    bpy.utils.unregister_class(edit_mode_delete_vertices)
    bpy.utils.unregister_class(edit_mode_just_vertices)
    bpy.utils.unregister_class(edit_mode_just_edges)
    bpy.utils.unregister_class(edit_mode_create_faces)
    bpy.utils.unregister_class(transform_edit_object_randomize_colors)
    bpy.utils.unregister_class(transform_edit_object_reset_colors)
    bpy.utils.unregister_class(display_panel_show_xray)
    bpy.utils.unregister_class(display_panel_show_wireframe)
    bpy.utils.unregister_class(display_panel_show_solid)
    bpy.utils.unregister_class(display_panel_show_material)
    bpy.utils.unregister_class(display_panel_show_rendered)
    bpy.utils.unregister_class(Themes_Panel)
    bpy.utils.unregister_class(themes_panel_mak)
    bpy.utils.unregister_class(themes_panel_white_chalk)
    bpy.utils.unregister_class(themes_panel_reset)
    bpy.utils.unregister_class(Modelling_Panel)
    bpy.utils.unregister_class(cutter_box)
    bpy.utils.unregister_class(cutter_box_object)
    bpy.utils.unregister_class(cutter_apply_modifier)
    
    bpy.utils.unregister_class(view_3d_top)
    bpy.utils.unregister_class(view_3d_bottom)
    bpy.utils.unregister_class(view_3d_front)
    bpy.utils.unregister_class(view_3d_back)
    bpy.utils.unregister_class(view_3d_right)
    bpy.utils.unregister_class(view_3d_left)
    bpy.utils.unregister_class(Modelling_Panel_Vertex_Selection)
    bpy.utils.unregister_class(vertex_selection_make_circle)
    bpy.utils.unregister_class(vertex_selection_rip_vertex)
    bpy.utils.unregister_class(vertex_selection_merge_vertex_last)
    bpy.utils.unregister_class(vertex_selection_dissolve_vertex)
    bpy.utils.unregister_class(vertex_selection_connect_vertex_path)
    bpy.utils.unregister_class(vertex_selection_create_vertices)
    bpy.utils.unregister_class(vertex_selection_assign_vertex_group)
    bpy.utils.unregister_class(Modelling_Panel_Vertex_Group_Panel)
    bpy.utils.unregister_class(Modelling_Panel_Modify_Selection)
    bpy.utils.unregister_class(loop_grow_edge_select)
    bpy.utils.unregister_class(loop_shrink_edge_select)
    bpy.utils.unregister_class(loop_auto_edge_loop)
    bpy.utils.unregister_class(Modelling_Panel_Modify_Edit_Faces)
    bpy.utils.unregister_class(modelling_edit_faces_flip_normals)
    bpy.utils.unregister_class(modelling_edit_faces_recalculate_outside)
    bpy.utils.unregister_class(modelling_edit_faces_extrude)
    bpy.utils.unregister_class(modelling_edit_faces_inset)
    bpy.utils.unregister_class(modelling_edit_faces_extrude_normals)
    bpy.utils.unregister_class(modelling_edit_faces_extrude_individual)
    bpy.utils.unregister_class(modelling_edit_faces_poke)
    bpy.utils.unregister_class(modelling_edit_faces_triangulate)
    bpy.utils.unregister_class(modelling_edit_faces_tris_to_quads)
    bpy.utils.unregister_class(modelling_edit_faces_solidify)
    bpy.utils.unregister_class(modelling_edit_faces_wireframe)
    bpy.utils.unregister_class(modelling_edit_edges_connect)
    bpy.utils.unregister_class(modelling_edit_edges_extrude)
    bpy.utils.unregister_class(modelling_edit_edges_collapse)
    bpy.utils.unregister_class(Modelling_Panel_Modify_Edit)
    bpy.utils.unregister_class(modelling_edit_loop_cut)
    bpy.utils.unregister_class(modelling_edit_rotate_edges)
    bpy.utils.unregister_class(modelling_edit_offset_edge_loop_cut)
    bpy.utils.unregister_class(modelling_edit_knife_cut)
    bpy.utils.unregister_class(modelling_edit_knife_bisect)
    bpy.utils.unregister_class(modelling_edit_x_mirror)
    bpy.utils.unregister_class(modelling_edit_x_mirror_minus)
    bpy.utils.unregister_class(modelling_edit_y_mirror)
    bpy.utils.unregister_class(modelling_edit_y_mirror_minus)
    bpy.utils.unregister_class(modelling_edit_z_mirror)
    bpy.utils.unregister_class(modelling_edit_z_mirror_minus)
    bpy.utils.unregister_class(modelling_edit_fill_sides)
    bpy.utils.unregister_class(modelling_edit_hide_unselected)
    bpy.utils.unregister_class(modelling_edit_hide_selected)
    bpy.utils.unregister_class(modelling_edit_reveal)
    bpy.utils.unregister_class(modelling_edit_orient_x)
    bpy.utils.unregister_class(modelling_edit_orient_y)
    bpy.utils.unregister_class(modelling_edit_orient_z)
    bpy.utils.unregister_class(Proxy_Panel)
    bpy.utils.unregister_class(proxy_panel_remeshx_result)
    bpy.utils.unregister_class(proxy_panel_convertto_point_cloud)
    bpy.utils.unregister_class(proxy_panel_object_list)
    bpy.utils.unregister_class(proxy_panel_add_objects)
    bpy.utils.unregister_class(proxy_panel_remove_objects)
    bpy.utils.unregister_class(proxy_panel_list_item)
    bpy.utils.unregister_class(proxy_panel_list_makes_parents)
    bpy.utils.unregister_class(proxy_panel_list_clear_parents)
    bpy.utils.unregister_class(proxy_panel_list_select_same_collection)
    bpy.utils.unregister_class(proxy_panel_list_apply_all_modifiers)
    bpy.utils.unregister_class(proxy_panel_convertto_hull_geometry)
    bpy.utils.unregister_class(proxy_panel_convertto_bound_box)
    bpy.utils.unregister_class(Scatter_Panel_Scatter_As)
    bpy.utils.unregister_class(scatter_panel_make_real_objects)
    bpy.utils.unregister_class(Scatter_Panel_Paint_Panel)
    bpy.utils.unregister_class(Scatter_Panel_Rotation_Panel)
    bpy.utils.unregister_class(Scatter_Panel_Object)
    bpy.utils.unregister_class(Scatter_Panel_Collection)
    bpy.utils.unregister_class(Scatter_Panel_Collection_Use_Count)
    bpy.utils.unregister_class(Scatter_Panel_Extra)
    # del bpy.types.Scene.mesh_list
    # del bpy.types.Scene.list_index
    # del bpy.types.Scene.proxy_item
    # del bpy.types.Object.mesh_list
    # del bpy.types.Object.list_index
    del bpy.types.Object.proxy_item_obj
    del bpy.types.Mesh.mesh_list
    del bpy.types.Mesh.list_index
    # del bpy.types.Mesh.proxy_item
    bpy.utils.unregister_class(Scatter_Panel)
    bpy.utils.unregister_class(scatter_panel_object_list)
    bpy.utils.unregister_class(scatter_panel_add_objects)
    bpy.utils.unregister_class(scatter_panel_remove_objects)
    bpy.utils.unregister_class(scatter_panel_list_item)
    del bpy.types.Mesh.scatter_mesh_list
    del bpy.types.Mesh.scatter_list_index
    del bpy.types.Object.scatter_item_obj
    bpy.utils.unregister_class(Camera_Panel)
    bpy.utils.unregister_class(camera_panel_add_camera_view)
    bpy.utils.unregister_class(camera_panel_list)   
    bpy.utils.unregister_class(camera_panel_add_camera)
    bpy.utils.unregister_class(camera_panel_remove_camera)
    bpy.utils.unregister_class(camera_panel_list_item)
    del bpy.types.Scene.camera_list
    del bpy.types.Scene.camera_list_index
    
    bpy.utils.unregister_class(data_context_camera_lock)
    bpy.utils.unregister_class(data_context_camera)
    bpy.utils.unregister_class(data_context_camera_lens)
    bpy.utils.unregister_class(data_context_camera_dof)
    bpy.utils.unregister_class(data_context_camera_dof_aperture)
    bpy.utils.unregister_class(data_context_camera_camera)
    bpy.utils.unregister_class(data_context_camera_safe_areas)
    bpy.utils.unregister_class(data_context_camera_safe_areas_center_cut)
    bpy.utils.unregister_class(data_context_camera_background_image)
    bpy.utils.unregister_class(data_context_camera_display)
    bpy.utils.unregister_class(data_context_camera_display_composition_guides)
    bpy.utils.unregister_class(lock_camera_to_object)
    
    

# ------------------------------------------------------------------------------


if __name__ == "__main__":
    register()
