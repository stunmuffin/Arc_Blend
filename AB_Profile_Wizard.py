import bpy
import os
import bpy.utils.previews
from mathutils import Matrix, Vector
from bpy_extras.view3d_utils import location_3d_to_region_2d
from math import radians
from bpy.props import StringProperty, EnumProperty, IntProperty


class UpdatePreviewsDirOperator(bpy.types.Operator):
    bl_idname = "wm.update_previews_dir"
    bl_label = "Update Previews Directory"
    bl_description = "Update my_previews_dir property"

    directory: StringProperty(subtype='DIR_PATH')

    def execute(self, context):
        if "WinMan" in bpy.data.window_managers:
            # Set another property to trigger an update
            bpy.data.window_managers["WinMan"].my_previews_update_trigger = not bpy.data.window_managers["WinMan"].my_previews_update_trigger
            bpy.data.window_managers["WinMan"].my_previews_dir = self.directory
            self.report({'INFO'}, f"Previews directory updated to: {self.directory}")
        else:
            self.report({'WARNING'}, "Window manager 'WinMan' not found")

        return {'FINISHED'}



def update_select_image(self, context):
    select_image = context.scene.image_property.select_image
    if select_image:
        context.scene.image_property.select_image = select_image


class ImagePropertiesGroup(bpy.types.PropertyGroup):
    image_preview_grid_settings: bpy.props.BoolProperty(
        name="Image Preview Grid Settings",
        description="Image Grid Settings"
    )
    
    select_image: bpy.props.PointerProperty(
        name='Image',
        type=bpy.types.Image,
        update=update_select_image
    )
    
    show_image_preview: bpy.props.BoolProperty(
        name="Show Image Preview",
        description="Show Image Preview"
    )
    
    show_preview_grid: bpy.props.BoolProperty(
        name="Show Preview in Grid",
        description="Show Preview in Grid",
        default=False,
    )
    
    thumbnail_path: bpy.props.StringProperty(
        name="Thumbnail Path",
        description="Absolute path to the image thumbnail",
        default="",
        subtype='FILE_PATH'
    )

bpy.types.Scene.image_icon_scale = bpy.props.FloatProperty(
    name="Icon Scale",
    default=9.0,
    min=0.1,
    description="Scale of the image preview icons"
)

preview_collections = {}

def enum_previews_from_directory_items(self, context):
    pcoll = preview_collections.get("main")
    if not pcoll:
        return []

    if bpy.data.window_managers["WinMan"].my_previews_dir == "":
        return []

    return pcoll.my_previews


class ABMoldingPanel(bpy.types.Panel):
    bl_label = "AB Profile Wizard"
    bl_idname = "PT_ABMoldingPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Arc Blend"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        category_moldings = context.scene.category_moldings
        layout.prop(category_moldings, "profile_type_enum", text="MOLDINGS")
        col = layout.column()
        if context.scene.category_moldings.profile_type_enum == 'Crown_Molding':
            self.draw_crown_molding_profiles(layout)
        else:
            pass
     
    def draw_crown_molding_profiles(self, layout):
        context= bpy.context
        layout = self.layout
        obj = bpy.context.active_object
        category_moldings = context.scene.category_moldings
        active_obj = bpy.context.active_object
        #profile_object = bpy.data.objects[bpy.data.curves[active_obj.name].bevel_object.name]

        layout = self.layout
        box = layout.box()
        col = box.column()
        col.label(text="Built-in Profiles:")
        wm = context.window_manager
        col.prop(wm, "my_previews_dir")
        col.template_icon_view(wm, "my_previews", scale=context.scene.image_icon_scale, show_labels=True, scale_popup=4)
        images = bpy.data.images
        # Corrected placement of the reload button
        col.operator("object.update_image_paths", text="Refresh Images", icon= "FILE_REFRESH")
        #col.label(text="Image Icon Size:")
        #col.prop(context.scene, "image_icon_scale")
        col.label(text="Pick Profiles:")
        col.prop(category_moldings, "reference_profile", text="Pick Profile")
        col.operator("object.make_profile", text="Create Crown Profile", icon="OUTLINER_OB_MESH")
        col.operator("object.change_profile", text="Change Crown Profile", icon="VIEW_PAN")
        col.operator("object.change_from_pick_profile", text="Change from Pick Profile", icon="OUTLINER_DATA_CURVE")
        col.split()
        if obj:
            col.label(text="Change Dimensions:")
            col.prop(bpy.context.object, "name",  text="Profile Name",emboss=False)
            row=col.row(align=True)
            row.operator("object.select_profile", text="Select The Profile" , icon="RESTRICT_SELECT_OFF")
            row.operator("object.select_main_curve", text="Select Main Curve" , icon="OUTLINER_OB_CURVE")
            
            col=box.column(align=True)
            if bpy.context.object.type == 'CURVE' and bpy.context.object.data.bevel_object:
                profile_object = bpy.data.objects.get(obj.data.bevel_object.name)
                col.label(text="Profile Options:")
                col.prop(profile_object, "dimensions", index=0, text="Width:")
                col.prop(profile_object, "dimensions", index=1, text="Height:")
            else:
                col.label(text="<Please Make Sure Curve  and has Profile!>")
                
            col=box.column(align=False)
            col.prop(category_moldings, "position_enum", text="Change Orgin")
            col.operator("object.bounding_box_origin_control", text="Change Origin", icon="OBJECT_ORIGIN")
            col=box.column(align=True)
            col.label(text="Profile Mirror :")
            col=box.column(align=True)
            col.prop(category_moldings, "flip_direction", text="")
            col.operator("object.flip_profile", text="Mirror", icon="MOD_MIRROR")
            col.label(text="Curve Tilt :")
            row=col.row(align=True)
            row.operator("transform.tilt", text="Tilt Profile")
            row.operator("object.tilt_clearprofile", text="Clear Tilt")
            row=col.row()

            col=box.column(align=False)
            col.label(text="Convert Options:")
            col.operator("object.convert_to_curve", text="Convert to Curve" ,icon="OUTLINER_OB_CURVE")
            col.operator("object.convert_to_mesh", text="Convert to Mesh" ,icon="OUTLINER_OB_MESH")
            col=box.column(align=False)
            

            if obj.type == "CURVE":
                col.label(text="Curve Options:")
                curve = context.active_object.data
                row=col.row()
                row.prop(curve, "dimensions", expand=True)
                row=col.row()
                row.prop(curve, "twist_mode")
                row=col.row()
                row.prop(curve, "fill_mode")
                row=col.row()
                row.prop(curve, "offset")
                row=col.row()
                row.prop(curve, "bevel_mode", expand=True)
                col.use_property_split = True
                if curve.bevel_mode == 'OBJECT':
                    col.prop(curve, "bevel_object", text="Object")
                else:
                    col.prop(curve, "bevel_depth", text="Depth")
                    col.prop(curve, "bevel_resolution", text="Resolution")
                col.prop(curve, "use_fill_caps")
                if curve.bevel_mode == 'PROFILE':
                    col.template_curveprofile(curve, "bevel_profile")
                    row=col.row(align=True)
                    row.operator("object.save_profile", text="Save Custom Profile")
                    row.operator("object.load_profile", text="Load Custom Profile")
                row=col.row()
                row.operator("curve.cyclic_toggle", text="Toggle Cyclic")
                row=col.row()
                row.operator("curve.switch_direction", text="Switch Direction")
                
        else:
            box.label(text="<Select a Profile or Create!>")

        


