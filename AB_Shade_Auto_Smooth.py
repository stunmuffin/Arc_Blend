import bpy

def use_auto_smooth_upd(self, context):
    mesh_property = context.mesh.mesh_property
    active_object = context.active_object
    if mesh_property.use_auto_smooth and context.active_object and context.active_object.type == 'MESH':
        smooth_angle = active_object.data.mesh_property.auto_smooth_angle
        bpy.ops.object.shade_smooth_by_angle(angle=smooth_angle, keep_sharp_edges=False)
    else:
        bpy.ops.object.shade_smooth(keep_sharp_edges=False)
    return None

def auto_smooth_angle_upd(self, context):
    mesh_property = context.mesh.mesh_property
    active_object = context.active_object
    if mesh_property.use_auto_smooth and context.active_object and context.active_object.type == 'MESH':
        smooth_angle = active_object.data.mesh_property.auto_smooth_angle
        bpy.ops.object.shade_smooth_by_angle(angle=smooth_angle, keep_sharp_edges=False)
    else:
        bpy.ops.object.shade_smooth(keep_sharp_edges=False)
    return None

class MeshPropertiesGroup(bpy.types.PropertyGroup):
    
    use_auto_smooth: bpy.props.BoolProperty(
        name="Auto Smooth",
        description="Auto smooth (based on smooth/sharp faces/edges and angle between faces) or use custom split normals data if available",
        update=use_auto_smooth_upd
    )
    
    auto_smooth_angle: bpy.props.FloatProperty(
        name="Auto Smooth Angle",
        description="Maximum angle between faces for auto smooth",
        default=0.523599,
        min=0,
        max=100,
        subtype='ANGLE',
        precision=2,
        update=auto_smooth_angle_upd
    )

class DATA_PT_normals(bpy.types.Panel):
    bl_label = "Normals"
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        mesh_property = context.active_object.data.mesh_property

        layout.use_property_split = True

        col = layout.column(align=False, heading="Auto Smooth")
        col.use_property_decorate = False
        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(mesh_property, "use_auto_smooth", text="")
        sub = sub.row(align=True)
        sub.prop(mesh_property, "auto_smooth_angle", text="")
        row.prop_decorator(mesh_property, "auto_smooth_angle")
        row = col.row(align=True)
        row = col.row(align=True)
        row.operator("OBJECT_OT_shade_smooth", text="Object Smooth")
        row.operator("OBJECT_OT_shade_flat", text="Object Flat")

# Register the panel
def register():
    bpy.utils.register_class(DATA_PT_normals)
    bpy.utils.register_class(MeshPropertiesGroup)
    bpy.types.Mesh.mesh_property = bpy.props.PointerProperty(type=MeshPropertiesGroup)

def unregister():
    bpy.utils.unregister_class(DATA_PT_normals)
    bpy.utils.unregister_class(MeshPropertiesGroup)
    del bpy.types.Mesh.mesh_property

if __name__ == "__main__":
    register()
