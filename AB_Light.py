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
# LIGHT PANEL

class LIGHT_PT_Panel (bpy.types.Panel):
    bl_label = "AB Light"
    bl_idname = "LIGHT_PT_Panel"
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
        col.label(text="Light Panel :" , icon="LIGHT")
        col.operator("object.button_light_point", text="Add Light to Scene", icon="OUTLINER_OB_LIGHT")
        # draw template
        col1 = row.column()
        col2 = row.column()
        template = col1
        template.template_list("LIGHT_UL_List", "light_list", scene, "light_list",
                                   scene, "light_list_index", rows=3)
        template.scale_y = 1.1
        # draw side bar
        col.separator(factor=0)
        
        #
        add = col2.column(align=True)
        AB_ADD = add.operator(
            "object.button_light_panel_add_light", icon='ADD', text="")
        
        rem = col2.column(align=True)
        AB_REMOVE = rem.operator(
            "object.button_light_panel_remove_light", icon='REMOVE', text="")

        col.column_flow(columns=3, align=True)

# ------------------------------------------------------------------------------
# LIGHT LIST


class LIGHT_UL_List(bpy.types.UIList):
    """UI Light List"""

    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_propname, index):

        scene = context.scene
        row = layout.row(align=True)
        sub = row.row(align=True)
        sub.scale_x = 2
        sub.prop(item, "light_item", text='', icon="OUTLINER_OB_LIGHT")
        sub = row.row(align=True)
        sub.scale_x = 1.1
        sub.enabled = bool(item.light_item)
        sub.prop(item, "light_display", text='',
                 icon='RESTRICT_VIEW_OFF' if item.light_display else 'RESTRICT_VIEW_ON')
        sub = row.row(align=True)
        sub.scale_x = 0.3
        sub.prop(item, "name", text="", icon="LAYER_ACTIVE", emboss=False)
        sub.enabled = False

# ------------------------------------------------------------------------------
# ADD LIGHT TO LIST

class light_panel_add_light (bpy.types.Operator):
    """Add a new item to the list"""

    bl_label = ""
    bl_idname = "object.button_light_panel_add_light"
    

    def execute(self, context):
        try:
            light_list_scn =[]
            for i in bpy.context.scene.objects[:]:
                if i.type == "LIGHT":
                    light_list_scn.append(i)
            for i in light_list_scn:
                scene= bpy.context.scene
                light = i
                index = scene.light_list_index
                item = scene.light_list.add()
                item.name = light.name
                item.light_ui_index = len(scene.light_list)
                scene.light_list_index = len(scene.light_list) - 1
        except (AttributeError,KeyError,UnboundLocalError) :
            pass

        return {'FINISHED'}

# ------------------------------------------------------------------------------
# DELETE OBJECT FROM LIST LIGHT


class light_panel_remove_light (bpy.types.Operator):
    """Remove item from the list"""

    bl_label = ""
    bl_idname = "object.button_light_panel_remove_light"

    def execute(self, context):
        try:
            light_list_scn =[]
            for i in bpy.context.scene.objects[:]:
                if i.type == "LIGHT":
                    light_list_scn.append(i)
            for i in light_list_scn:
                scene = bpy.context.scene
                light = i
                index = scene.light_list_index
                scene.light_list_index -= 1
                scene.light_list.remove(index)
        except (AttributeError,KeyError,UnboundLocalError) :
            pass
        return {'FINISHED'}

# ------------------------------------------------------------------------------
# DEF LIGHT
def light_return_one_time(scene, active_idx, prop_api):
    """Returning once per elements"""
    AB_list = scene.light_list
    
    for i in AB_list:
        if i.light_ui_index != active_idx:
            exec(f"i.{prop_api}= False")
    return None


def light_display_upd(self, context):
    
    if self.light_display == True:
        light_return_one_time(self.id_data, self.light_ui_index, "light_display")
    
        for i in bpy.data.scenes[bpy.context.scene.name].light_list[:]:
               if i.light_display== True:
                   bpy.context.active_object.select_set(False)
                   bpy.context.view_layer.objects.active = bpy.data.objects[i.name]
                   bpy.context.object.select_set(True)
       
    else:
        pass

# ------------------------------------------------------------------------------
# LIGHT PROPERTY GROUP


class light_panel_list_item(bpy.types.PropertyGroup):
    id: bpy.props.IntProperty()
    light: bpy.props.PointerProperty(name="Light",type=bpy.types.Light)

    # Name of the items in the list
    name: bpy.props.StringProperty(description="Light Name")
    # Random props in the lists
    light_ui_index: bpy.props.IntProperty(description='UI List Index')
    light_item: bpy.props.PointerProperty(type=bpy.types.Light, description='Light Name')
    light_display: bpy.props.BoolProperty(default=False, description="Display in Viewport", update=light_display_upd)
    
   

    def copy(self):
        self.light = self.id_data.copy()
        self.name = self.light.name
        return self.light

    def add(self, light):
        self.light = light
        self.name = light.name
        return self.light