def preview_dir_update(wm, context):
    """EnumProperty callback"""
    enum_items = []

    wm = context.window_manager
    directory = wm.my_previews_dir

    pcoll = preview_collections["main"]

    print("Scanning directory: %s" % directory)

    if directory and os.path.exists(directory):
        pcoll = preview_collections["main"]
        # Clear existing previews before loading new ones
        pcoll.clear()

        image_paths = [fn for fn in os.listdir(directory) if fn.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp"))]

        for i, name in enumerate(image_paths):
            filepath = os.path.join(directory, name)
            thumb = pcoll.load(name, filepath, 'IMAGE')
            # Remove file extension from the name
            name_without_extension, extension = os.path.splitext(name)

            enum_items.append((name, name_without_extension, "", thumb.icon_id, i))
            
            #enum_items.append((name, name, "", thumb.icon_id, i))

    pcoll.my_previews = enum_items
    pcoll.my_previews_dir = directory
    
    return None


def preview_enum_update(wm, context):
    return None

# Reload Area
class UpdateImagePathsOperator(bpy.types.Operator):
    bl_idname = "object.update_image_paths"
    bl_label = "Update Image Paths"
    bl_description = "Update and reload image paths"

    def execute(self, context):
        wm = context.window_manager
        try:
            preview_dir_update(wm, context)
            
        except KeyError:
            pass
        return {'FINISHED'}



#----------------------------------------------------------------------
#Change Profile Built-in Profiles

class OBJECT_OT_ChangeProfile(bpy.types.Operator):
    bl_idname = "object.change_profile"
    bl_label = "Change Profile"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Change the profile of the selected curve"

    def execute(self, context):
        
        #Profile Name
        name_define = bpy.data.window_managers["WinMan"].my_previews[:-4]
        
        # Get the active object (should be a curve)
        active_obj = context.active_object

        # Check if the active object is a curve
        if active_obj and active_obj.type == 'CURVE':
            # Check if the curve has a bevel object
            if active_obj.data.bevel_object:
                # Save the current profile name
                current_profile_name = active_obj.data.bevel_object.name

                # Check if the desired profile exists in the data
                target_profile_name = name_define
                #bpy.context.scene.category_moldings.crown_molding_profile

                if target_profile_name not in bpy.data.objects:
                    # Create a new profile if it doesn't exist
                    bpy.ops.object.make_profile()

                # Set the bevel object to the new or existing profile
                active_obj.data.bevel_object = bpy.data.objects[target_profile_name]

                self.report({'INFO'}, f"Profile changed to '{target_profile_name}'")

                # Select the curve object
                bpy.context.view_layer.objects.active = active_obj
                active_obj.select_set(True)
            else:
                # Change bevel mode to 'OBJECT'
                active_obj.data.bevel_mode = 'OBJECT'

                # Check if the desired profile exists in the data
                target_profile_name = name_define
                #bpy.context.scene.category_moldings.crown_molding_profile
                if target_profile_name not in bpy.data.objects:
                    # Create a new profile if it doesn't exist
                    bpy.ops.object.make_profile()

                # Set the bevel object to the new or existing profile
                active_obj.data.bevel_object = bpy.data.objects[target_profile_name]

                # Select the curve object
                bpy.context.view_layer.objects.active = active_obj
                active_obj.select_set(True)

                self.report({'INFO'}, f"Profile assigned to '{target_profile_name}'")
        else:
            self.report({'ERROR'}, "Please select a curve object.")

        return {'FINISHED'}


#----------------------------------------------------------------------
#Change Profile from Pick Profiles

class OBJECT_OT_ChangeFromPickProfile(bpy.types.Operator):
    bl_idname = "object.change_from_pick_profile"
    bl_label = "Change from Pick Profile"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Change the profile of the selected curve to the picked object's profile"



    def execute(self, context):
        # Get the active object (should be a curve)
        active_obj = context.active_object

        # Check if the active object is a curve
        if active_obj and active_obj.type == 'CURVE':
            # Check if the curve has a bevel object
            if active_obj.data.bevel_object:
                # Save the current profile name
                current_profile_name = active_obj.data.bevel_object.name

                # Check if there is a picked object
                picked_obj = bpy.context.scene.category_moldings.reference_profile
                if picked_obj and picked_obj.type == 'CURVE':
                    # Set the bevel object to the picked object's profile
                    active_obj.data.bevel_object = picked_obj

                    self.report({'INFO'}, f"Profile changed to '{picked_obj.name}'")

                    # Select the curve object
                    bpy.context.view_layer.objects.active = active_obj
                    active_obj.select_set(True)
                else:
                    self.report({'ERROR'}, "Please pick a curve object as the profile.")
            else:
                obj_ab_pick = bpy.context.scene.category_moldings.reference_profile
                if  bpy.context.scene.category_moldings.reference_profile.type == 'CURVE':
                    # Change bevel mode to 'OBJECT'
                    active_obj.data.bevel_mode = 'OBJECT'
                    # Set the bevel object to the new or existing profile
                    active_obj.data.bevel_object = bpy.data.objects[bpy.context.scene.category_moldings.reference_profile.name]
                    
                    self.report({'INFO'}, "The selected curve doesn't have a bevel object. Creating...")
                else:
                    self.report({'WARNING'}, f"You have to select 'CURVE' type Not! '{obj_ab_pick.type}' type! Change Pick Profile: '{obj_ab_pick.type}' to 'CURVE'!!!")
        else:
            self.report({'ERROR'}, "Please select a curve object.")
            

        return {'FINISHED'}

    
#----------------------------------------------------------------------
#Clear Tilt Profile
class ClearTiltProfileOperator(bpy.types.Operator):
    bl_idname = "object.tilt_clearprofile"
    bl_label = "Clear Tilt Profile"
    bl_description = "Clear the Tilts from Object"


    def execute(self, context):
        # Get the active object
        active_obj = bpy.context.active_object

        # Check if the active object is valid and has a curve associated with its bevel object
        if active_obj and active_obj.type == 'CURVE':
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.curve.select_all(action='SELECT')
            bpy.ops.curve.tilt_clear()
            bpy.ops.object.mode_set(mode='OBJECT')


        return {'FINISHED'}
#----------------------------------------------------------------------
#Selects Profile
class SelectProfileOperator(bpy.types.Operator):
    bl_idname = "object.select_profile"
    bl_label = "Select Profile"
    bl_description = "Selects from Curve to Profile Object!"

    def execute(self, context):
        active_obj = bpy.context.active_object

        # Check if the active object is valid and has a bevel object
        if active_obj and active_obj.type == 'CURVE' and active_obj.data and active_obj.data.bevel_object:
            active_curve = active_obj.data.bevel_object
            profile_name = active_curve.name

            # Check if the profile object exists
            if profile_name:
                # Clear the current selection
                bpy.ops.object.select_all(action='DESELECT')

                # Iterate through all objects in the scene
                for obj in bpy.context.scene.objects:
                    if obj.name == profile_name:
                        obj.select_set(True)  # Select the object
                        context.view_layer.objects.active = obj  # Make it the active object

            else:
                self.report({'WARNING'}, "No Profile Object Found!")

        else:
            self.report({'WARNING'}, "Invalid Active Object!")

        return {'FINISHED'}
#----------------------------------------------------------------------
#Selects Curve
class SelectMainCurveOperator(bpy.types.Operator):
    bl_idname = "object.select_main_curve"
    bl_label = "Select Main Curve"
    bl_description = "Selects from Profile to Curve Object!"

    def execute(self, context):
        # Get the active object
        obj_curve = []
        
        active_obj = bpy.context.active_object

        # Check if the active object is valid and has a curve associated with its bevel object
        if active_obj and active_obj.type == 'CURVE':
            active_objdata_name = active_obj.name
            obj_curve.append(active_objdata_name)
            #print(obj_curve[0])
            active_curve = bpy.data.curves.get(active_objdata_name)
            
            #print(active_curve.name)
            
            # Clear the current selection
            bpy.ops.object.select_all(action='DESELECT')
            
            scene_curve = []

            # Iterate through all objects in the scene
            for obj in bpy.context.scene.objects:
                #print(obj.data.name)
                if obj.type == 'CURVE':
                    scene_curve.append(obj.data)
            
            for curve in scene_curve:
                #print(curve.name)
                if curve.bevel_object and curve.bevel_object.name == obj_curve[0]:
                    for obj in bpy.context.scene.objects:
                        if obj.type == 'CURVE' and obj.data:
                            if obj.data.name == curve.name:
                                # Make it the active object
                                bpy.context.view_layer.objects.active = obj
                                # Select the curve object
                                bpy.context.view_layer.objects.active.select_set(True)
                                #print(curve.name)
                                #context.view_layer.objects.active = bpy.context.scene.objects[curve.name]  # Make it the active object
                                #bpy.context.view_layer.objects.active.select_set(True)
        else:
            self.report({'WARNING'}, "You have to select Profile! If the profile is not used by another curve you can still get this message!")


        return {'FINISHED'}

#----------------------------------------------------------------------
#Save Custom Curve Profile
class OBJECT_OT_SaveProfile(bpy.types.Operator):
    bl_idname = "object.save_profile"
    bl_label = "Save Bevel Profile"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Save Custom Curve Profile to your Computer as .txt file"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        # Check if there's an active object in the current context
        if context.active_object and context.active_object.type == 'CURVE':
            # Access the active object
            obj = context.active_object
            
            # Access the custom profile data
            custom_profile = obj.data.bevel_profile

            # Construct the file path using the object name
            file_dir = os.path.dirname(self.filepath)
            file_name = f"{obj.name}_Profile.txt"
            file_path = os.path.join(file_dir, file_name)

            # Save the profile points, curve object name, location, and handle types to the chosen text file
            with open(file_path, 'w') as file:
                file.write(f"Profile_Name: '{obj.name}'\n")
                
                # Save the profile points with custom numbering
                for i, point in enumerate(custom_profile.points, 1):
                    file.write(f"Number: {i}\n")
                    file.write(f"Location: {point.location.x},{point.location.y}\n")
                    file.write(f"Handle_Type_1: {point.handle_type_1}\n")
                    file.write(f"Handle_Type_2: {point.handle_type_2}\n")

            self.report({'INFO'}, f"Bevel profile saved to {file_path}")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "Please select a curve object before saving the profile.")
            return {'CANCELLED'}

    def invoke(self, context, event):
        # Open the file dialog
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

