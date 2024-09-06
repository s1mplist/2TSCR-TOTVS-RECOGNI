import argparse
import json
import logging
import os
import numpy as np
from collections import Counter
from faster_whisper import WhisperModel
from pathlib import Path

def transcribe_and_analyze(audio_path: str,
                            model_size: str = "large-v3",
                            device: str = "cuda",
                            compute_type: str = "float16",
                            magic_words: list[str] = None) -> None:
    """
    This function performs speech transcription and analysis using the Whisper model.

    Args:
        audio_path (str): Path to the audio file (.wav format preferred).
        model_size (str, optional): Whisper model size ("base", "medium", or "large-v3"). 
            Defaults to "large-v3". Larger models offer higher accuracy but require more resources.
        device (str, optional): Device to use for transcription ("cpu" or "cuda"). Defaults to "cuda" 
            if available, leveraging GPU acceleration.
        compute_type (str, optional): Compute type for transcription ("float16" or "float32"). Defaults to "float16" 
            for potential memory savings, but may impact accuracy slightly.
        magic_words (list[str], optional): List of specific words to track their occurrences in the transcription. 
            Defaults to None.
    """
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    contexto = "Essa é uma transcrição de uma ligação para avialiação de NPS da empresa TOTVS."

    try:
        model = WhisperModel(model_size, device=device, compute_type=compute_type)
        segments, _ = model.transcribe(audio=audio_path,
                                       language='pt',
                                       beam_size=5,
                                       initial_prompt=contexto)

        total_words = 0
        total_duration = 0
        word_count = Counter()
        
        magic_words = ["obrigado", "obrigada", "por favor", "desculpa", "desculpe", 
                    "por gentileza", "bom dia", "boa tarde", "boa noite", 
                    "agradeço", "agradece", "gratidão", "sinto muito", 
                    "perdão", "me perdoe", "com licença"]
        magic_word_count = Counter({word: 0 for word in magic_words})
        
        transcription_data_optimized = {
            "prompt": contexto,
            "model": model_size,
            "audio_path": str(audio_path),
            "transcription": [],
            "metrics": {}
        }

        id = 0

        for segment in segments:
            if isinstance(segment.text, str):
                words = np.vectorize(str.lower)(np.array([segment.text])).tolist()
            else:
                words = segment.text.lower().split()
    
            total_words += len(words)
            word_count.update(words)
            magic_word_count.update(set(words) & set(magic_words))
            total_duration += segment.end - segment.start
            transcription_data_optimized["transcription"].append({
                "order": id,
                "start": segment.start,
                "end": segment.end,
                "transcription": segment.text
            })
            id += 1
            
        if total_duration > 0 and total_words > 0:
            words_per_minute = (total_words / total_duration) * 60
            sorted_word_count = word_count.most_common(10) 
            magic_word_percentages = {word: (count / total_words) * 100 for word, count in magic_word_count.items()}
            transcription_data_optimized["metrics"].update({
                "total_words": total_words,
                "words_per_minute": words_per_minute,
                "top_10_words": sorted_word_count,
                "magic_word_percentages": magic_word_percentages,
            })
        else:
            transcription_data_optimized["metrics"].update({
                "total_words": total_words,
                "words_per_minute": 0,
                "top_10_words": [],
                "magic_word_percentages": {word: 0 for word in magic_words},
            })
            
        json_path = 'json_files'
        os.makedirs(json_path, exist_ok=True)

        json_file = os.path.join(json_path, os.path.basename(os.path.splitext(audio_path)[0])) + '.json'

        try:
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(transcription_data_optimized, f, ensure_ascii=False, indent=4, default=lambda o: str(o))
                logging.info(f"Transcription and metrics successfully saved in {json_file}")
        except IOError as e:
             logging.error(f"Failed to save JSON file: {e}")
            
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("audio_path", help="Path to an audio file or a directory containing audio files")
    parser.add_argument("--model_size", default="large-v3", help="Whisper model size")
    parser.add_argument("--device", default="cuda", help="Device to use for transcription")
    parser.add_argument("--compute_type", default="float16", help="Compute type for transcription")
    args = parser.parse_args()

    audio_path = Path(args.audio_path)

    if audio_path.is_file():
        transcribe_and_analyze(audio_path, args.model_size, args.device, args.compute_type)
    elif audio_path.is_dir():
        for audio_file in audio_path.glob("*.wav"):
            transcribe_and_analyze(audio_file, args.model_size, args.device, args.compute_type)
    else:
        logging.error(f"Error: {audio_path} is not a valid file or directory.")