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
# VERTEX EDİT PANEL


class EDIT_PT_Vertex_Edit (bpy.types.Panel):
    bl_label = "Vertex Edit Panel"
    bl_idname = "EDIT_PT_Vertex_Edit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_options = {'DEFAULT_CLOSED'}

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

        return {'FINISHED'}

def register():
    bpy.utils.register_class(EDIT_PT_Vertex_Edit)
    bpy.utils.register_class(edit_mode_add_vertex)
    bpy.utils.register_class(edit_mode_bridge_vertices)
    bpy.utils.register_class(edit_mode_delete_vertices)
    bpy.utils.register_class(edit_mode_just_vertices)
    bpy.utils.register_class(edit_mode_just_edges)
    bpy.utils.register_class(edit_mode_create_faces)
   

 
  

def unregister():
    bpy.utils.unregister_class(EDIT_PT_Vertex_Edit)
    bpy.utils.unregister_class(edit_mode_add_vertex)
    bpy.utils.unregister_class(edit_mode_bridge_vertices)
    bpy.utils.unregister_class(edit_mode_delete_vertices)
    bpy.utils.unregister_class(edit_mode_just_vertices)
    bpy.utils.unregister_class(edit_mode_just_edges)
    bpy.utils.unregister_class(edit_mode_create_faces)