# ------------------------------------------------------------------------------
# LIGHT BUTTON PANEL

class DataButtonsPanel:
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        active = bpy.context.active_object
        try:
            if active.type == "LIGHT":
                engine = context.engine
                return active.data and (engine in cls.COMPAT_ENGINES)
        except (AttributeError,KeyError):
            pass
# ------------------------------------------------------------------------------
# LIGHT BUTTON PANEL
    
class LIGHT_PT_List_Context_Light(DataButtonsPanel, Panel):
    bl_label = ""
    bl_options = {'HIDE_HEADER'}
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "LIGHT_PT_Panel"

    def draw(self, context):
        layout = self.layout
        ob = context.object
        space = context.space_data

        if ob:
            layout.template_ID(ob, "data")
        elif light:
            layout.template_ID(space, "pin_id")


# ------------------------------------------------------------------------------
# LIGHT PANEL LIST Light x

class LIGHT_PT_List_EEVEE_Light(DataButtonsPanel, Panel):
    bl_label = "Light"
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "LIGHT_PT_Panel"
    COMPAT_ENGINES = {'BLENDER_EEVEE'}

    def draw(self, context):
        active = bpy.context.active_object
        try:
            if active.type == "LIGHT":
                context = active.data
                layout = self.layout
                light = context
                # Compact layout for node editor.
                layout.use_property_split = False
                layout.row().prop(light, "type",expand=True)
                col = layout.column()
                col.prop(light, "color")
                col.prop(light, "energy")
                col.separator()
                col.prop(light, "diffuse_factor", text="Diffuse")
                col.prop(light, "specular_factor", text="Specular")
                col.prop(light, "volume_factor", text="Volume")
                col.separator()
                if light.type in {'POINT', 'SPOT'}:
                    col.prop(light, "shadow_soft_size", text="Radius")
                elif light.type == 'SUN':
                    col.prop(light, "angle")
                elif light.type == 'AREA':
                    col.prop(light, "shape")
                    sub = col.column(align=True)
                    if light.shape in {'SQUARE', 'DISK'}:
                        sub.prop(light, "size")
                    elif light.shape in {'RECTANGLE', 'ELLIPSE'}:
                        sub.prop(light, "size", text="Size X")
                        sub.prop(light, "size_y", text="Y")
        except (AttributeError,KeyError):
            pass
# ------------------------------------------------------------------------------
# LIGHT PANEL distance
class LIGHT_PT_List_EEVEE_Light_Distance(DataButtonsPanel, Panel):
    bl_label = "Custom Distance"
    bl_parent_id = "LIGHT_PT_List_EEVEE_Light"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'BLENDER_EEVEE'}

    @classmethod
    def poll(cls, context):
        active = bpy.context.active_object
        try:
            if active.type == "LIGHT":
                context1 = active.data
                light = context1
                engine = context.engine
                return (light and light.type != 'SUN') and (engine in cls.COMPAT_ENGINES)
        except (AttributeError,KeyError):
            pass
        
    def draw_header(self, context):
        active = bpy.context.active_object
        try:
            for i in bpy.context.scene.objects[:]:
                if i.type == "LIGHT":
                    context = i.data
                    light = context
                    layout = self.layout
                    layout.prop(light, "use_custom_distance", text="")
        except (AttributeError,KeyError):
            pass
    def draw(self, context):
        active = bpy.context.active_object
        try:
            if active.type == "LIGHT":
                context = active.data
                layout = self.layout
                light = context
                layout.active = light.use_custom_distance
                layout.use_property_split = True

                layout.prop(light, "cutoff_distance", text="Distance")
        except (AttributeError,KeyError):
            pass
# ------------------------------------------------------------------------------
# LIGHT PANEL shadow

