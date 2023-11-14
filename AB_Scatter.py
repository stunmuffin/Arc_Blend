
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
# SCATTER def PANEL


def particle_panel_enabled(context, psys):
    if psys is None:
        return True
    phystype = psys.settings.physics_type
    if psys.settings.type in {'EMITTER', 'REACTOR'} and phystype in {'NO', 'KEYED'}:
        return True
    else:
        return (psys.point_cache.is_baked is False) and (not psys.is_edited) and (not context.particle_system_editable)


def particle_panel_poll(cls, context):
    psys = context.particle_system
    engine = context.engine
    settings = 0

    if psys:
        settings = psys.settings
    elif isinstance(context.space_data.pin_id, bpy.types.ParticleSettings):
        settings = context.space_data.pin_id

    if not settings:
        return False

    return (settings.is_fluid is False) and (engine in cls.COMPAT_ENGINES)


def particle_get_settings(context):
    if context.particle_system:
        return context.particle_system.settings
    elif isinstance(context.space_data.pin_id, bpy.types.ParticleSettings):
        return context.space_data.pin_id
    return None


# ------------------------------------------------------------------------------
# SCATTER OBJECT LIST DEFINES

def find_modifier(ob, psys):
    for md in ob.modifiers:
        if md.type == 'PARTICLE_SYSTEM':
            if md.particle_system == psys:
                return md
    return None


# ------------------------------------------------------------------------------
# SCATTER OBJECT LIST


class SCATTER_UL_Object_List(bpy.types.UIList):
    """UI Scatter List"""

    def draw_item(self, _context, layout, data, item, icon, _active_data, _active_propname, _index, _flt_flag):
        ob = data
        psys = item

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            md = find_modifier(ob, psys)
            row = layout.row(align=True)

            row.prop(psys, "name", text="",
                     emboss=False, icon="STICKY_UVS_LOC")
            if md:
                row.prop(
                    md,
                    "show_viewport",
                    emboss=False,
                    icon_only=True,
                )
                row.prop(
                    md,
                    "show_render",
                    emboss=False,
                    icon_only=True,
                )

        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon="STICKY_UVS_LOC")

    # def draw_item(self, context, layout, data, item, icon, active_data,
     #             active_propname, index):

        #scene = context.scene
        #row = layout.row(align=True)

        # sub=row.row(align=True)
        #sub.scale_x = 2

        #sub.prop(item,"scatter_item",text='', icon="STICKY_UVS_LOC")

        # sub=row.row(align=True)
        #sub.scale_x = 1.1
        #sub.enabled = bool(item.scatter_item)
        #sub.prop(item,"scatter_display",text='', icon='RESTRICT_VIEW_OFF'  if item.scatter_display else'RESTRICT_VIEW_ON')

        # sub=row.row(align=True)
        #sub.scale_x = 0.3
        #sub.prop(item,"name", text="", icon="RADIOBUT_ON", emboss=False)
        # sub.enabled=False

        #sub.prop(item,"proxy_render_frame",text='', icon='RESTRICT_RENDER_OFF'if item.proxy_render_frame else'RESTRICT_RENDER_ON')


# ------------------------------------------------------------------------------
# SCATTER PANEL

class SCATTER_PT_Panel (bpy.types.Panel):
    bl_label = "AB Scatter"
    bl_idname = "SCATTER_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        ob = context.object
        scene = context.scene
        mesh = scatter_true_mesh_data(ob)
        Arc_Blend = scene.Arc_Blend
        ui = bpy.ops.ui
        main = layout.column()
        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass

        main.label(text="Scatter Panel : ", icon="STICKY_UVS_LOC")

        # define two rows
        row = main.row()
        col1 = row.column()
        col2 = row.column()

        # draw template
        template = col1.column()
        try:
            template.template_list("SCATTER_UL_Object_List", "particle_systems", ob, "particle_systems",
                                   ob.particle_systems, "active_index", rows=3)
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass
        template.scale_y = 1.1

        # draw side bar
        col2.separator(factor=0)
        #
        add = col2.column(align=True)
        AB_ADD = add.operator(
            "object.particle_system_add", icon='ADD', text="")

        #
        rem = col2.column(align=True)
        AB_REMOVE = rem.operator(
            "object.particle_system_remove", icon='REMOVE', text="")

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

        col = layout.column()
        col.prop(Arc_Blend, "object_scatter",
                 text="Object Scatter", icon="STICKY_UVS_LOC")
        try:
            if bpy.context.scene.Arc_Blend.object_scatter == True:

                # Emission
                col.prop(part, "count")
                col.prop(psys, "seed")
                col.prop(part, "hair_length", text="Object Lengths")
                # Viewport Display
                col.prop(part, "display_percentage",
                         slider=True, text="Amount")
                col.prop(context.object, "show_instancer_for_viewport",
                         text="Show Instancer", icon="STICKY_UVS_DISABLE")
                col.operator("object.button_scatter_panel_make_real_objects",
                             text="Make Instances Real", icon="OUTLINER_OB_MESH")

        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass


# ------------------------------------------------------------------------------
# ADD OBJECT TO LIST SCATTER


class scatter_panel_make_real_objects (bpy.types.Operator):
    """Make Instances Real"""

    bl_label = ""
    bl_idname = "object.button_scatter_panel_make_real_objects"

    def execute(self, context):
        bpy.ops.object.duplicates_make_real()

        return {'FINISHED'}

# ------------------------------------------------------------------------------
# SCATTER VIEW AS PANEL


class SCATTER_PT_Scatter_As (bpy.types.Panel):
    bl_label = ""
    bl_idname = "SCATTER_PT_Scatter_As"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "SCATTER_PT_Panel"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass
        return bpy.context.scene.Arc_Blend.object_scatter == True

    def draw_header(self, context):

        layout = self.layout

        layout.label(text="Scatter As", icon="STICKY_UVS_LOC")

    def draw(self, context):
        layout = self.layout
        ob = context.object
        scene = context.scene
        mesh = scatter_true_mesh_data(ob)
        Arc_Blend = scene.Arc_Blend
        ui = bpy.ops.ui
        main = layout.column()
        layout.use_property_split = False

        col = layout.column()

        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active

            if bpy.context.scene.Arc_Blend.object_scatter == True:

                # Render
                col.prop(Arc_Blend, "scatter_view_as", text="Render Type")

                if bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_object' or bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_collection':

                    col = layout.column(align=False)
                    col.prop(part, "particle_size", text="Scale")
                    col.prop(part, "size_random", slider=True,
                             text="Scale Randomness")

                if bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_path':
                    col.prop(part, "material_slot", text="Material")
                    col.prop(psys, "parent", text="Coordinate System")

        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass

# ------------------------------------------------------------------------------
# SCATTER PAINT PANEL


class SCATTER_PT_Paint_Panel (bpy.types.Panel):
    bl_label = ""
    bl_idname = "SCATTER_PT_Paint_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "SCATTER_PT_Panel"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass
        return bpy.context.scene.Arc_Blend.object_scatter == True

    def draw_header(self, context):

        layout = self.layout

        layout.label(text="Paint Panel", icon="BRUSHES_ALL")

    def draw(self, context):
        layout = self.layout
        ob = context.object
        scene = context.scene
        mesh = scatter_true_mesh_data(ob)
        Arc_Blend = scene.Arc_Blend
        ui = bpy.ops.ui
        #main = layout.column()
        layout.use_property_split = False

        #col = layout.column()
        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active

            layout.prop(Arc_Blend, "object_scatter_paint_panel",
                        text="PAINT", icon="BRUSHES_ALL")
            col = layout.column()
            row = col.row(align=True)
            sub = row.row(align=True)
            sub.use_property_decorate = False
            sub.prop_search(psys, "vertex_group_density", ob,
                            "vertex_groups", text="Density")
            row.prop(psys, "invert_vertex_group_density",
                     text="", toggle=True, icon='ARROW_LEFTRIGHT')

        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass

# ------------------------------------------------------------------------------
# SCATTER ROTATION PANEL


class SCATTER_PT_Rotation_Panel (bpy.types.Panel):
    bl_label = ""
    bl_idname = "SCATTER_PT_Rotation_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "SCATTER_PT_Panel"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass
        return bpy.context.scene.Arc_Blend.object_scatter == True

    def draw_header(self, context):

        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            psys = bpy.context.object.particle_systems.active

            layout = self.layout

            layout.prop(part, "use_rotations", text="Rotation",
                        icon="ORIENTATION_GIMBAL")

        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass

    def draw(self, context):
        layout = self.layout
        ob = context.object
        scene = context.scene
        mesh = scatter_true_mesh_data(ob)
        Arc_Blend = scene.Arc_Blend
        ui = bpy.ops.ui
        #main = layout.column()
        layout.use_property_split = False

        #col = layout.column()
        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active

            layout.use_property_split = False

            main = layout.column()

            main.prop(part, "rotation_mode")
            row1 = layout.row()
            row1.label(text="Randomize : ")
            row1.scale_x = 2
            row1.prop(part, "rotation_factor_random", slider=True, text="")

            col = layout.column()
            row2 = layout.row()
            row2.label(text="Phase : ")
            row2.scale_x = 2
            row2.prop(part, "phase_factor", slider=True, text="")

            col = layout.column()
            row3 = layout.row()
            row3.label(text="Rndm Phase : ")
            row3.scale_x = 2
            row3.prop(part, "phase_factor_random", text="", slider=True)

            if part.type != 'HAIR':
                col.prop(part, "use_dynamic_rotation")
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass


