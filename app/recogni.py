import argparse
import logging
import os
import ujson
import re

from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Tuple
from torch import cuda
from faster_whisper import WhisperModel

from dotenv import load_dotenv
from azure_cosmosdb import CosmosDBUploader

MAGIC_WORD_ROOTS = {
    "obrigado": 0,
    "por favor": 0,
    "desculpa": 0,
    "boa": 0,
    "agradeço": 0,
    "gratidão": 0,
    "sinto muito": 0,
    "perdão": 0,
    "com licença": 0,
}

MAGIC_WORD_PATTERNS = {
    root: re.compile(rf"\b{root}(a|o|as|os)?s?\b") for root in MAGIC_WORD_ROOTS
}

def setup_logging() -> None:
    """Configura o logging para salvar logs em um diretório 'logs'."""
    log_directory = "logs"
    os.makedirs(log_directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(log_directory, f"transcription_{timestamp}.log")

    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logging.getLogger().addHandler(console_handler)


def transcribe_and_analyze(
    audio_path: str, prompt: str, model: WhisperModel, beam_size: int
) -> Tuple[str, dict]:
    """Transcreve um arquivo de áudio e analisa a transcrição."""
    try:
        segments, _ = model.transcribe(
            audio=audio_path, language="pt", beam_size=beam_size, initial_prompt=prompt
        )

        transcription_data_optimized = {
            "prompt": prompt,
            "audio_path": str(audio_path),
            "transcription": [],
            "metrics": {
                "total_words": 0,
                "words_per_minute": 0,
                "top_10_words": [],
                "magic_word_percentages": {},  # Inicializa vazio
            },
        }
        
        total_words = 0
        word_count = Counter()
        total_duration = 0
        
        for root in MAGIC_WORD_ROOTS:
            MAGIC_WORD_ROOTS[root] = 0
        
        # Otimizando o loop de processamento de segmentos
        for id, segment in enumerate(segments):
            segment_text_lower = segment.text.lower()
            words = segment_text_lower.split()
            total_words += len(words)
            word_count.update(words)
            total_duration += segment.end - segment.start
            
            transcription_data_optimized["transcription"].append(
                {
                    "order": id,
                    "start": segment.start,
                    "end": segment.end,
                    "transcription": segment.text,
                }
            )
            
            # Buscar "magic words" usando regex
            for root, pattern in MAGIC_WORD_PATTERNS.items():
                matches = pattern.findall(segment_text_lower)
                MAGIC_WORD_ROOTS[root] += len(matches)

        if total_duration > 0 and total_words > 0:
            transcription_data_optimized["metrics"].update(
                {
                    "total_words": total_words,
                    "words_per_minute": (total_words / total_duration) * 60,
                    "top_10_words": word_count.most_common(10),
                    # Calcula a porcentagem aqui
                    "magic_word_percentages": {
                        root: (count / total_words) * 100
                        for root, count in MAGIC_WORD_ROOTS.items()
                    },
                }
            )

        json_filename = os.path.basename(os.path.splitext(audio_path)[0]) + ".json"
        return json_filename, transcription_data_optimized

    except Exception as e:
        logging.error(f"Erro ao processar arquivo {audio_path}: {e}")
        return None, None


def save_json(filename: str, data: dict) -> None:
    """Salva os dados em um arquivo JSON."""
    json_path = "../json_files"
    os.makedirs(json_path, exist_ok=True)
    json_file = os.path.join(json_path, filename)

    try:
        with open(json_file, "w", encoding="utf-8") as f:
            ujson.dump(data, f, ensure_ascii=False, indent=4)
        logging.info(f"Transcrição e métricas salvas com sucesso em {json_file}")
    except IOError as e:
        logging.error(f"Falha ao salvar arquivo JSON: {e}")


def process_file(audio_file: str, prompt: str, model: WhisperModel, beam_size: int) -> None:
    """Processa um único arquivo de áudio."""
    filename, data = transcribe_and_analyze(audio_file, prompt, model, beam_size)
    if filename and data:
        save_json(filename, data)

if __name__ == "__main__":
    setup_logging()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "audio_path",
        help="Caminho para um arquivo de áudio ou um diretório contendo arquivos de áudio",
    )
    parser.add_argument(
        "--prompt",
        default="Essa é uma transcrição de uma ligação para avaliação de NPS da empresa TOTVS.",
        help="Prompt inicial para ajudar o modelo a transcrever o áudio",
    )
    parser.add_argument(
        "--model_size", default="large-v3", help="Tamanho do modelo Whisper"
    )
    parser.add_argument(
        "--beam_size", default=5, help="Tamanho do beam"
    )
    parser.add_argument(
        "--device",
        default="cuda",
        help="Dispositivo para usar na transcrição (cuda ou cpu)",
    )
    parser.add_argument(
        "--compute_type",
        default="int8_float16",
        help="Tipo de computação para a transcrição (float16 ou int8_float16)",
    )
    args = parser.parse_args()

    # Verifica se a GPU está disponível
    if args.device == "cuda" and not cuda.is_available():
        logging.warning(
            "GPU não encontrada, utilizando CPU. Para usar a GPU, certifique-se de que o PyTorch esteja configurado corretamente."
        )
        args.device = "cpu"
    
    env_path = ".env"
    load_dotenv(env_path)

    audio_path = Path(args.audio_path)
    model = WhisperModel(
        args.model_size, device=args.device, compute_type=args.compute_type
    )

    uploader = CosmosDBUploader(
    os.environ["COSMOS_ENDPOINT"],
    os.environ["COSMOS_KEY"],
    "transcriptions-db",
    "container-result-transcription"
)
    
    if audio_path.is_file():
        process_file(audio_path, str(args.prompt), model, args.beam_size)
    elif audio_path.is_dir():
        audio_files = list(audio_path.glob("*.wav"))
        for audio_file in audio_files:
            process_file(audio_file, str(args.prompt), model, args.beam_size)
    else:
        logging.error(f"Erro: {audio_path} não é um arquivo ou diretório válido.")