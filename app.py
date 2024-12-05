import streamlit as st
import easyocr
import os
from PIL import Image
import io
import logging
from datetime import datetime
import sys
from pathlib import Path

# Configure logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Create logger
logger = logging.getLogger('ImageTextExtractor')
logger.setLevel(logging.DEBUG)

# Prevent duplicate logs
if logger.hasHandlers():
    logger.handlers.clear()

# Create handlers
file_handler = logging.FileHandler(log_file)
stream_handler = logging.StreamHandler(sys.stdout)

# Create formatters and add it to handlers
log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(log_format)
stream_handler.setFormatter(log_format)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Page configuration
st.set_page_config(
    page_title="Image Text Extractor",
    page_icon="📝",
    layout="wide"
)

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

# Initialize session state for edited text
if 'edited_texts' not in st.session_state:
    st.session_state.edited_texts = {}

def process_image(image_bytes, filename):
    """
    Process a single image and return extracted text
    """
    try:
        logger.info(f"Processing image: {filename}")
        
        # Initialize reader (only done once if already initialized)
        if 'reader' not in st.session_state:
            logger.info("Initializing EasyOCR reader")
            with st.spinner('Initializing EasyOCR... This may take a moment the first time.'):
                st.session_state.reader = easyocr.Reader(['en'])
        
        # Read image
        logger.debug("Performing OCR on image")
        results = st.session_state.reader.readtext(image_bytes)
        
        # Extract text
        text = '\n'.join([result[1] for result in results])
        logger.info(f"Successfully extracted text from {filename}")
        
        # Save to file
        output_filename = f"output/{os.path.splitext(filename)[0]}_output.txt"
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(text)
        logger.info(f"Saved extracted text to {output_filename}")
        
        return text, output_filename
    except Exception as e:
        logger.error(f"Error processing {filename}: {str(e)}", exc_info=True)
        st.error(f"Error processing {filename}: {str(e)}")
        return None, None

