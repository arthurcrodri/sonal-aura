# 🎵 Sonal Aura

> **A Hybrid AI Audio Engineering Assistant** > *Combining Digital Signal Processing (DSP) with Large Language Models for professional mixing feedback.*

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green)
![License](https://img.shields.io/badge/License-MIT-purple)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow)

## 📖 Overview

**Sonal Aura** is an open-source API designed to help musicians and producers improve their tracks. Unlike standard "AI Wrappers" that blindly send expensive audio files to an API, Sonal Aura uses a **cost-effective, hybrid architecture**:

1.  **The "Ears" (Local DSP):** It uses Python libraries (`librosa`, `pyloudnorm`) to perform a detailed technical analysis of the audio locally (Loudness, EQ, Stereo Image, Key).
2.  **The "Brain" (LLM):** It sends a lightweight JSON report of that data to an LLM (Google Gemini), which acts as a virtual mixing engineer to provide warm, actionable, and human-readable feedback.

This approach reduces API costs by over **99%** compared to multimodal audio processing, while maintaining high precision.

## ✨ Key Features

* **📊 Technical Analysis:**
    * **Dynamics:** Integrated LUFS measurement (industry standard for loudness).
    * **Spectral Profile:** Brightness centroid and high-frequency rolloff analysis.
    * **Stereo Imaging:** Phase correlation and width detection.
    * **Tonality:** Automatic key and scale detection.
* **🤖 AI Feedback (Coming Soon):** Translates raw technical data into advice (e.g., *"Your track is hitting -9 LUFS but lacks stereo width. Try panning your hi-hats..."*).
* **🚀 High-Performance API:** Built with **FastAPI** for asynchronous file handling.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **API Framework:** FastAPI & Uvicorn
* **Audio Processing (DSP):** Librosa, Pyloudnorm, Pydub, NumPy
* **AI/LLM:** Google Gemini API (`google-generativeai`)
* **Utilities:** Python-Dotenv (Security)

## 📂 Project Structure

This project follows a layered architecture to separate concerns between the API interface and the core business logic.

```text
Sonal-Aura/
├── sonal_aura/             # Core Application Logic
│   ├── __init__.py
│   └── analysis.py         # DSP Logic (The "Ears")
├── .env                    # Environment variables (API Keys) - NOT IN GIT
├── .gitignore              # Git ignore rules
├── main.py                 # FastAPI Entry Point (The API Layer)
├── requirements.txt        # Project Dependencies
└── README.md               # Documentation
```

## 🚀 Getting Started

##### Prerequisites

- Python 3.10 or higher
- ffmpeg installed on your system (required by pydub for handling mp3/m4a files).

##### Installation

1. Clone the repository:
```bash
git clone [https://github.com/YOUR_USERNAME/sonal-aura.git](https://github.com/YOUR_USERNAME/sonal-aura.git)
cd sonal-aura
```

2. Create and activate a virtual environment:

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up Environment Variables: Create a .env file in the root directory and add your Google API Key:

```ini
GOOGLE_API_KEY="your_google_api_key_here"
```

##### Running the Server

Start the FastAPI server using Uvicorn:

```bash
python main.py
```

The API will be available at http://127.0.0.1:8000.

## 🧪 Usage

Sonal Aura comes with automatic interactive documentation.

1. Run the server.
2. Open your browser to http://127.0.0.1:8000/docs.
3. Use the /analyze endpoint.
4. Upload an audio file (.mp3 or .wav) and click Execute.
5. The API will return a detailed JSON object with the track's technical profile.

## 🗺️ Roadmap

- [x] Phase 1: Architecture Setup (FastAPI skeleton, Environment security)
- [x] Phase 2: The "Ears" (DSP Analysis pipeline with Librosa)
- [ ] Phase 3: The "Brain" (Integration with Gemini API for text feedback)
- [ ] Phase 4: Frontend (Simple UI using Streamlit)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.
