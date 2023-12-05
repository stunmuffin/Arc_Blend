import random
import sys
from mathutils import Matrix, Vector,Euler
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
# ARC BLEND MODIFIERS PANEL


class ARCBLENDMODIFIERS_PT_Panel (bpy.types.Panel):
    bl_label = "AB Modify"
    bl_idname = "ARCBLENDMODIFIERS_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_options = {'DEFAULT_CLOSED'}

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
# Export Object


class EXPORT_PT_Object (bpy.types.Panel):
    bl_label = "Export Object Data"
    bl_idname = "EXPORT_PT_Object"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "ARCBLENDMODIFIERS_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}

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


class MODIFIER_PT_Transform_And_Edit (bpy.types.Panel):
    bl_label = "Transform & Edit"
    bl_idname = "MODIFIER_PT_Transform_And_Edit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "ARCBLENDMODIFIERS_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        obj = context.object
        row = layout.row()

# ------------------------------------------------------------------------------
# OBJECT  PANEL


class TRANSFORM_PT_Edit_Object_Panel (bpy.types.Panel):
    bl_label = "Object"
    bl_idname = "TRANSFORM_PT_Edit_Object_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "MODIFIER_PT_Transform_And_Edit"
    bl_options = {'DEFAULT_CLOSED'}
    
    
    @classmethod
    def poll(cls, context):
        return context.object is not None  # Check if there's an active object


    def draw(self, context):
        layout = self.layout
        obj = context.object
        collection = context.collection
        scene = context.scene
        Arc_Blend = scene.Arc_Blend
        col = layout.column()
        alignment_list = bpy.context.scene.alignment_list
        
        col.prop(obj, "name")
        col.prop(obj, "type")
        col.prop(obj, "active_material")
        col.prop(obj, "data")
        col.prop(obj, "parent")
        col.prop(obj, "parent_type")
        
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
                    sub.prop(Arc_Blend, "use_grid_3d", text="Distribute in Grid 3D")
                    if Arc_Blend.use_grid_3d:
                        sub.prop(Arc_Blend, "distribute_x", text="X Copy : ")
                        sub.prop(Arc_Blend, "distribute_y", text="Y Copy : ")
                        sub.prop(Arc_Blend, "distribute_z", text="Z Copy : ")
                        sub = box.column(align=True)
                        sub.label(text="Distribute Distance : ")
                        sub.prop(Arc_Blend, "x_distance")
                        sub.prop(Arc_Blend, "y_distance")
                        sub.prop(Arc_Blend, "z_distance")  
                        sub.operator("object.distribute_grid_3d", text="Distribute in Grid 3D")    
                    sub.prop(Arc_Blend, "use_circle", text="Distribute in Circle")
                    if Arc_Blend.use_circle:
                        sub.prop(Arc_Blend, "radius")
                        sub.operator("object.distribute_circle", text="Distribute in Circle")
                    sub.prop(Arc_Blend, "use_square", text="Distribute in Square")
                    if Arc_Blend.use_square:
                        sub.prop(Arc_Blend, "square_length")
                        sub.operator("object.distribute_square", text="Distribute in Square")
                    sub.prop(Arc_Blend, "use_arc", text="Distribute in Arc")
                    if Arc_Blend.use_arc:
                        sub.prop(Arc_Blend, "radius_arc")
                        sub.prop(Arc_Blend, "start_angle")
                        sub.prop(Arc_Blend, "end_angle")
                        sub.operator("object.distribute_arc", text="Distribute in Arc")
                    sub.prop(Arc_Blend, "use_curve", text="Distribute on Curve")
                    if Arc_Blend.use_curve:
                        sub.prop(Arc_Blend, "curve_object")
                        sub.operator("object.distribute_curve", text="Distribute Along Curve Segments")
                    sub.prop(Arc_Blend, "use_vertices", text="Distribute on Mesh")
                    if Arc_Blend.use_vertices:
                        sub.prop(Arc_Blend, "mesh_object")
                        sub.operator("object.distribute_on_vertices", text="Distribute Along Mesh Vertices")
                        sub.operator("object.distribute_on_vertices_rotated", text="Distribute Vertices (Rotated)")
                        sub.operator("object.distribute_on_edges", text="Distribute Along Mesh Edges")
                        sub.operator("object.distribute_on_edgesrotated", text="Distribute Edges (Rotated)")
                        sub.operator("object.distribute_on_faces", text="Distribute on Faces")
                        sub.operator("object.distribute_on_facesrotated", text="Distribute on Faces (Rotated)")
                else:
                    pass
                
                box.prop(Arc_Blend, "align_objects_panel",
                         text="Align Tools ", icon="ALIGN_JUSTIFY")
                if bpy.context.scene.Arc_Blend.align_objects_panel:
                    alignment_list = bpy.context.scene.alignment_list
                    col = layout.column()
                    box = layout.box()

                    # Main Label: Align Position (World)
                    box.label(text="Align Position (Global)", icon='WORLD_DATA')

                    # Features X Y Z check box
                    row = box.row()
                    
                    row.prop(alignment_list, "align_position_x" , text= "X")
                    row.prop(alignment_list, "align_position_y" , text= "Y")
                    row.prop(alignment_list, "align_position_z" , text= "Z")
                    
                    

                    # Align Position Options: Minimum, Center, Origin, Maximum
                    box.label(text="Align Position Options:")
                    
                    box.prop(alignment_list, "selected_alignment", text="Selected Object")
                    box.prop(alignment_list, "target_alignment", text="Target Object")
                    
                    box.operator("object.align_objects", text= "Align")

                        

                    box.prop(alignment_list, "target_objects")
                    

                    # Align Orientation (Local) X Y Z check box
                    box.label(text="Align Orientation (Local)")
                    row = box.row()
                    row.prop(alignment_list, "align_orientation_x", text= "X")
                    row.prop(alignment_list, "align_orientation_y", text= "Y")
                    row.prop(alignment_list, "align_orientation_z", text= "Z")

                    # Match Scale: X Y Z
                    box.label(text="Match Scale:")
                    row = box.row()
                    row.prop(alignment_list, "match_scale_x", text= "X")
                    row.prop(alignment_list, "match_scale_y", text= "Y")
                    row.prop(alignment_list, "match_scale_z", text= "Z")
                    
                    
                         
                box.prop(Arc_Blend, "proportional_align",
                         text="Proportional Align ", icon="SORTSIZE")
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
        if obj is not None:
                layout.prop(obj, "color", text="Object Color")
        else:
                layout.label(text="No object selected")
        row = layout.row()
        row = layout.row(align=True)
        row.operator(
                "object.button_transform_edit_object_randomize_colors", text="Randomize Colors")
        row.operator(
                "object.button_transform_edit_object_reset_colors", text="Reset Colors")
        
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
        
        if active is None:
            self.report({'ERROR'}, "No active object. Select an active object.")
            return {'CANCELLED'}
        
        for obj in selected:
            if obj and hasattr(obj, 'location'):
                obj.location.x = active.location.x
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
        if active is None:
            self.report({'ERROR'}, "No active object. Select an active object.")
            return {'CANCELLED'}
        
        for obj in selected:
            if obj and hasattr(obj, 'location'):
                obj.location.y = active.location.y
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
        if active is None:
            self.report({'ERROR'}, "No active object. Select an active object.")
            return {'CANCELLED'}
        
        for obj in selected:
            if obj and hasattr(obj, 'location'):
                obj.location.z = active.location.z
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


class TRANSFORM_PT_Panel (bpy.types.Panel):
    bl_label = "Transform"
    bl_idname = "TRANSFORM_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "MODIFIER_PT_Transform_And_Edit"
    bl_options = {'DEFAULT_CLOSED'}

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
# AB ALIGN TOOL UPDATES

# Store initial rotations
initial_rotations = {}

