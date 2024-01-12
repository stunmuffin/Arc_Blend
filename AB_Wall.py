import bpy
import math
from math import pi
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view
import mathutils
import bmesh

class WALL_OT_CreateWall(bpy.types.Operator):
    bl_idname = "object.create_wall"
    bl_label = "Create Wall"
    bl_description = "Creates a simple Wall location at 3D Cursor"

    width: bpy.props.FloatProperty(
        name="Width",
        default=2.0,
        min=0.01,
        description="Wall width"
    )
    height: bpy.props.FloatProperty(
        name="Height",
        default=3.0,
        min=0.01,
        description="Wall height"
    )
    depth: bpy.props.FloatProperty(
        name="Depth",
        default=0.2,
        min=0.01,
        description="Wall depth"
    )
    rotation_x: bpy.props.FloatProperty(
        name="Rotation X",
        default=0.0,
        description="Rotation angle around X-axis in degrees"
    )
    rotation_y: bpy.props.FloatProperty(
        name="Rotation Y",
        default=0.0,
        description="Rotation angle around Y-axis in degrees"
    )
    rotation_z: bpy.props.FloatProperty(
        name="Rotation Z",
        default=0.0,
        description="Rotation angle around Z-axis in degrees"
    )
    name: bpy.props.StringProperty(
        name="Object Name",
        default="Wall",
        description="Name of the created object"
    )

    def execute(self, context):
        # Store the current cursor location
        cursor_location = bpy.context.scene.cursor.location.copy()
        # Create a wall using the specified dimensions and rotation at the 3D cursor location
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=cursor_location)
        wall = bpy.context.object
        wall.dimensions = (self.width, self.depth, self.height)
        wall.rotation_euler = (self.rotation_x, self.rotation_y, self.rotation_z)
        wall.name = self.name
        wall.location.z = cursor_location.z + (self.height * 0.5)
        wall.location.x = cursor_location.x - (self.width * 0.5)
        wall.location.y = cursor_location.y - (self.depth * 0.5)
        # Calculate and set the origin point to the corner and in the middle
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        bpy.context.active_object.rotation_euler[2] = math.radians(180)
        #bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='BOUNDS')

        return {'FINISHED'}

class WALL_OT_FlipWall(bpy.types.Operator):
    bl_idname = "object.flip_wall"
    bl_label = "Flip Wall"
    #bl_options = {'REGISTER', 'UNDO'}

    flip_direction: bpy.props.EnumProperty(
        name="Flip Direction",
        items=[
            ('X', "X-Axis", "Flip along the X-Axis", '', 0),
            ('Y', "Y-Axis", "Flip along the Y-Axis", '', 1),
            ('Z', "Z-Axis", "Flip along the Z-Axis", '', 2),
        ],
        default='X'
    )

    def execute(self, context):
        #Get the 3D cursor's location
        cursor_location = bpy.context.scene.cursor.location.copy()
        # Mirror the locations of selected wall objects along the chosen axis
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                if bpy.context.scene.flip_direction == 'X':
                    bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'
                    bpy.ops.transform.mirror(orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False))
                    #obj.location.x = cursor_location.x + (cursor_location.x - obj.location.x)
                elif bpy.context.scene.flip_direction == 'Y':
                    bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'
                    bpy.ops.transform.mirror(orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False))
                    #obj.location.y = cursor_location.y + (cursor_location.y - obj.location.y)
                elif bpy.context.scene.flip_direction == 'Z':
                    bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'
                    bpy.ops.transform.mirror(orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True))
                    #obj.location.z = cursor_location.z + (cursor_location.z - obj.location.z)

        return {'FINISHED'}

#--------------------------------------------------------------------------------------
#Rotate Wall CCW

class WALL_OT_RotateWallCCW(bpy.types.Operator):
    bl_idname = "object.rotate_wall_ccw"
    bl_label = "Rotate Wall Rotate(CCW) "

    def execute(self, context):

        # Mirror the locations of selected wall objects along the chosen axis
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                bpy.context.active_object.rotation_euler[2] += math.radians(90)

        return {'FINISHED'}

