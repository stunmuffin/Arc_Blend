
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
# THEMES PANEL


class THEMES_PT_Panel (bpy.types.Panel):
    bl_label = "AB Themes"
    bl_idname = "THEMES_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_options = {'DEFAULT_CLOSED'}

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
# THEMES PANEL 

class VIEW3D_PT_AB_view3d_properties(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Arc Blend"
    bl_label = "View"
    bl_parent_id= "THEMES_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        view = context.space_data

        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        col = layout.column()

        subcol = col.column()
        subcol.active = bool(view.region_3d.view_perspective != 'CAMERA' or view.region_quadviews)
        subcol.prop(view, "lens", text="Focal Length")

        subcol = col.column(align=True)
        subcol.prop(view, "clip_start", text="Clip Start")
        subcol.prop(view, "clip_end", text="End")

        layout.separator()

        col = layout.column(align=False, heading="Local Camera")
        col.use_property_decorate = False
        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(view, "use_local_camera", text="")
        sub = sub.row(align=True)
        sub.enabled = view.use_local_camera
        sub.prop(view, "camera", text="")

        layout.separator()

        col = layout.column(align=True)
        col.prop(view, "use_render_border")
        col.active = view.region_3d.view_perspective != 'CAMERA'

# ------------------------------------------------------------------------------
# DARK THEME


class themes_panel_mak (bpy.types.Operator):
    """Dark Theme.Background "Black"Shows color object."""
    bl_label = ""
    bl_idname = "object.button_themes_panel_mak"

    def execute(self, context):
        for area in bpy.context.screen.areas: 
            if area.type == 'VIEW_3D':
                space = area.spaces.active
                if space.type == 'VIEW_3D':
                    space.shading.type = 'SOLID'
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
        for area in bpy.context.screen.areas: 
            if area.type == 'VIEW_3D':
                space = area.spaces.active
                if space.type == 'VIEW_3D':
                    space.shading.type = 'SOLID'
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
                    bpy.context.space_data.overlay.show_axis_z = False
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
        for area in bpy.context.screen.areas: 
            if area.type == 'VIEW_3D':
                space = area.spaces.active
                if space.type == 'VIEW_3D':
                    space.shading.type = 'SOLID'

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



def register():
    bpy.utils.register_class(THEMES_PT_Panel)
    bpy.utils.register_class(VIEW3D_PT_AB_view3d_properties)
    bpy.utils.register_class(themes_panel_mak)
    bpy.utils.register_class(themes_panel_white_chalk)
    bpy.utils.register_class(themes_panel_reset)

 
  

def unregister():
    bpy.utils.unregister_class(THEMES_PT_Panel)
    bpy.utils.unregister_class(VIEW3D_PT_AB__view3d_properties)
    bpy.utils.unregister_class(themes_panel_mak)
    bpy.utils.unregister_class(themes_panel_white_chalk)
    bpy.utils.unregister_class(themes_panel_reset)