def update_align_orientation_x(self, context):
    global initial_rotations
    # Access the selected objects and target object
    selected_objects = bpy.context.selected_objects
    target_object = bpy.context.scene.alignment_list.target_objects

    # Update or reset rotation based on align_orientation_x
    for obj in selected_objects:
        if self.align_orientation_x:
            # Store initial rotation if not already stored
            if obj.name not in initial_rotations:
                initial_rotations[obj.name] = obj.rotation_euler.copy()

            current_rotation = obj.rotation_euler

            obj.rotation_euler = Euler((target_object.rotation_euler.x, current_rotation.y, current_rotation.z))
        else:
            # Reset rotation to initial value if checkbox is unchecked
            if obj.name in initial_rotations:
                obj.rotation_euler = initial_rotations[obj.name]

    # Trigger update of the 3D view
    bpy.context.view_layer.update()

def update_align_orientation_y(self, context):
    global initial_rotations
    selected_objects = bpy.context.selected_objects
    target_object = bpy.context.scene.alignment_list.target_objects

    for obj in selected_objects:
        if self.align_orientation_y:
            if obj.name not in initial_rotations:
                initial_rotations[obj.name] = obj.rotation_euler.copy()

            current_rotation = obj.rotation_euler

            obj.rotation_euler = Euler((current_rotation.x, target_object.rotation_euler.y, current_rotation.z))
        else:
            if obj.name in initial_rotations:
                obj.rotation_euler = initial_rotations[obj.name]

    bpy.context.view_layer.update()

def update_align_orientation_z(self, context):
    global initial_rotations
    selected_objects = bpy.context.selected_objects
    target_object = bpy.context.scene.alignment_list.target_objects

    for obj in selected_objects:
        if self.align_orientation_z:
            if obj.name not in initial_rotations:
                initial_rotations[obj.name] = obj.rotation_euler.copy()

            current_rotation = obj.rotation_euler

            obj.rotation_euler = Euler((current_rotation.x, current_rotation.y, target_object.rotation_euler.z))
        else:
            if obj.name in initial_rotations:
                obj.rotation_euler = initial_rotations[obj.name]

    bpy.context.view_layer.update()


initial_scales = {}  # Define initial_scales dictionary outside any function or class scope

# Then use the update_match_scale_x function as previously shown
def update_match_scale_x(self, context):
    global initial_scales
    selected_objects = bpy.context.selected_objects
    target_object = bpy.context.scene.alignment_list.target_objects

    for obj in selected_objects:
        if self.match_scale_x:
            if obj.name not in initial_scales:
                initial_scales[obj.name] = obj.scale.copy()

            obj.scale.x = target_object.scale.x
        else:
            if obj.name in initial_scales:
                obj.scale.x = initial_scales[obj.name].x

    bpy.context.view_layer.update()


def update_match_scale_y(self, context):
    global initial_scales
    selected_objects = bpy.context.selected_objects
    target_object = bpy.context.scene.alignment_list.target_objects

    for obj in selected_objects:
        if self.match_scale_y:
            if obj.name not in initial_scales:
                initial_scales[obj.name] = obj.scale.copy()

            obj.scale.y = target_object.scale.y
        else:
            if obj.name in initial_scales:
                obj.scale.y = initial_scales[obj.name].y

    bpy.context.view_layer.update()

def update_match_scale_z(self, context):
    global initial_scales
    selected_objects = bpy.context.selected_objects
    target_object = bpy.context.scene.alignment_list.target_objects

    for obj in selected_objects:
        if self.match_scale_z:
            if obj.name not in initial_scales:
                initial_scales[obj.name] = obj.scale.copy()

            obj.scale.z = target_object.scale.z
        else:
            if obj.name in initial_scales:
                obj.scale.z = initial_scales[obj.name].z

    bpy.context.view_layer.update()




class AlignPropertiesGroup(bpy.types.PropertyGroup):

    x_copies: bpy.props.IntProperty(
        name="X Copies",
        default=1,
        min=0,
        description="Distribute X Copy"
        )

    x_distance: bpy.props.FloatProperty(
        name="X Distance",
        default=3.0,
        min=0,
        description="X Distance"
        )

    end_angle: bpy.props.StringProperty(
        name="End Angle",
        default="math.pi",
        description="End angle for distribution",
    )
    
    target_objects: bpy.props.PointerProperty(
    type=bpy.types.Object,
    name="Target Object",
    description="Select the Curve Object",
    )
  
    align_position_x: bpy.props.BoolProperty(
        name="Align Position X",
        default=False,
        description="Aligns X Position",
    )
    
    align_position_y: bpy.props.BoolProperty(
        name="Align Position Y",
        default=False,
        description="Aligns Y Position",
    )
    
    align_position_z: bpy.props.BoolProperty(
        name="Align Position Z",
        default=False,
        description="Aligns Z Position",
    )
    
    align_orientation_x: bpy.props.BoolProperty(
        name="Align Orientation X",
        default=False,
        description="Aligns X Orientation",
        update=update_align_orientation_x
    )
    
    align_orientation_y: bpy.props.BoolProperty(
        name="Align Orientation Y",
        default=False,
        description="AlignsY Orientation",
        update=update_align_orientation_y
    )
    
    align_orientation_z: bpy.props.BoolProperty(
        name="Align Orientation Z",
        default=False,
        description="Aligns Z Orientation",
        update=update_align_orientation_z
    )
    
    match_scale_x : bpy.props.BoolProperty(
        name="Align Match Scale X",
        default=False,
        description="Aligns Match Scales X",
        update=update_match_scale_x
    )
    
    match_scale_y : bpy.props.BoolProperty(
        name="Align Match Scale Y",
        default=False,
        description="Aligns Match Scales Y",
        update=update_match_scale_y
    )
    
    match_scale_z : bpy.props.BoolProperty(
        name="Align Match Scale Z",
        default=False,
        description="Aligns Match Scales Z",
        update=update_match_scale_z
    )
    
    selected_alignment: bpy.props.EnumProperty(
        items=[
            ('MINIMUM', 'Minimum', ''),
            ('CENTER', 'Center', ''),
            ('ORIGINS', 'Origins', ''),
            ('MAXIMUM', 'Maximum', '')
        ],
        name="Selected Alignment",
        description="Select the alignment type",
        default='MINIMUM'
    )
    
    target_alignment: bpy.props.EnumProperty(
        items=[
            ('MINIMUM', 'Minimum', ''),
            ('CENTER', 'Center', ''),
            ('ORIGINS', 'Origins', ''),
            ('MAXIMUM', 'Maximum', '')
        ],
        name="Target Alignment",
        description="Select the alignment type",
        default='MINIMUM'
    )



