import bpy
import random
import blf
import os
from bpy.props import CollectionProperty


class UpdateMaterialPreviewsDirOperator(bpy.types.Operator):
    bl_idname = "wm.update_materials_dir"
    bl_label = "Update Previews Directory"
    bl_description = "Update my_material_dir property"

    directory: bpy.props.StringProperty(subtype='DIR_PATH')

    def execute(self, context):
        if "WinMan" in bpy.data.window_managers:
            bpy.data.window_managers["WinMan"].my_material_previews_update_trigger = not bpy.data.window_managers["WinMan"].my_material_previews_update_trigger
            bpy.data.window_managers["WinMan"].my_material_dir = self.directory
            self.report({'INFO'}, f"Previews directory updated to: {self.directory}")
        else:
            self.report({'WARNING'}, "Window manager 'WinMan' not found")
        return {'FINISHED'}

# Operator to save the active material as a .blend file
class OBJECT_OT_SaveMaterialAsBlend(bpy.types.Operator):
    bl_idname = "object.save_material_as_blend"
    bl_label = "Save Material as Blend"
    bl_description = "Save this material as a .blend file"

    index: bpy.props.IntProperty()
    directory: bpy.props.StringProperty(subtype='DIR_PATH')

    def execute(self, context):
        selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        selected_image_name = bpy.data.window_managers["WinMan"].my_material_previews
        selected_image_name = os.path.splitext(selected_image_name)[0]
        selected_material = None
        for mat in bpy.data.materials:
            if mat.name == selected_image_name:
                selected_material = mat
                break
        if selected_material:
            for obj in selected_objects:
                obj.data.materials.clear()
                obj.data.materials.append(selected_material)
            active_material = bpy.context.object.active_material
            if active_material:
                filepath = os.path.join(self.directory, f"{active_material.name}.blend")
                try:
                    bpy.data.libraries.write(filepath, set([active_material]), fake_user=True)
                except OSError as e:
                    self.report({'ERROR'}, str(e))
                    return {'CANCELLED'}
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    def draw(self, context):
        layout = self.layout
        layout.label(text="Save the active material as a .blend file")


class SaveActiveMaterialsOperator(bpy.types.Operator):
    bl_idname = "object.save_active_materials"
    bl_label = "Save Active Materials"
    bl_description = "Save active materials as a separate .blend file"
    
    index: bpy.props.IntProperty()
    directory: bpy.props.StringProperty(subtype='DIR_PATH')

    def execute(self, context):
        active_material = bpy.context.object.active_material
        if active_material:
            filepath = os.path.join(self.directory, f"{active_material.name}.blend")
            try:
                bpy.data.libraries.write(filepath, set([active_material]), fake_user=True)
            except OSError as e:
                    self.report({'ERROR'}, str(e))
                    return {'CANCELLED'}
        return {"FINISHED"}
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    def draw(self, context):
            layout = self.layout
            layout.label(text="Save the active material as a .blend file")


class OBJECT_OT_SaveAllMaterialsInOne(bpy.types.Operator):
    bl_idname = "object.save_all_materials_in_one"
    bl_label = "Save All Materials in One"
    bl_description = "Save all materials in one .blend file"

    directory: bpy.props.StringProperty(subtype='DIR_PATH')

    def execute(self, context):
        filepath = os.path.join(self.directory, "All_Materials.blend")
        try:
            bpy.data.libraries.write(filepath, set(bpy.data.materials), fake_user=True)
        except OSError as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}
        return {'FINISHED'}
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    def draw(self, context):
        layout = self.layout
        layout.label(text="Save all materials in one .blend file")

class OBJECT_OT_CreateRandomMaterials(bpy.types.Operator):
    bl_idname = "object.create_random_materials"
    bl_label = "Create Random Materials"
    bl_description = "Create random materials"

    def execute(self, context):
        for i in range(1):
            material = bpy.data.materials.new(name=f"Random_Material_{i}")
            material.use_nodes = True
            material.diffuse_color = (random.random(), random.random(), random.random(), 1.0)
        return {'FINISHED'}