#--------------------------------------------------------------------------------------
#Rotate Wall CW

class WALL_OT_RotateWallCW(bpy.types.Operator):
    bl_idname = "object.rotate_wall_cw"
    bl_label = "Rotate Wall Rotate(CW) "

    def execute(self, context):

        # Mirror the locations of selected wall objects along the chosen axis
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                bpy.context.active_object.rotation_euler[2] -= math.radians(90)
        return {'FINISHED'}

#--------------------------------------------------------------------------------------
#Extend Wall

class WALL_OT_ExtendWall(bpy.types.Operator):
    bl_idname = "object.extend_wall"
    bl_label = "Extend Wall"
    
    def execute(self, context):
            selected_object = bpy.context.active_object
            cursor_location = bpy.context.scene.cursor.location
            rotation = round(math.degrees(selected_object.rotation_euler.z))

            # Extend Wall Operator
            for obj in bpy.context.selected_objects:
                if obj.type == 'MESH':
                    delta_x = cursor_location.x - obj.location.x
                    delta_y = cursor_location.y - obj.location.y
                    obj.scale.x = abs(delta_x) if rotation % 180 == 0 else abs(delta_y)
            return {'FINISHED'}

#--------------------------------------------------------------------------------------
#Select Active Wall

class WALL_OT_SelectActiveWall(bpy.types.Operator):
    bl_idname = "object.select_wall"
    bl_label = "Select Active Wall"
    
    def execute(self, context):
            bpy.context.object.select_set(True)
            return {'FINISHED'}

#--------------------------------------------------------------------------------------
#Join Selected Wall

class WALL_OT_JoinWalls(bpy.types.Operator):
    bl_idname = "object.join_walls"
    bl_label = "Join Walls"
    bl_description = "Join selected walls into one object"

    @classmethod
    def poll(cls, context):
        # Check if there are selected objects and all are meshes
        return context.selected_objects and all(obj.type == 'MESH' for obj in context.selected_objects)

    def execute(self, context):
        selected_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']

        if len(selected_objects) > 1:
            # Check if there is an active object among the selected objects
            if any(obj == context.active_object for obj in selected_objects):
                # Deselect all objects
                bpy.ops.object.select_all(action='DESELECT')
                
                # Select the walls to join
                for obj in selected_objects:
                    obj.select_set(True)
                
                # Join the selected walls
                bpy.ops.object.join()

                # Display a message in the Blender interface
                self.report({'INFO'}, f"{len(selected_objects)} walls joined into one object.")
            else:
                self.report({'INFO'}, "Please ensure there is an active object selected.")
        else:
            self.report({'INFO'}, "Please select more than one wall to join.")
        return {'FINISHED'}

#--------------------------------------------------------------------------------------
#Seperates Selected Wall

class WALL_OT_SeparateWalls(bpy.types.Operator):
    bl_idname = "object.separate_walls"
    bl_label = "Separate Walls"
    bl_description = "Separates selected joined walls into individual objects and sets origin to the lowest left corner"
    @classmethod
    def poll(cls, context):
        # Check if there is an active object and it's a mesh
        return context.active_object and context.active_object.type == 'MESH'

    def execute(self, context):
        active_object = context.active_object
        # Check if the active object is a joined mesh
        if active_object and active_object.type == 'MESH':
            # Exit edit mode if in edit mode
            bpy.ops.object.mode_set(mode='OBJECT')
            # Separate the selected joined mesh into individual meshes without losing materials
            bpy.ops.mesh.separate(type='LOOSE')

            # Set the origin of each selected object to the lowest left corner
            for obj in bpy.context.selected_objects:
                set_origin_to_lowest_left_corner(obj)

            # Display a message in the Blender interface
            self.report({'INFO'}, "Joined walls separated into individual objects with origins set to the lowest left corner.")
        else:
            self.report({'INFO'}, "Please select a joined wall to separate.")
        return {'FINISHED'}