class OBJECT_OT_AlignOperator(bpy.types.Operator):
    bl_idname = "object.align_objects"
    bl_label = "Align Objects"
    
    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        current_objs = bpy.context.selected_objects
        target_obj_name = bpy.context.scene.alignment_list.target_objects.name
        # Get the target object
        target_object = bpy.context.scene.alignment_list.target_objects
        target_obj = bpy.context.scene.alignment_list.target_objects
        

        selected_alignment = bpy.context.scene.alignment_list.selected_alignment
        target_alignment= bpy.context.scene.alignment_list.target_alignment
        align_x = bpy.context.scene.alignment_list.align_position_x
        align_y = bpy.context.scene.alignment_list.align_position_y
        align_z = bpy.context.scene.alignment_list.align_position_z
        align_orientation_x = bpy.context.scene.alignment_list.align_orientation_x
        align_orientation_y = bpy.context.scene.alignment_list.align_orientation_y
        align_orientation_z = bpy.context.scene.alignment_list.align_orientation_z
        match_scale_x = bpy.context.scene.alignment_list.match_scale_x
        match_scale_y = bpy.context.scene.alignment_list.match_scale_y
        match_scale_z = bpy.context.scene.alignment_list.match_scale_z

        
        
        # Check if the selected and target alignments are both set to 'MINIMUM'
        if selected_alignment == 'MINIMUM' and target_alignment == 'MINIMUM':
            if target_object and target_object.location:
                # Get the target object's world matrix and bounding box
                target_matrix = target_object.matrix_world
                target_local_verts = [Vector(v[:]) for v in target_object.bound_box]
                target_world_verts = [target_matrix @ v for v in target_local_verts]
                
                # Find the minimum X, Y, and Z-coordinates among the target object's bounding box vertices
                target_min_x = min(v.x for v in target_world_verts)
                target_min_y = min(v.y for v in target_world_verts)
                target_min_z = min(v.z for v in target_world_verts)
                
                for obj in selected_objects:
                    # Get the object's world matrix and bounding box
                    obj_matrix = obj.matrix_world
                    obj_local_verts = [Vector(v[:]) for v in obj.bound_box]
                    obj_world_verts = [obj_matrix @ v for v in obj_local_verts]
                    
                    # Find the minimum X, Y, and Z-coordinates among the bounding box vertices
                    obj_min_x = min(v.x for v in obj_world_verts)
                    obj_min_y = min(v.y for v in obj_world_verts)
                    obj_min_z = min(v.z for v in obj_world_verts)
                    
                    # Calculate the differences in X, Y, and Z-coordinates
                    x_diff = target_min_x - obj_min_x if align_x else 0.0
                    y_diff = target_min_y - obj_min_y if align_y else 0.0
                    z_diff = target_min_z - obj_min_z if align_z else 0.0
                    
                    # Translate the object by the calculated differences in coordinates
                    obj.location.x += x_diff
                    obj.location.y += y_diff
                    obj.location.z += z_diff

            else:
                print("Target object not found or has no location.")
            
            
        elif selected_alignment == 'MINIMUM' and target_alignment == 'CENTER':
                if target_object:
                    target_location = target_object.location
                    if target_location:
                        # Get the target object's world matrix and bounding box
                        target_matrix = target_object.matrix_world
                        target_local_verts = [Vector(v[:]) for v in target_object.bound_box]
                        target_world_verts = [target_matrix @ v for v in target_local_verts]
                        
                        # Find the center coordinates of the target object's bounding box
                        target_center = sum(target_world_verts, Vector()) / 8  # Center of the target object
                        
                        for obj in selected_objects:
                            obj_matrix = obj.matrix_world
                            obj_local_verts = [Vector(v[:]) for v in obj.bound_box]
                            obj_world_verts = [obj_matrix @ v for v in obj_local_verts]
                            
                            # Find the minimum X, Y, and Z-coordinates among the bounding box vertices
                            obj_min_x = min(v.x for v in obj_world_verts)
                            obj_min_y = min(v.y for v in obj_world_verts)
                            obj_min_z = min(v.z for v in obj_world_verts)
                            
                            # Calculate the differences in X, Y, and Z-coordinates
                            x_diff = target_center.x - obj_min_x if align_x else 0.0
                            y_diff = target_center.y - obj_min_y if align_y else 0.0
                            z_diff = target_center.z - obj_min_z if align_z else 0.0
                            
                            # Translate the object by the calculated differences in coordinates
                            obj.location.x += x_diff
                            obj.location.y += y_diff
                            obj.location.z += z_diff
                    else:
                        print("Target object has no location.")
                else:
                    print("Target object not found.")
        
        elif selected_alignment == 'MINIMUM' and target_alignment == 'ORIGINS':
            if target_object:
                # Get the target object's origin location
                target_origin = target_object.location
                
                for obj in selected_objects:
                    # Get the object's bounding box in world coordinates
                    world_verts = [obj.matrix_world @ Vector(point) for point in obj.bound_box]
                    
                    # Find the minimum coordinates among the bounding box vertices
                    obj_min_x = min(v.x for v in world_verts)
                    obj_min_y = min(v.y for v in world_verts)
                    obj_min_z = min(v.z for v in world_verts)
                    
                    # Calculate the differences in X, Y, and Z-coordinates
                    x_diff = target_origin.x - obj_min_x if align_x else 0.0
                    y_diff = target_origin.y - obj_min_y if align_y else 0.0
                    z_diff = target_origin.z - obj_min_z if align_z else 0.0
                    
                    # Translate the object by the calculated differences in coordinates
                    obj.location.x += x_diff
                    obj.location.y += y_diff
                    obj.location.z += z_diff
            else:
                print("Target object not found.")
                
        elif selected_alignment == 'MINIMUM' and target_alignment == 'MAXIMUM':
            if target_object:
                # Get the target object's bounding box in world coordinates
                target_verts = [target_object.matrix_world @ Vector(point) for point in target_object.bound_box]
                
                # Find the maximum coordinates among the target object's bounding box vertices
                target_max_x = max(v.x for v in target_verts)
                target_max_y = max(v.y for v in target_verts)
                target_max_z = max(v.z for v in target_verts)
                
                for obj in selected_objects:
                    # Get the object's bounding box in world coordinates
                    world_verts = [obj.matrix_world @ Vector(point) for point in obj.bound_box]
                    
                    # Find the minimum coordinates among the bounding box vertices
                    obj_min_x = min(v.x for v in world_verts)
                    obj_min_y = min(v.y for v in world_verts)
                    obj_min_z = min(v.z for v in world_verts)
                    
                    # Calculate the differences in X, Y, and Z-coordinates
                    x_diff = target_max_x - obj_min_x if align_x else 0.0
                    y_diff = target_max_y - obj_min_y if align_y else 0.0
                    z_diff = target_max_z - obj_min_z if align_z else 0.0
                    
                    # Translate the object by the calculated differences in coordinates
                    obj.location.x += x_diff
                    obj.location.y += y_diff
                    obj.location.z += z_diff
            else:
                print("Target object not found.")
                
                
        elif selected_alignment == 'CENTER' and target_alignment == 'MINIMUM':
                if target_object:
                    # Get the target object's bounding box in world coordinates
                    target_verts = [target_object.matrix_world @ Vector(point) for point in target_object.bound_box]
                    
                    # Find the minimum coordinates among the target object's bounding box vertices
                    target_min_x = min(v.x for v in target_verts)
                    target_min_y = min(v.y for v in target_verts)
                    target_min_z = min(v.z for v in target_verts)
                    
                    for obj in selected_objects:
                        # Get the object's bounding box in world coordinates
                        world_verts = [obj.matrix_world @ Vector(point) for point in obj.bound_box]
                        
                        # Calculate the center coordinates of the object's bounding box
                        obj_center = sum(world_verts, Vector()) / 8
                        
                        # Calculate the differences in X, Y, and Z-coordinates
                        x_diff = target_min_x - obj_center.x if align_x else 0.0
                        y_diff = target_min_y - obj_center.y if align_y else 0.0
                        z_diff = target_min_z - obj_center.z if align_z else 0.0
                        
                        # Translate the object by the calculated differences in coordinates
                        obj.location.x += x_diff
                        obj.location.y += y_diff
                        obj.location.z += z_diff
                else:
                     print("Target object not found.")
                     
                     
        elif selected_alignment == 'CENTER' and target_alignment == 'CENTER':
            if target_object:
                # Get the target object's bounding box in world coordinates
                target_verts = [target_object.matrix_world @ Vector(point) for point in target_object.bound_box]
                
                # Calculate the center coordinates of the target object's bounding box
                target_center = sum(target_verts, Vector()) / 8
                
                for obj in selected_objects:
                    # Get the object's bounding box in world coordinates
                    world_verts = [obj.matrix_world @ Vector(point) for point in obj.bound_box]
                    
                    # Calculate the center coordinates of the object's bounding box
                    obj_center = sum(world_verts, Vector()) / 8
                    
                    # Calculate the differences in X, Y, and Z-coordinates
                    x_diff = target_center.x - obj_center.x if align_x else 0.0
                    y_diff = target_center.y - obj_center.y if align_y else 0.0
                    z_diff = target_center.z - obj_center.z if align_z else 0.0
                    
                    # Translate the object by the calculated differences in coordinates
                    obj.location.x += x_diff
                    obj.location.y += y_diff
                    obj.location.z += z_diff
            else:
                print("Target object not found.")
                
        elif selected_alignment == 'CENTER' and target_alignment == 'ORIGINS':
            if target_object:
                # Get the target object's origin
                target_origin = target_object.location
                
                for obj in selected_objects:
                    # Calculate the center coordinates of the object's bounding box
                    world_verts = [obj.matrix_world @ Vector(point) for point in obj.bound_box]
                    obj_center = sum(world_verts, Vector()) / 8
                    
                    # Calculate the differences in X, Y, and Z-coordinates
                    x_diff = target_origin.x - obj_center.x if align_x else 0.0
                    y_diff = target_origin.y - obj_center.y if align_y else 0.0
                    z_diff = target_origin.z - obj_center.z if align_z else 0.0
                    
                    # Translate the object by the calculated differences in coordinates
                    obj.location.x += x_diff
                    obj.location.y += y_diff
                    obj.location.z += z_diff
            else:
                print("Target object not found.")
                
                
        elif selected_alignment == 'CENTER' and target_alignment == 'MAXIMUM' and target_object:
                # Get the target object's bounding box in world coordinates
                target_verts = [target_object.matrix_world @ Vector(point) for point in target_object.bound_box]
                
                # Find the maximum coordinates among the bounding box vertices of the target object
                target_max_x = max(v.x for v in target_verts)
                target_max_y = max(v.y for v in target_verts)
                target_max_z = max(v.z for v in target_verts)
                
                # Calculate the center of the target object's bounding box
                target_center = sum(target_verts, Vector()) / 8  # Assuming a bounding box with 8 vertices
                
                for obj in selected_objects:
                    # Get the object's bounding box in world coordinates
                    obj_verts = [obj.matrix_world @ Vector(point) for point in obj.bound_box]
                    
                    # Find the center coordinates of the object
                    obj_center = sum(obj_verts, Vector()) / 8  # Assuming a bounding box with 8 vertices
                    
                    # Calculate the differences in X, Y, and Z-coordinates from the object's center to the target's maximum
                    x_diff = target_max_x - obj_center.x if align_x else 0.0
                    y_diff = target_max_y - obj_center.y if align_y else 0.0
                    z_diff = target_max_z - obj_center.z if align_z else 0.0
                    
                    # Translate the object by the calculated differences in coordinates
                    obj.location.x += x_diff
                    obj.location.y += y_diff
                    obj.location.z += z_diff
                    
        elif selected_alignment == 'ORIGINS' and target_alignment == 'MINIMUM' and target_object:
            # Get the target object's minimum location
            target_min = target_object.matrix_world @ Vector(target_object.bound_box[0])
            
            for obj in selected_objects:
                # Get the object's origin location
                obj_origin = obj.matrix_world.translation
                
                # Calculate the differences in X, Y, and Z-coordinates from the object's origin to target's minimum
                x_diff = target_min.x - obj_origin.x if align_x else 0.0
                y_diff = target_min.y - obj_origin.y if align_y else 0.0
                z_diff = target_min.z - obj_origin.z if align_z else 0.0
                
                # Translate the object by the calculated differences in coordinates
                obj.location.x += x_diff
                obj.location.y += y_diff
                obj.location.z += z_diff
                
        elif selected_alignment == 'ORIGINS' and target_alignment == 'CENTER' and target_object:
            # Get the target object's center location
            target_center = target_object.location
            
            for obj in selected_objects:
                # Get the object's origin location
                obj_origin = obj.matrix_world.translation
                
                # Calculate the differences in X, Y, and Z-coordinates from the object's origin to target's center
                x_diff = target_center.x - obj_origin.x if align_x else 0.0
                y_diff = target_center.y - obj_origin.y if align_y else 0.0
                z_diff = target_center.z - obj_origin.z if align_z else 0.0
                
                # Translate the object by the calculated differences in coordinates
                obj.location.x += x_diff
                obj.location.y += y_diff
                obj.location.z += z_diff
                
        elif selected_alignment == 'ORIGINS' and target_alignment == 'ORIGINS' and target_object:
            # Get the target object's origin location
            target_origin = target_object.matrix_world.translation
            
            for obj in selected_objects:
                # Get the object's origin location
                obj_origin = obj.matrix_world.translation
                
                # Calculate the differences in X, Y, and Z-coordinates from the object's origin to target's origin
                x_diff = target_origin.x - obj_origin.x if align_x else 0.0
                y_diff = target_origin.y - obj_origin.y if align_y else 0.0
                z_diff = target_origin.z - obj_origin.z if align_z else 0.0
                
                # Translate the object by the calculated differences in coordinates
                obj.location.x += x_diff
                obj.location.y += y_diff
                obj.location.z += z_diff


                
        elif selected_alignment == 'ORIGINS' and target_alignment == 'MAXIMUM' and target_object:
            # Get the maximum point of the target object
            target_verts = [target_object.matrix_world @ Vector(point) for point in target_object.bound_box]
            target_max = Vector((max(v.x for v in target_verts), max(v.y for v in target_verts), max(v.z for v in target_verts)))
            
            for obj in selected_objects:
                # Get the object's origin location
                obj_origin = obj.matrix_world.translation
                
                # Calculate the differences in X, Y, and Z-coordinates from the object's origin to target's maximum
                x_diff = target_max.x - obj_origin.x if align_x else 0.0
                y_diff = target_max.y - obj_origin.y if align_y else 0.0
                z_diff = target_max.z - obj_origin.z if align_z else 0.0
                
                # Translate the object by the calculated differences in coordinates
                obj.location.x += x_diff
                obj.location.y += y_diff
                obj.location.z += z_diff
                
        elif selected_alignment == 'MAXIMUM' and target_alignment == 'MINIMUM':
            if target_object:
                # Get the target object's bounding box in world coordinates
                target_verts = [target_object.matrix_world @ Vector(point) for point in target_object.bound_box]
                
                # Find the minimum coordinates among the target object's bounding box vertices
                target_min_x = min(v.x for v in target_verts)
                target_min_y = min(v.y for v in target_verts)
                target_min_z = min(v.z for v in target_verts)
                
                for obj in selected_objects:
                    # Get the object's bounding box in world coordinates
                    world_verts = [obj.matrix_world @ Vector(point) for point in obj.bound_box]
                    
                    # Find the maximum coordinates among the bounding box vertices
                    obj_max_x = max(v.x for v in world_verts)
                    obj_max_y = max(v.y for v in world_verts)
                    obj_max_z = max(v.z for v in world_verts)
                    
                    # Calculate the differences in X, Y, and Z-coordinates
                    x_diff = target_min_x - obj_max_x if align_x else 0.0
                    y_diff = target_min_y - obj_max_y if align_y else 0.0
                    z_diff = target_min_z - obj_max_z if align_z else 0.0
                    
                    # Translate the object by the calculated differences in coordinates
                    obj.location.x += x_diff
                    obj.location.y += y_diff
                    obj.location.z += z_diff
                
        elif selected_alignment == 'MAXIMUM' and target_alignment == 'CENTER' and target_object:
            # Get the target object's center location
            target_center = target_object.location
            
            for obj in selected_objects:
                # Get the object's bounding box in world coordinates
                obj_verts = [obj.matrix_world @ Vector(point) for point in obj.bound_box]
                
                # Find the maximum coordinates among the bounding box vertices of each selected object
                obj_max_x = max(v.x for v in obj_verts)
                obj_max_y = max(v.y for v in obj_verts)
                obj_max_z = max(v.z for v in obj_verts)
                
                # Calculate the differences in X, Y, and Z-coordinates from the object's maximum to target's center
                x_diff = target_center.x - obj_max_x if align_x else 0.0
                y_diff = target_center.y - obj_max_y if align_y else 0.0
                z_diff = target_center.z - obj_max_z if align_z else 0.0
                
                # Translate the object by the calculated differences in coordinates
                obj.location.x += x_diff
                obj.location.y += y_diff
                obj.location.z += z_diff
                
        elif selected_alignment == 'MAXIMUM' and target_alignment == 'ORIGINS' and target_object:
            # Get the target object's origin location
            target_origin = target_object.location
            
            for obj in selected_objects:
                # Get the object's bounding box in world coordinates
                obj_verts = [obj.matrix_world @ Vector(point) for point in obj.bound_box]
                
                # Find the maximum coordinates among the bounding box vertices of each selected object
                obj_max_x = max(v.x for v in obj_verts)
                obj_max_y = max(v.y for v in obj_verts)
                obj_max_z = max(v.z for v in obj_verts)
                
                # Calculate the differences in X, Y, and Z-coordinates from the object's maximum to target's origin
                x_diff = target_origin.x - obj_max_x if align_x else 0.0
                y_diff = target_origin.y - obj_max_y if align_y else 0.0
                z_diff = target_origin.z - obj_max_z if align_z else 0.0
                
                # Translate the object by the calculated differences in coordinates
                obj.location.x += x_diff
                obj.location.y += y_diff
                obj.location.z += z_diff
                
        elif selected_alignment == 'MAXIMUM' and target_alignment == 'MAXIMUM' and target_object:
            # Get the target object's bounding box in world coordinates
            target_verts = [target_object.matrix_world @ Vector(point) for point in target_object.bound_box]
            
            # Find the maximum coordinates among the target object's bounding box vertices
            target_max_x = max(v.x for v in target_verts)
            target_max_y = max(v.y for v in target_verts)
            target_max_z = max(v.z for v in target_verts)
            
            for obj in selected_objects:
                # Get the object's bounding box in world coordinates
                obj_verts = [obj.matrix_world @ Vector(point) for point in obj.bound_box]
                
                # Find the maximum coordinates among the bounding box vertices of each selected object
                obj_max_x = max(v.x for v in obj_verts)
                obj_max_y = max(v.y for v in obj_verts)
                obj_max_z = max(v.z for v in obj_verts)
                
                # Calculate the differences in X, Y, and Z-coordinates from the object's maximum to target's maximum
                x_diff = target_max_x - obj_max_x if align_x else 0.0
                y_diff = target_max_y - obj_max_y if align_y else 0.0
                z_diff = target_max_z - obj_max_z if align_z else 0.0
                
                # Translate the object by the calculated differences in coordinates
                obj.location.x += x_diff
                obj.location.y += y_diff
                obj.location.z += z_diff
        else:
            print("Target object not found or alignment scenario not supported.")
        
        return {'FINISHED'}
















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
        name="Z level", soft_min=0, soft_max=100, update=origin_set_manuel_upd, subtype="PERCENTAGE")
    arc_blend_manuel_origin_y: bpy.props.IntProperty(
        name="Y level", soft_min=0, soft_max=100, update=origin_set_manuel_upd_y, subtype="PERCENTAGE")
    arc_blend_manuel_origin_x: bpy.props.IntProperty(
        name="X level", soft_min=0, soft_max=100, update=origin_set_manuel_upd_x, subtype="PERCENTAGE")
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
        name="Distance Object X", soft_min=0, soft_max=100)
    distance_object_y: bpy.props.FloatProperty(
        name="Distance Object Y", soft_min=0, soft_max=100)
    distance_object_z: bpy.props.FloatProperty(
        name="Distance Object Z", soft_min=0, soft_max=100)
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
    distance_object_x: bpy.props.FloatProperty(
        name="Distance Object X", soft_min=0, soft_max=100, update=distance_object_x_upd)
    distance_object_y: bpy.props.FloatProperty(
        name="Distance Object Y", soft_min=0, soft_max=100, update=distance_object_y_upd)
    distance_object_z: bpy.props.FloatProperty(
        name="Distance Object Z", soft_min=0, soft_max=100, update=distance_object_z_upd)
    # ----------Distribute Objects-----------------------------
    distribute_x: bpy.props.IntProperty(
        name="Distribute Object X", min=0, max=10000, default=1)
    distribute_y: bpy.props.IntProperty(
        name="Distribute Object Y", min=0, max=10000, default=1)
    distribute_z: bpy.props.IntProperty(
        name="Distribute Object Z", min=1, max=10000 , default=1)
    distribute_objects: bpy.props.BoolProperty(
        name="Distribute Objects : ", default=False)
    align_objects_panel: bpy.props.BoolProperty(
        name="Align Objects : ", default=False)
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
    
    
    x_distance: bpy.props.FloatProperty(
        name="X Distance",
        default=3.0,
        min=0,
        description="X Distance"
        )
    y_distance: bpy.props.FloatProperty(
        name="Y Distance",
        default=3.0,
        min=0,
        description="Y Distance"
        )
    z_distance: bpy.props.FloatProperty(
        name="Z Distance",
        default=3.0,
        min=0,
        description="Z Distance"
        )
    
    
    radius: bpy.props.FloatProperty(
        name="Radius Circle",
        default=3.0,
        min=0,
        description="Distribute the Circle Radius"
        )
    square_length: bpy.props.FloatProperty(
        name="Square Length",
        default=3.0,
        min=0,
        description="Distribute the Square Length"
        )
    radius_arc:bpy.props.FloatProperty(
        name="Radius Arc",
        default=3.0,
        min=0,
        description="Distribute Radius Arc"
        )
    start_angle :bpy.props.FloatProperty(
        name="Start Angle Radius Arc",
        default=3.0,
        min=0,
        description="Start Angle Radius Arc"
        )
    end_angle: bpy.props.StringProperty(
        name="End Angle",
        default="math.pi",
        description="End angle for distribution",
    )
    curve_object: bpy.props.PointerProperty(
    type=bpy.types.Object,
    name="Select Curve",
    description="Select the Curve Object",
    )
    
    mesh_object: bpy.props.PointerProperty(
        name="Select Mesh",
        type=bpy.types.Object,
        description="Select the Mesh Object",
    )
    
    use_grid_3d: bpy.props.BoolProperty(
        name="Distribute in 3D Grid",
        default=False,
        description="Enable distribution in a 3D grid pattern",
    )
    
    use_circle: bpy.props.BoolProperty(
        name="Distribute in Circle",
        default=False,
        description="Enable distribution in a circular pattern",
    )
    
    use_square: bpy.props.BoolProperty(
        name="Distribute in Square",
        default=False,
        description="Enable distribution in a square pattern",
    )
    use_arc: bpy.props.BoolProperty(
        name="Distribute in Arc",
        default=False,
        description="Enable distribution in an Arc pattern",
    )
    
    use_curve: bpy.props.BoolProperty(
        name="Distribute on Curve",
        default=False,
        description="Enable distribution on a Curve pattern",
    )
    
    use_vertices: bpy.props.BoolProperty(
        name="Distribute on Mesh",
        default=False,
        description="Enable distribution on a Mesh vertices pattern",
    )
    
