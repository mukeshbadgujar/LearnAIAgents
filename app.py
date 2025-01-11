import os
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from services.summarizer import summarize_content
import logging
from config import FONT_DIR, DEFAULT_REPO
from services.image_generator import generate_image
from services.fetch_data import fetch_github_releases

# Configure logging
logging.basicConfig(filename="logs/app.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

DEFAULT_TEXT = "Your Daily Tech Update\nPowered by AI!"

# --- Helper Functions ---
def list_available_fonts(font_dir):
    """
    Lists all TTF fonts available in the specified directory.
    :param font_dir: Directory containing font files.
    :return: List of font names (without path).
    """
    if not os.path.exists(font_dir):
        os.makedirs(font_dir)
    return [f for f in os.listdir(font_dir) if f.endswith(".ttf")]



# --- Streamlit App ---
st.title("Dynamic Image Generator for Instagram Posts")
st.write("Create Instagram-style posts with dynamic fonts and real-time previews.")
repo = st.text_input("Enter GitHub Repository (e.g., huggingface/transformers)", DEFAULT_REPO)

# Section: Font Selection
st.subheader("Font Selection")
available_fonts = list_available_fonts(FONT_DIR)
if not available_fonts:
    st.warning("No fonts available. Please add `.ttf` font files to the `fonts/` directory.")
else:
    selected_font = st.selectbox("Choose a font", available_fonts, index=0)

# Section: Text Customization
st.subheader("Customize Your Text")
text_input = st.text_area("Enter your post text", value=DEFAULT_TEXT)
font_size = st.slider("Font Size", min_value=20, max_value=150, value=50)
text_color = st.color_picker("Text Color", value="#000000")
bg_color = st.color_picker("Background Color", value="#FFFFFF")

# Section: Font Preview
st.subheader("Font Preview")
if available_fonts:
    font_preview = Image.new("RGB", (500, 150), color=(255, 255, 255))
    preview_draw = ImageDraw.Draw(font_preview)
    try:
        preview_font_path = os.path.join(FONT_DIR, selected_font)
        preview_font = ImageFont.truetype(preview_font_path, 40)
        preview_draw.text((10, 50), "Font Preview", font=preview_font, fill=(0, 0, 0))
    except Exception as e:
        st.error(f"Error loading preview font: {e}")
    st.image(font_preview, caption=f"Preview of {selected_font}")

# Section: Generate Image
st.subheader("Generated Image")
if st.button("Generate Image"):
    if not text_input.strip():
        st.warning("Please enter some text.")
    elif selected_font:
        img = generate_image(text_input, selected_font, font_size, text_color, bg_color)
        if img:
            st.image(img, caption="Generated Instagram Post")
            img.save("output/instagram_post.png")  # Save the image for future use

st.subheader("Generated AI Image")
if st.button("Generate AI Post"):
    try:
        # Fetch latest release
        title, content = fetch_github_releases(repo)
        if title and content:
            st.write(f"**Title:** {title}")
            st.write(f"**Content:** {content}")

            # Summarize content
            summarized = summarize_content(content)
            st.write(f"**Summarized Content:** {summarized}")

            # Generate image
            # image_path = generate_image(summarized, title)
            image_path = generate_image(summarized, selected_font, font_size, text_color, bg_color)
            if image_path:
                st.image(image_path, caption="Generated Instagram Post")
            else:
                st.error("Failed to generate the image.")
        else:
            st.error("No releases found or an error occurred.")
    except Exception as e:
        logging.error(f"Error generating post: {e}")
        st.error("An unexpected error occurred. Check logs for details.")

# Instructions for adding fonts
st.sidebar.title("Instructions")
st.sidebar.write("1. Add `.ttf` font files to the `fonts/` directory.")
st.sidebar.write("2. Reload the app to see new fonts.")
st.sidebar.write("3. Customize text, font, and colors to create your post.")

