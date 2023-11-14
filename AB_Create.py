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
from rna_prop_ui import PropertyPanel
from bpy_extras.node_utils import find_node_input
from bpy_extras import (asset_utils,)



# ------------------------------------------------------------------------------
# ARC BLEND PANEL


class ARCBLEND_PT_Panel (bpy.types.Panel):
    bl_label = "AB Create"
    bl_idname = "ARCBLEND_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

# ------------------------------------------------------------------------------
# MESH PANEL


class ADDMESH_PT_Panel (bpy.types.Panel):
    bl_label = "Mesh"
    bl_idname = "ADDMESH_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "ARCBLEND_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}

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


class ADDCURVE_PT_Panel (bpy.types.Panel):
    bl_label = "Curve"
    bl_idname = "ADDCURVE_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "ARCBLEND_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}

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


class ADDSURFACE_PT_Panel (bpy.types.Panel):
    bl_label = "Surface"
    bl_idname = "ADDSURFACE_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "ARCBLEND_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}

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


class ADDMETABALL_PT_Panel (bpy.types.Panel):
    bl_label = "METABALL"
    bl_idname = "ADDMETABALL_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "ARCBLEND_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}

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


class ADDTEXT_PT_Panel (bpy.types.Panel):
    bl_label = "Add Text"
    bl_idname = "ADDTEXT_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "ARCBLEND_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Add Text")
        row = layout.row()
        row.operator("object.text_add", icon="OUTLINER_OB_FONT")
        row = layout.row()

# ------------------------------------------------------------------------------
# ----------------------------------------------VOLUME PANEL----------------------------------------------------


class ADDVOLUME_PT_Panel (bpy.types.Panel):
    bl_label = "Volume"
    bl_idname = "ADDVOLUME_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "ARCBLEND_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}

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


class ADDGREASEPENCIL_PT_Panel (bpy.types.Panel):
    bl_label = "GREASE PENCIL"
    bl_idname = "ADDGREASEPENCIL_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "ARCBLEND_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}

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


class ADDARMATURE_PT_Panel (bpy.types.Panel):
    bl_label = "Armature"
    bl_idname = "ADDARMATURE_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "ARCBLEND_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}

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


class ADDLATTICE_PT_Panel (bpy.types.Panel):
    bl_label = "Lattice"
    bl_idname = "ADDLATTICE_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "ARCBLEND_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}

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


class ADDEMPTY_PT_Panel (bpy.types.Panel):
    bl_label = "Empty"
    bl_idname = "ADDEMPTY_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "ARCBLEND_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}

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


class ADDIMAGE_PT_Panel (bpy.types.Panel):
    bl_label = "Image"
    bl_idname = "ADDIMAGE_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "ARCBLEND_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}

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


class ADDLIGHT_PT_Panel (bpy.types.Panel):
    bl_label = "Light"
    bl_idname = "ADDLIGHT_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "ARCBLEND_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}

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


class ADDLIGHTPROBE_PT_Panel (bpy.types.Panel):
    bl_label = "Light Probe"
    bl_idname = "ADDLIGHTPROBE_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "ARCBLEND_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}

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


class ADDCAMERA_PT_Panel (bpy.types.Panel):
    bl_label = "Camera"
    bl_idname = "ADDCAMERA_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "ARCBLEND_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}

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


class ADDSPEAKER_PT_Panel (bpy.types.Panel):
    bl_label = "Speaker"
    bl_idname = "ADDSPEAKER_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "ARCBLEND_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}

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


class ADDFORCEFIELD_PT_Panel (bpy.types.Panel):
    bl_label = "Force Field"
    bl_idname = "ADDFORCEFIELD_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "ARCBLEND_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}

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


class ADDCOLLECTION_PT_Panel (bpy.types.Panel):
    bl_label = "Collection"
    bl_idname = "ADDCOLLECTION_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "ARCBLEND_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}

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
# REGISTRATION AREA

def register():
    bpy.utils.register_class(ARCBLEND_PT_Panel)
    bpy.utils.register_class(ADDMESH_PT_Panel)
    bpy.utils.register_class(ADDCURVE_PT_Panel)
    bpy.utils.register_class(ADDSURFACE_PT_Panel)
    bpy.utils.register_class(ADDMETABALL_PT_Panel)
    bpy.utils.register_class(ADDTEXT_PT_Panel)
    bpy.utils.register_class(ADDVOLUME_PT_Panel)
    bpy.utils.register_class(ADDGREASEPENCIL_PT_Panel)
    bpy.utils.register_class(ADDARMATURE_PT_Panel)
    bpy.utils.register_class(ADDLATTICE_PT_Panel)
    bpy.utils.register_class(ADDEMPTY_PT_Panel)
    bpy.utils.register_class(ADDIMAGE_PT_Panel)
    bpy.utils.register_class(ADDLIGHT_PT_Panel)
    bpy.utils.register_class(ADDLIGHTPROBE_PT_Panel)
    bpy.utils.register_class(ADDCAMERA_PT_Panel)
    bpy.utils.register_class(ADDSPEAKER_PT_Panel)
    bpy.utils.register_class(ADDFORCEFIELD_PT_Panel)
    bpy.utils.register_class(ADDCOLLECTION_PT_Panel)
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

def unregister():
    bpy.utils.unregister_class(ARCBLEND_PT_Panel)
    bpy.utils.unregister_class(ADDMESH_PT_Panel)
    bpy.utils.unregister_class(ADDCURVE_PT_Panel)
    bpy.utils.unregister_class(ADDSURFACE_PT_Panel)
    bpy.utils.unregister_class(ADDMETABALL_PT_Panel)
    bpy.utils.unregister_class(ADDTEXT_PT_Panel)
    bpy.utils.unregister_class(ADDVOLUME_PT_Panel)
    bpy.utils.unregister_class(ADDGREASEPENCIL_PT_Panel)
    bpy.utils.unregister_class(ADDARMATURE_PT_Panel)
    bpy.utils.unregister_class(ADDLATTICE_PT_Panel)
    bpy.utils.unregister_class(ADDEMPTY_PT_Panel)
    bpy.utils.unregister_class(ADDIMAGE_PT_Panel)
    bpy.utils.unregister_class(ADDLIGHT_PT_Panel)
    bpy.utils.unregister_class(ADDLIGHTPROBE_PT_Panel)
    bpy.utils.unregister_class(ADDCAMERA_PT_Panel)
    bpy.utils.unregister_class(ADDSPEAKER_PT_Panel)
    bpy.utils.unregister_class(ADDFORCEFIELD_PT_Panel)
    bpy.utils.unregister_class(ADDCOLLECTION_PT_Panel)
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