import bpy
import xml.etree.ElementTree as ET
import re
import os



class UnifiedPaintPanel:
    # subclass must set
    # bl_space_type = 'IMAGE_EDITOR'
    # bl_region_type = 'UI'

    @staticmethod
    def get_brush_mode(context):
        """ Get the correct mode for this context. For any context where this returns None,
            no brush options should be displayed."""
        mode = context.mode

        if mode == 'PARTICLE':
            # Particle brush settings currently completely do their own thing.
            return None

        from bl_ui.space_toolsystem_common import ToolSelectPanelHelper
        tool = ToolSelectPanelHelper.tool_active_from_context(context)

        if not tool:
            # If there is no active tool, then there can't be an active brush.
            return None

        if not tool.has_datablock:
            # tool.has_datablock is always true for tools that use brushes.
            return None

        space_data = context.space_data
        tool_settings = context.tool_settings

        if space_data:
            space_type = space_data.type
            if space_type == 'IMAGE_EDITOR':
                if space_data.show_uvedit:
                    return 'UV_SCULPT'
                return 'PAINT_2D'
            elif space_type in {'VIEW_3D', 'PROPERTIES'}:
                if mode == 'PAINT_TEXTURE':
                    if tool_settings.image_paint:
                        return mode
                    else:
                        return None
                return mode
        return None

    @staticmethod
    def paint_settings(context):
        tool_settings = context.tool_settings

        mode = UnifiedPaintPanel.get_brush_mode(context)

        # 3D paint settings
        if mode == 'SCULPT':
            return tool_settings.sculpt
        elif mode == 'PAINT_VERTEX':
            return tool_settings.vertex_paint
        elif mode == 'PAINT_WEIGHT':
            return tool_settings.weight_paint
        elif mode == 'PAINT_TEXTURE':
            return tool_settings.image_paint
        elif mode == 'PARTICLE':
            return tool_settings.particle_edit
        # 2D paint settings
        elif mode == 'PAINT_2D':
            return tool_settings.image_paint
        elif mode == 'UV_SCULPT':
            return tool_settings.uv_sculpt
        # Grease Pencil settings
        elif mode == 'PAINT_GPENCIL':
            return tool_settings.gpencil_paint
        elif mode == 'SCULPT_GPENCIL':
            return tool_settings.gpencil_sculpt_paint
        elif mode == 'WEIGHT_GPENCIL':
            return tool_settings.gpencil_weight_paint
        elif mode == 'VERTEX_GPENCIL':
            return tool_settings.gpencil_vertex_paint
        elif mode == 'SCULPT_CURVES':
            return tool_settings.curves_sculpt
        return None

    @staticmethod
    def prop_unified(
            layout,
            context,
            brush,
            prop_name,
            unified_name=None,
            pressure_name=None,
            icon='NONE',
            text=None,
            slider=False,
            header=False,
    ):
        """ Generalized way of adding brush options to the UI,
            along with their pen pressure setting and global toggle, if they exist. """
        row = layout.row(align=True)
        ups = context.tool_settings.unified_paint_settings
        prop_owner = brush
        if unified_name and getattr(ups, unified_name):
            prop_owner = ups

        row.prop(prop_owner, prop_name, icon=icon, text=text, slider=slider)

        if pressure_name:
            row.prop(brush, pressure_name, text="")

        if unified_name and not header:
            # NOTE: We don't draw UnifiedPaintSettings in the header to reduce clutter. D5928#136281
            row.prop(ups, unified_name, text="", icon='BRUSHES_ALL')

        return row

    @staticmethod
    def prop_unified_color(parent, context, brush, prop_name, *, text=None):
        ups = context.tool_settings.unified_paint_settings
        prop_owner = ups if ups.use_unified_color else brush
        parent.prop(prop_owner, prop_name, text=text)

    @staticmethod
    def prop_unified_color_picker(parent, context, brush, prop_name, value_slider=True):
        ups = context.tool_settings.unified_paint_settings
        prop_owner = ups if ups.use_unified_color else brush
        parent.template_color_picker(prop_owner, prop_name, value_slider=value_slider)