class OBJECT_OT_RemoveMaterialFromList(bpy.types.Operator):
    bl_idname = "object.remove_material_from_list"
    bl_label = "Remove Material From List"
    bl_description = "Remove from selected objects"

    def execute(self, context):
        selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        selected_image_name = bpy.data.window_managers["WinMan"].my_material_previews
        selected_image_name = os.path.splitext(selected_image_name)[0]
        selected_material = None
        for mat in bpy.data.materials:
            if mat.name == selected_image_name:
                selected_material = mat
                break

        if selected_material:
            for obj in selected_objects:
                obj.data.materials.clear()
        else:
            self.report({'ERROR'}, f"Material '{selected_image_name}' not found in the scene.")
        return {'FINISHED'}

# Operator to apply the selected material to a single object
class OBJECT_OT_ApplyMaterialToSingle(bpy.types.Operator):
    bl_idname = "object.apply_material_to_single"
    bl_label = "Apply Material To Single"
    bl_description = "Apply the selected material to a selected objects"

    def execute(self, context):
        selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        selected_image_name = bpy.data.window_managers["WinMan"].my_material_previews
        selected_image_name = os.path.splitext(selected_image_name)[0]
        selected_material = None
        for mat in bpy.data.materials:
            if mat.name == selected_image_name:
                selected_material = mat
                break
        if selected_material:
            for obj in selected_objects:
                obj.data.materials.clear()
                obj.data.materials.append(selected_material)
        else:
            self.report({'ERROR'}, f"Material '{selected_image_name}' not found in the scene.")
        return {'FINISHED'}


def update_select_image(self, context):
    select_image = context.scene.material_property.select_image
    if select_image:
        context.scene.material_property.select_image = select_image


class MaterialPropertiesGroup(bpy.types.PropertyGroup):
    
    material_preview_grid_settings: bpy.props.BoolProperty(
        name="Material Preview Grid Settings",
        description="Material Grid Settings"
    )
    select_image : bpy.props.PointerProperty(
        name='Image',
        type=bpy.types.Image,
        update=update_select_image)
    show_material_preview: bpy.props.BoolProperty(
        name="Show Material Preview",
        description="Show Material Preview"
    )
    show_preview_grid: bpy.props.BoolProperty(
        name="Show Preview in Grid",
        description="Show  Preview in Grid",
        default=False,
    )
    thumbnail_path: bpy.props.StringProperty(
        name="Thumbnail Path",
        description="Absolute path to the material thumbnail",
        default="",
        subtype='FILE_PATH'
    )


bpy.types.Scene.material_items_per_row = bpy.props.IntProperty(
        name="Items Per Row",
        default=1,
        min=1,
        description="Number of material items to display per row"
    )

bpy.types.Scene.material_rows = bpy.props.IntProperty(
        name="Rows",
        default=1,
        min=1,
        description="Number of rows of materials to display"
    )

bpy.types.Scene.material_icon_scale = bpy.props.FloatProperty(
        name="Icon Scale",
        default=8.0,
        min=0.1,
        description="Scale of the material preview icons"
    )

material_preview_collections = {}


def enum_material_previews_from_directory_items(self, context):
    pcoll = material_preview_collections.get("main")
    if not pcoll:
        return []

    if bpy.data.window_managers["WinMan"].my_material_dir == "":
        return []
    return pcoll.my_material_previews


