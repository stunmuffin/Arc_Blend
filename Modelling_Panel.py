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
# MODELLING PANEL

class MODELLING_PT_Panel(bpy.types.Panel):
    bl_label = "AB Modelling"
    bl_idname = "MODELLING_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_options = {'DEFAULT_CLOSED'}
    
        
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
            except (AttributeError,UnboundLocalError,TypeError,KeyError):
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
        len_mod = len(bpy.context.object.modifiers[:])
        if bpy.context.object.modifiers[:]==[]:
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
                active.select_set(True)
                new_collection = ensure_collection(context.scene, "AB_Cutters_Collection")
                bpy.context.object.modifiers[active_cutter].collection = bpy.data.collections["AB_Cutters_Collection"]
                for i in bpy.data.collections['AB_Cutters_Collection'].objects:
                    i.color = (1, 0.0252077, 0.021955, 0.342857)
                    i.display_type = 'WIRE'
        
        elif bpy.context.object.modifiers[:]!=[]:
                all_boolean_coll =[] 
                for mod in bpy.context.object.modifiers[:]:
                    if mod.type == "BOOLEAN" and mod.operand_type=="COLLECTION" and mod.collection == None:
                        bpy.ops.object.modifier_remove(modifier=mod.name)
                    collection_same=[]
                    if mod.type == "BOOLEAN" and mod.operand_type=="COLLECTION" and mod.collection != None:
                        collection_same.append(mod.name)
                    len_collection_same = len(collection_same)
                    count_collection=[]
                    for i in range(0,len_collection_same):
                       count_collection.append([collection_same.count("AB_Cutter_Collection"),collection_same[i]])
                    Cutter_collection_list = []
                    for i in count_collection:
                        if not i.count(1):
                            Cutter_collection_list.append(i)
                    for g in Cutter_collection_list:
                        bpy.ops.object.modifier_remove(modifier=g[1])
                        
                    
                    if mod.type == "BOOLEAN" and mod.operand_type == "COLLECTION":
                        all_boolean_coll.append(mod.name)
                if all_boolean_coll == []:
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
                    active.select_set(True)
                    new_collection = ensure_collection(context.scene, "AB_Cutters_Collection")
                    bpy.context.object.modifiers[active_cutter].collection = bpy.data.collections["AB_Cutters_Collection"]
                    for i in bpy.data.collections['AB_Cutters_Collection'].objects:
                        i.color = (1, 0.0252077, 0.021955, 0.342857)
                        i.display_type = 'WIRE'
                if all_boolean_coll != None:
                    bpy.context.object.modifiers["AB_Cutter_Collection"].collection = bpy.data.collections["AB_Cutters_Collection"]
                    for i in bpy.data.collections['AB_Cutters_Collection'].objects:
                        i.color = (1, 0.0252077, 0.021955, 0.342857)
                        i.display_type = 'WIRE'
        return {"FINISHED"}

# ------------------------------------------------------------------------------
# BOX CUTTER OBJECT


