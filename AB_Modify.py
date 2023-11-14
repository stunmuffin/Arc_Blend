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
    