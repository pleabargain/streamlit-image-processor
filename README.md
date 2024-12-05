# Streamlit Image Text Extractor

github:
https://github.com/pleabargain/streamlit-image-processor


streamlit:
https://pleabargain-streamlit-image-processor-app-fncmav.streamlit.app/


video:
https://www.youtube.com/watch?v=-eGwRqlEtCc

# motivation
Few people like working with receipts so I thought I'd make a simple tool to help with that.


A powerful web application built with Streamlit and EasyOCR that allows users to extract text from images. Upload single or multiple images and get the extracted text in downloadable format.

## 🌟 Features

- 📤 Upload multiple images simultaneously
- 📝 Extract text from images using EasyOCR
- 💾 Automatically save extracted text to files
- ⬇️ Download extracted text files
- 👀 Preview images and extracted text side by side
- 🎯 Support for PNG, JPG, and JPEG formats
- 🚀 User-friendly interface
- 📱 Responsive layout

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/streamlit-image-processor.git
cd streamlit-image-processor
```

2. Create a virtual environment (recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided URL (typically http://localhost:8501)

3. Upload images using the file uploader:
   - Click "Browse files" or drag and drop images
   - Select one or multiple images
   - Supported formats: PNG, JPG, JPEG

4. View results:
   - See the uploaded image and extracted text side by side
   - Download text files for each processed image
   - Find saved text files in the `output` directory

## 📁 Project Structure

```
streamlit-image-processor/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── LICENSE            # MIT License
├── README.md          # Project documentation
├── .gitignore         # Git ignore file
└── output/            # Directory for saved text files
```

## ⚙️ Technical Details

- **Streamlit**: Provides the web interface and file handling
- **EasyOCR**: Powers the text extraction from images
- **PIL**: Handles image processing and manipulation
- **Python 3.6+**: Required for running the application

## 🔍 Notes

- First run may take longer as EasyOCR downloads necessary language models
- Currently supports English text extraction
- Processing time depends on image size and complexity
- Text files are saved with the format: `original_filename_output.txt`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🔮 Future Improvements

- [ ] Add support for more languages
- [ ] Implement batch processing options
- [ ] Add image preprocessing options
- [ ] Support for more image formats
- [ ] Export results in different formats (PDF, DOCX)
- [ ] Add progress tracking for multiple files