#-------------------------------------------------------------------------------
#Import Custom Curve Profile
class OBJECT_OT_LoadProfile(bpy.types.Operator):
    bl_idname = "object.load_profile"
    bl_label = "Load Bevel Profile"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Import Custom Curve Profile from your Computer .txt file\nBefore load you have to Preset >> Default to clear!"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        # Check if there's an active object in the current context
        if context.active_object and context.active_object.type == 'CURVE':
            # Access the active object
            obj = context.active_object

            # Check if the curve is using a custom bevel profile
            if hasattr(obj.data, 'bevel_profile'):
                # Read the saved profile data from the text file
                with open(self.filepath, 'r') as file:
                    lines = file.readlines()

                    # Create a dictionary to store points based on their indices
                    point_dict = {}

                    # Iterate over lines and update the bevel profile dictionary
                    for line in lines:
                        if line.startswith("Number:"):
                            current_index = int(line.split(":")[1])
                            point_dict[current_index] = {'Location': None, 'Handle_Type_1': None, 'Handle_Type_2': None}
                        elif line.startswith("Location:"):
                            x, y = map(float, line.split(":")[1].split(","))
                            point_dict[current_index]['Location'] = (x, y)
                        elif line.startswith("Handle_Type_1:"):
                            point_dict[current_index]['Handle_Type_1'] = line.split(":")[1].strip()
                        elif line.startswith("Handle_Type_2:"):
                            point_dict[current_index]['Handle_Type_2'] = line.split(":")[1].strip()

                # Reconstruct the bevel profile using the stored dictionary
                for index in sorted(point_dict.keys()):
                    data = point_dict[index]

                    # Skip the first and last points as they are path points
                    if index != 1 and index != max(point_dict.keys()):
                        new_point = obj.data.bevel_profile.points.add(x, y)
                        new_point.location = (data['Location'][0], data['Location'][1])
                        new_point.handle_type_1 = data['Handle_Type_1']
                        new_point.handle_type_2 = data['Handle_Type_2']

                self.report({'INFO'}, f"Bevel profile loaded from {self.filepath}")
                return {'FINISHED'}
            else:
                self.report({'WARNING'}, "Please make sure the curve is using a custom bevel profile.")
                return {'CANCELLED'}
        else:
            self.report({'WARNING'}, "Please select a curve object before loading the profile.")
            return {'CANCELLED'}


    def invoke(self, context, event):
        # Open the file dialog
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