def set_origin_to_lowest_left_corner(obj):
    # Accessing object data and world matrix
    me = obj.data
    mw = obj.matrix_world
    # Transforming bounding box vertices to world space
    local_verts = [obj.matrix_world @ Vector(v[:]) for v in obj.bound_box]
    # Calculating the lowest left corner
    o = min(local_verts, key=lambda v: (v[0], v[1], v[2]))  # Get the minimum x, y, z
    # Transforming the calculated origin point back to object space
    o = obj.matrix_world.inverted() @ o
    # Applying the transformation to the mesh data
    me.transform(Matrix.Translation(-o))
    # Updating the object's world matrix translation
    mw.translation = mw @ o

#--------------------------------------------------------------------------------------
#2D line to 3D Wall

def offset_and_extrude_wall(obj, thickness, height):
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Switch to Edit Mode for the specific object
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')

    # Get the mesh data
    mesh = obj.data
    bm = bmesh.from_edit_mesh(mesh)

    # Delete faces
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.delete(type='ONLY_FACE')

    # Switch to Edge Mode
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
    bpy.ops.mesh.select_all(action='SELECT')

    # Offset and Extrude wall using bmesh
    selected_edges = [e for e in bm.edges if e.select]

    # Extrude selected edges
    bmesh.ops.extrude_edge_only(bm, edges=selected_edges)

    # Translate the extruded edges
    extrude_translation = (0, 0, height)
    bmesh.ops.translate(bm, verts=[v for v in bm.verts if v.select], vec=extrude_translation)

    # Switch back to Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')
    

class WALL_OT_ConvertTo2DPlane(bpy.types.Operator):
    bl_idname = "object.convert_to_2d_plane"
    bl_label = "Convert to 3D Wall"
    bl_description = "Convert a Line to a 3D Wall"

    def execute(self, context):
        thickness_x = bpy.context.scene.AB_Wall.thickness
        height_z = bpy.context.scene.AB_Wall.height

        # Check if any objects are selected
        selected_objects = bpy.context.selected_objects

        if any(obj.type == 'MESH' for obj in selected_objects):
            # Iterate over selected objects
            for target_object in selected_objects:
                # Assuming the first selected object is the target
                # Specify thickness and height
                thickness = thickness_x
                height = height_z

                # Execute the wall creation operation for each object
                offset_and_extrude_wall(target_object, thickness, height)

                # Set the active object to the target object
                bpy.context.view_layer.objects.active = target_object

                # Check if a Solidify modifier already exists
                solidify_modifier = None
                for modifier in target_object.modifiers:
                    if modifier.type == 'SOLIDIFY':
                        solidify_modifier = modifier
                        break

                # If Solidify modifier exists, use it; otherwise, add a new one
                if solidify_modifier:
                    # Modify existing Solidify modifier
                    solidify_modifier.name = "AB_Solidify"
                    solidify_modifier.solidify_mode = 'NON_MANIFOLD'
                    solidify_modifier.nonmanifold_thickness_mode = 'EVEN'
                    solidify_modifier.nonmanifold_boundary_mode = 'NONE'
                    solidify_modifier.thickness = thickness
                    solidify_modifier.offset = -1
                    solidify_modifier.nonmanifold_merge_threshold = 0.0001
                    solidify_modifier.use_rim = True
                else:
                    # Add a new Solidify modifier
                    bpy.ops.object.modifier_add(type='SOLIDIFY')
                    bpy.context.object.modifiers["Solidify"].name = "AB_Solidify"
                    bpy.context.object.modifiers["AB_Solidify"].solidify_mode = 'NON_MANIFOLD'
                    bpy.context.object.modifiers["AB_Solidify"].nonmanifold_thickness_mode = 'EVEN'
                    bpy.context.object.modifiers["AB_Solidify"].nonmanifold_boundary_mode = 'NONE'
                    bpy.context.object.modifiers["AB_Solidify"].thickness = thickness
                    bpy.context.object.modifiers["AB_Solidify"].offset = -1
                    bpy.context.object.modifiers["AB_Solidify"].nonmanifold_merge_threshold = 0.0001
                    bpy.context.object.modifiers["AB_Solidify"].use_rim = True

                    self.report({'INFO'}, "Wall creation successful.")
        else:
            bpy.context.window_manager.popup_menu(
                lambda self, context: self.layout.label(text="You have to select at least 1 'MESH' object"),
                title="Warning", icon='ERROR'
            )
        return {'FINISHED'}
    