# ------------------------------------------------------------------------------
# RELATIVE OFFSET


class OFFSET_PT_Relative_Offset (bpy.types.Panel):
    bl_label = "Relative Offset"
    bl_idname = "OFFSET_PT_Relative_Offset"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "ARRAY_PT_Panel"  # Parent ID
    bl_options = {'DEFAULT_CLOSED'}

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
# DISPLAY PANEL


class DISPLAY_PT_Panel (bpy.types.Panel):
    bl_label = "Display Panel"
    bl_idname = "DISPLAY_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "MODIFIER_PT_Transform_And_Edit"
    bl_options = {'DEFAULT_CLOSED'}

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
        for area in bpy.context.screen.areas: 
            if area.type == 'VIEW_3D':
                space = area.spaces.active
                if space.type == 'VIEW_3D':
                    space.shading.type = 'WIREFRAME'
        #bpy.context.space_data.shading.type = 'WIREFRAME'
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
# Function to get the position along the chosen axis
def get_position(obj, axis='X'):
    if axis == 'X':
        return obj.location.x
    elif axis == 'Y':
        return obj.location.y
    elif axis == 'Z':
        return obj.location.z
    else:
        return 0  # Return default value if axis is not recognized




# ------------------------------------------------------------------------------
#Distribute Grid 3D
class OBJECT_OT_DistributeGrid3D(bpy.types.Operator):
    bl_idname = "object.distribute_grid_3d"
    bl_label = "Distribute in 3D Grid"
    
    def execute(self, context):
        # Accessing scene properties directly
        scene = context.scene
        x_copies = scene.Arc_Blend.distribute_x
        y_copies = scene.Arc_Blend.distribute_y
        z_copies = scene.Arc_Blend.distribute_z
        x_distance = bpy.context.scene.Arc_Blend.x_distance
        y_distance = bpy.context.scene.Arc_Blend.y_distance 
        z_distance = bpy.context.scene.Arc_Blend.z_distance
            
        selected_objects = bpy.context.selected_objects
        if len(selected_objects) < 1:
            self.report({'ERROR'}, "Please select at least one object.")
            return {'CANCELLED'}

        # Sort objects based on their positions along X, Y, and Z axes
        sorted_objects_x = sorted(selected_objects, key=lambda obj: obj.location.x)
        sorted_objects_y = sorted(selected_objects, key=lambda obj: obj.location.y)
        sorted_objects_z = sorted(selected_objects, key=lambda obj: obj.location.z)

        # Distribute objects in a 3D grid pattern along X, Y, and Z axes
        for i in range(z_copies):
            for j in range(y_copies):
                for k in range(x_copies):
                    index = i * (y_copies * x_copies) + j * x_copies + k
                    if index < len(sorted_objects_x):
                        obj = sorted_objects_x[index]
                        location = obj.location.copy()
                        location.x = k * x_distance  # Set X position
                        location.y = j * y_distance  # Set Y position
                        location.z = i * z_distance  # Set Z position
                        obj.location = location
        
        return {'FINISHED'}