class LIGHT_PT_List_EEVEE_Shadow(DataButtonsPanel, Panel):
    bl_label = "Shadow"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "LIGHT_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'BLENDER_EEVEE'}

    @classmethod
    def poll(cls, context):
        active = bpy.context.active_object
        try:
            if active.type == "LIGHT":
                context1 = active.data
                light = context1
                engine = context.engine
                return (
                    (light and light.type in {'POINT', 'SUN', 'SPOT', 'AREA'}) and
                    (engine in cls.COMPAT_ENGINES)
                )
        except (AttributeError,KeyError):
            pass
    def draw_header(self, context):
        active = bpy.context.active_object
        try:
            if active.type == "LIGHT":
                context = active.data
                light = context
                self.layout.prop(light, "use_shadow", text="")
        except (AttributeError,KeyError):
            pass

    def draw(self, context):
        active = bpy.context.active_object
        try:
            if active.type == "LIGHT":
                context = active.data
                layout = self.layout
                layout.use_property_split = True
                light = context
                layout.active = light.use_shadow
                col = layout.column()
                sub = col.column(align=True)
                if light.type != 'SUN':
                    sub.prop(light, "shadow_buffer_clip_start", text="Clip Start")
                col.prop(light, "shadow_buffer_bias", text="Bias")
        except (AttributeError,KeyError):
            pass
# ------------------------------------------------------------------------------
# LIGHT PANEL shadow map
class LIGHT_PT_List_EEVEE_Shadow_Cascaded_Shadow_Map(DataButtonsPanel, Panel):
    bl_label = "Cascaded Shadow Map"
    bl_parent_id = "LIGHT_PT_List_EEVEE_Shadow"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'BLENDER_EEVEE'}

    @classmethod
    def poll(cls, context):
        active = bpy.context.active_object
        try:
            if active.type == "LIGHT":
                context1 = active.data
                light = context1
                engine = context.engine
                return (light and light.type == 'SUN') and (engine in cls.COMPAT_ENGINES)
        except (AttributeError,KeyError):
            pass
    def draw(self, context):
        active = bpy.context.active_object
        try:
            if active.type == "LIGHT":
                context = active.data
                layout = self.layout
                light = context
                layout.use_property_split = True

                col = layout.column()

                col.prop(light, "shadow_cascade_count", text="Count")
                col.prop(light, "shadow_cascade_fade", text="Fade")

                col.prop(light, "shadow_cascade_max_distance", text="Max Distance")
                col.prop(light, "shadow_cascade_exponent", text="Distribution")
        except (AttributeError,KeyError):
            pass
# ------------------------------------------------------------------------------
# LIGHT PANEL shadow contact
class LIGHT_PT_List_EEVEE_Shadow_Contact(DataButtonsPanel, Panel):
    bl_label = "Contact Shadows"
    bl_parent_id = "LIGHT_PT_List_EEVEE_Shadow"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    COMPAT_ENGINES = {'BLENDER_EEVEE'}

    @classmethod
    def poll(cls, context):
        active = bpy.context.active_object
        try:
            if active.type == "LIGHT":
                context1 = active.data
                light = context1
                engine = context.engine
                return (
                    (light and light.type in {'POINT', 'SUN', 'SPOT', 'AREA'}) and
                    (engine in cls.COMPAT_ENGINES)
                )
        except (AttributeError,KeyError):
            pass

    def draw_header(self, context):
        active = bpy.context.active_object
        try:
            if active.type == "LIGHT":
                context = active.data
                light = context
                layout = self.layout
                layout.active = light.use_shadow
                layout.prop(light, "use_contact_shadow", text="")
        except (AttributeError,KeyError):
            pass

    def draw(self, context):
        active = bpy.context.active_object
        try:
            if active.type == "LIGHT":
                context = active.data
                layout = self.layout
                light = context
                layout.use_property_split = True

                col = layout.column()
                col.active = light.use_shadow and light.use_contact_shadow

                col.prop(light, "contact_shadow_distance", text="Distance")
                col.prop(light, "contact_shadow_bias", text="Bias")
                col.prop(light, "contact_shadow_thickness", text="Thickness")
        except (AttributeError,KeyError):
            pass

# ------------------------------------------------------------------------------
# LIGHT PANEL area
class LIGHT_PT_List_Area(DataButtonsPanel, Panel):
    bl_label = "Area Shape"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_WORKBENCH'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "LIGHT_PT_Panel"

    @classmethod
    def poll(cls, context):
        active = bpy.context.active_object
        try:
            if active.type == "LIGHT":
                context1 = active.data
                light = context1
                engine = context.engine
                return (light and light.type == 'AREA') and (engine in cls.COMPAT_ENGINES)
        except AttributeError:
            pass
    def draw(self, context):
        active = bpy.context.active_object
        try:
            if active.type == "LIGHT":
                context = active.data
                layout = self.layout
                light = context
                col = layout.column()
                col.row().prop(light, "shape", expand=True)
                sub = col.row(align=True)
                if light.shape in {'SQUARE', 'DISK'}:
                    sub.prop(light, "size")
                elif light.shape in {'RECTANGLE', 'ELLIPSE'}:
                    sub.prop(light, "size", text="Size X")
                    sub.prop(light, "size_y", text="Size Y")
        except AttributeError:
            pass
