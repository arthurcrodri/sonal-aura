# sonal_aura/analysis.py

import pydub
import librosa
import pyloudnorm as pyln
import numpy as np
import logging
import os

logger = logging.getLogger(__name__)

# Audio analysis function (the "Ears" of Sonal Aura)
def create_audio_report(file_path: str) -> dict:
    """
    Analyzes a given audio file and returns a technical report.
    """

    wav_path = ""       # Initializing wav_path variable

    try:
        # Converting to WAV format
        logger.info(f"Loading audio file: {file_path}")
        audio = pydub.AudioSegment.from_file(file_path)

        # Creating a temporary WAV file path
        wav_path = os.path.join(os.path.dirname(file_path), "temp_analysis.wav")
        audio.export(wav_path, format="wav")
        logger.info(f"Converted to WAV at: {wav_path}")

        # Loading with librosa
        y, sr = librosa.load(wav_path, sr=None, mono=False)
        y_mono = librosa.to_mono(y)

        # Running analyses

        # Dynamics (Loudness)
        meter = pyln.Meter(sr)
        data_for_loudness = y.T if y.ndim > 1 else y
        loudness_lufs = meter.integrated_loudness(data_for_loudness)

        # Spectral (EQ / Frequency)
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y_mono, sr=sr))
        spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=y_mono, sr=sr))

        # Stereo Image
        stereo_report = {}
        if y.ndim > 1:
            correlation = np.corrcoef(y[0], y[1])[0, 1]
            stereo_report = {
                "is_stereo": True,
                "l_r_correlation": round(float(correlation), 3)
            }
        else:
            stereo_report = {
                "is_stereo": False,
                "l_r_correlation": 1.0
            }
        
        # Tonality (Key / Scale)
        chroma = librosa.feature.chroma_stft(y=y_mono, sr=sr)
        key_histogram = np.sum(chroma, axis=1)
        dominant_key_index = np.argmax(key_histogram)
        key_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        dominant_key = key_notes[dominant_key_index]

        # Building the report
        report = {
            "dynamics": {
                "integrated_lufs": round(loudness_lufs, 2)
            },
            "spectral": {
                "brightness_centroid_hz": round(spectral_centroid, 2),
                "high_end_rolloff_hz": round(spectral_rolloff, 2)
            },
            "stereo": stereo_report,
            "tonality": {
                "dominant_key": dominant_key
            }
        }

        return report
    
    except Exception as e:
        logger.error(f"Error during audio analysis: {e}")
        raise Exception(f"Audio analysis failed: {str(e)}")
    
    finally:
        # Cleaning up temporary WAV file
        if os.path.exists(wav_path):
            os.remove(wav_path)
            logger.info(f"Cleaned up temporary WAV file: {wav_path}")