#Distribute objects in a circular pattern
class OBJECT_OT_DistributeCircle(bpy.types.Operator):
    bl_idname = "object.distribute_circle"
    bl_label = "Distribute in Circle"
    
    def execute(self, context):
        radius= bpy.context.scene.Arc_Blend.radius
        selected_objects = bpy.context.selected_objects
        num_objects = len(selected_objects)

        if num_objects < 1:
            print("Please select at least one object.")
            return

        angle_increment = (2 * math.pi) / num_objects
        angle = 0

        # Sort objects based on their positions along the circle
        sorted_objects = sorted(selected_objects, key=lambda obj: obj.name)

        # Distribute objects along a circular path
        for obj in sorted_objects:
            location = obj.location.copy()
            location.x = radius * math.cos(angle)  # Calculate X position
            location.y = radius * math.sin(angle)  # Calculate Y position
            obj.location = location
            angle += angle_increment
        return {'FINISHED'}



#Distribute objects in a Square pattern
class OBJECT_OT_DistributeSquare(bpy.types.Operator):
    bl_idname = "object.distribute_square"
    bl_label = "Distribute in Square"
    
    def execute(self, context):
        side_length = bpy.context.scene.Arc_Blend.square_length 
        selected_objects = bpy.context.selected_objects
    
        num_objects = len(selected_objects)

        if num_objects < 1:
            print("Please select at least one object.")
            return

        # Determine the number of objects per side
        objects_per_side = int(math.sqrt(num_objects))

        # Sort objects based on their positions for even distribution
        sorted_objects = sorted(selected_objects, key=lambda obj: obj.name)

        # Distribute objects along a square path
        for i, obj in enumerate(sorted_objects):
            row = i // objects_per_side
            col = i % objects_per_side

            location = obj.location.copy()
            location.x = (col - objects_per_side / 2) * side_length  # Calculate X position
            location.y = (row - objects_per_side / 2) * side_length  # Calculate Y position
            obj.location = location
        return {'FINISHED'}


