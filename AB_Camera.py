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
# CAMERA PANEL

class CAMERA_PT_Panel (bpy.types.Panel):
    bl_label = "AB Camera"
    bl_idname = "CAMERA_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_options = {'DEFAULT_CLOSED'}
    

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
        template.template_list("CAMERA_UL_List", "camera_list", scene, "camera_list",
                                   scene, "camera_list_index", rows=3)
        
        template.scale_y = 1.1
        

        # draw side bar
        col.separator(factor=0)
        #
        add = col2.column(align=True)
        AB_ADD = add.operator("object.button_camera_panel_add_camera", icon='ADD', text="")


        #
        rem = col2.column(align=True)
        AB_REMOVE = rem.operator("object.button_camera_panel_remove_camera", icon='REMOVE', text="")


        col.column_flow(columns=3, align=True)

        

# ------------------------------------------------------------------------------
# ADD CAMERA TO VIEW OPERATOR

class camera_panel_add_camera_view (bpy.types.Operator):
    """Add camera to view (Current View)"""
    bl_label = "Add Camera"
    bl_idname = "object.button_camera_panel_add_camera_view"
 

    def execute(self, context):
        bpy.context.scene.camera = None
        bpy.ops.object.camera_add()
        bpy.context.object.data.name = bpy.context.object.name
        bpy.ops.view3d.camera_to_view()
        bpy.context.scene.camera = None
        bpy.ops.view3d.object_as_camera()
        return {'FINISHED'}

# ------------------------------------------------------------------------------
# CAMERA LIST


class CAMERA_UL_List(bpy.types.UIList):
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

# ------------------------------------------------------------------------------
# ADD CAMERA TO LIST


class camera_panel_add_camera (bpy.types.Operator):
    """Add a new item to the list"""
    bl_label = ""
    bl_idname = "object.button_camera_panel_add_camera"

    def execute(self, context):
        try:
            scene = bpy.context.scene
            len_cam_scn = len(bpy.data.scenes[:])
            for i in range(0,len_cam_scn):
                camera = bpy.data.scenes[i].camera
                index = scene.camera_list_index
                item = scene.camera_list.add()
                item.name = camera.name
                item.camera_ui_index = len(scene.camera_list)
                scene.camera_list_index = len(scene.camera_list) - 1
        except (AttributeError,KeyError,UnboundLocalError) :
            pass

        return {'FINISHED'}
# ------------------------------------------------------------------------------
# DELETE OBJECT FROM LIST


class camera_panel_remove_camera (bpy.types.Operator):
    """Remove item from the list"""

    bl_label = ""
    bl_idname = "object.button_camera_panel_remove_camera"

    def execute(self, context):
        
        try:
            scene = bpy.context.scene
            len_cam_scn = len(bpy.data.scenes[:])
            for i in range(0,len_cam_scn):
                camera = bpy.data.scenes[i].camera
                index = scene.camera_list_index
                scene.camera_list_index -= 1
                scene.camera_list.remove(index)
        except (AttributeError,KeyError,UnboundLocalError) :
            pass
        return {'FINISHED'}
# ------------------------------------------------------------------------------
# DEF CAMERA


def camera_return_one_time(mesh, active_idx, prop_api):
    """Returning once per elements"""
    scene = bpy.context.scene
    AB_list = scene.camera_list
    for i in AB_list:
        if i.camera_ui_index != active_idx:
            exec(f"i.{prop_api} = False")
    return None

def camera_display_upd(self, context):
    if self.camera_display:
        camera_return_one_time(self.id_data, self.camera_ui_index, "camera_display")
        len_cam = len(bpy.context.scene.camera_list)
        for i in range(0, len_cam):
            a = bpy.context.scene.camera_list[i].camera_item.name
            b = bpy.context.scene.camera_list[i].camera_display
            if b:
                if bpy.context.view_layer.objects.active is not None:
                    bpy.context.view_layer.objects.active.select_set(False)
                bpy.context.scene.camera = bpy.data.objects[a]
                bpy.context.view_layer.objects.active = bpy.data.objects[a]
                bpy.context.object.select_set(True)
                try:
                    if bpy.context.active_object.type == 'CAMERA':
                        for area in bpy.context.screen.areas:
                            if area.type == 'VIEW_3D':
                                area.spaces[0].region_3d.view_perspective = 'CAMERA'
                                break
                except AttributeError:
                    pass
    else:
        pass


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

class CAMERA_PT_Data_Context_Camera_Lock(Panel):
    bl_label = "View Lock"
    bl_idname = "CAMERA_PT_Data_Context_Camera_Lock"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "CAMERA_PT_Panel"
   
    
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