class ExportCSSPaletteOperator(bpy.types.Operator):
    bl_idname = "object.export_css_palette_operator"
    bl_label = "Export CSS Palette"

    def execute(self, context):
        scene = context.scene
        filepath = scene.css_palette_file

        try:
            if not filepath:
                self.report({'ERROR'}, "No file selected!")
                return {'CANCELLED'}

            # Get the active palette
            active_palette = context.tool_settings.image_paint.palette
            if not active_palette:
                self.report({'ERROR'}, "No active palette found!")
                return {'CANCELLED'}

            # Set to store unique colors
            unique_colors = set()

            # Open the file for writing
            with open(filepath, 'w') as file:
                file.write("/* Color Theme Swatches in Hex */\n")
                # Write colors in hex format to the CSS file
                for i, color in enumerate(active_palette.colors):
                    hex_color = "#{:02X}{:02X}{:02X}".format(
                        int(color.color[0] * 255),
                        int(color.color[1] * 255),
                        int(color.color[2] * 255)
                    )
                    # Check if the color is unique before writing
                    if hex_color not in unique_colors:
                        file.write(f".My-Color-Theme-{i + 1}-hex {{ color: {hex_color}; }}\n")
                        unique_colors.add(hex_color)

            self.report({'INFO'}, f"Exported {len(unique_colors)} unique colors to CSS file.")
        except Exception as e:
            self.report({'ERRORd'}, f"Failed to export colors: {str(e)}")

        return {'FINISHED'}


class ImportCSSPaletteOperator(bpy.types.Operator):
    bl_idname = "object.import_css_palette_operator"
    bl_label = "Import CSS Palette"

    def execute(self, context):
        scene = context.scene
        filepath = scene.css_palette_file

        try:
            if not filepath:
                self.report({'ERROR'}, "No file selected!")
                return {'CANCELLED'}

            # Read the CSS file content
            with open(filepath, 'r') as file:
                css_content = file.read()

            # Use regular expression to extract color values in hexadecimal format from CSS content
            colors_hex = re.findall(r'#([A-Fa-f0-9]{6})', css_content)

            # Create a new palette if it doesn't exist
            palette_name = bpy.path.display_name_from_filepath(filepath)
            if palette_name not in bpy.data.palettes:
                palette = bpy.data.palettes.new(palette_name)
            else:
                palette = bpy.data.palettes[palette_name]

            # Add colors to the palette (hexadecimal)
            for color_hex in colors_hex:
                r = int(color_hex[0:2], 16) / 255.0
                g = int(color_hex[2:4], 16) / 255.0
                b = int(color_hex[4:6], 16) / 255.0
                new_color = (r, g, b)

                # Round color components to a certain precision to avoid floating-point comparison issues
                precision = 5  # Adjust the precision level as needed
                new_color_rounded = tuple(round(c, precision) for c in new_color)

                # Check if the color already exists in the palette
                existing_colors = [tuple(round(c, precision) for c in col.color) for col in palette.colors]
                if new_color_rounded not in existing_colors:
                    color = palette.colors.new()
                    color.color = new_color

            total_colors = len(colors_hex)
            self.report({'INFO'}, f"Imported {total_colors} unique colors from CSS file.")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to import colors: {str(e)}")

        return {'FINISHED'}



#------------------------------------------------------------------------
def draw_color_settings(context, layout, brush, color_type=False):
    """Draw color wheel and gradient settings."""
    ups = context.scene.tool_settings.unified_paint_settings

    if color_type:
        row = layout.row()
        row.use_property_split = False
        row.prop(brush, "color_type", expand=True)

    # Color wheel
    if brush.color_type == 'COLOR':
        UnifiedPaintPanel.prop_unified_color_picker(layout, context, brush, "color", value_slider=True)

        row = layout.row(align=True)
        UnifiedPaintPanel.prop_unified_color(row, context, brush, "color", text="")
        UnifiedPaintPanel.prop_unified_color(row, context, brush, "secondary_color", text="")
        row.separator()
        row.operator("paint.brush_colors_flip", icon='FILE_REFRESH', text="", emboss=False)
        row.prop(ups, "use_unified_color", text="", icon='BRUSHES_ALL')
    # Gradient
    elif brush.color_type == 'GRADIENT':
        layout.template_color_ramp(brush, "gradient", expand=True)

        layout.use_property_split = True

        col = layout.column()

        if brush.image_tool == 'DRAW':
            UnifiedPaintPanel.prop_unified(
                col,
                context,
                brush,
                "secondary_color",
                unified_name="use_unified_color",
                text="Background Color",
                header=True,
            )

            col.prop(brush, "gradient_stroke_mode", text="Gradient Mapping")
            if brush.gradient_stroke_mode in {'SPACING_REPEAT', 'SPACING_CLAMP'}:
                col.prop(brush, "grad_spacing")