# ------------------------------------------------------------------------------
# SCATTER OBJECT PANEL

class SCATTER_PT_Object (bpy.types.Panel):
    bl_label = ""
    bl_idname = "SCATTER_PT_Object"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "SCATTER_PT_Scatter_As"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass
        return bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_object'

    def draw_header(self, context):

        layout = self.layout

        layout.label(text="Object", icon="OUTLINER_OB_MESH")

    def draw(self, context):
        layout = self.layout
        ob = context.object
        scene = context.scene
        mesh = scatter_true_mesh_data(ob)
        Arc_Blend = scene.Arc_Blend
        ui = bpy.ops.ui
        main = layout.column()
        layout.use_property_split = False

        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active

            if bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_object':

                col = layout.column()

                col.prop(part, "instance_object",
                         text="Instance", icon="STICKY_UVS_LOC")
                sub = col.column()
                sub.prop(part, "use_global_instance",
                         text="Global Coordinates")
                sub.prop(part, "use_rotation_instance", text="Object Rotation")
                sub.prop(part, "use_scale_instance", text="Object Scale")

        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass
# ------------------------------------------------------------------------------
# SCATTER COLLECTION PANEL


class SCATTER_PT_Collection (bpy.types.Panel):
    bl_label = ""
    bl_idname = "SCATTER_PT_Collection"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "SCATTER_PT_Scatter_As"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass
        return bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_collection'

    def draw_header(self, context):

        layout = self.layout

        layout.label(text="Collection", icon="OUTLINER_COLLECTION")

    def draw(self, context):
        layout = self.layout
        ob = context.object
        scene = context.scene
        mesh = scatter_true_mesh_data(ob)
        Arc_Blend = scene.Arc_Blend
        ui = bpy.ops.ui
        main = layout.column()
        layout.use_property_split = False

        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active

            col = layout.column()

            if bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_collection':
                col.prop(part, "instance_collection",
                         text="Instance Collection")
                col.prop(part, "use_whole_collection")
                sub = col.column()
                sub.active = (part.use_whole_collection is False)
                sub.prop(part, "use_collection_pick_random")
                sub.prop(part, "use_global_instance",
                         text="Global Coordinates")
                sub.prop(part, "use_rotation_instance", text="Object Rotation")
                sub.prop(part, "use_scale_instance", text="Object Scale")
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass


# ------------------------------------------------------------------------------
# SCATTER COLLECTION USE COUNT PANEL

class SCATTER_PT_Collection_Use_Count (bpy.types.Panel):
    bl_label = ""
    bl_idname = "SCATTER_PT_Collection_Use_Count"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "SCATTER_PT_Collection"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass
        return bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_collection'

    def draw_header(self, context):

        layout = self.layout

        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active

            part = bpy.context.object.particle_systems.data.particle_systems.active.settings

            layout.active = not part.use_whole_collection

            layout.prop(part, "use_collection_count",
                        text="Proportion (Elements)", icon="OUTLINER_COLLECTION")
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass

    def draw(self, context):
        layout = self.layout
        ob = context.object
        scene = context.scene
        mesh = scatter_true_mesh_data(ob)
        Arc_Blend = scene.Arc_Blend
        ui = bpy.ops.ui
        main = layout.column()
        layout.use_property_split = False

        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass

        col = layout.column()

        try:
            layout.active = part.use_collection_count and not part.use_whole_collection

            row = layout.row()
            row.template_list("UI_UL_list", "particle_instance_weights", part, "instance_weights",
                              part, "active_instanceweight_index")

            col = row.column()
            sub = col.row()
            subsub = sub.column(align=True)
            subsub.operator("particle.dupliob_copy", icon='ADD', text="")
            subsub.operator("particle.dupliob_remove", icon='REMOVE', text="")
            subsub.operator("particle.dupliob_move_up",
                            icon='TRIA_UP', text="")
            subsub.operator("particle.dupliob_move_down",
                            icon='TRIA_DOWN', text="")
            subsub.separator()
            subsub.operator("particle.dupliob_refresh",
                            icon='FILE_REFRESH', text="")

            weight = part.active_instanceweight
            if weight:
                row = layout.row()
                row.prop(weight, "count")
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass


# ------------------------------------------------------------------------------
# SCATTER EXTRA PANEL

class SCATTER_PT_Extra (bpy.types.Panel):
    bl_label = ""
    bl_idname = "SCATTER_PT_Extra"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_parent_id = "SCATTER_PT_Scatter_As"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active
        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass
        return bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_object' or bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_collection'

    def draw_header(self, context):

        layout = self.layout

        layout.label(text="Extra", icon="SETTINGS")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False

        col = layout.column()
        try:
            part = bpy.context.object.particle_systems.data.particle_systems.active.settings
            # bpy.context.object.modifiers[bpy.context.object.particle_systems.data.particle_systems.active.name].particle_system
            psys = bpy.context.object.particle_systems.active

            if bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_object' or bpy.context.scene.Arc_Blend.scatter_view_as == 'arc_blend_scatter_as_collection':

                col.prop(part, "use_parent_particles", text="Parent Particles")
                col.prop(part, "show_unborn", text="Unborn")
                col.prop(part, "use_dead", text="Dead")

        except (TypeError, AttributeError, UnboundLocalError, KeyError):
            pass

# ------------------------------------------------------------------------------
# ADD OBJECT TO LIST SCATTER


class scatter_panel_add_objects (bpy.types.Operator):
    """Add a new item to the list"""

    bl_label = ""
    bl_idname = "object.button_scatter_panel_add_objects"

    add: bpy.props.StringProperty()
    scatter_mesh_name: bpy.props.StringProperty()

    def execute(self, context):
        try:
            mesh = bpy.data.meshes[self.scatter_mesh_name]
            index = mesh.scatter_list_index

            if self.add == 'ADD':

                item = mesh.scatter_mesh_list.add()

                item.name = mesh.name

                item.scatter_ui_index = len(mesh.scatter_mesh_list)

                mesh.scatter_list_index = len(mesh.scatter_mesh_list)-1

                scatter_fill_original_pointer(mesh)

        except (AttributeError, KeyError):
            pass

        return {'FINISHED'}
# ------------------------------------------------------------------------------
# DELETE OBJECT FROM LIST


class scatter_panel_remove_objects (bpy.types.Operator):
    """Remove item from the list"""

    bl_label = ""
    bl_idname = "object.button_scatter_panel_remove_objects"

    remove: bpy.props.StringProperty()
    scatter_mesh_name: bpy.props.StringProperty()

    def execute(self, context):
        try:
            mesh = bpy.data.meshes[self.scatter_mesh_name]
            index = mesh.scatter_list_index
            if self.remove == 'REMOVE':
                mesh.scatter_list_index -= 1
                mesh.scatter_mesh_list.remove(index)
                scatter_clean_original_pointer()
                # maybe user deleted active boolean
        except (AttributeError, KeyError):
            pass

        return {'FINISHED'}

# ------------------------------------------------------------------------------
# DEFINES


def scatter_find_instances(scatter_mesh_data):
    """Finds the instances"""
    r = []
    for o in bpy.data.objects:
        if (o.type == 'MESH'):
            if scatter_true_mesh_data(o) == scatter_mesh_data:
                r.append(o)
    return r


def scatter_fill_original_pointer(scatter_mesh_data):
    """Pointer filled first active object"""

    for ob in scatter_find_instances(scatter_mesh_data):
        # if ui list not empty but pointer is -> fill pointer
        if (len(ob.data.scatter_mesh_list) > 0) and (not ob.scatter_item_obj):
            ob.scatter_item_obj = scatter_mesh_data
    return None


def scatter_clean_original_pointer():
    """Clean original pointer"""

    for ob in bpy.data.objects:
        if ob.type == 'MESH':
            # if ui list empty but pointer original full -> restore and clean
            if (ob.scatter_item_obj) and (len(ob.scatter_item_obj.scatter_mesh_list) == 0):
                if ob.data != ob.scatter_item_obj:
                    ob.data = ob.scatter_item_obj
                ob.scatter_item_obj = None
    return None


