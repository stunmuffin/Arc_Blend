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
# Material Panel
class MATERIAL_PT_abpanel (bpy.types.Panel):
    bl_id = "MATERIAL_PT_abpanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_label= "AB Material"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self,context):
        layout=self.layout
        col= layout.column()
        col.label(text= "Copy or Paste Menu:")
        row= layout.row()
        row.operator("object.copy_material", text="Copy Material" , icon="COPYDOWN")
        row.operator("object.paste_material", text="Paste Material", icon="PASTEDOWN")
        col=layout.column()
        col.label(text= "Material Options :")
        col=layout.column()
 
 
 
 
 
class OBJECT_OT_CopyMaterial(bpy.types.Operator):
    bl_idname = "object.copy_material"
    bl_label = "Copy Material"
    bl_description = "Copy material name from active object"

    def execute(self, context):
        if context.active_object:
            active_material = context.active_object.active_material
            if active_material:
                bpy.context.window_manager.clipboard = active_material.name
                self.report({'INFO'}, f"Copied material name: {active_material.name}")
            else:
                self.report({'WARNING'}, "Active object has no material")
        else:
            self.report({'WARNING'}, "No active object")

        return {'FINISHED'}

class OBJECT_OT_PasteMaterial(bpy.types.Operator):
    bl_idname = "object.paste_material"
    bl_label = "Paste Material"
    bl_description = "Paste material name from clipboard to selected objects"

    def execute(self, context):
        material_name = bpy.context.window_manager.clipboard
        if material_name:
            selected_objects = context.selected_objects
            for obj in selected_objects:
                if obj.type == 'MESH':  # Adjust the type check as per your requirement
                    obj.active_material = bpy.data.materials.get(material_name)
                    if obj.active_material:
                        self.report({'INFO'}, f"Pasted material '{material_name}' to {obj.name}")
                    else:
                        self.report({'WARNING'}, f"Material '{material_name}' not found in the scene")
                else:
                    self.report({'WARNING'}, f"Object '{obj.name}' is not a mesh")
        else:
            self.report({'WARNING'}, "Clipboard has no material name")

        return {'FINISHED'}
    
class MATERIAL_MT_ab_context_menu(Menu):
    bl_label = "Material Specials"

    def draw(self, _context):
        layout = self.layout

        layout.operator("material.copy", icon='COPYDOWN')
        layout.operator("object.material_slot_copy")
        layout.operator("material.paste", icon='PASTEDOWN')
        layout.operator("object.material_slot_remove_unused")
# ------------------------------------------------------------------------------
# Material Ui List

class MATERIAL_UL_ab_matslots(bpy.types.UIList):

    def draw_item(self, _context, layout, _data, item, icon, _active_data, _active_propname, _index):
        slot = item
        ma = slot.material

        layout.context_pointer_set("id", ma)
        layout.context_pointer_set("material_slot", slot)

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if ma:
                layout.prop(ma, "name", text="", emboss=False, icon_value=icon)
            else:
                layout.label(text="", icon_value=icon)
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)
# ------------------------------------------------------------------------------
# Material Button Panel
    
class MaterialButtonsPanel:
    bl_context = "material"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id="MATERIAL_PT_abpanel"
    # COMPAT_ENGINES must be defined in each subclass, external engines can add themselves here

    @classmethod
    def poll(cls, context):
        mat = context.active_object.active_material
        return mat and (context.engine in cls.COMPAT_ENGINES) and not mat.grease_pencil

# ------------------------------------------------------------------------------
# Context Material
       