#Distribute objects in a Arc pattern
class OBJECT_OT_DistributeArc(bpy.types.Operator):
    bl_idname = "object.distribute_arc"
    bl_label = "Distribute in Arc"
    
    def execute(self, context):
        radius = bpy.context.scene.Arc_Blend.radius_arc 
        start_angle = bpy.context.scene.Arc_Blend.start_angle 
        end_angle = eval(bpy.context.scene.Arc_Blend.end_angle.replace("'", ""))

        
        
        selected_objects = bpy.context.selected_objects
        
        num_objects = len(selected_objects)

        if num_objects < 1:
            print("Please select at least one object.")
            return

        angle_increment = (end_angle - start_angle) / max(num_objects - 1, 1)

        # Sort objects based on their positions for even distribution
        sorted_objects = sorted(selected_objects, key=lambda obj: obj.name)

        # Distribute objects along an arc path
        angle = start_angle
        for obj in sorted_objects:
            location = obj.location.copy()
            location.x = radius * math.cos(angle)  # Calculate X position
            location.y = radius * math.sin(angle)  # Calculate Y position
            obj.location = location
            angle += angle_increment
        return {'FINISHED'}
  

# Function to calculate the distance between two points in 3D space
def distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)



class OBJECT_OT_DistributeCurve(bpy.types.Operator):
    bl_idname = "object.distribute_curve"
    bl_label = "Distribute Along Curve"
    
    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        if len(selected_objects) < 1:
            print("Please select at least one object.")
            return {'CANCELLED'}
        
        curve_object = context.scene.Arc_Blend.curve_object
        if curve_object is None or curve_object.type != 'CURVE':
            print("Please select a curve object.")
            return {'CANCELLED'}
        
        curve_data = curve_object.data

        # Calculate the total length of the curve
        curve_length = 0
        for spline in curve_data.splines:
            for segment in spline.bezier_points:
                if segment.handle_right:
                    curve_length += (segment.handle_right - segment.co).length
                if segment.handle_left:
                    curve_length += (segment.handle_left - segment.co).length

        # Calculate the step along the curve for object distribution
        num_objects = len(selected_objects)
        step = curve_length / max(num_objects - 1, 1)

        # Place objects along the curve
        current_position = 0
        for obj in selected_objects:
            current_length = 0
            found_segment = None

            # Find the segment where the object should be placed
            for spline in curve_data.splines:
                for segment in spline.bezier_points:
                    if segment.handle_right:
                        seg_length = (segment.handle_right - segment.co).length
                        current_length += seg_length
                        if current_length >= current_position:
                            found_segment = segment
                            break
                    if found_segment:
                        break
                    if segment.handle_left:
                        seg_length = (segment.handle_left - segment.co).length
                        current_length += seg_length
                        if current_length >= current_position:
                            found_segment = segment
                            break
                    if found_segment:
                        break
                
                if found_segment:
                    break
            
            if found_segment:
                location = curve_object.matrix_world @ found_segment.co
                obj.location = location
            
            current_position += step

        return {'FINISHED'}