#--------------------------------------------------------------------------------------
# Property Group
    
class WallPropertiesGroup(bpy.types.PropertyGroup):

    thickness: bpy.props.FloatProperty(
        name="Thickness",
        default=0.2 ,
        min=0,
        description="Thickness of Wall"
        )
        
    height : bpy.props.FloatProperty(
        name="Height",
        default=3 ,
        min=0,
        description="Height of Wall"
        )
#--------------------------------------------------------------------------------------
#Snap Magnet 

def snap_update(self, context):
    if self.snap_vertex:
        context.scene.tool_settings.use_snap = True
        context.scene.tool_settings.snap_elements = {'VERTEX'}
    else:
        context.scene.tool_settings.use_snap = False
    return None


#--------------------------------------------------------------------------------------
#Flip Normals

class Wall_OT_FlipNormals(bpy.types.Operator):
    """Flip Normals"""
    bl_label = "Flip Normals"
    bl_idname = "object.wall_flipnormals"

    def execute(self, context):
        # Check if there is an active object
        if context.active_object and context.active_object.type == 'MESH':
            # Check if not in Edit Mode or not in Face Select mode
            if context.mode != 'EDIT' or bpy.context.tool_settings.mesh_select_mode[0] == False:
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')

            bpy.ops.mesh.flip_normals()

            # Check if still in Edit Mode
            if context.mode == 'EDIT':
                bpy.ops.object.mode_set(mode='OBJECT')

        else:
            self.report({'INFO'}, "Select a valid mesh object first.")

        return {"FINISHED"}

#--------------------------------------------------------------------------------------
#Edit Mode Face Selection Active

class OBJECT_OT_EnterEditMode(bpy.types.Operator):
    bl_idname = "object.enter_edit_mode"
    bl_label = "Enter Edit Mode with Face Selection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Check if there is an active object
        if context.active_object and context.active_object.type == 'MESH':
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(type='FACE')
        else:
            self.report({'INFO'}, "Select a valid mesh object first.")

        return {'FINISHED'}

#--------------------------------------------------------------------------------------
#Edit mode face seperates Wall
class Wall_OT_SeparateFaces(bpy.types.Operator):
    """Separate Selected Faces"""
    bl_label = "Separate Faces"
    bl_idname = "object.wall_separate_faces"

    def execute(self, context):
        # Check if there is an active object
        if context.active_object and context.active_object.type == 'MESH':
            bpy.ops.object.mode_set(mode='EDIT')

            # Check if there are selected faces
            bpy.ops.mesh.select_mode(type='FACE')
            
            # Separate selected faces into a new object
            bpy.ops.mesh.separate(type='SELECTED')

        else:
            self.report({'INFO'}, "Select a valid mesh object first.")

        return {'FINISHED'}
#--------------------------------------------------------------------------------------
#Wall Panel 