class cutter_box_object(bpy.types.Operator):
    """Cutter: Makes boolean modifier > named "AB_Cutter_Object" > Object Type operand > Object > Solver Fast"""
    bl_label = ""
    bl_idname = "object.button_cutter_box_object"
    
        
    def execute(self, context):
        if bpy.context.object.modifiers[:]==[]:
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
                active.select_set(True)
                bpy.context.object.modifiers[active_cutter].collection = bpy.data.collections["AB_Cutters_Object"]
            for i in range(0,leng) :
                bpy.context.object.modifiers["AB_Cutter_Object"+ str(i)].object = bpy.data.collections['AB_Cutters_Object'].objects[i]
                bpy.context.object.modifiers["AB_Cutter_Object"+ str(i)].object.color = (0.0517386, 0.70876, 1, 0.342857)
                bpy.context.object.modifiers["AB_Cutter_Object"+ str(i)].object.display_type = 'WIRE'
        elif bpy.context.object.modifiers[:]!=[]:
                leng = len(bpy.data.collections['AB_Cutters_Object'].objects)
                mod_list_object=[]
                for mod in bpy.context.object.modifiers[:]:
                    if mod.type == "BOOLEAN" and mod.operand_type=="OBJECT" and mod.object == None:
                        mod_list_object.append(mod.name)
                len_mod_list_object= len(mod_list_object)
                count_object=[]
                for i in range(0,len_mod_list_object):
                   count_object.append([mod_list_object.count("AB_Cutter_Object"+str(i)),mod_list_object[i]])
                Cutter_object_list = []
                for i in count_object:
                    if not i.count(1):
                        Cutter_object_list.append(i)
                for j in Cutter_object_list:
                    bpy.ops.object.modifier_remove(modifier=j[1])
                len_mod_object_count = []
                for mod in bpy.context.object.modifiers[:]:
                    if mod.type == "BOOLEAN" and mod.operand_type=="OBJECT" and mod.object != None:
                        len_mod_object_count.append(mod.name)
                len_len_mod_object_count = len(len_mod_object_count)
                if leng < len_len_mod_object_count:
                    for mod in len_mod_object_count:
                        bpy.ops.object.modifier_remove(modifier=mod)
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
                        active.select_set(True)
                        bpy.context.object.modifiers[active_cutter].collection = bpy.data.collections["AB_Cutters_Object"]
                    for i in range(0,leng) :
                        bpy.context.object.modifiers["AB_Cutter_Object"+ str(i)].object = bpy.data.collections['AB_Cutters_Object'].objects[i]
                        bpy.context.object.modifiers["AB_Cutter_Object"+ str(i)].object.color = (0.0517386, 0.70876, 1, 0.342857)
                        bpy.context.object.modifiers["AB_Cutter_Object"+ str(i)].object.display_type = 'WIRE'
                elif leng == len_len_mod_object_count:
                    for mod in len_mod_object_count:
                        bpy.ops.object.modifier_remove(modifier= mod)
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
                        active.select_set(True)
                        bpy.context.object.modifiers[active_cutter].collection = bpy.data.collections["AB_Cutters_Object"]
                    for i in range(0,leng) :
                        bpy.context.object.modifiers["AB_Cutter_Object"+ str(i)].object = bpy.data.collections['AB_Cutters_Object'].objects[i]
                        bpy.context.object.modifiers["AB_Cutter_Object"+ str(i)].object.color = (0.0517386, 0.70876, 1, 0.342857)
                        bpy.context.object.modifiers["AB_Cutter_Object"+ str(i)].object.display_type = 'WIRE'    
                elif leng > len_len_mod_object_count:
                    for mod in len_mod_object_count:
                        bpy.ops.object.modifier_remove(modifier= mod)
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
                        active.select_set(True)
                        bpy.context.object.modifiers[active_cutter].collection = bpy.data.collections["AB_Cutters_Object"]
                    for i in range(0,leng) :
                        bpy.context.object.modifiers["AB_Cutter_Object"+ str(i)].object = bpy.data.collections['AB_Cutters_Object'].objects[i]
                        bpy.context.object.modifiers["AB_Cutter_Object"+ str(i)].object.color = (0.0517386, 0.70876, 1, 0.342857)
                        bpy.context.object.modifiers["AB_Cutter_Object"+ str(i)].object.display_type = 'WIRE'
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


class MODELLING_PT_Vertex_Selection (bpy.types.Panel):
    bl_label = ""
    bl_idname = "MODELLING_PT_Vertex_Selection"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "MODELLING_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}

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

class MODELLING_PT_Vertex_Group_Panel (bpy.types.Panel):
    bl_label = ""
    bl_idname = "MODELLING_PT_Vertex_Group_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "MODELLING_PT_Vertex_Selection"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    bl_options = {'DEFAULT_CLOSED'}

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


