import bpy

class ASSETBROWSER_PT_arcblend(bpy.types.Panel):
        bl_id = "ASSETBROWSER_PT_arcblend"
        bl_label = "Asset Browser"
        bl_space_type = "VIEW_3D"
        bl_region_type = "UI"
        bl_category = "Arc Blend"
        bl_options = {'DEFAULT_CLOSED'}

        def draw(self, context):
            layout = self.layout
            col = layout.column(align=False)
            col.label(text="<<<Coming Soon>>>")

# ------------------------------------------------------------------------------
# REGISTRATION AREA

def register():
    bpy.utils.register_class(ASSETBROWSER_PT_arcblend)

def unregister():
    bpy.utils.unregister_class(ASSETBROWSER_PT_arcblend)

