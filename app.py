import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API key configuration
GOOGLE_API_KEY = os.getenv("KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not found")
genai.configure(api_key=GOOGLE_API_KEY)

def is_image_related_prompt(prompt):
    # Keywords that suggest the prompt is not about the image
    non_image_keywords = [
        'weather', 'time', 'date', 'news', 'stock', 'price',
        'temperature', 'population', 'distance', 'location',
        'what is your name', 'who are you', 'how old'
    ]
    
    prompt = prompt.lower()
    return not any(keyword in prompt for keyword in non_image_keywords)

def main():
    # Page styling
    st.set_page_config(
        page_title="Image Reader AI",
        page_icon="🖼️",
        layout="centered",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.title("🖼️ Image Reader AI")
    st.markdown("---")
    
    # Sidebar with instructions
    with st.sidebar:
        st.header("📝 Instructions")
        st.info("""
        1. Upload your image
        2. Type your prompt/question about the image content only
        3. Click 'Analyze Image' button
        4. Wait for AI response
        
        Note: Please ask questions only about the image content.
        """)
        
        st.markdown("---")
        st.markdown("Made with ❤️ by Shaheer Ahmad")

    # Main content
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg', 'gif', 'bmp'])
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_container_width=True)
        
        # Text input for prompt
        user_prompt = st.text_area("Enter your prompt or question about the image:", 
                                 placeholder="Example: Describe what's in this image...")
        
        # Process button
        if st.button("🔍 Analyze Image", type="primary"):
            if not user_prompt:
                st.warning("Please enter a prompt or question.")
            elif not is_image_related_prompt(user_prompt):
                st.error("I apologize, but I can only answer questions about the content of the uploaded image. Please ask something about what you can see in the image.")
            else:
                with st.spinner('AI is analyzing your image...'):
                    try:
                        # Load model
                        model = genai.GenerativeModel("gemini-2.0-flash-exp")
                        
                        # Generate response
                        response = model.generate_content([user_prompt, image])
                        
                        # Display response in a nice box
                        st.markdown("### 🤖 AI Response:")
                        st.markdown("""
                        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
                        """ + response.text + """
                        </div>
                        """, unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Only ask questions about what you can see in the image
    - Be specific in your prompts about image content
    - You can ask about objects, colors, text, or context visible in the image
    - The AI will not answer questions unrelated to the image
    """)

if __name__ == "__main__":
    main() 