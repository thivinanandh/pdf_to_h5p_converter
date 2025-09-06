````markdown
# 📄 PDF to H5P Converter

Easily convert your PDF slides into interactive **H5P presentations** for uploading to LMS platforms like **Moodle**, **Canvas**, and **Blackboard**.

## 🚀 Features

- 📝 Converts PDF slides → H5P interactive slides
- 📦 Generates clean, LMS-ready H5P packages
- 🎯 Supports custom DPI and resolution
- 🔗 Compatible with LUMI and other H5P editors
- 💻 Simple Flask-based Web UI & CLI support

## 🛠️ Prerequisites

Before using this project, make sure you have:

- **Python 3.8+**
- **Poppler (pdftoppm)** → for PDF → image conversion

### Installation of Poppler

#### Ubuntu / Debian
```bash
sudo apt-get install poppler-utils
````

#### macOS

```bash
brew install poppler
```

### Required Python Packages

```bash
pip install -r requirements.txt
```

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/thivinanandh/pdf_to_h5p_converter.git
cd pdf_to_h5p_converter
```

## 🧩 Usage

### Option 1 — CLI Mode (Recommended)

Convert a PDF into an H5P file:

```bash
python3 generateh5p.py lecture.pdf
```

With custom DPI & resolution:

```bash
python3 generateh5p.py lecture.pdf --dpi 600 --resolution 1920
```

Default values:

* dpi = 600
* resolution = 1920

The H5P file will be generated in the root folder.

### Option 2 — Web UI Mode 🌐

Run the Flask app locally:

```bash
python3 app.py
```

Then open:

```
http://127.0.0.1:8000
```

Upload your PDF, set DPI & resolution, and download the H5P package.

## ⚠️ Troubleshooting

**Problem:** Can't upload H5P to Moodle or Canvas

**Solution:**

* Open the generated `.h5p` file using **LUMI**
* Save → Upload again ✅

## 🗂️ Folder Structure

```
pdf_to_h5p_converter/
├── app.py                  # Flask Web UI
├── generateh5p.py          # PDF → H5P conversion logic
├── BaseTemplate/           # H5P template
├── contentBase/            # Default content JSON
├── instance/uploads/       # Uploaded PDFs & generated H5Ps
├── static/                 # Bootstrap, JS, and CSS files
├── templates/              # HTML templates (index.html)
└── requirements.txt
```

## 🌍 Deployment

Previously deployed on **Heroku**:

* [https://h5p2pdf.herokuapp.com](https://h5p2pdf.herokuapp.com)

**Note:** Free Heroku hosting has been discontinued. Self-host using Flask or Docker.

## 🛠️ Roadmap

* ➕ Add interactive quizzes in H5P slides
* 🐳 Add Docker support
* 🔗 Enable LMS direct integration
* ⏱️ Real-time PDF → H5P progress tracking

## 🤝 Contributing

Contributions are welcome! Fork, create a branch, make changes, and submit a pull request.

## ⭐ Support

If you find this project useful, please star the repository on GitHub: `thivinanandh/pdf_to_h5p_converter`

```
```