#-----------------------------------------------------------------------------------
#Convert Curve
class OBJECT_OT_ConvertToCurve(bpy.types.Operator):
    bl_idname = "object.convert_to_curve"
    bl_label = "Convert to Curve"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Select any Mesh object to convert Curve"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        # Get the active object
        obj = context.active_object
        # Check if the object is valid
        if obj and obj.type == 'MESH':
            # Convert the mesh to a curve
            bpy.ops.object.convert(target='CURVE')
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "Please select a valid mesh object.")
            return {'CANCELLED'}


#-----------------------------------------------------------------------------------
#Convert to Mesh
class OBJECT_OT_ConvertToMesh(bpy.types.Operator):
    bl_idname = "object.convert_to_mesh"
    bl_label = "Convert to Mesh"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Select any Curve object to convert Mesh"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        # Get the active object
        obj = context.active_object
        # Check if the object is valid
        if obj and obj.type == 'CURVE':
            # Convert the curve to a mesh
            bpy.ops.object.convert(target='MESH')
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "Please select a valid curve object.")
            return {'CANCELLED'}
#-------------------------------------------------------------------------------------------
#Flip mirror
class OBJECT_OT_FlipProfile(bpy.types.Operator):
    bl_idname = "object.flip_profile"
    bl_label = "Flip Profile"
    #bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Flip the Profile of the Selected Object along the X, Y, or Z axis. \nNote!: This operation requires the object to have a profile.\n If your object does not have any profile, this operation will not work."

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'CURVE' and context.active_object.data.bevel_object
    
    
    def execute(self, context):
        obj = bpy.context.active_object

        if obj.type == 'CURVE' and obj.data.bevel_object:
            profile_object = bpy.data.objects.get(obj.data.bevel_object.name)
            selected_curve = [obj.name]

            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = bpy.context.scene.objects[profile_object.name]
            bpy.context.view_layer.objects.active.select_set(True)

            bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'

            if bpy.context.scene.category_moldings.flip_direction == 'X':
                bpy.ops.transform.mirror(orient_type='GLOBAL', constraint_axis=(True, False, False))
            elif bpy.context.scene.category_moldings.flip_direction == 'Y':
                bpy.ops.transform.mirror(orient_type='GLOBAL', constraint_axis=(False, True, False))
            elif bpy.context.scene.category_moldings.flip_direction == 'Z':
                bpy.ops.transform.mirror(orient_type='GLOBAL', constraint_axis=(False, False, True))

            bpy.context.view_layer.update()

            bpy.ops.object.select_all(action='DESELECT')
            context.view_layer.objects.active = bpy.context.scene.objects[selected_curve[0]]
            bpy.context.view_layer.objects.active.select_set(True)

            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Active object is not a valid curve with a bevel object.")
            
            return {'CANCELLED'}