class CAMERA_PT_Data_Context_Camera(bpy.types.Panel):
    bl_label = "Camera Settings"
    bl_idname = "CAMERA_PT_Data_Context_Camera"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "CAMERA_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}
   
    def draw(self, context):
        layout = self.layout

# ------------------------------------------------------------------------------
# CAMERA LENS

class CAMERA_PT_Data_Context_Camera_Lens(bpy.types.Panel):
    bl_label = "Lens"
    bl_idname = "CAMERA_PT_Data_Context_Camera_Lens"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "CAMERA_PT_Data_Context_Camera"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    bl_options = {'DEFAULT_CLOSED'}
    
   
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

class CAMERA_PT_Data_Context_Camera_Dof(bpy.types.Panel):
    bl_label = "Depth of Field"
    bl_idname = "CAMERA_PT_Data_Context_Camera_Dof"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "CAMERA_PT_Data_Context_Camera"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        try:
            cam = context.scene.camera.data
            dof = cam.dof
            self.layout.prop(dof, "use_dof", text="")
        except AttributeError :
            pass
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        
        try:
            cam = context.scene.camera.data
            dof = cam.dof
            layout.active = dof.use_dof

            col = layout.column()
            col.prop(dof, "focus_object", text="Focus on Object")
            sub = col.column()
            sub.active = (dof.focus_object is None)
            sub.prop(dof, "focus_distance", text="Focus Distance")
        except AttributeError :
            pass
# ------------------------------------------------------------------------------
# CAMERA DOF APERTURE

class CAMERA_PT_Data_Context_Camera_Dof_Aperture(bpy.types.Panel):
    bl_label = "Aperture"
    bl_idname = "CAMERA_PT_Data_Context_Camera_Dof_Aperture"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "CAMERA_PT_Data_Context_Camera_Dof"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        try:
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
        except AttributeError :
            pass

# ------------------------------------------------------------------------------
# CAMERA 


class CAMERA_PT_presets(PresetPanel, Panel):
    bl_label = "Camera Presets"
    preset_subdir = "camera"
    preset_operator = "script.execute_preset"
    preset_add_operator = "camera.preset_add"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    
class CAMERA_PT_Data_Context_Camera_Settings(bpy.types.Panel):
    bl_label = "Camera"
    bl_idname = "CAMERA_PT_Data_Context_Camera_Settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "CAMERA_PT_Data_Context_Camera"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header_preset(self, _context):
        CAMERA_PT_presets.draw_panel_header(self.layout)
        

    def draw(self, context):
        layout = self.layout
        try:
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
        except AttributeError :
            pass
 
# ------------------------------------------------------------------------------
# SAFE AREAS
class SAFE_AREAS_PT_presets(PresetPanel, Panel):
    bl_label = "Camera Presets"
    preset_subdir = "safe_areas"
    preset_operator = "script.execute_preset"
    preset_add_operator = "safe_areas.preset_add"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

class CAMERA_PT_Data_Context_Camera_Safe_Areas(bpy.types.Panel):
    bl_label = "Safe Areas"
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "CAMERA_PT_Data_Context_Camera"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        try:
            cam = context.scene.camera.data
            self.layout.prop(cam, "show_safe_areas", text="")
        except AttributeError :
            pass
    def draw_header_preset(self, _context):
        SAFE_AREAS_PT_presets.draw_panel_header(self.layout)

    def draw(self, context):
        layout = self.layout
        try:
            safe_data = context.scene.safe_areas
            camera = context.scene.camera.data
            layout.use_property_split = True
            layout.active = camera.show_safe_areas
            col = layout.column()
            sub = col.column()
            sub.prop(safe_data, "title", slider=True)
            sub.prop(safe_data, "action", slider=True)
        except AttributeError :
            pass

class CAMERA_PT_Data_Context_Camera_Safe_Areas_Center_Cut(bpy.types.Panel):
    bl_label = "Center-Cut Safe Areas"
    bl_parent_id = "CAMERA_PT_Data_Context_Camera_Safe_Areas"
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    

    def draw_header(self, context):
        try:
            cam = context.scene.camera.data
            layout = self.layout
            layout.active = cam.show_safe_areas
            layout.prop(cam, "show_safe_center", text="")
        except AttributeError :
            pass

    def draw(self, context):
        layout = self.layout
        try:
            safe_data = context.scene.safe_areas
            camera = context.scene.camera.data
            layout.use_property_split = True
            layout.active = camera.show_safe_areas and camera.show_safe_center
            col = layout.column()
            col.prop(safe_data, "title_center", slider=True)
            col.prop(safe_data, "action_center", slider=True)
        except AttributeError :
            pass
