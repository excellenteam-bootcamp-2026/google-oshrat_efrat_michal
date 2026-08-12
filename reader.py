import zipfile
import re
import time
from collections import defaultdict
from models.sentence import Sentence

def normalize_text(text: str) -> str:
    """Rend le texte en minuscules et conserve uniquement les caractères alphanumériques et espaces."""
    text = text.lower()
    # Conserve lettres, chiffres et espaces
    return re.sub(r'[^a-z0-9\s]', '', text)

def load_corpus_from_zip(zip_path: str) -> dict[str, list[Sentence]]:
    """Lit les fichiers texte dans Archive.zip et construit l'index simple mot -> [Sentence]."""
    word_to_sentences = defaultdict(list)
    sentence_id_counter = 0

    print("Début de la lecture et de l'indexation du zip...")
    start_time = time.time()

    with zipfile.ZipFile(zip_path, 'r') as z:
        for file_info in z.infolist():
            # On ne traite que les fichiers texte .txt
            if file_info.is_dir() or not file_info.filename.endswith('.txt'):
                continue
            
            with z.open(file_info) as f:
                for line_num, raw_line in enumerate(f, start=1):
                    # Décodage avec gestion des caractères spéciaux
                    line_str = raw_line.decode('utf-8', errors='ignore').strip()
                    if not line_str:
                        continue

                    normalized = normalize_text(line_str)
                    tokens = normalized.split()

                    sentence = Sentence(
                        id=sentence_id_counter,
                        text=line_str,
                        normalized_text=normalized,
                        tokens=tokens,
                        file_path=file_info.filename,
                        line_number=line_num
                    )
                    sentence_id_counter += 1

                    # Indexation simple : chaque mot pointe vers cette phrase
                    # Utilisation d'un set pour éviter d'ajouter la même phrase plusieurs fois si un mot y est répété
                    unique_tokens = set(tokens)
                    for token in unique_tokens:
                        word_to_sentences[token].append(sentence)

    elapsed_time = time.time() - start_time
    print(f"Indexation terminée en {elapsed_time:.2f} secondes.")
    print(f"Total de phrases indexées : {sentence_id_counter}")
    print(f"Total de mots uniques dans l'index : {len(word_to_sentences)}")

    return word_to_sentences