class WALL_PT_Panel(bpy.types.Panel):
    bl_label = "AB Wall"
    bl_idname = "WALL_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Arc Blend"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene= context.scene
        AB_Wall = bpy.context.scene.AB_Wall
        # Create Wall Section
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Create 3D Wall:", icon='MESH_CUBE')
        row = col.row(align=True)
        row.operator("object.create_wall", text="Create 3D Wall")
        col.prop(scene, "snap_vertex", text="Snap", icon='SNAP_ON')
        # Wall Manipulation Section
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Wall Manipulation:", icon='MODIFIER')
        row = col.row(align=True)
        row.operator("object.flip_wall", text="Flip")
        row.prop(context.scene, "flip_direction", text="")
        row = col.row(align=True)
        row.operator("object.rotate_wall_ccw", text="Rotate CCW")
        row.operator("object.rotate_wall_cw", text="Rotate CW")
        row = col.row(align=True)
        row.operator("object.extend_wall", text="Extend Wall")
        # Wall Management Section
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Wall Management:", icon='OUTLINER_OB_MESH')
        row = col.row(align=True)
        row.operator("object.join_walls", text="Join Walls")
        row.operator("object.separate_walls", text="Separate Walls")
        #Create a collapsible sub-panel for Wall Properties and Edit Rotation
        sub_panel = layout.box()
        sub_panel.prop(scene, "show_sub_panel", text="3D Wall Settings", icon='SETTINGS')
        if scene.show_sub_panel and bpy.context.object and bpy.context.object.type == 'MESH' :
            # Wall Properties Section
            sub_panel.prop(scene, "show_wall_properties", text="Show Wall Properties")
            if scene.show_wall_properties and bpy.context.object and bpy.context.object.type == 'MESH':
                sub_panel.label(text="Wall Properties:", icon='OBJECT_DATA')
                col = sub_panel.column(align=True)
                col.prop(bpy.context.object, "name", text="Wall Name")
                col.prop(bpy.context.object, "dimensions", index=0, text="Width")
                col.prop(bpy.context.object, "dimensions", index=1, text="Thickness")
                col.prop(bpy.context.object, "dimensions", index=2, text="Height")
                col.separator()
            # Edit Rotation Section
            sub_panel.prop(scene, "show_edit_rotation", text="Show Edit Rotation")
            if scene.show_edit_rotation and bpy.context.object and bpy.context.object.type == 'MESH':
                sub_panel.label(text="Edit Rotation (Degrees):")
                col = sub_panel.column(align=True)
                col.prop(bpy.context.object, "rotation_euler", index=0, text="Rotation X")
                col.prop(bpy.context.object, "rotation_euler", index=1, text="Rotation Y")
                col.prop(bpy.context.object, "rotation_euler", index=2, text="Rotation Z")
        
        #Create a collapsible sub-panel for 2D Wall Properties and Edit Rotation
        sub_panel = layout.box()
        sub_panel.prop(scene, "show_2d_wall", text="2D Wall Settings", icon='SETTINGS')
        if scene.show_2d_wall and bpy.context.object and bpy.context.object.type == 'MESH':
                sub_panel.label(text="2D Wall Settings:")
                col = layout.box()
                col.label(text="Step 1 (2D line to 3D Wall):")
                #col = sub_panel.column(align=True)
                
                col.prop(AB_Wall, "thickness" , text= "Thickness")
                col.prop(AB_Wall, "height" , text= "Height")
                col.operator("object.convert_to_2d_plane", text="2D Line to 3D Wall")
                
                col = layout.box()
                col.label(text="Step 2 (Height and Thickness):")
                col.prop(bpy.context.object, "dimensions", index=2, text="Height")
                # Check if the active object has a "AB_Solidify" modifier
                # Get the active object
                obj = context.active_object
                if obj and "AB_Solidify" in obj.modifiers:
                    solidify_modifier = obj.modifiers["AB_Solidify"]
                    # Add a property slider for thickness
                    col.prop(solidify_modifier, "thickness")
                else:
                    pass
                col = layout.box()
                col.label(text="Step 3 (Adjust Wall Sides):")
                col.label(text="*Face Selection in Edit Mode")
                col.operator("object.enter_edit_mode", text="Face Selection Active")
                col.operator("object.wall_flipnormals", text="Flip Wall Side")
                col.operator("object.wall_separate_faces", text="Seperate Face Walls")