class EEVEE_MATERIAL_PT_ab_context_material(MaterialButtonsPanel, Panel):
    bl_label = ""
    bl_context = "material"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id ="MATERIAL_PT_abpanel"
    bl_options = {'HIDE_HEADER'}
    COMPAT_ENGINES = {'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    @classmethod
    def poll(cls, context):
        ob = context.object
        mat = bpy.context.object.active_material

        if (ob and ob.type == 'GPENCIL') or (mat and mat.grease_pencil):
            return False

        return (ob or mat) and (context.engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout

        mat = bpy.context.object.active_material
        ob = context.object
        #slot = context.object.material_slots
        slot = context.object.material_slots
        space = context.space_data

        if ob:
            is_sortable = len(ob.material_slots) > 1
            rows = 3
            if is_sortable:
                rows = 5

            row = layout.row()

            row.template_list("MATERIAL_UL_matslots", "", ob, "material_slots", ob, "active_material_index", rows=rows)

            col = row.column(align=True)
            col.operator("object.material_slot_add", icon='ADD', text="")
            col.operator("object.material_slot_remove", icon='REMOVE', text="")

            col.separator()

            col.menu("MATERIAL_MT_context_menu", icon='DOWNARROW_HLT', text="")

            if is_sortable:
                col.separator()

                col.operator("object.material_slot_move", icon='TRIA_UP', text="").direction = 'UP'
                col.operator("object.material_slot_move", icon='TRIA_DOWN', text="").direction = 'DOWN'

        row = layout.row()

        if ob:
            row.template_ID(ob, "active_material", new="material.new")


            if ob.mode == 'EDIT':
                row = layout.row(align=True)
                row.operator("object.material_slot_assign", text="Assign")
                row.operator("object.material_slot_select", text="Select")
                row.operator("object.material_slot_deselect", text="Deselect")

        elif mat:
            row.template_ID(space, "pin_id")

# ------------------------------------------------------------------------------
# Node Panel Draw    
 
def panel_node_draw(layout, ntree, _output_type, input_name):
    node = ntree.get_output_node('EEVEE')

    if node:
        input = find_node_input(node, input_name)
        if input:
            layout.template_node_view(ntree, node, input)
        else:
            layout.label(text="Incompatible output node")
    else:
        layout.label(text="No output node")
# ------------------------------------------------------------------------------
# Surface Panel

class EEVEE_MATERIAL_PT_ab_surface(MaterialButtonsPanel, Panel):
    bl_label = "Surface"
    bl_context = "material"
    COMPAT_ENGINES = {'BLENDER_EEVEE'}

    def draw(self, context):
        layout = self.layout

        mat = bpy.context.active_object.active_material

        layout.prop(mat, "use_nodes", icon='NODETREE')
        layout.separator()

        layout.use_property_split = True

        if mat.use_nodes:
            panel_node_draw(layout, mat.node_tree, 'OUTPUT_MATERIAL', "Surface")
        else:
            layout.prop(mat, "diffuse_color", text="Base Color")
            layout.prop(mat, "metallic")
            layout.prop(mat, "specular_intensity", text="Specular")
            layout.prop(mat, "roughness")
# ------------------------------------------------------------------------------
# Volume Panel

class EEVEE_MATERIAL_PT_ab_volume(MaterialButtonsPanel, Panel):
    bl_label = "Volume"
    bl_context = "material"
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'BLENDER_EEVEE'}

    @classmethod
    def poll(cls, context):
        engine = context.engine
        mat = bpy.context.active_object.active_material
        return mat and mat.use_nodes and (engine in cls.COMPAT_ENGINES) and not mat.grease_pencil

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True

        mat = bpy.context.active_object.active_material

        panel_node_draw(layout, mat.node_tree, 'OUTPUT_MATERIAL', "Volume")
# ------------------------------------------------------------------------------
# Volume Panel

def draw_material_settings(self, context):
    layout = self.layout
    layout.use_property_split = True
    layout.use_property_decorate = False

    mat = bpy.context.active_object.active_material

    layout.prop(mat, "use_backface_culling")
    layout.prop(mat, "blend_method")
    layout.prop(mat, "shadow_method")

    row = layout.row()
    row.active = ((mat.blend_method == 'CLIP') or (mat.shadow_method == 'CLIP'))
    row.prop(mat, "alpha_threshold")

    if mat.blend_method not in {'OPAQUE', 'CLIP', 'HASHED'}:
        layout.prop(mat, "show_transparent_back")

    layout.prop(mat, "use_screen_refraction")
    layout.prop(mat, "refraction_depth")
    layout.prop(mat, "use_sss_translucency")
    layout.prop(mat, "pass_index")

class EEVEE_MATERIAL_PT_ab_settings(MaterialButtonsPanel, Panel):
    bl_label = "Settings"
    bl_context = "material"
    COMPAT_ENGINES = {'BLENDER_EEVEE'}

    def draw(self, context):
        draw_material_settings(self, context)
        
# ------------------------------------------------------------------------------
# Material Panel Viewport
        
class MATERIAL_PT_ab_viewport_settings(MaterialButtonsPanel, Panel):
    bl_label = "Settings"
    bl_context = "material"
    bl_parent_id = "MATERIAL_PT_ab_viewport"
    COMPAT_ENGINES = {'BLENDER_RENDER'}

    def draw(self, context):
        draw_material_settings(self, context)


class MATERIAL_PT_ab_viewport(MaterialButtonsPanel, Panel):
    bl_label = "Viewport Display"
    bl_context = "material"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 10

    @classmethod
    def poll(cls, context):
        mat = bpy.context.active_object.active_material
        return mat and not mat.grease_pencil

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        mat = bpy.context.active_object.active_material

        col = layout.column()
        col.prop(mat, "diffuse_color", text="Color")
        col.prop(mat, "metallic")
        col.prop(mat, "roughness")
# ------------------------------------------------------------------------------
# Material Panel Viewport

class MATERIAL_PT_ab_lineart(MaterialButtonsPanel, Panel):
    bl_label = "Line Art"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 10

    @classmethod
    def poll(cls, context):
        mat = bpy.context.active_object.active_material
        return mat and not mat.grease_pencil

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        mat = bpy.context.active_object.active_material
        lineart = mat.lineart

        layout.prop(lineart, "use_material_mask", text="Material Mask")

        col = layout.column(align=True)
        col.active = lineart.use_material_mask
        row = col.row(align=True, heading="Masks")
        for i in range(8):
            row.prop(lineart, "use_material_mask_bits", text=" ", index=i, toggle=True)
            if i == 3:
                row = col.row(align=True)

        row = layout.row(align=True, heading="Custom Occlusion")
        row.prop(lineart, "mat_occlusion", text="Levels")


# ------------------------------------------------------------------------------
# REGISTRATION AREA

def register():
    #Material Panel
    bpy.utils.register_class(MATERIAL_PT_abpanel)
    bpy.utils.register_class(MATERIAL_MT_ab_context_menu)
    bpy.utils.register_class(MATERIAL_UL_ab_matslots)
    bpy.utils.register_class(EEVEE_MATERIAL_PT_ab_context_material)
    bpy.utils.register_class(EEVEE_MATERIAL_PT_ab_surface)
    bpy.utils.register_class(EEVEE_MATERIAL_PT_ab_volume)
    bpy.utils.register_class(EEVEE_MATERIAL_PT_ab_settings)
    bpy.utils.register_class(MATERIAL_PT_ab_viewport)
    bpy.utils.register_class(MATERIAL_PT_ab_viewport_settings)
    bpy.utils.register_class(MATERIAL_PT_ab_lineart)
    bpy.utils.register_class(OBJECT_OT_CopyMaterial)
    bpy.utils.register_class(OBJECT_OT_PasteMaterial)
    
def unregister():
    #Material Panel
    bpy.utils.unregister_class(OBJECT_OT_PasteMaterial)
    bpy.utils.unregister_class(OBJECT_OT_CopyMaterial)
    bpy.utils.unregister_class(MATERIAL_PT_ab_lineart)
    bpy.utils.unregister_class(MATERIAL_PT_ab_viewport_settings)
    bpy.utils.unregister_class(MATERIAL_PT_ab_viewport)
    bpy.utils.unregister_class(EEVEE_MATERIAL_PT_ab_settings)
    bpy.utils.unregister_class(EEVEE_MATERIAL_PT_ab_volume)
    bpy.utils.unregister_class(EEVEE_MATERIAL_PT_ab_surface)
    bpy.utils.unregister_class(EEVEE_MATERIAL_PT_ab_context_material)
    bpy.utils.unregister_class(MATERIAL_UL_ab_matslots)
    bpy.utils.unregister_class(MATERIAL_MT_ab_context_menu)
    bpy.utils.unregister_class(MATERIAL_PT_abpanel)