class MATERIAL_PT_MaterialPreviewPanel(bpy.types.Panel):
    bl_label = "AB Material Management"
    bl_idname = "MATERIAL_PT_material_preview_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Arc Blend"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        material_property= scene.material_property
        col=layout.column()
        icon_scale = context.scene.material_icon_scale
        wm = context.window_manager
        col.prop(wm, "my_material_dir")
        col.template_icon_view(wm, "my_material_previews", scale=icon_scale ,show_labels=True, scale_popup=4)
        materials = bpy.data.materials
        filtered_materials = [mat for mat in materials if context.scene.material_filter.lower() in mat.name.lower()]
        items_per_row = context.scene.material_items_per_row
        rows = context.scene.material_rows
        icon_scale = context.scene.material_icon_scale
        items_per_page = items_per_row * rows
        page = context.scene.material_page
        start_index = page * items_per_page
        end_index = min(start_index + items_per_page, len(filtered_materials))
        remaining_items = end_index - start_index
        rows_to_display = (remaining_items + items_per_row - 1) // items_per_row
        col.operator("object.update_material_image_paths", text="Refresh Images", icon="FILE_REFRESH")
        col.operator("object.apply_material_to_single", text="Apply", icon="PLAY")
        col.operator("object.remove_material_from_list", text="Remove", icon="PANEL_CLOSE")
        col.operator("object.save_material_as_blend", text="Save Material", icon="FILE_BACKUP")
        col = layout.column()
        row= layout.row()
        row.operator("object.copy_material", text="Copy Material" , icon="COPYDOWN")
        row.operator("object.paste_material", text="Paste Material", icon="PASTEDOWN")
        row.operator("object.select_same_material", text="Select Same", icon="ACTION_TWEAK")
        col = layout.column()
        ob=context.object
        if ob:
            col.template_ID(ob, "active_material", new="material.new")
        else:
            pass
        col = layout.column()
        sub = col.row(align=True)
        sub.prop(material_property, "material_preview_grid_settings", text="Change Material Icon Size" ,icon="X")
        if bpy.context.scene.material_property.material_preview_grid_settings:
            box = layout.box()
            sub = box.row(align=True)
            sub.label(text="Material Icon Size:")
            sub = box.column(align=True)
            sub.prop(context.scene, "material_icon_scale")
        layout.operator("object.create_random_materials", text="Create Random Materials", icon="SHADING_TEXTURE")
        layout.operator("object.import_materials", text="Import Materials", icon="IMPORT")
        layout.operator("object.save_active_materials", text="Save Active Material", icon="LAYER_ACTIVE")
        layout.operator("object.save_all_materials_as_blend", text="Save All Materials", icon="FILE_VOLUME")
        layout.operator("object.save_all_materials_in_one", text="Save All Materials in One", icon="FILE_BLEND")
        layout.operator("object.create_material_preview", text="Generate/Update Previews (Multiple)" , icon="FILE_REFRESH")
        layout.operator("object.activate_material_preview", text="Generate/Update  Active Previews" , icon="SHADING_RENDERED")
        layout.operator("object.create_visible_light_spectrum", text="Generate Image Spectrum" ,icon="GP_MULTIFRAME_EDITING")
        layout.operator("object.pack_material",  text="Pack Resources", icon ="PACKAGE")
        col = layout.column()
        material = bpy.data.materials[context.scene.active_material_index] if context.scene.active_material_index >= 0 else None
        if material:
            col.prop(material, "is_active", text="Select Same All", toggle=True)
            if material.is_active:
                col.label(text="Material Details:")
                col.separator()
                col.label(text=f"Name: {material.name}")
                col.label(text=f"Diffuse Color: {material.diffuse_color}")
                col.label(text=f"Specular Intensity: {material.specular_intensity}")
        