def scatter_true_mesh_data(obj):
    """Original Mesh Data"""
    try:
        if obj.scatter_item_obj:
            return obj.scatter_item_obj
        else:
            return obj.data
    except AttributeError:
        pass


def scatter_return_one_time(mesh, active_idx, prop_api):
    """Returning once per elements"""
    AB_list = mesh.scatter_mesh_list
    for i in AB_list:
        if i.scatter_ui_index != active_idx:
            exec(f"i.{prop_api}= False")
    return None


def scatter_item_upd(self, context):
    if not self.scatter_item:
        self.scatter_render_frame = self.scatter_display = False
    return None


def scatter_display_upd(self, context):
    if self.scatter_display == True:
        scatter_return_one_time(
            self.id_data, self.scatter_ui_index, "scatter_display")
    bpy.data.particles["AB_Scatter"].type = 'HAIR'
    bpy.data.particles["AB_Scatter"].render_type = 'OBJECT'
    bpy.data.particles["AB_Scatter"].instance_object = bpy.data.objects["Cube"]

    return None

# ------------------------------------------------------------------------------
# SCATTER PROPERTY GROUP


class scatter_panel_list_item(bpy.types.PropertyGroup):
    id: bpy.props.IntProperty()
    object: bpy.props.PointerProperty(
        name="Object",
        type=bpy.types.Object,)

    # Name of the items in the list
    name: bpy.props.StringProperty(description="Object Name")
    # Random props in the lists
    scatter_ui_index: bpy.props.IntProperty(description='UI List Index')
    scatter_item: bpy.props.PointerProperty(
        type=bpy.types.Mesh, description='Mesh Name', update=scatter_item_upd)
    scatter_display: bpy.props.BoolProperty(
        default=False, description="Display in Viewport", update=scatter_display_upd)

    def copy(self):
        self.object = self.id_data.copy()
        self.name = self.object.name
        return self.object

    def add(self, ob):
        self.object = ob
        self.name = ob.name
        return self.object

def register():
    bpy.utils.register_class(SCATTER_PT_Panel)
    bpy.utils.register_class(scatter_panel_make_real_objects)
    bpy.utils.register_class(SCATTER_UL_Object_List)
    bpy.utils.register_class(scatter_panel_add_objects)
    bpy.utils.register_class(scatter_panel_remove_objects)
    bpy.utils.register_class(scatter_panel_list_item)
    bpy.utils.register_class(SCATTER_PT_Scatter_As)
    bpy.utils.register_class(SCATTER_PT_Paint_Panel)
    bpy.utils.register_class(SCATTER_PT_Rotation_Panel)
    bpy.utils.register_class(SCATTER_PT_Object)
    bpy.utils.register_class(SCATTER_PT_Collection)
    bpy.utils.register_class(SCATTER_PT_Collection_Use_Count)
    bpy.utils.register_class(SCATTER_PT_Extra)
    # Object
    bpy.types.Object.scatter_item_obj = bpy.props.PointerProperty(type=bpy.types.Mesh, description='Original Mesh-Data name')
    # Mesh
    bpy.types.Mesh.scatter_mesh_list = bpy.props.CollectionProperty(type=scatter_panel_list_item)
    bpy.types.Mesh.scatter_list_index = bpy.props.IntProperty(
        name="Index for scatter_mesh_list", default=0)

 
  

def unregister():
    bpy.utils.unregister_class(SCATTER_PT_Panel)
    bpy.utils.unregister_class(scatter_panel_make_real_objects)
    bpy.utils.unregister_class(SCATTER_UL_Object_List)
    bpy.utils.unregister_class(scatter_panel_add_objects)
    bpy.utils.unregister_class(scatter_panel_remove_objects)
    bpy.utils.unregister_class(scatter_panel_list_item)
    bpy.utils.unregister_class(SCATTER_PT_Scatter_As)
    bpy.utils.unregister_class(SCATTER_PT_Paint_Panel)
    bpy.utils.unregister_class(SCATTER_PT_Rotation_Panel)
    bpy.utils.unregister_class(SCATTER_PT_Object)
    bpy.utils.unregister_class(SCATTER_PT_Collection)
    bpy.utils.unregister_class(SCATTER_PT_Collection_Use_Count)
    bpy.utils.unregister_class(SCATTER_PT_Extra)

    del bpy.types.Mesh.scatter_mesh_list
    del bpy.types.Mesh.scatter_list_index
    del bpy.types.Object.scatter_item_obj
    
    
    
    