class OBJECT_OT_BoundingBoxOriginControl(bpy.types.Operator):
    bl_idname = "object.bounding_box_origin_control"
    bl_label = "Bounding Box Origin Control"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Select from Change 'Origin and Change' the Active Object Origin"

    def execute(self, context):

        if bpy.context.object.type == 'CURVE' and bpy.context.object.data.bevel_object:
            name_origin_profile = []
            selected_curve=[]
            obj = bpy.context.active_object
            active_obj = bpy.data.objects.get(obj.data.bevel_object.name)
            name_origin_profile.append(obj.data.bevel_object.name)
            selected_curve.append(bpy.context.active_object.name)
            # Check if there is an active object
            if active_obj:
                # Get the bounding box dimensions
                min_x, min_y, _ = active_obj.bound_box[0]
                max_x, max_y, _ = active_obj.bound_box[6]

                # Calculate the new origin point based on the selected position
                if bpy.context.scene.category_moldings.position_enum == 'CENTER':
                    # Calculate the center of the bounding box
                    corner_8 = []

                    # Get the active object
                    obj = bpy.data.objects.get(obj.data.bevel_object.name)

                    # Get the bounding box in 3D space in global coordinates
                    bbox_3d_global = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]

                    # Print the resulting 3D bounding box coordinates in global space
                    for i, coord_3d_global in enumerate(bbox_3d_global):
                        # print(f"Corner {i+1} (Global 3D): {coord_3d_global}")
                        corner_8.append(coord_3d_global)

                    # Check if corner_8 is not empty
                    if corner_8:
                        # Calculate the center of the bounding box
                        center_location = sum(corner_8, Vector()) / 8

                        # Set the cursor location to the center
                        bpy.context.scene.cursor.location = center_location
                        bpy.ops.object.select_all(action='DESELECT')
                        context.view_layer.objects.active = bpy.context.scene.objects[name_origin_profile[0]]  # Make it the active object
                        bpy.context.view_layer.objects.active.select_set(True)
                        # Set the object origin to the cursor location
                        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
                        bpy.ops.object.select_all(action='DESELECT')
                        context.view_layer.objects.active = bpy.context.scene.objects[selected_curve[0]]  # Make it the active object
                        bpy.context.view_layer.objects.active.select_set(True)
                        
                        
                    else:
                        print("Error: corner_8 is empty.")

                    # Reset the cursor location
                    bpy.context.scene.cursor.location = (0, 0, 0)

                    return {'FINISHED'}
                    
                elif bpy.context.scene.category_moldings.position_enum == 'TOP_LEFT':
                        # Find the index of the corner with the lowest X, highest Y, and lowest Z coordinates
                        corner_8 = []

                        # Get the active object
                        obj = bpy.data.objects.get(obj.data.bevel_object.name)

                        # Get the bounding box in 3D space in global coordinates
                        bbox_3d_global = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]

                        # Print the resulting 3D bounding box coordinates in global space
                        for i, coord_3d_global in enumerate(bbox_3d_global):
                            # print(f"Corner {i+1} (Global 3D): {coord_3d_global}")
                            corner_8.append(coord_3d_global)

                        # Check if corner_8 is not empty
                        if corner_8:
                            # Find the index of the corner with the lowest X, highest Y, and lowest Z coordinates
                            top_left_index = min(range(len(corner_8)), key=lambda i: (corner_8[i][0], -corner_8[i][1], corner_8[i][2]))

                            # Set the cursor location to the bottom-right corner
                            bpy.context.scene.cursor.location = corner_8[top_left_index]

                            #Every one is same
                            bpy.ops.object.select_all(action='DESELECT')
                            context.view_layer.objects.active = bpy.context.scene.objects[name_origin_profile[0]]  # Make it the active object
                            bpy.context.view_layer.objects.active.select_set(True)
                            # Set the object origin to the cursor location
                            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
                            bpy.ops.object.select_all(action='DESELECT')
                            context.view_layer.objects.active = bpy.context.scene.objects[selected_curve[0]]  # Make it the active object
                            bpy.context.view_layer.objects.active.select_set(True)
                        
                        else:
                            print("Error: corner_8 is empty.")

                        # Reset the cursor location
                        bpy.context.scene.cursor.location = (0, 0, 0)

                        return {'FINISHED'}
                    
                #The main Place
                elif bpy.context.scene.category_moldings.position_enum == 'TOP_RIGHT':
                    # Find the index of the corner with the highest X and Y coordinates
                    corner_8 = []
                    
                    # Get the active object
                    obj = bpy.data.objects.get(obj.data.bevel_object.name)
                    
                    # Get the bounding box in 3D space in global coordinates
                    bbox_3d_global = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
                    
                    # Print the resulting 3D bounding box coordinates in global space
                    for i, coord_3d_global in enumerate(bbox_3d_global):
                        # print(f"Corner {i+1} (Global 3D): {coord_3d_global}")
                        corner_8.append(coord_3d_global)
                    
                    # Check if corner_8 is not empty
                    if corner_8:
                        # Find the index of the corner with the highest X and Y coordinates
                        upper_right_index = max(range(len(corner_8)), key=lambda i: (corner_8[i][0], corner_8[i][1], corner_8[i][2]))
                    
                        # Set the cursor location to the upper-right corner
                        bpy.context.scene.cursor.location[0] = corner_8[upper_right_index][0]
                        bpy.context.scene.cursor.location[1] = corner_8[upper_right_index][1]
                        bpy.context.scene.cursor.location[2] = corner_8[upper_right_index][2]
                        
                        
                        #Every one is same
                        bpy.ops.object.select_all(action='DESELECT')
                        context.view_layer.objects.active = bpy.context.scene.objects[name_origin_profile[0]]  # Make it the active object
                        bpy.context.view_layer.objects.active.select_set(True)
                        # Set the object origin to the cursor location
                        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
                        bpy.ops.object.select_all(action='DESELECT')
                        context.view_layer.objects.active = bpy.context.scene.objects[selected_curve[0]]  # Make it the active object
                        bpy.context.view_layer.objects.active.select_set(True)
                    else:
                        print("Error: corner_8 is empty.")
                    
                    # Reset the cursor location
                    bpy.context.scene.cursor.location = (0, 0, 0)
                    
                    
                    return {'FINISHED'}

                elif bpy.context.scene.category_moldings.position_enum == 'BOTTOM_LEFT':
                    # Find the index of the corner with the lowest X, Y, and Z coordinates
                    corner_8 = []

                    # Get the active object
                    obj = bpy.data.objects.get(obj.data.bevel_object.name)

                    # Get the bounding box in 3D space in global coordinates
                    bbox_3d_global = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]

                    # Print the resulting 3D bounding box coordinates in global space
                    for i, coord_3d_global in enumerate(bbox_3d_global):
                        # print(f"Corner {i+1} (Global 3D): {coord_3d_global}")
                        corner_8.append(coord_3d_global)

                    # Check if corner_8 is not empty
                    if corner_8:
                        # Find the index of the corner with the lowest X, Y, and Z coordinates
                        bottom_left_index = min(range(len(corner_8)), key=lambda i: (corner_8[i][0], corner_8[i][1], corner_8[i][2]))

                        # Set the cursor location to the bottom-left corner
                        bpy.context.scene.cursor.location = corner_8[bottom_left_index]

                        #Every one is same
                        bpy.ops.object.select_all(action='DESELECT')
                        context.view_layer.objects.active = bpy.context.scene.objects[name_origin_profile[0]]  # Make it the active object
                        bpy.context.view_layer.objects.active.select_set(True)
                        # Set the object origin to the cursor location
                        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
                        bpy.ops.object.select_all(action='DESELECT')
                        context.view_layer.objects.active = bpy.context.scene.objects[selected_curve[0]]  # Make it the active object
                        bpy.context.view_layer.objects.active.select_set(True)
                    else:
                        print("Error: corner_8 is empty.")

                    # Reset the cursor location
                    bpy.context.scene.cursor.location = (0, 0, 0)


                    return {'FINISHED'}
                
                elif bpy.context.scene.category_moldings.position_enum == 'BOTTOM_RIGHT':
                    # Find the bottom-right corner of the bounding box
                    corner_8 = []

                    # Get the active object
                    obj = bpy.data.objects.get(obj.data.bevel_object.name)

                    # Get the bounding box in 3D space in global coordinates
                    bbox_3d_global = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]

                    # Print the resulting 3D bounding box coordinates in global space
                    for i, coord_3d_global in enumerate(bbox_3d_global):
                        # print(f"Corner {i+1} (Global 3D): {coord_3d_global}")
                        corner_8.append(coord_3d_global)

                    # Check if corner_8 is not empty
                    if corner_8:
                        # Find the index of the corner with the highest X, lowest Y, and lowest Z coordinates
                        bottom_right_index = max(range(len(corner_8)), key=lambda i: (corner_8[i][0], -corner_8[i][1], -corner_8[i][2]))

                        # Set the cursor location to the bottom-right corner
                        bpy.context.scene.cursor.location = corner_8[bottom_right_index]

                        #Every one is same
                        bpy.ops.object.select_all(action='DESELECT')
                        context.view_layer.objects.active = bpy.context.scene.objects[name_origin_profile[0]]  # Make it the active object
                        bpy.context.view_layer.objects.active.select_set(True)
                        # Set the object origin to the cursor location
                        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
                        bpy.ops.object.select_all(action='DESELECT')
                        context.view_layer.objects.active = bpy.context.scene.objects[selected_curve[0]]  # Make it the active object
                        bpy.context.view_layer.objects.active.select_set(True)
                    else:
                        print("Error: corner_8 is empty.")

                    # Reset the cursor location
                    bpy.context.scene.cursor.location = (0, 0, 0)


                    return {'FINISHED'}



                elif bpy.context.scene.category_moldings.position_enum == 'MIDDLE_TOP':
                    # Find the middle point at the bottom-center of the bounding box
                    corner_8 = []

                    # Get the active object
                    obj = bpy.data.objects.get(obj.data.bevel_object.name)

                    # Get the bounding box in 3D space in global coordinates
                    bbox_3d_global = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]

                    # Print the resulting 3D bounding box coordinates in global space
                    for i, coord_3d_global in enumerate(bbox_3d_global):
                        # print(f"Corner {i+1} (Global 3D): {coord_3d_global}")
                        corner_8.append(coord_3d_global)

                    # Check if corner_8 is not empty
                    if corner_8:
                        # Find the index of the corner with the middle X and lowest Y coordinates
                        middle_top_index = max(range(len(corner_8)), key=lambda i: (corner_8[i][0], corner_8[i][1], corner_8[i][2]))

                        # Calculate the middle point at the bottom-center
                        middle_top_location = (corner_8[middle_top_index] + corner_8[middle_top_index - 4]) / 2

                        # Set the cursor location to the middle point
                        bpy.context.scene.cursor.location = middle_top_location

                        #Every one is same
                        bpy.ops.object.select_all(action='DESELECT')
                        context.view_layer.objects.active = bpy.context.scene.objects[name_origin_profile[0]]  # Make it the active object
                        bpy.context.view_layer.objects.active.select_set(True)
                        # Set the object origin to the cursor location
                        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
                        bpy.ops.object.select_all(action='DESELECT')
                        context.view_layer.objects.active = bpy.context.scene.objects[selected_curve[0]]  # Make it the active object
                        bpy.context.view_layer.objects.active.select_set(True)
                    else:
                        print("Error: corner_8 is empty.")

                    # Reset the cursor location
                    bpy.context.scene.cursor.location = (0, 0, 0)


                    return {'FINISHED'}


                elif bpy.context.scene.category_moldings.position_enum == 'MIDDLE_BOTTOM':
                    # Find the bottom-right corner of the bounding box
                    corner_8 = []

                    # Get the active object
                    obj = bpy.data.objects.get(obj.data.bevel_object.name)

                    # Get the bounding box in 3D space in global coordinates
                    bbox_3d_global = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]

                    # Print the resulting 3D bounding box coordinates in global space
                    for i, coord_3d_global in enumerate(bbox_3d_global):
                        # print(f"Corner {i+1} (Global 3D): {coord_3d_global}")
                        corner_8.append(coord_3d_global)

                    # Check if corner_8 is not empty
                    if corner_8:
                        # Find the index of the corner with the highest X, lowest Y, and lowest Z coordinates
                        middle_bottom_index = max(range(len(corner_8)), key=lambda i: (corner_8[i][0], -corner_8[i][1], -corner_8[i][2]))

                        # Set the cursor location to the bottom-right corner
                        bpy.context.scene.cursor.location = (corner_8[middle_bottom_index] + corner_8[middle_bottom_index-4])/2

                        #Every one is same
                        bpy.ops.object.select_all(action='DESELECT')
                        context.view_layer.objects.active = bpy.context.scene.objects[name_origin_profile[0]]  # Make it the active object
                        bpy.context.view_layer.objects.active.select_set(True)
                        # Set the object origin to the cursor location
                        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
                        bpy.ops.object.select_all(action='DESELECT')
                        context.view_layer.objects.active = bpy.context.scene.objects[selected_curve[0]]  # Make it the active object
                        bpy.context.view_layer.objects.active.select_set(True)
                    else:
                        print("Error: corner_8 is empty.")

                    # Reset the cursor location
                    bpy.context.scene.cursor.location = (0, 0, 0)


                    return {'FINISHED'}




                elif bpy.context.scene.category_moldings.position_enum == 'MIDDLE_LEFT':
                    # Find the middle point at the bottom-left corner of the bounding box
                    corner_8 = []

                    # Get the active object
                    obj = bpy.data.objects.get(obj.data.bevel_object.name)

                    # Get the bounding box in 3D space in global coordinates
                    bbox_3d_global = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]

                    # Print the resulting 3D bounding box coordinates in global space
                    for i, coord_3d_global in enumerate(bbox_3d_global):
                        # print(f"Corner {i+1} (Global 3D): {coord_3d_global}")
                        corner_8.append(coord_3d_global)

                    # Check if corner_8 is not empty
                    if corner_8:
                        # Find the index of the corner with the lowest X, highest Y, and lowest Z coordinates
                        middle_left_index = min(range(len(corner_8)), key=lambda i: (corner_8[i][0], -corner_8[i][1], corner_8[i][2]))

                        # Set the cursor location to the bottom-left corner
                        middle_left_location = (corner_8[middle_left_index]+corner_8[middle_left_index-1])/2
                        
                        bpy.context.scene.cursor.location = middle_left_location

                        #Every one is same
                        bpy.ops.object.select_all(action='DESELECT')
                        context.view_layer.objects.active = bpy.context.scene.objects[name_origin_profile[0]]  # Make it the active object
                        bpy.context.view_layer.objects.active.select_set(True)
                        # Set the object origin to the cursor location
                        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
                        bpy.ops.object.select_all(action='DESELECT')
                        context.view_layer.objects.active = bpy.context.scene.objects[selected_curve[0]]  # Make it the active object
                        bpy.context.view_layer.objects.active.select_set(True)
                    else:
                        print("Error: corner_8 is empty.")

                    # Reset the cursor location
                    bpy.context.scene.cursor.location = (0, 0, 0)


                    return {'FINISHED'}


                elif bpy.context.scene.category_moldings.position_enum == 'MIDDLE_RIGHT':
                    # Find the middle point at the top of the bounding box
                    corner_8 = []

                    # Get the active object
                    obj = bpy.data.objects.get(obj.data.bevel_object.name)

                    # Get the bounding box in 3D space in global coordinates
                    bbox_3d_global = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]

                    # Print the resulting 3D bounding box coordinates in global space
                    for i, coord_3d_global in enumerate(bbox_3d_global):
                        # print(f"Corner {i+1} (Global 3D): {coord_3d_global}")
                        corner_8.append(coord_3d_global)

                    # Check if corner_8 is not empty
                    if corner_8:
                        # Find the index of the corner with the highest X, highest Y, and lowest Z coordinates
                        middle_right_index = max(range(len(corner_8)), key=lambda i: (corner_8[i][0], corner_8[i][1], corner_8[i][2]))

                        # Calculate the middle point at the top of the bounding box
                        middle_right_location = (corner_8[middle_right_index] + corner_8[middle_right_index - 1]) / 2

                        # Set the cursor location to the middle point
                        bpy.context.scene.cursor.location = middle_right_location

                        #Every one is same
                        bpy.ops.object.select_all(action='DESELECT')
                        context.view_layer.objects.active = bpy.context.scene.objects[name_origin_profile[0]]  # Make it the active object
                        bpy.context.view_layer.objects.active.select_set(True)
                        # Set the object origin to the cursor location
                        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
                        bpy.ops.object.select_all(action='DESELECT')
                        context.view_layer.objects.active = bpy.context.scene.objects[selected_curve[0]]  # Make it the active object
                        bpy.context.view_layer.objects.active.select_set(True)
                    else:
                        print("Error: corner_8 is empty.")

                    # Reset the cursor location
                    bpy.context.scene.cursor.location = (0, 0, 0)


                    return {'FINISHED'}

                else:
                    self.report({'WARNING'}, "Invalid position_enum for changing origin")
                    return {'CANCELLED'}
            else:
                self.report({'WARNING'}, "No active curve object selected")
                return {'CANCELLED'}
        else:
            self.report({'WARNING'}, "Please Select Curve and Has Profile!")
            return {'CANCELLED'}