class OBJECT_OT_DistributeOnVertices(bpy.types.Operator):
    bl_idname = "object.distribute_on_vertices"
    bl_label = "Distribute on Vertices"
    
    def execute(self, context):
        
        mesh_object = bpy.context.scene.Arc_Blend.mesh_object

        
        selected_objects = bpy.context.selected_objects
        if len(selected_objects) < 1:
            print("Please select at least one object.")
            return {'CANCELLED'}
        
 
        if mesh_object is None or mesh_object.type != 'MESH':
            print("Please select a mesh object.")
            return {'CANCELLED'}
        
        distribution_objects = bpy.context.selected_objects
        #[obj for obj in bpy.context.selected_objects if obj.type != 'MESH']
        
        if not distribution_objects:
            print("Please select objects to distribute.")
            return {'CANCELLED'}
        
        selected_vertices = [v for v in mesh_object.data.vertices if v.select]
        
        if not selected_vertices:
            print("Please select vertices on the mesh object.")
            return {'CANCELLED'}
        
        num_vertices = len(selected_vertices)
        num_distribution_objects = len(distribution_objects)
        
        if num_vertices == 0 or num_distribution_objects == 0:
            print("No vertices selected or no objects to distribute.")
            return {'CANCELLED'}
        
        # Distribute objects on selected vertices of the mesh object
        for i, vertex in enumerate(selected_vertices):
            obj_index = i % num_distribution_objects
            target_object = distribution_objects[obj_index]
            
            # Place the distribution object on the vertex location
            target_object.location = mesh_object.matrix_world @ vertex.co
        
        return {'FINISHED'}

class OBJECT_OT_DistributeOnEdges(bpy.types.Operator):
    bl_idname = "object.distribute_on_edges"
    bl_label = "Distribute on Edges"
    
    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        mesh_object = bpy.context.scene.Arc_Blend.mesh_object

        if len(selected_objects) < 1:
            print("Please select at least one object.")
            return {'CANCELLED'}

        if mesh_object is None or mesh_object.type != 'MESH':
            print("Please select a mesh object.")
            return {'CANCELLED'}

        distribution_objects = selected_objects

        selected_edges = [e for e in mesh_object.data.edges if e.select]

        if not selected_edges:
            print("Please select edges on the mesh object.")
            return {'CANCELLED'}

        num_edges = len(selected_edges)
        num_distribution_objects = len(distribution_objects)

        if num_edges == 0 or num_distribution_objects == 0:
            print("No edges selected or no objects to distribute.")
            return {'CANCELLED'}

        # Distribute objects along selected edges of the mesh object
        for i, edge in enumerate(selected_edges):
            obj_index = i % num_distribution_objects
            target_object = distribution_objects[obj_index]

            if len(edge.vertices) != 2:
                continue  # Skip edges without two vertices

            # Calculate the center of the edge
            edge_center = (mesh_object.matrix_world @ mesh_object.data.vertices[edge.vertices[0]].co +
                           mesh_object.matrix_world @ mesh_object.data.vertices[edge.vertices[1]].co) / 2

            # Place the distribution object at the edge center
            target_object.location = edge_center

        return {'FINISHED'}

class OBJECT_OT_DistributeOnEdgesRotated(bpy.types.Operator):
    bl_idname = "object.distribute_on_edgesrotated"
    bl_label = "Distribute on Edges Rotated"
    
    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        mesh_object = bpy.context.scene.Arc_Blend.mesh_object

        if len(selected_objects) < 1:
            print("Please select at least one object.")
            return {'CANCELLED'}

        if mesh_object is None or mesh_object.type != 'MESH':
            print("Please select a mesh object.")
            return {'CANCELLED'}

        distribution_objects = selected_objects

        selected_edges = [e for e in mesh_object.data.edges if e.select]

        if not selected_edges:
            print("Please select edges on the mesh object.")
            return {'CANCELLED'}

        num_edges = len(selected_edges)
        num_distribution_objects = len(distribution_objects)

        if num_edges == 0 or num_distribution_objects == 0:
            print("No edges selected or no objects to distribute.")
            return {'CANCELLED'}

        # Distribute objects along selected edges of the mesh object
        for i, edge in enumerate(selected_edges):
            obj_index = i % num_distribution_objects
            target_object = distribution_objects[obj_index]

            if len(edge.vertices) != 2:
                continue  # Skip edges without two vertices

            # Calculate the center of the edge
            edge_center = (mesh_object.matrix_world @ mesh_object.data.vertices[edge.vertices[0]].co +
                           mesh_object.matrix_world @ mesh_object.data.vertices[edge.vertices[1]].co) / 2

            # Place the distribution object at the edge center
            target_object.location = edge_center

            # Calculate the rotation for the object
            vec = mesh_object.data.vertices[edge.vertices[1]].co - mesh_object.data.vertices[edge.vertices[0]].co
            quat = vec.to_track_quat('X', 'Z')
            target_object.rotation_euler = quat.to_euler()

        return {'FINISHED'}

class OBJECT_OT_DistributeOnFacesRotated(bpy.types.Operator):
    bl_idname = "object.distribute_on_facesrotated"
    bl_label = "Distribute on Faces Rotated"
    
    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        mesh_object = bpy.context.scene.Arc_Blend.mesh_object

        if len(selected_objects) < 1:
            print("Please select at least one object.")
            return {'CANCELLED'}

        if mesh_object is None or mesh_object.type != 'MESH':
            print("Please select a mesh object.")
            return {'CANCELLED'}

        distribution_objects = selected_objects

        selected_faces = [f for f in mesh_object.data.polygons if f.select]

        if not selected_faces:
            print("Please select faces on the mesh object.")
            return {'CANCELLED'}

        num_faces = len(selected_faces)
        num_distribution_objects = len(distribution_objects)

        if num_faces == 0 or num_distribution_objects == 0:
            print("No faces selected or no objects to distribute.")
            return {'CANCELLED'}

        # Distribute objects along selected faces of the mesh object
        for i, face in enumerate(selected_faces):
            obj_index = i % num_distribution_objects
            target_object = distribution_objects[obj_index]

            # Calculate the center of the face
            face_center = mesh_object.matrix_world @ face.center

            # Place the distribution object at the face center
            target_object.location = face_center

            # Calculate the normal of the face
            face_normal = face.normal

            # Calculate the rotation for the object
            quat = face_normal.to_track_quat('Z', 'Y')
            target_object.rotation_euler = quat.to_euler()

        return {'FINISHED'}
    
    
    
class OBJECT_OT_DistributeOnFaces(bpy.types.Operator):
    bl_idname = "object.distribute_on_faces"
    bl_label = "Distribute on Faces"
    
    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        mesh_object = bpy.context.scene.Arc_Blend.mesh_object

        if len(selected_objects) < 1:
            print("Please select at least one object.")
            return {'CANCELLED'}

        if mesh_object is None or mesh_object.type != 'MESH':
            print("Please select a mesh object.")
            return {'CANCELLED'}

        distribution_objects = selected_objects

        selected_faces = [f for f in mesh_object.data.polygons if f.select]

        if not selected_faces:
            print("Please select faces on the mesh object.")
            return {'CANCELLED'}

        num_faces = len(selected_faces)
        num_distribution_objects = len(distribution_objects)

        if num_faces == 0 or num_distribution_objects == 0:
            print("No faces selected or no objects to distribute.")
            return {'CANCELLED'}

        # Distribute objects along selected faces of the mesh object
        for i, face in enumerate(selected_faces):
            obj_index = i % num_distribution_objects
            target_object = distribution_objects[obj_index]

            # Calculate the center of the face
            face_center = mesh_object.matrix_world @ face.center

            # Place the distribution object at the face center
            target_object.location = face_center

        return {'FINISHED'}