# ------------------------------------------------------------------------------
# LIGHT PANEL spot
class LIGHT_PT_List_Spot(DataButtonsPanel, Panel):
    bl_label = "Spot Shape"
    bl_parent_id = "LIGHT_PT_List_EEVEE_Light"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"

    @classmethod
    def poll(cls, context):
        active = bpy.context.active_object
        try:
            if active.type == "LIGHT":
                context1 = active.data
                light = context1
                engine = context.engine
                return (light and light.type == 'SPOT') and (engine in cls.COMPAT_ENGINES)
        except AttributeError:
            pass
    def draw(self, context):
        active = bpy.context.active_object
        try:
            if active.type == "LIGHT":
                context = active.data
                layout = self.layout
                layout.use_property_split = True
                light = context
                col = layout.column()
                col.prop(light, "spot_size", text="Size")
                col.prop(light, "spot_blend", text="Blend", slider=True)
                col.prop(light, "show_cone")
        except AttributeError:
            pass
# ------------------------------------------------------------------------------
# LIGHT PANEL falloff curve
class LIGHT_PT_List_Falloff_Curve(DataButtonsPanel, Panel):
    bl_label = "Falloff Curve"
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE'}

    @classmethod
    def poll(cls, context):
        active = bpy.context.active_object
        try:
            if active.type == "LIGHT":
                context1 = active.data
                light = context1
                engine = context.engine

                return (
                    (light and light.type in {'POINT', 'SPOT'} and light.falloff_type == 'CUSTOM_CURVE') and
                    (engine in cls.COMPAT_ENGINES)
                )
        except AttributeError:
            pass
    def draw(self, context):
        active = bpy.context.active_object
        try:
            if active.type == "LIGHT":
                context = active.data
                light = context

                self.layout.template_curve_mapping(
                    light, "falloff_curve", use_negative_slope=True)
        except AttributeError:
            pass


# ------------------------------------------------------------------------------
# REGISTRATION AREA

def register():
    #Light
    bpy.utils.register_class(LIGHT_PT_Panel)
    bpy.utils.register_class(LIGHT_UL_List)   
    bpy.utils.register_class(light_panel_add_light)
    bpy.utils.register_class(light_panel_remove_light)
    bpy.utils.register_class(light_panel_list_item)
    #Light Scene
    bpy.types.Scene.light_list = bpy.props.CollectionProperty(type=light_panel_list_item)
    bpy.types.Scene.light_list_index = bpy.props.IntProperty(name="Index for light_list", default=0)
    bpy.utils.register_class(LIGHT_PT_List_Context_Light)
    bpy.utils.register_class(LIGHT_PT_List_EEVEE_Light)
    bpy.utils.register_class(LIGHT_PT_List_EEVEE_Light_Distance)
    bpy.utils.register_class(LIGHT_PT_List_EEVEE_Shadow)
    bpy.utils.register_class(LIGHT_PT_List_EEVEE_Shadow_Cascaded_Shadow_Map)
    bpy.utils.register_class(LIGHT_PT_List_EEVEE_Shadow_Contact)
    bpy.utils.register_class(LIGHT_PT_List_Area)
    bpy.utils.register_class(LIGHT_PT_List_Spot)
    bpy.utils.register_class(LIGHT_PT_List_Falloff_Curve)

def unregister():
     #Light
    bpy.utils.unregister_class(LIGHT_PT_Panel)
    bpy.utils.unregister_class(LIGHT_UL_List)   
    bpy.utils.unregister_class(light_panel_add_light)
    bpy.utils.unregister_class(light_panel_remove_light)
    bpy.utils.unregister_class(light_panel_list_item)
    #Light Scene
    del bpy.types.Scene.light_list
    del bpy.types.Scene.light_list_index
    bpy.utils.unregister_class(LIGHT_PT_List_Context_Light)
    bpy.utils.unregister_class(LIGHT_PT_List_EEVEE_Light)
    bpy.utils.unregister_class(LIGHT_PT_List_EEVEE_Light_Distance)
    bpy.utils.unregister_class(LIGHT_PT_List_EEVEE_Shadow)
    bpy.utils.unregister_class(LIGHT_PT_List_EEVEE_Shadow_Cascaded_Shadow_Map)
    bpy.utils.unregister_class(LIGHT_PT_List_EEVEE_Shadow_Contact)
    bpy.utils.unregister_class(LIGHT_PT_List_Area)
    bpy.utils.unregister_class(LIGHT_PT_List_Spot)
    bpy.utils.unregister_class(LIGHT_PT_List_Falloff_Curve)