#--------------------------------------------------------------------------------
#Make Profile Operator
class OBJECT_OT_MakeProfile(bpy.types.Operator):
    bl_idname = "object.make_profile"
    bl_label = "Make Crown Profile"
    bl_description = "Creates moldings from selected profile"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Get the directory of the addon script
        addon_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the path to the 'profiles' folder within the addon directory
        profiles_dir = os.path.join(addon_dir, "profiles")


        # Check if the 'profiles' folder exists
        if os.path.exists(profiles_dir):
            # Extract the last four characters from the my_previews property
            name_define = bpy.data.window_managers["WinMan"].my_previews[:-4]
            
            print(name_define)

            # Check if name_define is empty or not valid
            if not name_define:
                self.report({'ERROR'}, "Invalid profile selected")
                return {'CANCELLED'}

            # Construct the file path for the text file corresponding to the selected profile
            txt_file_path = os.path.join(profiles_dir, f'{os.path.splitext(name_define)[0]}.txt')

            # Check if the text file exists
            if os.path.exists(txt_file_path):
                # Set the profile image based on the extracted name
                bpy.data.window_managers["WinMan"].my_previews = f'{name_define}.png'

                # Read the data from the text file
                with open(txt_file_path, 'r') as file:
                    data = file.read()
                    parsed_data = {}
                    exec(data, None, parsed_data)

                    verts = parsed_data.get('verts', [])
                    edges = parsed_data.get('edges', [])
                    faces = parsed_data.get('faces', [])

                    # Create a new mesh
                    mesh = bpy.data.meshes.new(name=name_define)
                    mesh.from_pydata(verts, edges, faces)

                    # Create a new mesh object and link it to the scene
                    obj = bpy.data.objects.new(name_define, mesh)
                    bpy.context.collection.objects.link(obj)

                    # Set the mesh object as the active object and select it
                    bpy.context.view_layer.objects.active = obj
                    obj.select_set(True)
                    bpy.ops.object.convert(target='CURVE')
                    obj.select_set(False)

                    return {'FINISHED'}
            else:
                self.report({'ERROR'}, f"Text file not found: {txt_file_path}")
        else:
            self.report({'ERROR'}, "Profiles folder not found")

        return {'CANCELLED'}
