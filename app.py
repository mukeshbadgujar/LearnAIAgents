import os
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from services.summarizer import summarize_content
import logging
from config import FONT_DIR, DEFAULT_REPO, IMAGE_SIZE
from services.image_generator import generate_image
from services.fetch_data import fetch_github_releases
from emoji import emojize

# Configure logging
logging.basicConfig(filename="logs/app.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

DEFAULT_TEXT = "Your Daily Tech Update\nPowered by AI!"

# --- Helper Functions ---
def list_available_fonts(font_dir):
    if not os.path.exists(font_dir):
        os.makedirs(font_dir)
    return [f for f in os.listdir(font_dir) if f.endswith(".ttf")]

# Sidebar: Settings for Image Design
st.sidebar.title("Design Your Post")

# Font Selection
available_fonts = list_available_fonts(FONT_DIR)
if not available_fonts:
    st.sidebar.warning("No fonts available. Add `.ttf` font files to the `fonts/` directory.")
    selected_font = None
else:
    selected_font = st.sidebar.selectbox("Choose a font", available_fonts, index=0)

# Text Customization
text_input = st.sidebar.text_area("Enter your post text", value=DEFAULT_TEXT)
font_size = st.sidebar.slider("Font Size", min_value=20, max_value=150, value=50)
text_color = st.sidebar.color_picker("Text Color", value="#000000")
bg_color = st.sidebar.color_picker("Background Color", value="#FFFFFF")

# Background Options
bg_option = st.sidebar.radio("Background Type", ["Solid Color", "Upload Image"])
if bg_option == "Upload Image":
    uploaded_bg = st.sidebar.file_uploader("Upload Background Image (JPG/PNG)", type=["jpg", "png"])
    if uploaded_bg:
        bg_image = Image.open(uploaded_bg).resize(IMAGE_SIZE)
    else:
        bg_image = None
else:
    bg_image = None  # Use solid color background

# Emoji Options
emoji_list = {
    "😀 Smileys & Emotion": ["😀", "😂", "😍", "🥰", "😎", "😭", "🤔"],
    "🎉 Celebration": ["🎉", "✨", "🎂", "🎁", "🥳"],
    "⚽ Sports": ["⚽", "🏀", "🏈", "⚾", "🎾"],
    "🍔 Food": ["🍔", "🍕", "🍣", "🍩", "🍎"],
}
# Select an emoji category
selected_category = st.sidebar.selectbox("Select Emoji Category", list(emoji_list.keys()))
# Select emoji from the chosen category
emoji_input = st.sidebar.selectbox("Choose Emoji", emoji_list[selected_category])
st.sidebar.write(f"Selected Emoji: {emoji_input}")

# emoji_input = st.sidebar.text_input("Enter Emoji(s)", value="😊")
emoji_size = st.sidebar.slider("Emoji Size", min_value=20, max_value=200, value=50)
emoji_x = st.sidebar.slider("Emoji X Position", min_value=0, max_value=IMAGE_SIZE[0], value=IMAGE_SIZE[0] // 2)
emoji_y = st.sidebar.slider("Emoji Y Position", min_value=0, max_value=IMAGE_SIZE[1], value=IMAGE_SIZE[1] // 2)

# Main Section: Real-Time Design Preview
st.title("Dynamic Image Generator for Instagram Posts")
st.write("See your changes in real-time below.")

st.subheader("Real-Time Design Preview")
try:
    if bg_image:
        img = bg_image.copy()
    else:
        img = Image.new("RGB", IMAGE_SIZE, color=bg_color)

    draw = ImageDraw.Draw(img)
    if selected_font:
        font_path = os.path.join(FONT_DIR, selected_font)
        font = ImageFont.truetype(font_path, font_size)

        # Add text
        bbox = draw.multiline_textbbox((0, 0), text_input, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        text_x = (IMAGE_SIZE[0] - text_width) // 2
        text_y = (IMAGE_SIZE[1] - text_height) // 2
        draw.multiline_text((text_x, text_y), text_input, font=font, fill=text_color, align="center")

    # Load an emoji-compatible font for rendering emojis
    emoji_font_path = "./fonts/NotoColorEmoji-Regular.ttf"  # Update to a confirmed compatible font path
    if os.path.exists(emoji_font_path):
        try:
            emoji_font = ImageFont.truetype(emoji_font_path, emoji_size)
            # Add the selected emoji
            draw.text((emoji_x, emoji_y), emoji_input, font=emoji_font, fill="black")
        except Exception as e:
            st.error(f"Error rendering emoji: {e}")
    else:
        st.error("Emoji-compatible font not found. Please check the font path.")

    # Display the generated image
    st.image(img, caption="Real-Time Design Preview", use_container_width=True)

except Exception as e:
    st.error(f"Error generating preview: {e}")

# Buttons for Actions
st.subheader("Actions")
col1, col2 = st.columns(2)

with col1:
    if st.button("Generate Final Image"):
        try:
            img.save("output/instagram_post.png")
            st.success("Image generated and saved successfully!")
            st.image(img, caption="Final Instagram Post")
        except Exception as e:
            st.error(f"Error generating image: {e}")

with col2:
    if st.button("Generate AI Post"):
        try:
            # Fetch latest release
            title, content = fetch_github_releases(DEFAULT_REPO)
            if title and content:
                st.write(f"**Title:** {title}")
                st.write(f"**Content:** {content}")

                # Summarize content
                summarized = summarize_content(content)
                st.write(f"**Summarized Content:** {summarized}")

                # Generate image
                ai_image = generate_image(
                    summarized,
                    selected_font,
                    font_size,
                    text_color,
                    bg_color,
                    emojis=emoji_input,
                    emoji_size=emoji_size,
                    emoji_position=(emoji_x, emoji_y)
                )
                if ai_image:
                    st.image(ai_image, caption="Generated Instagram Post")
                else:
                    st.error("Failed to generate the image.")
            else:
                st.error("No releases found or an error occurred.")
        except Exception as e:
            logging.error(f"Error generating AI post: {e}")
            st.error("An unexpected error occurred. Check logs for details.")

# Sidebar Instructions
st.sidebar.title("Instructions")
st.sidebar.write("1. Add `.ttf` font files to the `fonts/` directory.")
st.sidebar.write("2. Reload the app to see new fonts.")
st.sidebar.write("3. Customize text, background, and emojis to create your post.")


