import os

import streamlit as st
from PIL import Image, ImageFont, ImageDraw

from config import IMAGE_SIZE


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


def add_border_and_frame(image, border_width, border_color, frame_option, frame_image=None):
    draw = ImageDraw.Draw(image)

    # Add border
    if border_width > 0:
        draw.rectangle(
            [border_width, border_width, IMAGE_SIZE[0] - border_width, IMAGE_SIZE[1] - border_width],
            outline=border_color,
            width=border_width
        )

    # Add frame
    if frame_option == "Simple Frame":
        draw.rectangle(
            [0, 0, IMAGE_SIZE[0], IMAGE_SIZE[1]],
            outline=border_color,
            width=border_width
        )
    elif frame_option == "Patterned Frame" and frame_image:
        frame = Image.open(frame_image).resize(image.size)
        image.paste(frame, mask=frame)

    return image


# Apply transformations
def edit_image(image, rotate_angle, flip_option):
    # Rotate image
    if rotate_angle:
        image = image.rotate(rotate_angle, expand=True)

    # Flip image
    if flip_option == "Horizontal":
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    elif flip_option == "Vertical":
        image = image.transpose(Image.FLIP_TOP_BOTTOM)

    return image


def add_overlays(image, watermark_text, gradient_color, font_name):
    draw = ImageDraw.Draw(image)

    # Add watermark
    if watermark_text:
        font = ImageFont.truetype(font_name, 20)
        bbox = font.getbbox(watermark_text)
        # text_width, text_height = draw.textsize(watermark_text, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        position = (IMAGE_SIZE[0] - text_width - 10, IMAGE_SIZE[1] - text_height - 10)
        draw.text(position, watermark_text, font=font, fill="white")

    # # Add gradient
    # if gradient_color:
    #     for y in range(IMAGE_SIZE[1]):
    #         color = tuple(int(gradient_color[i:i+2], 16) for i in (1, 3, 5))
    #         alpha = int(255 * (y / IMAGE_SIZE[1]))
    #         draw.line([(0, y), (IMAGE_SIZE[0], y)], fill=color + (alpha,))

    return image