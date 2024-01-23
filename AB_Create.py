import bpy

# ------------------------------------------------------------------------------
# ARC BLEND PANEL

class ARCBLEND_PT_Panel (bpy.types.Panel):
    bl_label = "AB Create"
    bl_idname = "ARCBLEND_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arc Blend"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        # Add the enum property to the layout as a dropdown list
        layout.prop(context.scene, "object_type_enum", text="Add Object Type")
        # Draw the selected panel based on the enum
        if context.scene.object_type_enum == 'ADDMESH_PT_Panel':
            self.draw_mesh_objects(layout)
        elif context.scene.object_type_enum == 'ADDCURVE_PT_Panel':
            self.draw_curve_objects(layout)
        elif context.scene.object_type_enum == 'ADDSURFACE_PT_Panel':
            self.draw_surface_objects(layout)
        elif context.scene.object_type_enum == 'ADDMETABALL_PT_Panel':
            self.draw_metaball_objects(layout)
        elif context.scene.object_type_enum == 'ADDTEXT_PT_Panel':
            self.draw_text_objects(layout)
        elif context.scene.object_type_enum == 'ADDVOLUME_PT_Panel':
            self.draw_volume_objects(layout)
        elif context.scene.object_type_enum == 'ADDGREASEPENCIL_PT_Panel':
            self.draw_grease_pencil_objects(layout)
        elif context.scene.object_type_enum == 'ADDARMATURE_PT_Panel':
            self.draw_armature_objects(layout)
        elif context.scene.object_type_enum == 'ADDLATTICE_PT_Panel':
            self.draw_lattice_objects(layout)
        elif context.scene.object_type_enum == 'ADDEMPTY_PT_Panel':
            self.draw_empty_objects(layout)
        elif context.scene.object_type_enum == 'ADDIMAGE_PT_Panel':
            self.draw_image_objects(layout)
        elif context.scene.object_type_enum == 'ADDLIGHT_PT_Panel':
            self.draw_light_objects(layout)
        elif context.scene.object_type_enum == 'ADDLIGHTPROBE_PT_Panel':
            self.draw_light_probe_objects(layout)
        elif context.scene.object_type_enum == 'ADDCAMERA_PT_Panel':
            self.draw_camera_objects(layout)
        elif context.scene.object_type_enum == 'ADDSPEAKER_PT_Panel':
            self.draw_speaker_objects(layout)
        elif context.scene.object_type_enum == 'ADDFORCEFIELD_PT_Panel':
            self.draw_force_field_objects(layout)
        elif context.scene.object_type_enum == 'ADDCOLLECTION_PT_Panel':
            self.draw_collection_objects(layout)

    #MESH DRAW LAYOUT
    def draw_mesh_objects(self, layout):
        box = layout.box()
        col = box.column()
        col.label(text="Add Mesh Objects", icon="OUTLINER_OB_MESH")
        row = col.row(align=True)
        row.operator("mesh.primitive_plane_add", icon="MESH_PLANE")
        row.operator("mesh.primitive_cube_add", icon="CUBE")
        row = col.row(align=True)
        row.operator("mesh.primitive_circle_add", icon="MESH_CIRCLE")
        row.operator("mesh.primitive_uv_sphere_add", icon="MESH_UVSPHERE")
        row = col.row(align=True)
        row.operator("mesh.primitive_ico_sphere_add", icon="MESH_ICOSPHERE")
        row.operator("mesh.primitive_cylinder_add", icon="MESH_CYLINDER")
        row = col.row(align=True)
        row.operator("mesh.primitive_cone_add", icon="MESH_CONE")
        row.operator("mesh.primitive_torus_add", icon="MESH_TORUS")
        row = col.row(align=True)
        row.operator("mesh.primitive_grid_add", icon="MESH_GRID")
        row.operator("mesh.primitive_monkey_add", icon="MESH_MONKEY")
    
    #CURVE DRAW LAYOUT
    def draw_curve_objects(self, layout):
        box = layout.box()
        col = box.column()
        col.label(text="Add Curve Objects", icon="OUTLINER_OB_CURVE")
        row = col.row(align=True)
        row.operator("curve.primitive_bezier_curve_add", icon="CURVE_BEZCURVE")
        row.operator("curve.primitive_bezier_circle_add", icon="CURVE_BEZCIRCLE")
        row = col.row(align=True)
        row.operator("curve.primitive_nurbs_curve_add", icon="CURVE_NCURVE")
        row.operator("curve.primitive_nurbs_circle_add", icon="CURVE_NCIRCLE")
        row = col.row(align=True)
        row.operator("curve.primitive_nurbs_path_add", icon="CURVE_PATH")
        if bpy.app.version >= (3, 5, 0):
            col.operator("object.curves_empty_hair_add", icon="CURVES_DATA", text="Empty Hair")
            col.operator("object.quick_fur", icon="CURVES_DATA", text="Fur")
        else:
            pass
    
    #SURFACE DRAW LAYOUT
    def draw_surface_objects(self, layout):
        box = layout.box()
        col = box.column()
        col.label(text="Add Surface Objects", icon="OUTLINER_OB_SURFACE")
        row = col.row(align=True)
        row.operator("surface.primitive_nurbs_surface_curve_add",
                     icon="SURFACE_NCURVE")
        row.operator("surface.primitive_nurbs_surface_circle_add",
                     icon="SURFACE_NCIRCLE")
        row = col.row(align=True)
        row.operator("surface.primitive_nurbs_surface_surface_add",
                     icon="SURFACE_NSURFACE")
        row.operator("surface.primitive_nurbs_surface_cylinder_add",
                     icon="SURFACE_NCYLINDER")
        row = col.row(align=True)
        row.operator("surface.primitive_nurbs_surface_sphere_add",
                     icon="SURFACE_NSPHERE")
        row.operator("surface.primitive_nurbs_surface_torus_add",
                     icon="SURFACE_NTORUS")
        row = col.row(align=True)
    
    #METABALL DRAW LAYOUT
    def draw_metaball_objects(self, layout):
        box = layout.box()
        col = box.column()
        col.label(text="Add Metaball Objects", icon="OUTLINER_OB_META")
        row = col.row(align=True)
        row.operator("object.metaball_add", icon="META_BALL", text="Ball").type='BALL'
        row.operator("object.metaball_add", icon="META_CAPSULE", text="Capsule").type='CAPSULE'
        row = col.row(align=True)
        row.operator("object.metaball_add", icon="META_PLANE", text="Plane").type='PLANE'
        row.operator("object.metaball_add", icon="META_ELLIPSOID", text="Ellipsoid").type='ELLIPSOID'
        row = col.row(align=True)
        row.operator("object.metaball_add", icon="META_CUBE", text="Cube").type='CUBE'
        
    #TEXT DRAW LAYOUT
    def draw_text_objects(self, layout):
        box = layout.box()
        col = box.column()
        col.label(text="Add Text Objects", icon="OUTLINER_OB_FONT")
        row = col.row(align=True)
        row.operator("object.text_add", icon="OUTLINER_OB_FONT")
    
    #VOLUME DRAW LAYOUT
    def draw_volume_objects(self, layout):
        box = layout.box()
        col = box.column()
        col.label(text="Add Volume Objects", icon="OUTLINER_OB_VOLUME")
        row = col.row(align=True)
        col.operator("object.volume_import", icon="VOLUME_DATA", text="Import OpenVDB...")
        col.operator("object.volume_add", icon="VOLUME_DATA", text="Empty")
    
    #GREASE PENCIL DRAW LAYOUT
    def draw_grease_pencil_objects(self, layout):
        layout = self.layout
        box = layout.box()
        col = box.column()
        col.label(text="Add Grease Pencil Objects", icon="OUTLINER_OB_GREASEPENCIL")
        row = col.row(align=True)
        col.operator("object.gpencil_add", icon="EMPTY_AXIS", text="Blank").type='EMPTY'
        col.operator("object.gpencil_add", icon="STROKE", text="Stroke").type='STROKE'
        col.operator("object.gpencil_add", icon="MONKEY", text="Monkey").type='MONKEY'
        col.operator("object.gpencil_add", icon="SCENE_DATA", text="Scene Line Art").type='LRT_SCENE'
        col.operator("object.gpencil_add", icon="OUTLINER_COLLECTION", text="Scene Line Art").type='LRT_COLLECTION'
        col.operator("object.gpencil_add", icon="OBJECT_DATA", text="Object Line Art").type='LRT_OBJECT'
        
    #ARMATURE DRAW LAYOUT
    def draw_armature_objects(self, layout):
        box = layout.box()
        col = box.column()
        col.label(text="Add Armature Objects", icon="OUTLINER_OB_ARMATURE")
        row = col.row(align=True)
        row.operator("object.armature_add", icon="OUTLINER_OB_ARMATURE")
        
    #LATTICE DRAW LAYOUT
    def draw_lattice_objects(self, layout):
        box = layout.box()
        col = box.column()
        col.label(text="Add Lattice Objects", icon="OUTLINER_OB_LATTICE")
        row = col.row(align=True)
        row.operator("object.add", icon="OUTLINER_OB_LATTICE", text="Lattice").type='LATTICE'
        
    #EMPTY DRAW LAYOUT
    def draw_empty_objects(self, layout):
        box = layout.box()
        col = box.column()
        col.label(text="Add Empty Objects", icon="OUTLINER_OB_EMPTY")
        row = col.row(align=True)
        row.operator("object.empty_add", icon="EMPTY_AXIS", text="Plain Axes").type='PLAIN_AXES'
        row.operator("object.empty_add", icon="EMPTY_ARROWS", text="Arrows").type='ARROWS'
        row = col.row(align=True)
        row.operator("object.empty_add", icon="EMPTY_SINGLE_ARROW", text="Single Arrow").type='SINGLE_ARROW'
        row.operator("object.empty_add", icon="MESH_CIRCLE", text="Circle").type='CIRCLE'
        row = col.row(align=True)
        row.operator("object.empty_add", icon="CUBE", text="Cube").type='CUBE'
        row.operator("object.empty_add", icon="SPHERE", text="Sphere").type='SPHERE'
        row = col.row(align=True)
        row.operator("object.empty_add", icon="CONE", text="Cone").type='CONE'
        row.operator("object.empty_add", icon="IMAGE_DATA", text="Image").type='IMAGE'
    
    #IMAGE DRAW LAYOUT
    def draw_image_objects(self, layout):
        box = layout.box()
        col = box.column()
        col.label(text="Add Image Objects", icon="OUTLINER_OB_IMAGE")
        row = col.row(align=True)
        col.operator("object.load_reference_image", icon="IMAGE_REFERENCE", text="Referance Image")
        col.operator("object.load_background_image", icon="IMAGE_BACKGROUND", text="Background Image")
    
    #LIGHT DRAW LAYOUT
    def draw_light_objects(self, layout):
        box = layout.box()
        col = box.column()
        col.label(text="Add Light Objects", icon="OUTLINER_OB_LIGHT")
        row = col.row(align=True)
        col.operator("object.light_add", icon="LIGHT_POINT", text="Point").type='POINT'
        col.operator("object.light_add", icon="LIGHT_SUN", text="Sun").type='SUN'
        col.operator("object.light_add", icon="LIGHT_SPOT", text="Spot").type='SPOT'
        col.operator("object.light_add", icon="LIGHT_AREA", text="Area").type='AREA'
    
    #LIGHT PROBE DRAW LAYOUT
    def draw_light_probe_objects(self, layout):
        box = layout.box()
        col = box.column()
        col.label(text="Add Light Probe Objects", icon="OUTLINER_OB_LIGHTPROBE")
        row = col.row(align=True)

        if bpy.app.version >= (4, 1, 0):
            col.operator("object.lightprobe_add", icon="LIGHTPROBE_SPHERE", text="Sphere").type='SPHERE'
            col.operator("object.lightprobe_add", icon="LIGHTPROBE_PLANE", text="Plane").type='PLANE'
            col.operator("object.lightprobe_add", icon="LIGHTPROBE_VOLUME", text="Volume").type='VOLUME'
        else:
            col.operator("object.lightprobe_add", icon="LIGHTPROBE_CUBEMAP", text="Reflection Cubemap").type='CUBEMAP'
            col.operator("object.lightprobe_add", icon="LIGHTPROBE_PLANAR", text="Reflection Plane").type='PLANAR'
            col.operator("object.lightprobe_add", icon="LIGHTPROBE_GRID", text="Irradiance Volume").type='GRID'
        
    #CAMERA DRAW LAYOUT
    def draw_camera_objects(self, layout):
        box = layout.box()
        col = box.column()
        col.label(text="Add Camera Objects", icon="OUTLINER_OB_CAMERA")
        row = col.row(align=True)
        row.operator("object.camera_add", icon="OUTLINER_OB_CAMERA", text="Camera")
    
    #SPEAKER DRAW LAYOUT
    def draw_speaker_objects(self, layout):
        box = layout.box()
        col = box.column()
        col.label(text="Add Speaker Objects", icon="OUTLINER_OB_SPEAKER")
        row = col.row(align=True)
        row.operator("object.speaker_add", icon="OUTLINER_OB_SPEAKER", text="Speaker")
        
    #FORCE FIELD DRAW LAYOUT
    def draw_force_field_objects(self, layout):
        box = layout.box()
        col = box.column()
        col.label(text="Add Force Field Objects", icon="OUTLINER_OB_FORCE_FIELD")
        row = col.row(align=True)
        row.operator("object.effector_add", icon="FORCE_FORCE", text="Force").type='FORCE'
        row.operator("object.effector_add", icon="FORCE_WIND", text="Wind").type='WIND'
        row = col.row(align=True)
        row.operator("object.effector_add", icon="FORCE_VORTEX", text="Vortex").type='VORTEX'
        row.operator("object.effector_add", icon="FORCE_MAGNETIC", text="Magnetic").type='MAGNET'
        row = col.row(align=True)
        row.operator("object.effector_add", icon="FORCE_HARMONIC", text="Harmonic").type='HARMONIC'
        row.operator("object.effector_add", icon="FORCE_CHARGE", text="Charge").type='CHARGE'
        row = col.row(align=True)
        row.operator("object.effector_add", icon="FORCE_LENNARDJONES", text="Lennard-Jones").type='LENNARDJ'
        row.operator("object.effector_add", icon="FORCE_TEXTURE", text="Texture").type='TEXTURE'
        row = col.row(align=True)
        row.operator("object.effector_add", icon="FORCE_CURVE", text="Curve Guide").type='GUIDE'
        row.operator("object.effector_add", icon="FORCE_BOID", text="Boid").type='BOID'
        row = col.row(align=True)
        row.operator("object.effector_add", icon="FORCE_TURBULENCE", text="Turbulence").type='TURBULENCE'
        row.operator("object.effector_add", icon="FORCE_DRAG", text="Drag").type='DRAG'
        row = col.row(align=True)
        row.operator("object.effector_add", icon="FORCE_FLUIDFLOW", text="Fluid Flow").type='FLUID'
    
    #COLLECTION DRAW LAYOUT
    def draw_collection_objects(self, layout):
        box = layout.box()
        col = box.column()
        col.label(text="Add Collection Objects", icon="OUTLINER_OB_GROUP_INSTANCE")
        row = col.row(align=True)
        row.operator("object.collection_instance_add", icon="OUTLINER_COLLECTION", text="Collection")

