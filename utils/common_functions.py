import os

import streamlit as st
from PIL import Image, ImageFont, ImageDraw


# Function to display font preview
def font_preview(font_list, font_dir, preview_text="Sample Text"):
    preview_images = {}
    for font_name in font_list:
        try:
            font_path = os.path.join(font_dir, font_name)
            pil_font = ImageFont.truetype(font_path, 40)  # Adjust font size for preview
            img = Image.new("RGB", (300, 100), color=(255, 255, 255))  # Preview size
            draw = ImageDraw.Draw(img)
            draw.text((10, 25), preview_text, font=pil_font, fill=(0, 0, 0))
            preview_images[font_name] = img
        except Exception as e:
            st.warning(f"Could not load font {font_name}: {e}")
    return preview_images

def generate_custom_dropdown(font_list, font_dir):
    """
    Generate custom HTML for dropdown where each font name is styled in its font.
    """
    # CSS for handling the dropdown customization
    custom_css = """
    <style>
    .custom-select {
        width: 100%;
        font-size: 16px;
        height: 35px;
        border: 1px solid #cccccc;
        border-radius: 4px;
        padding: 5px;
    }
    </style>
    """

    # Generate the dropdown with dynamically applied font styles
    font_items_html = ""
    for font_name in font_list:
        font_path = os.path.join(font_dir, font_name)
        font_face_name = font_name.replace(".ttf", "").replace("_", " ")
        font_items_html += f"""
        <option style="font-family: '{font_face_name}';" value="{font_name}">
            {font_face_name}
        </option>
        """

    dropdown_html = f"""
    {custom_css}
    <select class="custom-select" id="font-dropdown" onchange="updateFontSelection(this.value)">
        {font_items_html}
    </select>

    <script>
    function updateFontSelection(fontName) {{
        // Write the selection to a text input field hidden in DOM
        document.getElementById("selected-font").value = fontName;
        document.getElementById("selected-font").dispatchEvent(new Event('input'));
    }}
    </script>
    """

    return dropdown_html


def load_fonts_in_browser(font_list, font_dir):
    """
    Dynamically load fonts into the browser using HTML `@font-face`.
    """
    font_face_css = "<style>"
    for font_name in font_list:
        font_path = os.path.join(font_dir, font_name).replace(" ", "%20")
        font_face_name = font_name.replace(".ttf", "").replace("_", " ")
        font_face_css += f"""
        @font-face {{
            font-family: '{font_face_name}';
            src: url('{font_path}');
        }}
        """
    font_face_css += "</style>"
    return font_face_css