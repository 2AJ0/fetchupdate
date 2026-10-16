import os
import base64
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from openai import OpenAI
from db import get_pet_list, get_pet_profile

# Load environment variables
load_dotenv()

st.set_page_config(page_title="FetchUpdate", page_icon="🐾", layout="centered")
st.title("🐾 FetchUpdate – AI Pet Sitter Assistant")

# Fetch pet list & profile from MongoDB
try:
    pets = get_pet_list()
    pet_options = {pet["name"]: pet["pet_id"] for pet in pets}
    selected_pet_name = st.selectbox("Select Pet Profile", list(pet_options.keys()))
    profile = get_pet_profile(pet_options[selected_pet_name])
except Exception as e:
    st.error(f"MongoDB connection error: {e}")
    st.stop()

# Display selected pet info
st.info(
    f"**Owner:** {profile.get('owner_name')} | "
    f"**Breed:** {profile.get('breed')}\n\n"
    f"**Instructions:** {profile.get('special_instructions')}"
)

uploaded_file = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption=f"Photo of {selected_pet_name}", use_container_width=True)

    if st.button("✨ Generate SMS Update", type="primary"):
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            st.error("OPENROUTER_API_KEY is missing from .env file.")
            st.stop()

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

        # Convert image to Base64
        image_bytes = uploaded_file.getvalue()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        data_url = f"data:image/jpeg;base64,{base64_image}"

        prompt = (
            f"Pet Name: {profile['name']} ({profile['breed']})\n"
            f"Special Instructions: {profile['special_instructions']}\n"
            f"Owner Name: {profile['owner_name']}\n\n"
            "Task: Write a short, friendly, 2-sentence SMS update to the owner describing what the pet is doing in the photo. "
            "Include an emoji. Output ONLY the SMS text."
        )

        with st.spinner("Generating update via Vision Model..."):
            try:
                response = client.chat.completions.create(
                    model="google/gemini-2.5-flash",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": data_url}},
                            ],
                        }
                    ],
                    max_tokens=150
                )
                
                output_text = response.choices[0].message.content
                
                st.success("Update Generated!")
                st.text_area("Ready to send:", value=output_text, height=120, key="sms_output_area")
            except Exception as e:
                st.error(f"Error calling OpenRouter API: {e}")