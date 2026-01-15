"""
Audio preprocessing utilities for the Flask demo application.

This module handles format conversion, resampling, and normalization
for all incoming audio files (uploaded or recorded).

All audio is normalized to:
- Sample rate: 22050 Hz
- Channels: Mono
- Format: PCM-16 WAV
"""

import os
import tempfile
import warnings
from pathlib import Path
from typing import Tuple

import librosa
import soundfile as sf


# Audio processing constants (match feature extraction pipeline)
TARGET_SAMPLE_RATE = 22050
MAX_DURATION_SECONDS = 60 * 10 
MAX_FILE_SIZE_MB = 50  


class AudioValidationError(Exception):
    """Raised when audio file validation fails."""
    pass


def normalize_audio_file(input_path: str) -> Tuple[str, dict]:
    """
    Normalize any audio file to standard format for inference.
    
    Accepts any format supported by librosa (WAV, MP3, FLAC, WebM, Opus, etc.)
    and converts to mono PCM-16 WAV at 22050 Hz sample rate.
    
    Args:
        input_path: Path to input audio file (any format)
        
    Returns:
        Tuple of (normalized_wav_path, audio_info_dict)
        
    Raises:
        AudioValidationError: If audio is invalid, corrupt, or exceeds limits
    """
    # Validate file size
    file_size_mb = os.path.getsize(input_path) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        raise AudioValidationError(
            f"File size ({file_size_mb:.1f} MB) exceeds limit of {MAX_FILE_SIZE_MB} MB"
        )
    
    try:
        # Load audio with librosa (handles format conversion automatically)
        # Note: When loading non-WAV formats (WebM, MP3, etc.), librosa may emit
        # warnings about PySoundFile fallback. This is expected - the output will
        # always be normalized to PCM-16 WAV regardless of input format.
        # sr=TARGET_SAMPLE_RATE forces resampling
        # mono=True converts to mono
        # duration limits memory usage
        with warnings.catch_warnings():
            # Suppress expected warnings when decoding non-WAV formats
            warnings.filterwarnings("ignore", category=UserWarning, module="librosa")
            warnings.filterwarnings("ignore", category=FutureWarning, module="librosa")
            
            audio_data, sample_rate = librosa.load(
                input_path,
                sr=TARGET_SAMPLE_RATE,
                mono=True,
                duration=MAX_DURATION_SECONDS + 1  # Load slightly more to check limit
            )
        
    except Exception as e:
        raise AudioValidationError(
            f"Failed to decode audio file. The file may be corrupt or in an unsupported format. Error: {e}"
        )
    
    # Validate duration
    duration_seconds = len(audio_data) / sample_rate
    if duration_seconds > MAX_DURATION_SECONDS:
        raise AudioValidationError(
            f"Audio duration ({duration_seconds:.1f}s) exceeds limit of {MAX_DURATION_SECONDS}s"
        )
    
    # Validate audio has content
    if len(audio_data) == 0:
        raise AudioValidationError("Audio file is empty or has no samples")
    
    # Check for silent audio (all samples near zero)
    if abs(audio_data).max() < 0.001:
        raise AudioValidationError("Audio appears to be silent or has extremely low volume")
    
    # Create temporary WAV file for normalized audio
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        normalized_path = tmp.name
    
    try:
        # Write normalized audio as PCM-16 WAV
        # This ensures feature extraction ALWAYS receives a standard WAV file,
        # regardless of the original upload format (WebM, MP3, etc.)
        sf.write(
            normalized_path,
            audio_data,
            sample_rate,
            subtype='PCM_16'
        )
        
    except Exception as e:
        # Clean up temp file on error
        if os.path.exists(normalized_path):
            os.unlink(normalized_path)
        raise AudioValidationError(f"Failed to write normalized audio: {e}")
    
    # Return path and metadata
    audio_info = {
        "duration_seconds": duration_seconds,
        "sample_rate": sample_rate,
        "channels": 1,
        "format": "PCM-16 WAV",
        "samples": len(audio_data),
    }
    
    return normalized_path, audio_info


def cleanup_audio_file(file_path: str | None) -> None:
    """
    Safely delete a temporary audio file.
    
    Args:
        file_path: Path to file to delete (can be None)
    """
    if file_path and os.path.exists(file_path):
        try:
            os.unlink(file_path)
        except Exception:
            # Silently ignore cleanup errors
            pass