#-------------------------------------------------------------


class ImportJPEGPaletteOperator(bpy.types.Operator):
    bl_idname = "object.import_jpeg_palette_operator"
    bl_label = "Import JPEG Palette"

    def execute(self, context):
        try:
            # Get the file path of the image
            file_path = context.scene.css_palette_file
            
            # Extract just the file name
            file_name = os.path.basename(file_path)
            
            
            if not file_path:
                self.report({'ERROR'}, "No file selected!")
                return {'CANCELLED'}
            
            # Open the image file
            bpy.ops.image.open(filepath=file_path)
            
            # Get the loaded image
            loaded_image = bpy.context.active_object

            if loaded_image is None:
                self.report({'ERROR'}, "Failed to load the image")
                return {'CANCELLED'}

            # Switch the context to the Image Editor
            bpy.context.area.ui_type = 'IMAGE_EDITOR'

            # Access the image data block
            bpy.data.images[file_name].name = file_name
            
            bpy.ops.image.open(filepath=file_path,files=[{"name":file_name, "name":file_name}], relative_path=True, show_multiview=False)

            # Run the palette extraction operator
            bpy.ops.palette.extract_from_image()

            # Switch back to the 3D View context
            bpy.context.area.ui_type = 'VIEW_3D'

            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to import the palette: {str(e)}")
            return {'CANCELLED'}


def rgb_to_hex(rgb):
    # Convert each color component to its hexadecimal representation
    hex_color = "#{:02x}{:02x}{:02x}".format(
        int(rgb[0] * 255),
        int(rgb[1] * 255),
        int(rgb[2] * 255)
    )
    return hex_color.upper()  # Optionally, convert to uppercase

    
class PANEL_PT_ColorPaletteArcBlend(bpy.types.Panel):
    bl_label = "AB Color Palette"
    bl_idname = "PANEL_PT_ColorPaletteArcBlend"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Arc Blend"
    bl_options = {'DEFAULT_CLOSED'}
    
    @staticmethod
    def paint_settings(context):
        return context.tool_settings.image_paint if context.tool_settings.image_paint else context.tool_settings.sculpt
   
   

    def draw(self, context):
        layout = self.layout
        settings = self.paint_settings(context)
        sima = context.space_data
        ups = context.scene.tool_settings.unified_paint_settings

        col=layout.column()
        col.separator()
        col.label(text="Import/Export CSS Palette:")
        col.prop(context.scene, "css_palette_file", text="")

        col.separator()
        col.operator("object.import_css_palette_operator", text="Import CSS Palette")
        col.operator("object.export_css_palette_operator", text="Export CSS Palette")
        col.operator("object.import_jpeg_palette_operator", text="JPG to Palette")
        
        
        col.separator()
        col.label(text="Color Picker:")
        
        # Get the active brush
        brush = bpy.context.tool_settings.image_paint.brush
        
        # Define color_type or remove the usage
        color_type = True  # Set to True or False as per your logic
        
        if color_type:
            row = layout.row()
            row.use_property_split = False
            row.prop(brush, "color_type", expand=True)

        # Color wheel
        if brush.color_type == 'COLOR':
            UnifiedPaintPanel.prop_unified_color_picker(layout, context, brush, "color", value_slider=True)

            row = layout.row(align=True)
            UnifiedPaintPanel.prop_unified_color(row, context, brush, "color", text="")
            UnifiedPaintPanel.prop_unified_color(row, context, brush, "secondary_color", text="")
            row.separator()
            row.operator("paint.brush_colors_flip", icon='FILE_REFRESH', text="", emboss=False)
            row.prop(ups, "use_unified_color", text="", icon='BRUSHES_ALL')
        
        # Gradient
        elif brush.color_type == 'GRADIENT':
            layout.template_color_ramp(brush, "gradient", expand=True)

            layout.use_property_split = True

            col = layout.column()

            if brush.image_tool == 'DRAW':
                UnifiedPaintPanel.prop_unified(
                    col,
                    context,
                    brush,
                    "secondary_color",
                    unified_name="use_unified_color",
                    text="Background Color",
                    header=True,
                )

                col.prop(brush, "gradient_stroke_mode", text="Gradient Mapping")
                if brush.gradient_stroke_mode in {'SPACING_REPEAT', 'SPACING_CLAMP'}:
                    col.prop(brush, "grad_spacing")
        
        
        
        #color_rgb = bpy.data.brushes["TexDraw"].color
        #hex_color = rgb_to_hex(color_rgb)
        
        # Custom property for hex color
        layout.prop(context.scene, "hex_color", text= "")
        
        layout.operator("object.update_hex_color", text="Update Hex Color")
        layout.operator("color_palette.copy_hex", text="Copy Hex Color")
        layout.operator("color_palette.paste_hex", text="Paste Hex Color")
        
        


        col.separator()
        col=layout.column()
        col.label(text="Palette Properties:")
        layout.template_ID(settings, "palette", new="palette.new")
        if settings.palette:
            layout.template_palette(settings, "palette", color=True)
      
      
