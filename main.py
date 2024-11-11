import streamlit as st
from elevenlabs import ElevenLabs, play
from few_shot import FewShotPosts
from post_generator import generate_post

# Options for length and language
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]

# ElevenLabs API key and voice ID
API_KEY = "sk_ad250103a293862c41ea0cc893c1c85b5cfb71b178e222ce"
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # Voice ID for "Liam"

# Initialize ElevenLabs client
client = ElevenLabs(api_key=API_KEY)

# Apply custom CSS for styling
st.markdown("""
    <style>
    .main-title {
        font-size: 32px;
        font-weight: bold;
        color: #4F8DF5;
        text-align: center;
    }
    .subheader {
        color: #333333;
        font-size: 22px;
        font-weight: bold;
    }
    .label {
        font-size: 18px;
        color: #666666;
        font-weight: 500;
    }
    .stButton>button {
        background-color: #4F8DF5;
        color: white;
        border-radius: 8px;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #3B72CC;
    }
    </style>
""", unsafe_allow_html=True)

# Main app layout
def main():
    st.markdown("<div class='main-title'>🚀 Twitter Post Generator: CATalysts</div>", unsafe_allow_html=True)
    st.write("")

    # Checkbox to enable/disable voice generation
    enable_voice = st.checkbox("🔊 Enable Voice Generation", value=True)

    # Create a section for dropdowns with a header
    st.markdown("<div class='subheader'>🎛️ Post Customization Options</div>", unsafe_allow_html=True)
    st.write("")

    # Create three columns for the dropdowns
    col1, col2, col3 = st.columns(3)

    fs = FewShotPosts()
    tags = fs.get_tags()

    with col1:
        st.markdown("<div class='label'>📚 Topic</div>", unsafe_allow_html=True)
        selected_tag = st.selectbox("", options=tags, label_visibility="collapsed")

    with col2:
        st.markdown("<div class='label'>📏 Length</div>", unsafe_allow_html=True)
        selected_length = st.selectbox("", options=length_options, label_visibility="collapsed")

    with col3:
        st.markdown("<div class='label'>🌐 Language</div>", unsafe_allow_html=True)
        selected_language = st.selectbox("", options=language_options, label_visibility="collapsed")

    # Generate Button with some spacing
    st.write("")
    if st.button("🎨 Generate Post"):
        # Step 1: Generate the text post
        post = generate_post(selected_length, selected_language, selected_tag)
        st.markdown("<div class='subheader'>📝 Generated Post</div>", unsafe_allow_html=True)
        st.write(post)

        # Step 2: Generate and play the audio if the checkbox is ticked
        if enable_voice:
            try:
                audio = client.generate(
                    text=post,
                    voice=VOICE_ID,
                    model="eleven_multilingual_v2"
                )
                st.write("")
                st.write("🔊 **Playing Generated Voice...**")
                play(audio)  # Plays the audio using ElevenLabs play function
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Run the app
if __name__ == "__main__":
    main()