def register():
    bpy.utils.register_class(ARCBLEND_PT_Panel)
    bpy.types.Scene.object_type_enum = bpy.props.EnumProperty(
        items=[
            ('ADDMESH_PT_Panel', 'Mesh', 'Shows ADDMESH Panel', 'OUTLINER_OB_MESH', 1),
            ('ADDCURVE_PT_Panel', 'Curve', 'Shows ADDCURVE Panel', 'OUTLINER_OB_CURVE', 2),
            ('ADDSURFACE_PT_Panel', 'Surface', 'Shows ADDSURFACE Panel', 'OUTLINER_OB_SURFACE', 3),
            ('ADDMETABALL_PT_Panel', 'Metaball', 'Shows ADDMETABALL Panel', 'OUTLINER_OB_META', 4),
            ('ADDTEXT_PT_Panel', 'Text', 'Shows ADDTEXT Panel', 'OUTLINER_OB_FONT', 5),
            ('ADDVOLUME_PT_Panel', 'Volume', 'Shows ADDVOLUME Panel', 'OUTLINER_OB_VOLUME', 6),
            ('ADDGREASEPENCIL_PT_Panel', 'Grease Pencil', 'Shows ADDGREASEPENCIL Panel', 'OUTLINER_OB_GREASEPENCIL', 7),
            ('ADDARMATURE_PT_Panel', 'Armature', 'Shows ADDARMATURE Panel', 'OUTLINER_OB_ARMATURE', 8),
            ('ADDLATTICE_PT_Panel', 'Lattice', 'Shows ADDLATTICE Panel', 'OUTLINER_OB_LATTICE', 9),
            ('ADDEMPTY_PT_Panel', 'Empty', 'Shows ADDEMPTY Panel', 'OUTLINER_OB_EMPTY', 10),
            ('ADDIMAGE_PT_Panel', 'Image', 'Shows ADDIMAGE Panel', 'OUTLINER_OB_IMAGE', 11),
            ('ADDLIGHT_PT_Panel', 'Light', 'Shows ADDLIGHT Panel', 'OUTLINER_OB_LIGHT', 12),
            ('ADDLIGHTPROBE_PT_Panel', 'Light Probe', 'Shows ADDLIGHTPROBE Panel', 'OUTLINER_OB_LIGHTPROBE', 13),
            ('ADDCAMERA_PT_Panel', 'Camera', 'Shows ADDCAMERA Panel', 'OUTLINER_OB_CAMERA', 14),
            ('ADDSPEAKER_PT_Panel', 'Speaker', 'Shows ADDSPEAKER Panel', 'OUTLINER_OB_SPEAKER', 15),
            ('ADDFORCEFIELD_PT_Panel', 'Force Field', 'Shows ADDFORCEFIELD Panel', 'OUTLINER_OB_FORCE_FIELD', 16),
            ('ADDCOLLECTION_PT_Panel', 'Collection Instance', 'Shows ADDCOLLECTION Panel', 'OUTLINER_OB_GROUP_INSTANCE', 17)
        ],
        description="Select the type of object to add. Add Object",
        default='ADDMESH_PT_Panel'
    )

def unregister():
    bpy.utils.unregister_class(ARCBLEND_PT_Panel)
    del bpy.types.Scene.object_type_enum