class OBJECT_OT_DistributeOnVerticesRotated(bpy.types.Operator):
    bl_idname = "object.distribute_on_vertices_rotated"
    bl_label = "Distribute on Vertices Rotated"

    def execute(self, context):
        mesh_object = bpy.context.scene.Arc_Blend.mesh_object
        selected_objects = bpy.context.selected_objects

        if len(selected_objects) < 1:
            print("Please select at least one object.")
            return {'CANCELLED'}

        if mesh_object is None or mesh_object.type != 'MESH':
            print("Please select a mesh object.")
            return {'CANCELLED'}

        distribution_objects = selected_objects

        selected_vertices = [v for v in mesh_object.data.vertices if v.select]

        if not selected_vertices:
            print("Please select vertices on the mesh object.")
            return {'CANCELLED'}

        num_vertices = len(selected_vertices)
        num_distribution_objects = len(distribution_objects)

        if num_vertices == 0 or num_distribution_objects == 0:
            print("No vertices selected or no objects to distribute.")
            return {'CANCELLED'}

        # Distribute objects on selected vertices of the mesh object
        for i, vertex in enumerate(selected_vertices):
            obj_index = i % num_distribution_objects
            target_object = distribution_objects[obj_index]

            # Place the distribution object on the vertex location
            target_object.location = mesh_object.matrix_world @ vertex.co

            # Calculate the rotation for the object based on the vertex normal
            normal = mesh_object.data.vertices[vertex.index].normal

            # Calculate the rotation angles from the normal
            rot_quat = normal.to_track_quat('Z', 'Y')

            # Apply the rotation to the object
            target_object.rotation_euler = rot_quat.to_euler()

        return {'FINISHED'}


def register():
    bpy.utils.register_class(ARCBLENDMODIFIERS_PT_Panel)
    bpy.utils.register_class(MODIFIER_PT_Transform_And_Edit)
    bpy.utils.register_class(TRANSFORM_PT_Edit_Object_Panel)
    bpy.utils.register_class(transform_edit_object_align_x)
    bpy.utils.register_class(transform_edit_object_align_y)
    bpy.utils.register_class(transform_edit_object_align_z)
    bpy.utils.register_class(transform_edit_object_align_bound)
    bpy.utils.register_class(transform_edit_object_purge)
    bpy.utils.register_class(TRANSFORM_PT_Panel)
    bpy.utils.register_class(modifier_array_detail)
    bpy.types.Scene.Arc_Blend = bpy.props.PointerProperty(
        type=modifier_array_detail)
    bpy.utils.register_class(DISPLAY_PT_Panel)
    bpy.utils.register_class(EXPORT_PT_Object)
    bpy.utils.register_class(loop_multiple_select)
    bpy.utils.register_class(loop_multiple_select_ring)
    bpy.utils.register_class(loop_select)
    bpy.utils.register_class(loop_select_boundry_faces)
    bpy.utils.register_class(loop_mesh_seperate)
    bpy.utils.register_class(loop_mesh_shortest_path_pick)
    bpy.utils.register_class(loop_mesh_split)
    bpy.utils.register_class(loop_mesh_tris_convert_to_quads)
    bpy.utils.register_class(loop_mesh_quads_convert_to_tris)
    bpy.utils.register_class(loop_mesh_find_trios)
    bpy.utils.register_class(loop_mesh_find_quads)
    bpy.utils.register_class(loop_sde)
    bpy.utils.register_class(loop_idtm)
    bpy.utils.register_class(transform_edit_object_randomize_colors)
    bpy.utils.register_class(transform_edit_object_reset_colors)
    bpy.utils.register_class(display_panel_show_xray)
    bpy.utils.register_class(display_panel_show_wireframe)
    bpy.utils.register_class(display_panel_show_solid)
    bpy.utils.register_class(display_panel_show_material)
    bpy.utils.register_class(display_panel_show_rendered)
    bpy.utils.register_class(OBJECT_OT_DistributeGrid3D)
    bpy.utils.register_class(OBJECT_OT_DistributeCircle)
    bpy.utils.register_class(OBJECT_OT_DistributeSquare)
    bpy.utils.register_class(OBJECT_OT_DistributeArc)
    bpy.utils.register_class(OBJECT_OT_DistributeCurve)
    bpy.utils.register_class(OBJECT_OT_DistributeOnVertices)
    bpy.utils.register_class(OBJECT_OT_DistributeOnEdges)
    bpy.utils.register_class(OBJECT_OT_DistributeOnEdgesRotated)
    bpy.utils.register_class(OBJECT_OT_DistributeOnFaces)
    bpy.utils.register_class(OBJECT_OT_DistributeOnFacesRotated)
    bpy.utils.register_class(OBJECT_OT_DistributeOnVerticesRotated)
    #AlignTool
    bpy.utils.register_class(AlignPropertiesGroup)
    bpy.types.Scene.alignment_list = bpy.props.PointerProperty(type=AlignPropertiesGroup)
    bpy.utils.register_class(OBJECT_OT_AlignOperator)
    


def unregister():
    bpy.utils.unregister_class(ARCBLENDMODIFIERS_PT_Panel)
    bpy.utils.unregister_class(MODIFIER_PT_Transform_And_Edit)
    bpy.utils.unregister_class(TRANSFORM_PT_Edit_Object_Panel)
    bpy.utils.unregister_class(transform_edit_object_align_x)
    bpy.utils.unregister_class(transform_edit_object_align_y)
    bpy.utils.unregister_class(transform_edit_object_align_z)
    bpy.utils.unregister_class(transform_edit_object_align_bound)
    bpy.utils.unregister_class(transform_edit_object_purge)
    bpy.utils.unregister_class(TRANSFORM_PT_Panel)
    bpy.utils.unregister_class(modifier_array_detail)
    bpy.utils.unregister_class(OFFSET_PT_Relative_Offset)
    del bpy.types.Scene.Arc_Blend
    bpy.utils.unregister_class(DISPLAY_PT_Panel)
    bpy.utils.unregister_class(EXPORT_PT_Object)
    bpy.utils.unregister_class(loop_multiple_select)
    bpy.utils.unregister_class(loop_multiple_select_ring)
    bpy.utils.unregister_class(loop_select)
    bpy.utils.unregister_class(loop_select_boundry_faces)
    bpy.utils.unregister_class(loop_mesh_seperate)
    bpy.utils.unregister_class(loop_mesh_shortest_path_pick)
    bpy.utils.unregister_class(loop_mesh_split)
    bpy.utils.unregister_class(loop_mesh_tris_convert_to_quads)
    bpy.utils.unregister_class(loop_mesh_quads_convert_to_tris)
    bpy.utils.unregister_class(loop_mesh_find_trios)
    bpy.utils.unregister_class(loop_mesh_find_quads)
    bpy.utils.unregister_class(loop_sde)
    bpy.utils.unregister_class(loop_idtm)
    bpy.utils.unregister_class(transform_edit_object_randomize_colors)
    bpy.utils.unregister_class(transform_edit_object_reset_colors)
    bpy.utils.unregister_class(display_panel_show_xray)
    bpy.utils.unregister_class(display_panel_show_wireframe)
    bpy.utils.unregister_class(display_panel_show_solid)
    bpy.utils.unregister_class(display_panel_show_material)
    bpy.utils.unregister_class(display_panel_show_rendered)
    bpy.utils.unregister_class(OBJECT_OT_DistributeGrid3D)
    bpy.utils.unregister_class(OBJECT_OT_DistributeCircle)
    bpy.utils.unregister_class(OBJECT_OT_DistributeSquare)
    bpy.utils.unregister_class(OBJECT_OT_DistributeArc)
    bpy.utils.unregister_class(OBJECT_OT_DistributeCurve)
    bpy.utils.unregister_class(OBJECT_OT_DistributeOnVertices)
    bpy.utils.unregister_class(OBJECT_OT_DistributeOnEdges)
    bpy.utils.unregister_class(OBJECT_OT_DistributeOnEdgesRotated)
    bpy.utils.unregister_class(OBJECT_OT_DistributeOnFaces)
    bpy.utils.unregister_class(OBJECT_OT_DistributeOnFacesRotated)
    bpy.utils.unregister_class(OBJECT_OT_DistributeOnVerticesRotated)
    #Align Tools
    bpy.utils.unregister_class(AlignPropertiesGroup)
    del bpy.types.Scene.alignment_list
    bpy.utils.unregister_class(OBJECT_OT_AlignOperator)
