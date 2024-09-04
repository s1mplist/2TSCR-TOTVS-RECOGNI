# %%
#from ctranslate2 import converters
#converters.TransformersConverter(model_name_or_path='openai/whisper-large-v3',copy_files=['tokenizer.json', 'preprocessor_config.json']).convert(output_dir='whisper-large-v3-ct2', quantization='float16')

# %%
from collections import Counter
from faster_whisper import WhisperModel

# %%
contexto = "Essa é uma transcrição de uma ligação para avialiação de NPS da empresa TOTVS."
audio_path="audio_samples/2874774.wav"

# %%
model_size = "large-v3"
model = WhisperModel(model_size, device="cuda", compute_type="float16")

# %%
# Transcrição do áudio
segments, info = model.transcribe(audio=audio_path,
                                  language='pt',
                                  beam_size=5,
                                  initial_prompt=contexto
                                  )

# %%
# Inicializando variáveis para métricas
total_words = 0
word_count = Counter()
magic_words = ["obrigado", "obrigada", "por favor", "desculpa", "desculpe", 
               "por gentileza", "bom dia", "boa tarde", "boa noite", 
               "agradeço", "agradece", "gratidão", "sinto muito", 
               "perdão", "me perdoe", "com licença"]
magic_word_count = Counter({word: 0 for word in magic_words})
total_duration = 0

# %%
# Processando a transcrição para calcular métricas
for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

    # Dividindo o texto em palavras e convertendo para minúsculas
    words = segment.text.lower().split()
    total_words += len(words)
    word_count.update(words)

    # Contabilizando palavras mágicas
    for word in magic_words:
        magic_word_count[word] += words.count(word)

    # Calculando duração total do áudio em segundos
    total_duration += (segment.end - segment.start)

# %%
# Calculando métricas finais
words_per_minute = (total_words / total_duration) * 60 if total_duration > 0 else 0
sorted_word_count = word_count.most_common()
magic_word_percentages = {word: (count / total_words) * 100 for word, count in magic_word_count.items() if total_words > 0}

# Exibindo as métricas
print("Métricas:")
print(f"\nQuantidade total de palavras: {total_words}")

print(f"\nQuantidade de palavras por minuto: {words_per_minute:.2f}")

print("\nTop 10 palavras mais faladas:")
for word, count in sorted_word_count[:10]:
    print(f"{word}: {count}")

print("\nPercentual de palavras mágicas:")
for word, percentage in magic_word_percentages.items():
    print(f"{word}: {percentage:.2f}%")