#--------------------------------------------------------------------------------
#Main Category
class Molding_Properties(bpy.types.PropertyGroup):
    profile_type_enum : bpy.props.EnumProperty(
        items=[
            ('Crown_Molding', 'Crown Molding', 'Shows Crown Molding Panel', 'OUTLINER_OB_MESH', 1),
            #('Baseboard_Molding', 'Baseboard Molding', 'Shows Baseboard Molding Panel', 'OUTLINER_OB_CURVE', 2),
            #('Chair_Rail_Molding', 'Chair Rail Molding', 'Shows Chair Rail Molding Panel', 'OUTLINER_OB_SURFACE', 3)
        ],
        description="Select the type of object to add. Add Object",
        default='Crown_Molding'
    )
  
    position_enum: bpy.props.EnumProperty(
        items=[
            ('CENTER', "Center", "Center of Bounding Box"),
            ('TOP_LEFT', "Top Left", "Top Left Corner"),
            ('TOP_RIGHT', "Top Right", "Top Right Corner"),
            ('BOTTOM_LEFT', "Bottom Left", "Bottom Left Corner"),
            ('BOTTOM_RIGHT', "Bottom Right", "Bottom Right Corner"),
            ('MIDDLE_TOP', "Middle Top", "Middle of Top Edge"),
            ('MIDDLE_BOTTOM', "Middle Bottom", "Middle of Bottom Edge"),
            ('MIDDLE_LEFT', "Middle Left", "Middle of Left Edge"),
            ('MIDDLE_RIGHT', "Middle Right", "Middle of Right Edge"),
        ],
        default='CENTER',
        description='Change Origin'
    )
    
    flip_direction: bpy.props.EnumProperty(
        name="Flip Direction",
        items=[
            ('X', "X-Axis", "Flip along the X-Axis", '', 0),
            ('Y', "Y-Axis", "Flip along the Y-Axis", '', 1),
            ('Z', "Z-Axis", "Flip along the Z-Axis", '', 2),
        ],
        default='X'
    )
    
    reference_profile: bpy.props.PointerProperty(
        type = bpy.types.Object,
        name="Reference Profile",
        description="Select another Profile",
    )
    