# ------------------------------------------------------------------------------
# SAFE AREAS        
        
class CAMERA_PT_Data_Context_Camera_Background_Image(bpy.types.Panel):
    bl_label = "Background Images"
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "CAMERA_PT_Data_Context_Camera"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    def draw_header(self, context):
        try:
            cam = context.scene.camera.data
            self.layout.prop(cam, "show_background_images", text="")
        except AttributeError :
            pass
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        try:
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
        except AttributeError :
            pass

# ------------------------------------------------------------------------------
# VIEWPORT DISPLAY


class CAMERA_PT_Data_Context_Camera_Display(bpy.types.Panel):
    bl_label = "Viewport Display"
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "CAMERA_PT_Data_Context_Camera"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    def draw(self, context):
        layout = self.layout
        try:
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
        except AttributeError :
            pass


class CAMERA_PT_Data_Context_Camera_Display_Composition_Guides(bpy.types.Panel):
    bl_label = "Composition Guides"
    bl_parent_id = "CAMERA_PT_Data_Context_Camera_Display"
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        try:
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
        except AttributeError :
            pass



# ------------------------------------------------------------------------------
# REGISTRATION AREA

def register():
    #Camera     
    bpy.utils.register_class(CAMERA_PT_Panel)
    bpy.utils.register_class(camera_panel_add_camera_view)
    bpy.utils.register_class(CAMERA_UL_List)   
    bpy.utils.register_class(camera_panel_add_camera)
    bpy.utils.register_class(camera_panel_remove_camera)
    bpy.utils.register_class(camera_panel_list_item)
    #Camera Scene
    bpy.types.Scene.camera_list = bpy.props.CollectionProperty(type=camera_panel_list_item)
    bpy.types.Scene.camera_list_index = bpy.props.IntProperty(name="Index for camera_list", default=0)
    bpy.utils.register_class(CAMERA_PT_Data_Context_Camera_Lock)
    bpy.utils.register_class(CAMERA_PT_Data_Context_Camera)
    bpy.utils.register_class(CAMERA_PT_Data_Context_Camera_Lens)
    bpy.utils.register_class(CAMERA_PT_Data_Context_Camera_Dof)
    bpy.utils.register_class(CAMERA_PT_Data_Context_Camera_Dof_Aperture)
    bpy.utils.register_class(CAMERA_PT_Data_Context_Camera_Settings)
    bpy.utils.register_class(CAMERA_PT_Data_Context_Camera_Safe_Areas)
    bpy.utils.register_class(CAMERA_PT_Data_Context_Camera_Safe_Areas_Center_Cut)
    bpy.utils.register_class(CAMERA_PT_Data_Context_Camera_Background_Image)
    bpy.utils.register_class(CAMERA_PT_Data_Context_Camera_Display)
    bpy.utils.register_class(CAMERA_PT_Data_Context_Camera_Display_Composition_Guides)
    bpy.utils.register_class(lock_camera_to_object)

def unregister():
    #Camera
    bpy.utils.unregister_class(CAMERA_PT_Panel)
    bpy.utils.unregister_class(camera_panel_add_camera_view)
    bpy.utils.unregister_class(CAMERA_UL_List)   
    bpy.utils.unregister_class(camera_panel_add_camera)
    bpy.utils.unregister_class(camera_panel_remove_camera)
    bpy.utils.unregister_class(camera_panel_list_item)
    del bpy.types.Scene.camera_list
    del bpy.types.Scene.camera_list_index
    
    bpy.utils.unregister_class(CAMERA_PT_Data_Context_Camera_Lock)
    bpy.utils.unregister_class(CAMERA_PT_Data_Context_Camera)
    bpy.utils.unregister_class(CAMERA_PT_Data_Context_Camera_Lens)
    bpy.utils.unregister_class(CAMERA_PT_Data_Context_Camera_Dof)
    bpy.utils.unregister_class(CAMERA_PT_Data_Context_Camera_Dof_Aperture)
    bpy.utils.unregister_class(CAMERA_PT_Data_Context_Camera_Settings)
    bpy.utils.unregister_class(CAMERA_PT_Data_Context_Camera_Safe_Areas)
    bpy.utils.unregister_class(CAMERA_PT_Data_Context_Camera_Safe_Areas_Center_Cut)
    bpy.utils.unregister_class(CAMERA_PT_Data_Context_Camera_Background_Image)
    bpy.utils.unregister_class(CAMERA_PT_Data_Context_Camera_Display)
    bpy.utils.unregister_class(CAMERA_PT_Data_Context_Camera_Display_Composition_Guides)
    bpy.utils.unregister_class(lock_camera_to_object)


