import zipfile
import time
from pathlib import Path
from collections import defaultdict

from models.sentence import Sentence
from models.occurrence import Occurrence


def normalize_text(text: str) -> str:
    """
    Basic normalization:
    - lowercase
    - remove extra spaces
    """
    return " ".join(text.lower().split())


def read_archive(archive_path: str) -> list[Sentence]:
    archive = Path(archive_path)

    if not archive.exists():
        raise FileNotFoundError(
            f"Archive not found: {archive_path}"
        )

    if not zipfile.is_zipfile(archive):
        raise ValueError(
            f"The file is not a valid ZIP archive: {archive_path}"
        )

    print(f"Opening archive: {archive_path}")

    sentences: list[Sentence] = []

    current_id = 1

    with zipfile.ZipFile(archive, "r") as zip_file:

        for file_info in zip_file.infolist():

            if file_info.is_dir():
                continue

            if not file_info.filename.lower().endswith(".txt"):
                continue

            with zip_file.open(file_info) as file:

                content = file.read().decode(
                    "utf-8",
                    errors="ignore"
                )

                lines = content.splitlines()

                for line_number, line in enumerate(lines, start=1):

                    if not line.strip():
                        continue

                    normalized = normalize_text(line)

                    sentence = Sentence(
                        id=current_id,
                        text=line,
                        normalized_text=normalized,
                        tokens=normalized.split(),
                        file_path=file_info.filename,
                        line_number=line_number
                    )

                    sentences.append(sentence)

                    current_id += 1

    return sentences


def build_word_index(
    sentences: list[Sentence]
) -> dict[str, list[Occurrence]]:

    print("\nBuilding word index...")

    word_index = defaultdict(list)

    total_sentences = len(sentences)

    # זמן של כל בניית האינדקס
    total_start = time.perf_counter()

    # זמן של הבלוק הנוכחי של 100,000
    batch_start = time.perf_counter()

    for index, sentence in enumerate(sentences, start=1):

        for position, word in enumerate(sentence.tokens):

            word_index[word].append(
                Occurrence(
                    sentence_id=sentence.id,
                    position=position
                )
            )

        if index % 100_000 == 0:

            now = time.perf_counter()

            batch_time = now - batch_start
            total_time = now - total_start

            print(
                f"Indexed {index:,} / {total_sentences:,} | "
                f"Last 100,000: {batch_time:.2f}s | "
                f"Total: {total_time:.2f}s"
            )

            # מתחילים למדוד את ה-100,000 הבאים
            batch_start = time.perf_counter()

    return dict(word_index)


if __name__ == "__main__":

    # =============================
    # Total timer
    # =============================

    total_start = time.perf_counter()


    # =============================
    # Stage 1 - Read archive
    # =============================

    read_start = time.perf_counter()

    sentences = read_archive(
        "data/Archive.zip"
    )

    read_end = time.perf_counter()

    read_time = read_end - read_start


    print()
    print("Finished reading archive")
    print(
        f"Total sentences: "
        f"{len(sentences):,}"
    )

    print(
        f"Archive reading time: "
        f"{read_time:.2f} seconds"
    )


    # =============================
    # Stage 2 - Build word index
    # =============================

    index_start = time.perf_counter()

    word_index = build_word_index(
        sentences
    )

    index_end = time.perf_counter()

    index_time = index_end - index_start


    # =============================
    # Total time
    # =============================

    total_end = time.perf_counter()

    total_time = total_end - total_start


    print("\n--- Performance ---")

    print(
        f"Reading time: "
        f"{read_time:.2f} seconds"
    )

    print(
        f"Index building time: "
        f"{index_time:.2f} seconds"
    )

    print(
        f"Total time: "
        f"{total_time:.2f} seconds"
    )

    print(
        f"Unique words: "
        f"{len(word_index):,}"
    )


    # =============================
    # Test the index
    # =============================

    test_word = "networking"

    occurrences = word_index.get(
        test_word,
        []
    )

    print(
        f"\n'{test_word}' appears "
        f"{len(occurrences):,} times"
    )

    print("\nFirst 5 occurrences:")

    for occurrence in occurrences[:5]:

        # sentence IDs start from 1,
        # list indexes start from 0
        sentence = sentences[
            occurrence.sentence_id - 1
        ]

        print(
            f"Sentence ID: "
            f"{occurrence.sentence_id} | "
            f"Position: "
            f"{occurrence.position} | "
            f"Text: "
            f"{sentence.text}"
        )