# Register - Unregister Area
def register():
    import bpy
    from bpy.types import WindowManager
    from bpy.props import StringProperty, EnumProperty

    bpy.utils.register_class(ImagePropertiesGroup)
    # Get the directory of the addon script
    addon_dir = os.path.dirname(os.path.abspath(__file__))
    profiles_dir = os.path.join(addon_dir, "profiles")

    WindowManager.my_previews_dir = StringProperty(
        name="Profile Folder",
        description="Select the folder containing image previews",
        subtype='DIR_PATH',
        default=os.path.join(addon_dir, "renders"), 
        update=preview_dir_update,
    )
    
    WindowManager.my_previews_update_trigger = bpy.props.BoolProperty(default=False)
    WindowManager.my_previews = EnumProperty(
        items=enum_previews_from_directory_items,
        update=preview_enum_update,
    )

    import bpy.utils.previews
    
    pcol = preview_collections.setdefault("main", bpy.utils.previews.new())
    
    bpy.utils.register_class(UpdatePreviewsDirOperator)


    bpy.types.Scene.image_filter = bpy.props.StringProperty()
    bpy.types.Image.is_active = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.active_image_index = bpy.props.IntProperty(default=-1)
    bpy.types.Scene.image_property = bpy.props.PointerProperty(type=ImagePropertiesGroup)
    bpy.types.Scene.custom_image_index = bpy.props.IntProperty()
    
    bpy.utils.register_class(UpdateImagePathsOperator)
    bpy.utils.register_class(ABMoldingPanel)
    bpy.utils.register_class(OBJECT_OT_MakeProfile)
    bpy.utils.register_class(Molding_Properties)
    bpy.types.Scene.category_moldings = bpy.props.PointerProperty(type=Molding_Properties)
    bpy.utils.register_class(OBJECT_OT_BoundingBoxOriginControl)
    bpy.utils.register_class(OBJECT_OT_FlipProfile)
    bpy.utils.register_class(OBJECT_OT_ConvertToCurve)
    bpy.utils.register_class(OBJECT_OT_ConvertToMesh)
    bpy.utils.register_class(OBJECT_OT_SaveProfile)
    bpy.utils.register_class(OBJECT_OT_LoadProfile)
    bpy.utils.register_class(SelectProfileOperator)
    bpy.utils.register_class(SelectMainCurveOperator)
    bpy.utils.register_class(ClearTiltProfileOperator)
    bpy.utils.register_class(OBJECT_OT_ChangeProfile)
    bpy.utils.register_class(OBJECT_OT_ChangeFromPickProfile)
    

def unregister():
    bpy.utils.unregister_class(ImagePropertiesGroup)

    del bpy.types.Scene.custom_image_index
    del bpy.types.Scene.image_filter
    del bpy.types.Image.is_active
    del bpy.types.Scene.active_image_index
    
    del bpy.types.Scene.image_property
    #del bpy.types.Scene.image_icon_scale

    from bpy.types import WindowManager
    try:
        del WindowManager.my_previews
        del WindowManager.my_previews_update_trigger
    except AttributeError:
        pass
    
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()

    bpy.utils.unregister_class(UpdatePreviewsDirOperator)
    
    bpy.utils.unregister_class(UpdateImagePathsOperator)
    bpy.utils.unregister_class(ABMoldingPanel)
    bpy.utils.unregister_class(OBJECT_OT_MakeProfile)
    bpy.utils.unregister_class(Molding_Properties)
    del bpy.types.Scene.category_moldings
    bpy.utils.unregister_class(OBJECT_OT_BoundingBoxOriginControl)
    bpy.utils.unregister_class(OBJECT_OT_FlipProfile)
    bpy.utils.unregister_class(OBJECT_OT_ConvertToCurve)
    bpy.utils.unregister_class(OBJECT_OT_ConvertToMesh)
    bpy.utils.unregister_class(OBJECT_OT_SaveProfile)
    bpy.utils.unregister_class(OBJECT_OT_LoadProfile)
    bpy.utils.unregister_class(SelectProfileOperator)
    bpy.utils.unregister_class(SelectMainCurveOperator)
    bpy.utils.unregister_class(ClearTiltProfileOperator)
    bpy.utils.unregister_class(OBJECT_OT_ChangeProfile)
    bpy.utils.unregister_class(OBJECT_OT_ChangeFromPickProfile)