#Updates the Hex Color showing the hex      
class UpdateHexColorOperator(bpy.types.Operator):
    bl_idname = "object.update_hex_color"
    bl_label = "Update Hex Color"

    def execute(self, context):
        color_rgb = bpy.data.brushes["TexDraw"].color
        hex_color = rgb_to_hex(color_rgb)
        context.scene.hex_color = hex_color
        return {'FINISHED'}


# Operator to copy hex value to clipboard
class CopyHexOperator(bpy.types.Operator):
    bl_idname = "color_palette.copy_hex"
    bl_label = "Copy Hex Value"

    def execute(self, context):
        color_rgb = bpy.data.brushes["TexDraw"].color
        hex_color = rgb_to_hex(color_rgb)
        bpy.context.window_manager.clipboard = hex_color
        return {'FINISHED'}
    
    
# Operator to paste hex value from clipboard
class PasteHexOperator(bpy.types.Operator):
    bl_idname = "color_palette.paste_hex"
    bl_label = "Paste Hex Value"

    index: bpy.props.IntProperty()

    def execute(self, context):
        color_rgb = bpy.data.brushes["TexDraw"].color  # Assuming this is the Color object you want to modify
        hex_color = bpy.context.window_manager.clipboard.strip()
        bpy.context.scene.hex_color = hex_color

        r = int(hex_color[1:3], 16) / 255.0
        g = int(hex_color[3:5], 16) / 255.0
        b = int(hex_color[5:], 16) / 255.0
        color_rgb = (r, g, b)  # Assign the converted RGB values to the color object

        
        #if hex_color.startswith("#") and len(hex_color) == 7:
            
            # Optionally update other relevant properties related to the color object

        return {'FINISHED'}

#----------------------------------------------------------------
def register():
    bpy.types.Scene.css_palette_file = bpy.props.StringProperty(subtype="FILE_PATH")
    bpy.types.Scene.jpeg_palette_file = bpy.props.StringProperty(subtype="FILE_PATH")  # New property for JPEG file
    bpy.types.Scene.hex_color = bpy.props.StringProperty(
        name="Hex Color",
        default=""  # Set default hex color here
    )
    bpy.utils.register_class(PANEL_PT_ColorPaletteArcBlend)
    bpy.utils.register_class(ImportCSSPaletteOperator)
    bpy.utils.register_class(ExportCSSPaletteOperator)
    bpy.utils.register_class(ImportJPEGPaletteOperator)  # Register the new operator
    bpy.utils.register_class(UpdateHexColorOperator)
    bpy.utils.register_class(CopyHexOperator)
    bpy.utils.register_class(PasteHexOperator)
    
    
    


def unregister():
    del bpy.types.Scene.css_palette_file
    del bpy.types.Scene.jpeg_palette_file  # Remove the JPEG file property
    del bpy.types.Scene.hex_color
    bpy.utils.unregister_class(PANEL_PT_ColorPaletteArcBlend)
    bpy.utils.unregister_class(ImportCSSPaletteOperator)
    bpy.utils.unregister_class(ExportCSSPaletteOperator)
    bpy.utils.unregister_class(ImportJPEGPaletteOperator)  # Register the new operator
    bpy.utils.unregister_class(UpdateHexColorOperator)
    bpy.utils.unregister_class(CopyHexOperator)
    bpy.utils.unregister_class(PasteHexOperator)

if __name__ == "__main__":
    register()