class MODELLING_PT_Modify_Selection (bpy.types.Panel):
    bl_label = ""
    bl_idname = "MODELLING_PT_Modify_Selection"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "MODELLING_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}

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

class MODELLING_PT_Modify_Edit (bpy.types.Panel):
    bl_label = ""
    bl_idname = "MODELLING_PT_Modify_Edit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "MODELLING_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}

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

class MODELLING_PT_Modify_Edit_Faces (bpy.types.Panel):
    bl_label = ""
    bl_idname = "MODELLING_PT_Modify_Edit_Faces"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "MODELLING_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}

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


def register():
    bpy.utils.register_class(MODELLING_PT_Panel)
    bpy.utils.register_class(cutter_box)
    bpy.utils.register_class(cutter_box_object)
    bpy.utils.register_class(cutter_apply_modifier)
    bpy.utils.register_class(view_3d_top)
    bpy.utils.register_class(view_3d_bottom)
    bpy.utils.register_class(view_3d_front)
    bpy.utils.register_class(view_3d_back)
    bpy.utils.register_class(view_3d_right)
    bpy.utils.register_class(view_3d_left)
    bpy.utils.register_class(MODELLING_PT_Vertex_Selection)
    bpy.utils.register_class(vertex_selection_make_circle)
    bpy.utils.register_class(vertex_selection_rip_vertex)
    bpy.utils.register_class(vertex_selection_merge_vertex_last)
    bpy.utils.register_class(vertex_selection_dissolve_vertex)
    bpy.utils.register_class(vertex_selection_connect_vertex_path)
    bpy.utils.register_class(vertex_selection_create_vertices)
    bpy.utils.register_class(vertex_selection_assign_vertex_group)
    bpy.utils.register_class(MODELLING_PT_Vertex_Group_Panel)
    bpy.utils.register_class(MODELLING_PT_Modify_Selection)
    bpy.utils.register_class(loop_grow_edge_select)
    bpy.utils.register_class(loop_shrink_edge_select)
    bpy.utils.register_class(loop_auto_edge_loop)
    bpy.utils.register_class(MODELLING_PT_Modify_Edit_Faces)
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
    bpy.utils.register_class(MODELLING_PT_Modify_Edit)
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
   

 
  

def unregister():
    bpy.utils.unregister_class(MODELLING_PT_Panel)
    bpy.utils.unregister_class(cutter_box)
    bpy.utils.unregister_class(cutter_box_object)
    bpy.utils.unregister_class(cutter_apply_modifier)
    
    bpy.utils.unregister_class(view_3d_top)
    bpy.utils.unregister_class(view_3d_bottom)
    bpy.utils.unregister_class(view_3d_front)
    bpy.utils.unregister_class(view_3d_back)
    bpy.utils.unregister_class(view_3d_right)
    bpy.utils.unregister_class(view_3d_left)
    bpy.utils.unregister_class(MODELLING_PT_Vertex_Selection)
    bpy.utils.unregister_class(vertex_selection_make_circle)
    bpy.utils.unregister_class(vertex_selection_rip_vertex)
    bpy.utils.unregister_class(vertex_selection_merge_vertex_last)
    bpy.utils.unregister_class(vertex_selection_dissolve_vertex)
    bpy.utils.unregister_class(vertex_selection_connect_vertex_path)
    bpy.utils.unregister_class(vertex_selection_create_vertices)
    bpy.utils.unregister_class(vertex_selection_assign_vertex_group)
    bpy.utils.unregister_class(MODELLING_PT_Vertex_Group_Panel)
    bpy.utils.unregister_class(MODELLING_PT_Modify_Selection)
    bpy.utils.unregister_class(loop_grow_edge_select)
    bpy.utils.unregister_class(loop_shrink_edge_select)
    bpy.utils.unregister_class(loop_auto_edge_loop)
    bpy.utils.unregister_class(MODELLING_PT_Modify_Edit_Faces)
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
    bpy.utils.unregister_class(MODELLING_PT_Modify_Edit)
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
   