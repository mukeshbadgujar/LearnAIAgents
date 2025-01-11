from PIL import Image, ImageDraw, ImageFont
import os
import textwrap
import streamlit as st
from config import IMAGE_SIZE, FONT_DIR

# Path to an emoji-compatible font
EMOJI_FONT_PATH = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

def generate_image(text, font_name, font_size, text_color, bg_color, emojis=None, emoji_size=50, emoji_position=(0, 0)):
    """
    Generates an Instagram-style post image with the given text and styles.
    :param text: The text to display.
    :param font_name: Font file name (e.g., "Poppins-Regular.ttf").
    :param font_size: Font size for the text.
    :param text_color: Color of the text.
    :param bg_color: Background color of the image.
    :param emojis: Emojis to add to the image.
    :param emoji_size: Size of the emojis.
    :param emoji_position: Position of the emojis (x, y).
    :return: PIL Image object.
    """
    # Create a blank canvas
    img = Image.new("RGB", IMAGE_SIZE, color=bg_color)
    draw = ImageDraw.Draw(img)

    # Load selected font
    try:
        font_path = os.path.join(FONT_DIR, font_name)
        font = ImageFont.truetype(font_path, font_size)
    except Exception as e:
        st.error(f"Error loading font: {e}")
        return None

    # Wrap the text to fit within the image width
    max_width = IMAGE_SIZE[0] - 20  # Adding padding
    lines = []
    for line in text.split('\n'):  # Handle existing newlines
        wrapped_lines = textwrap.wrap(line, width=40)  # Wrap lines at 40 characters
        lines.extend(wrapped_lines)

    wrapped_text = "\n".join(lines)

    # Calculate text position for centering
    bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)  # Get bounding box of the wrapped text
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]  # Calculate width and height
    position = ((IMAGE_SIZE[0] - text_width) // 2, (IMAGE_SIZE[1] - text_height) // 2)

    # Draw text on the canvas
    draw.multiline_text(position, wrapped_text, font=font, fill=text_color, align="center")

    # Add emojis using an emoji-compatible font
    if emojis:
        try:
            emoji_font = ImageFont.truetype(EMOJI_FONT_PATH, emoji_size)
            draw.text(emoji_position, emojis, font=emoji_font, fill=text_color)
        except Exception as e:
            st.error(f"Error loading emoji font: {e}")

    return img