def material_preview_dir_update(wm, context):
    """EnumProperty callback"""
    enum_items = []
    wm = context.window_manager
    directory = wm.my_material_dir
    pcoll = material_preview_collections["main"]
    print("Scanning directory: %s" % directory)
    if directory and os.path.exists(directory):
        pcoll = material_preview_collections["main"]
        pcoll.clear()
        image_paths = [fn for fn in os.listdir(directory) if fn.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp"))]
        for i, name in enumerate(image_paths):
            filepath = os.path.join(directory, name)
            thumb = pcoll.load(name, filepath, 'IMAGE')
            name_without_extension, extension = os.path.splitext(name)
            enum_items.append((name, name_without_extension, "", thumb.icon_id, i))
    pcoll.my_material_previews = enum_items
    pcoll.my_material_dir = directory
    return None


def material_preview_enum_update(wm, context):
    return None


class UpdateMaterialImagePathsOperator(bpy.types.Operator):
    bl_idname = "object.update_material_image_paths"
    bl_label = "Update Material Image Paths"
    bl_description = "Update and reload  Material image paths"

    def execute(self, context):
        wm = context.window_manager
        try:
            material_preview_dir_update(wm, context)
        except KeyError:
            pass
        return {'FINISHED'}


class OBJECT_OT_CopyMaterialManagement(bpy.types.Operator):
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


class OBJECT_OT_PasteMaterialManagement(bpy.types.Operator):
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


class SelectSameMaterialOperator(bpy.types.Operator):
    bl_idname = "object.select_same_material"
    bl_label = "Select Objects with Same Material"
    bl_description = "Selects all objects in the scene with the same material as the active object"

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH'

    def execute(self, context):
        active_object = context.active_object
        if active_object.active_material:
            active_material = active_object.active_material
            bpy.ops.object.select_all(action='DESELECT')
            selected_objects = [] 
            for obj in bpy.context.scene.objects:
                if obj.type == 'MESH':
                    if obj.active_material == active_material:
                        obj.select_set(True)
                        selected_objects.append(obj.name)
            active_object.select_set(True)
            if selected_objects:
                material_name = active_material.name
                selected_objects_str = ', '.join(selected_objects)
                self.report({'INFO'}, f"Selected objects with material '{material_name}'")
            else:
                self.report({'INFO'}, f"No other objects found with the same material as {active_object.name}")
        return {'FINISHED'}


class OBJECT_OT_ImportMaterials(bpy.types.Operator):
    bl_idname = "object.import_materials"
    bl_label = "Import Materials"
    bl_description = "Import all materials from a selected .blend file"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    filter_glob: bpy.props.StringProperty(default="*.blend", options={'HIDDEN'})

    def execute(self, context):
        try:
            with bpy.data.libraries.load(self.filepath, link=False) as (data_from, data_to):
                if data_from.materials:
                    data_to.materials = data_from.materials
                else:
                    self.report({'WARNING'}, "No materials found in the selected file.")
                    return {'CANCELLED'}
        except Exception as e:
            self.report({'ERROR'}, f"An error occurred: {e}")
            return {'CANCELLED'}
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw_func(self, context):
        layout = self.layout
        layout.operator("object.import_materials", text="Import All Materials")


class OBJECT_OT_SaveAllMaterialsAsBlend(bpy.types.Operator):
    bl_idname = "object.save_all_materials_as_blend"
    bl_label = "Save All Materials as Blend"
    bl_description = "Save all materials as a .blend file"

    directory: bpy.props.StringProperty(subtype='DIR_PATH')

    def execute(self, context):
        for material in bpy.data.materials:
            filepath = os.path.join(self.directory, f"{material.name}.blend")
            try:
                bpy.data.libraries.write(filepath, set([material]), fake_user=True)
            except OSError as e:
                self.report({'ERROR'}, str(e))
                return {'CANCELLED'}
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        layout.label(text="Save all materials as a .blend file")


def hide_all_objects():
    for obj in bpy.context.scene.objects:
        obj.hide_render = True

def generate_material_preview_image(material, filepath):
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.device = 'GPU'
    bpy.context.scene.cycles.use_preview_denoising = True
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.resolution_x = 256
    bpy.context.scene.render.resolution_y = 256
    bpy.context.scene.render.filepath = filepath
    bpy.ops.render.render(write_still=True)

def create_material_preview_sphere():
    bpy.ops.mesh.primitive_uv_sphere_add(radius=3.0, location=(0, 0, 0))
    sphere = bpy.context.object
    sphere.name = "MaterialPreviewSphere"
    return sphere

def create_lights():
    bpy.ops.object.light_add(type='POINT', location=(5, 5, 5))
    light1 = bpy.context.object
    light1.data.energy = 650
    bpy.ops.object.light_add(type='POINT', location=(-5, -5, 5))
    light2 = bpy.context.object
    light2.data.energy = 650
    bpy.ops.object.light_add(type='POINT', location=(5, -5, 5))
    light3 = bpy.context.object
    light3.data.energy = 650

class OBJECT_OT_CreateMaterialPreview(bpy.types.Operator):
    bl_idname = "object.create_material_preview"
    bl_label = "Create Material Preview"
    bl_description = "Generate a preview for the selected material"

    index: bpy.props.IntProperty()

    directory: bpy.props.StringProperty(subtype='DIR_PATH')

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        hide_all_objects()
        bpy.ops.object.camera_add()
        new_camera = bpy.context.object
        create_lights()
        materials = bpy.data.materials
        total_materials = len(materials)
        percentage = 0

        for index, material in enumerate(materials):
            name_material = bpy.data.window_managers["WinMan"].my_material_previews[:-4]
            filepath = os.path.join(self.directory, f"{name_material}.png")
            bpy.ops.mesh.primitive_plane_add(size=500, enter_editmode=False, align='WORLD', location=(0, 0, -2))
            new_plane = bpy.context.object
            if bpy.app.version <= (3, 00):
                bpy.context.object.cycles_visibility.camera = False
                bpy.context.object.cycles_visibility.diffuse = False
            else:
                bpy.context.object.visible_diffuse = False
                bpy.context.object.visible_camera = False
            bpy.ops.mesh.primitive_uv_sphere_add(radius=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
            new_sphere = bpy.context.object
            bpy.ops.object.shade_smooth()
            bpy.ops.object.subdivision_set(level=2, relative=False)
            new_sphere.data.materials.append(material)
            bpy.context.view_layer.objects.active = new_sphere
            bpy.ops.view3d.camera_to_view_selected()
            generate_material_preview_image(material, filepath)
            bpy.data.objects.remove(new_plane)
            bpy.data.objects.remove(new_sphere)
            percentage = (index + 1) / total_materials * 100
            self.report({'INFO'}, f"Generating material previews: {int(percentage)}% completed")
        bpy.data.objects.remove(new_camera)
        for obj in bpy.context.scene.objects:
            if obj.type == 'LIGHT':
                bpy.data.objects.remove(obj)
        self.report({'INFO'}, "All Previews created")

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "directory", text="Directory")

class OBJECT_OT_ActivateMaterialPreview(bpy.types.Operator):
    bl_idname = "object.activate_material_preview"
    bl_label = "Activate Material Preview"
    bl_description = "Generate a preview for the selected active material"

    directory: bpy.props.StringProperty(subtype='DIR_PATH')

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        material = bpy.context.active_object.active_material
        hide_all_objects()
        bpy.ops.object.camera_add()
        new_camera = bpy.context.object
        create_lights()
        if material is None:
            self.report({'ERROR'}, "No active material found")
            return {'CANCELLED'}
        
        filepath = os.path.join(self.directory, f"{material.name}.png")
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = None
        bpy.ops.mesh.primitive_plane_add(size=500, enter_editmode=False, align='WORLD', location=(0, 0, -2))
        new_plane = bpy.context.object

        if bpy.app.version <= (3, 00):
            bpy.context.object.cycles_visibility.camera = False
            bpy.context.object.cycles_visibility.diffuse = False
        else:
            bpy.context.object.visible_diffuse = False
            bpy.context.object.visible_camera = False
        bpy.ops.mesh.primitive_uv_sphere_add(radius=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        new_sphere = bpy.context.object
        bpy.ops.object.shade_smooth()
        bpy.ops.object.subdivision_set(level=2, relative=False)
        new_sphere.data.materials.append(material)
        bpy.context.view_layer.objects.active = new_sphere
        bpy.ops.view3d.camera_to_view_selected()
        generate_material_preview_image(material, filepath)
        bpy.data.objects.remove(new_plane)
        bpy.data.objects.remove(new_sphere)
        bpy.data.objects.remove(new_camera)
        for obj in bpy.context.scene.objects:
            if obj.type == 'LIGHT':
                bpy.data.objects.remove(obj)

        self.report({'INFO'}, f"Material preview created: {filepath}")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "directory", text="Directory")
        
class CreateVisibleLightSpectrumOperator(bpy.types.Operator):
    bl_idname = "object.create_visible_light_spectrum"
    bl_label = "Create Visible Light Spectrum"
    
    def execute(self, context):
        
        visible_light_spectrum_material = create_visible_light_spectrum_material("Visible Light Spectrum")
        
        return {'FINISHED'}

def create_visible_light_spectrum_image():
    width = 800
    height = 1
    spectrum_image = bpy.data.images.new(name='VisibleLightSpectrum', width=width, height=height)
    pixels = []
    for x in range(width):
        wavelength = 380 + (x / width) * (780 - 380)
        r, g, b = wavelength_to_rgb(wavelength)
        pixels.extend([r, g, b, 1.0])
    spectrum_image.pixels = pixels

    return spectrum_image

def wavelength_to_rgb(wavelength):
    factor = 0.0
    if 380 <= wavelength <= 440:
        red = -(wavelength - 440) / (440 - 380)
        green = 0.0
        blue = 1.0
    elif 440 <= wavelength <= 490:
        red = 0.0
        green = (wavelength - 440) / (490 - 440)
        blue = 1.0
    elif 490 <= wavelength <= 510:
        red = 0.0
        green = 1.0
        blue = -(wavelength - 510) / (510 - 490)
    elif 510 <= wavelength <= 580:
        red = (wavelength - 510) / (580 - 510)
        green = 1.0
        blue = 0.0
    elif 580 <= wavelength <= 645:
        red = 1.0
        green = -(wavelength - 645) / (645 - 580)
        blue = 0.0
    else:
        red = 1.0
        green = 0.0
        blue = 0.0
    if 380 <= wavelength < 420:
        factor = 0.3 + 0.7 * (wavelength - 380) / (420 - 380)
    elif 420 <= wavelength < 645:
        factor = 1.0
    elif 645 <= wavelength < 780:
        factor = 0.3 + 0.7 * (780 - wavelength) / (780 - 645)

    return tuple(intensity * factor for intensity in (red, green, blue))

def create_visible_light_spectrum_material(name):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    spectrum_image = create_visible_light_spectrum_image()
    tex_image = nodes.new(type='ShaderNodeTexImage')
    tex_image.image = spectrum_image
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (200, 0)
    links = mat.node_tree.links
    link = links.new(tex_image.outputs['Color'], output.inputs['Surface'])
    return mat

class Pack_OT_Material(bpy.types.Operator):
    bl_idname= "object.pack_material"
    bl_label = "Packs Material File"
    bl_description ="Pack all used external files into this .blend."

    def execute (self, context):
        bpy.ops.file.pack_all()
        return {"FINISHED"}

# Register classes
def register():
    import bpy
    from bpy.types import WindowManager
    from bpy.props import (
            StringProperty,
            EnumProperty,
            )
    WindowManager.my_material_dir = StringProperty(
            name="Folder of Material Previews",
            description= "You have to select Preview Image Folder.\nIf you don't have any Go to Below Generate Previews to generate material previews",
            subtype='DIR_PATH',
            default="",
            update=material_preview_dir_update,
            )
    WindowManager.my_material_previews_update_trigger = bpy.props.BoolProperty(default=False)
    WindowManager.my_material_previews = EnumProperty(
            items=enum_material_previews_from_directory_items,
            update=material_preview_enum_update,
                )
    import bpy.utils.previews
    pcol = material_preview_collections.setdefault("main", bpy.utils.previews.new())
    bpy.utils.register_class(UpdateMaterialPreviewsDirOperator)
    bpy.utils.register_class(UpdateMaterialImagePathsOperator)
    bpy.utils.register_class(OBJECT_OT_CreateRandomMaterials)
    bpy.utils.register_class(OBJECT_OT_ApplyMaterialToSingle)
    bpy.utils.register_class(OBJECT_OT_RemoveMaterialFromList)
    bpy.utils.register_class(OBJECT_OT_ImportMaterials)
    bpy.utils.register_class(OBJECT_OT_SaveMaterialAsBlend)
    bpy.utils.register_class(OBJECT_OT_SaveAllMaterialsAsBlend)
    bpy.utils.register_class(OBJECT_OT_SaveAllMaterialsInOne)
    bpy.utils.register_class(OBJECT_OT_CreateMaterialPreview)
    bpy.utils.register_class(MATERIAL_PT_MaterialPreviewPanel)
    bpy.types.Scene.material_page = bpy.props.IntProperty(default=0)
    bpy.types.Scene.material_filter = bpy.props.StringProperty()
    bpy.types.Scene.active_material_index = bpy.props.IntProperty(default=-1)
    bpy.types.Material.is_active = bpy.props.BoolProperty(default=False)
    bpy.utils.register_class(MaterialPropertiesGroup)
    bpy.types.Scene.material_property = bpy.props.PointerProperty(type=MaterialPropertiesGroup)
    bpy.types.Scene.custom_material_index = bpy.props.IntProperty()
    bpy.utils.register_class(CreateVisibleLightSpectrumOperator)
    bpy.utils.register_class(OBJECT_OT_CopyMaterialManagement)
    bpy.utils.register_class(OBJECT_OT_PasteMaterialManagement)
    bpy.utils.register_class(SelectSameMaterialOperator)
    bpy.utils.register_class(Pack_OT_Material)
    bpy.utils.register_class(SaveActiveMaterialsOperator)
    bpy.utils.register_class(OBJECT_OT_ActivateMaterialPreview)
    

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_CreateRandomMaterials)
    bpy.utils.unregister_class(OBJECT_OT_ApplyMaterialToSingle)
    bpy.utils.unregister_class(OBJECT_OT_RemoveMaterialFromList)
    bpy.utils.unregister_class(OBJECT_OT_ImportMaterials)
    bpy.utils.unregister_class(OBJECT_OT_SaveMaterialAsBlend)
    bpy.utils.unregister_class(OBJECT_OT_SaveAllMaterialsAsBlend)
    bpy.utils.unregister_class(OBJECT_OT_SaveAllMaterialsInOne)
    bpy.utils.unregister_class(OBJECT_OT_CreateMaterialPreview)
    bpy.utils.unregister_class(MATERIAL_PT_MaterialPreviewPanel)
    bpy.utils.unregister_class(MaterialPropertiesGroup)
    del bpy.types.Scene.custom_material_index
    del bpy.types.Scene.material_filter
    del bpy.types.Material.is_active
    del bpy.types.Scene.active_material_index
    del bpy.types.Scene.material_property
    bpy.utils.unregister_class(CreateVisibleLightSpectrumOperator)
    bpy.utils.unregister_class(OBJECT_OT_CopyMaterialManagement)
    bpy.utils.unregister_class(OBJECT_OT_PasteMaterialManagement)
    bpy.utils.unregister_class(SelectSameMaterialOperator)
    #------------------------------------------------------------
    from bpy.types import WindowManager
    try:
        del WindowManager.my_material_previews
        del WindowManager.my_material_previews_update_trigger
    except AttributeError:
        pass
    for pcoll in material_preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    material_preview_collections.clear()
    bpy.utils.unregister_class(UpdateMaterialPreviewsDirOperator)
    bpy.utils.unregister_class(UpdateMaterialImagePathsOperator)
    
    #Packs the Textures in File
    bpy.utils.unregister_class(Pack_OT_Material)
    bpy.utils.unregister_class(SaveActiveMaterialsOperator)
    bpy.utils.unregister_class(OBJECT_OT_ActivateMaterialPreview)