def save_edited_text(text, output_file):
    """
    Save edited text to file and return success status
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        logger.info(f"Saved edited text to {output_file}")
        return True
    except Exception as e:
        logger.error(f"Error saving changes to {output_file}: {str(e)}", exc_info=True)
        return False

def show_ocr_tab():
    st.title("📝 Image Text Extractor")
    st.write("Upload one or more images to extract text using EasyOCR")
    
    # Sample images section
    st.subheader("Sample Images")
    try:
        sample_images = [f for f in os.listdir("sample_images") if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if sample_images:
            logger.info(f"Found {len(sample_images)} sample images")
            st.write("Try these sample images:")
            cols = st.columns(len(sample_images))
            for idx, sample in enumerate(sample_images):
                with cols[idx]:
                    sample_path = os.path.join("sample_images", sample)
                    try:
                        image = Image.open(sample_path)
                        st.image(image, caption=sample, use_container_width=True)
                        with open(sample_path, "rb") as f:
                            st.download_button(
                                label="Use this image",
                                data=f.read(),
                                file_name=sample,
                                mime=f"image/{sample.split('.')[-1].lower()}",
                                key=f"sample_download_{idx}"
                            )
                    except Exception as e:
                        logger.error(f"Error loading sample image {sample}: {str(e)}", exc_info=True)
                        st.error(f"Error loading sample image {sample}")
    except Exception as e:
        logger.error(f"Error accessing sample images: {str(e)}", exc_info=True)
        st.error("Error loading sample images directory")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Choose image files",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        key="file_uploader"
    )
    
    if uploaded_files:
        logger.info(f"Processing {len(uploaded_files)} uploaded files")
        st.write("---")
        st.write(f"Processing {len(uploaded_files)} file(s)...")
        
        # Create columns for better layout
        for idx, uploaded_file in enumerate(uploaded_files):
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader(f"Image: {uploaded_file.name}")
                try:
                    image = Image.open(uploaded_file)
                    st.image(image, use_container_width=True)
                except Exception as e:
                    logger.error(f"Error displaying image {uploaded_file.name}: {str(e)}", exc_info=True)
                    st.error(f"Error displaying image {uploaded_file.name}")
            
            with col2:
                st.subheader("Extracted Text")
                with st.spinner('Extracting text...'):
                    try:
                        # Convert image to bytes
                        img_byte_arr = io.BytesIO()
                        image.save(img_byte_arr, format=image.format)
                        img_byte_arr = img_byte_arr.getvalue()
                        
                        # Process image and get results
                        text, output_file = process_image(img_byte_arr, uploaded_file.name)
                        
                        if text and output_file:
                            st.success(f"Text saved to: {output_file}")
                            
                            # Create a unique key for this text
                            text_key = f"text_{uploaded_file.name}_{idx}"
                            
                            # Initialize session state for this text if not exists
                            if text_key not in st.session_state.edited_texts:
                                st.session_state.edited_texts[text_key] = text
                            
                            # Create columns for edit area and buttons
                            edit_col, button_col = st.columns([3, 1])
                            
                            with edit_col:
                                # Editable text area
                                edited_text = st.text_area(
                                    "Edit extracted text:",
                                    value=st.session_state.edited_texts[text_key],
                                    height=300,
                                    key=f"edit_{text_key}"
                                )
                                
                                # Update session state with edited text
                                st.session_state.edited_texts[text_key] = edited_text
                            
                            with button_col:
                                st.write("")  # Add some spacing
                                st.write("")  # Add some spacing
                                
                                # Save button
                                if st.button("💾 Save Changes", key=f"save_{idx}"):
                                    if save_edited_text(edited_text, output_file):
                                        st.success("Changes saved!")
                                    else:
                                        st.error("Failed to save changes")
                                
                                st.write("")  # Add some spacing
                                
                                # Download button
                                st.download_button(
                                    label="⬇️ Download Text",
                                    data=edited_text,
                                    file_name=os.path.basename(output_file),
                                    mime="text/plain",
                                    key=f"download_{idx}"
                                )
                            
                    except Exception as e:
                        logger.error(f"Error processing {uploaded_file.name}: {str(e)}", exc_info=True)
                        st.error(f"Error processing {uploaded_file.name}: {str(e)}")
            
            st.write("---")
    
    else:
        # Instructions
        st.info("👆 Upload one or more image files to begin processing")
        
        st.header("Instructions")
        st.markdown("""
        1. Click the 'Browse files' button above or drag and drop image files
        2. Supported formats: PNG, JPG, JPEG
        3. You can upload multiple files at once
        4. Each image will be processed and text will be extracted
        5. Edit the extracted text if needed
        6. Click 'Save Changes' to update the saved file
        7. Click 'Download Text' to download your changes
        """)

def show_output_tab():
    st.title("📁 Output Files")
    
    if not os.path.exists("output"):
        logger.warning("Output directory not found")
        st.warning("No output directory found. Process some images first!")
        return
        
    output_files = [f for f in os.listdir("output") if f.endswith(".txt")]
    
    if not output_files:
        logger.info("No output files found")
        st.info("No output files yet. Process some images to see results here!")
        return
        
    logger.info(f"Displaying {len(output_files)} output files")
    for idx, file in enumerate(output_files):
        with st.expander(f"📄 {file}"):
            try:
                # Create a unique key for this file
                file_key = f"output_{file}_{idx}"
                
                # Read current content
                with open(os.path.join("output", file), "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Initialize session state for this file if not exists
                if file_key not in st.session_state.edited_texts:
                    st.session_state.edited_texts[file_key] = content
                
                # Create columns for edit area and buttons
                edit_col, button_col = st.columns([3, 1])
                
                with edit_col:
                    # Editable text area
                    edited_content = st.text_area(
                        "Edit content:",
                        value=st.session_state.edited_texts[file_key],
                        height=200,
                        key=f"edit_{file_key}"
                    )
                    
                    # Update session state with edited content
                    st.session_state.edited_texts[file_key] = edited_content
                
                with button_col:
                    st.write("")  # Add some spacing
                    st.write("")  # Add some spacing
                    
                    # Save button
                    if st.button("💾 Save Changes", key=f"save_{file_key}"):
                        if save_edited_text(edited_content, os.path.join("output", file)):
                            st.success("Changes saved!")
                        else:
                            st.error("Failed to save changes")
                    
                    st.write("")  # Add some spacing
                    
                    # Download button
                    st.download_button(
                        label="⬇️ Download Text",
                        data=edited_content,
                        file_name=file,
                        mime="text/plain",
                        key=f"download_{file_key}"
                    )
                    
            except Exception as e:
                logger.error(f"Error reading {file}: {str(e)}", exc_info=True)
                st.error(f"Error reading {file}: {str(e)}")

def show_readme_tab():
    st.title("📚 Documentation")
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            st.markdown(f.read())
    except Exception as e:
        logger.error(f"Error loading README.md: {str(e)}", exc_info=True)
        st.error(f"Error loading README.md: {str(e)}")

def show_source_tab():
    st.title("💻 Source Code")
    
    files = {
        "app.py": "Main application file",
        "requirements.txt": "Project dependencies",
        ".gitignore": "Git ignore rules",
        "LICENSE": "MIT License"
    }
    
    logger.info("Displaying source code files")
    for idx, (filename, description) in enumerate(files.items()):
        with st.expander(f"📄 {filename} - {description}"):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    content = f.read()
                    st.code(content, language="python" if filename.endswith(".py") else "text")
                    st.download_button(
                        label="Download",
                        data=content,
                        file_name=filename,
                        mime="text/plain",
                        key=f"source_download_{idx}"
                    )
            except Exception as e:
                logger.error(f"Error reading {filename}: {str(e)}", exc_info=True)
                st.error(f"Error reading {filename}: {str(e)}")

def show_logs_tab():
    st.title("📊 Application Logs")
    
    try:
        log_files = [f for f in os.listdir(log_dir) if f.endswith('.log')]
        log_files.sort(reverse=True)  # Show newest logs first
        
        if not log_files:
            st.info("No log files available yet.")
            return
            
        # Allow user to select which log file to view
        selected_log = st.selectbox(
            "Select log file:",
            log_files,
            key="log_select"
        )
        
        # Display log file content
        with open(os.path.join(log_dir, selected_log), 'r') as f:
            log_content = f.read()
            
        # Add filters
        log_levels = ['ALL', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        selected_level = st.selectbox(
            "Filter by log level:",
            log_levels,
            key="level_select"
        )
        
        search_term = st.text_input(
            "Search logs:",
            "",
            key="log_search"
        )
        
        # Filter logs based on selection
        filtered_logs = []
        for line in log_content.split('\n'):
            if selected_level != 'ALL' and selected_level not in line:
                continue
            if search_term and search_term.lower() not in line.lower():
                continue
            filtered_logs.append(line)
        
        # Display filtered logs
        st.text_area(
            "Log Content:",
            value='\n'.join(filtered_logs),
            height=400,
            key="log_content"
        )
        
        # Download button for log file
        st.download_button(
            label="Download Log File",
            data=log_content,
            file_name=selected_log,
            mime="text/plain",
            key="log_download"
        )
        
    except Exception as e:
        logger.error(f"Error displaying logs: {str(e)}", exc_info=True)
        st.error(f"Error displaying logs: {str(e)}")

def main():
    logger.info("Starting application")
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 OCR Processing",
        "📚 Documentation",
        "📁 Output Files",
        "💻 Source Code",
        "📊 Logs"
    ])
    
    with tab1:
        show_ocr_tab()
    
    with tab2:
        show_readme_tab()
    
    with tab3:
        show_output_tab()
    
    with tab4:
        show_source_tab()
    
    with tab5:
        show_logs_tab()

if __name__ == "__main__":
    main()