# ------------------------------------------------------------------------------
# REGISTRATION AREA
        
def register():
    bpy.utils.register_class(WALL_OT_CreateWall)
    bpy.utils.register_class(WALL_OT_FlipWall)
    bpy.utils.register_class(WALL_PT_Panel)
    bpy.utils.register_class(WALL_OT_RotateWallCCW)
    bpy.utils.register_class(WALL_OT_RotateWallCW)
    bpy.utils.register_class(WALL_OT_ExtendWall)
    bpy.utils.register_class(WALL_OT_SelectActiveWall)
    bpy.types.Scene.flip_direction = bpy.props.EnumProperty(
        name="Flip Direction",
        items=[
            ('X', "X-Axis", "Flip along the X-Axis", '', 0),
            ('Y', "Y-Axis", "Flip along the Y-Axis", '', 1),
            ('Z', "Z-Axis", "Flip along the Z-Axis", '', 2),
        ],
        default='X'
    )
    # Define the boolean properties
    bpy.types.Scene.show_sub_panel = bpy.props.BoolProperty(
        name="Show Wall Settings",
        default=False,
        description="Toggle visibility of Wall Settings sub-panel"
    )
    bpy.types.Scene.show_wall_properties = bpy.props.BoolProperty(
        name="Show Wall Properties",
        default=False,
        description="Toggle visibility of Wall Properties"
    )
    bpy.types.Scene.show_edit_rotation = bpy.props.BoolProperty(
        name="Show Rotation Properties",
        default=False,
        description="Toggle visibility of Wall Properties"
    )
    bpy.types.Scene.snap_vertex = bpy.props.BoolProperty(
        name="Snap Vertex",
        default=False,
        description="Snap Vertex",
        update =snap_update
    )
    bpy.types.Scene.show_2d_wall = bpy.props.BoolProperty(
        name="Show 2D Wall Settings",
        default=False,
        description="Toggle visibility of Wall Settings sub-panel"
    )
    bpy.utils.register_class(WALL_OT_JoinWalls)
    bpy.utils.register_class(WALL_OT_SeparateWalls)
    bpy.utils.register_class(WALL_OT_ConvertTo2DPlane)
    bpy.utils.register_class(WallPropertiesGroup)
    bpy.types.Scene.AB_Wall = bpy.props.PointerProperty(type=WallPropertiesGroup)
    bpy.utils.register_class(Wall_OT_FlipNormals)
    bpy.utils.register_class(OBJECT_OT_EnterEditMode)
    bpy.utils.register_class(Wall_OT_SeparateFaces)
    
  
def unregister():
    bpy.utils.unregister_class(WALL_OT_CreateWall)
    bpy.utils.unregister_class(WALL_OT_FlipWall)
    bpy.utils.unregister_class(WALL_PT_Panel)
    bpy.utils.unregister_class(WALL_OT_RotateWallCCW)
    bpy.utils.unregister_class(WALL_OT_RotateWallCW)
    bpy.utils.unregister_class(WALL_OT_ExtendWall)
    bpy.utils.unregister_class(WALL_OT_SelectActiveWall)
    del bpy.types.Scene.flip_direction
    del bpy.types.Scene.show_sub_panel
    del bpy.types.Scene.show_wall_properties
    del bpy.types.Scene.show_edit_rotation
    bpy.utils.unregister_class(WALL_OT_JoinWalls)
    bpy.utils.unregister_class(WALL_OT_SeparateWalls)
    bpy.utils.unregister_class(WALL_OT_ConvertTo2DPlane)
    bpy.utils.unregister_class(WallPropertiesGroup)
    del bpy.types.Scene.AB_Wall
    bpy.utils.unregister_class(Wall_OT_FlipNormals)
    bpy.utils.unregister_class(OBJECT_OT_EnterEditMode)
    bpy.utils.unregister_class(Wall_OT_SeparateFaces)
