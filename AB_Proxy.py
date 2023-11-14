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
# PROXY PANEL

class PROXY_PT_PANEL (bpy.types.Panel):
    bl_label = "AB Proxy"
    bl_idname = "PROXY_PT_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_options = {'DEFAULT_CLOSED'}

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
                "PROXY_UL_Object_List", "", mesh, "mesh_list", mesh, "list_index", rows=2)
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

class PROXY_PT_REMESHER (bpy.types.Panel):
    """Remesh it.All data layers keeps in program"""

    bl_label = ""
    bl_idname = "PROXY_PT_REMESHER"
    bl_parent_id = "PROXY_PT_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    def draw_header(self, context):
        
        layout = self.layout

        layout.label(text="REMESH", icon="MONKEY")
        

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        row = layout.row()
        
        if bpy.context.selected_objects != []:

            mesh = bpy.context.object.data
            row.prop(mesh, "remesh_mode", text="Mode", expand=True)
            col = layout.column()
            if mesh.remesh_mode == 'VOXEL':
                col.prop(mesh, "remesh_voxel_size")
                col.prop(mesh, "remesh_voxel_adaptivity")
                col.prop(mesh, "use_remesh_fix_poles")

                col = layout.column(heading="Preserve")
                col.prop(mesh, "use_remesh_preserve_volume", text="Volume")
                col.prop(mesh, "use_remesh_preserve_paint_mask", text="Paint Mask")
                col.prop(mesh, "use_remesh_preserve_sculpt_face_sets", text="Face Sets")
                col.prop(mesh, "use_remesh_preserve_vertex_colors", text="Color Attributes")

                col.operator("object.voxel_remesh", text="Voxel Remesh")
            else:
                col.operator("object.quadriflow_remesh", text="QuadriFlow Remesh")
        else:
            pass
        
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


class PROXY_UL_Object_List(bpy.types.UIList):
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
# REGISTRATION AREA

def register():
    bpy.utils.register_class(PROXY_PT_PANEL)
    bpy.utils.register_class(PROXY_PT_REMESHER)
    bpy.utils.register_class(proxy_panel_convertto_point_cloud)
    bpy.utils.register_class(PROXY_UL_Object_List)
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

def unregister():
    bpy.utils.unregister_class(PROXY_PT_PANEL)
    bpy.utils.unregister_class(PROXY_PT_REMESHER)
    bpy.utils.unregister_class(proxy_panel_convertto_point_cloud)
    bpy.utils.unregister_class(PROXY_UL_Object_List)
    bpy.utils.unregister_class(proxy_panel_add_objects)
    bpy.utils.unregister_class(proxy_panel_remove_objects)
    bpy.utils.unregister_class(proxy_panel_list_item)
    bpy.utils.unregister_class(proxy_panel_list_makes_parents)
    bpy.utils.unregister_class(proxy_panel_list_clear_parents)
    bpy.utils.unregister_class(proxy_panel_list_select_same_collection)
    bpy.utils.unregister_class(proxy_panel_list_apply_all_modifiers)
    bpy.utils.unregister_class(proxy_panel_convertto_hull_geometry)
    bpy.utils.unregister_class(proxy_panel_convertto_bound_box)
    
    # del bpy.types.Scene.mesh_list
    # del bpy.types.Scene.list_index
    # del bpy.types.Scene.proxy_item
    # del bpy.types.Object.mesh_list
    # del bpy.types.Object.list_index
    del bpy.types.Object.proxy_item_obj
    del bpy.types.Mesh.mesh_list
    del bpy.types.Mesh.list_index
    # del bpy.types.Mesh.proxy_item

