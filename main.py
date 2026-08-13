import time

from archive_reader.reader import build_corpus
from search_logic.autocomplete_service import AutocompleteService


ARCHIVE_PATH = "data/Archive.zip"


def main() -> None:
    corpus = build_corpus(ARCHIVE_PATH)
    autocomplete = AutocompleteService(corpus)

    current_query = ""

    print("\nAutocomplete is ready.")
    print("Type text and press Enter to search.")
    print("Type # to start a new sentence.")
    print("Type ## to exit.\n")

    while True:
        if current_query:
            print(f"Current text: {current_query}")

        new_text = input("Type more > ")

        # סוגר את התוכנית
        if new_text.strip() == "##":
            print("Autocomplete closed.")
            break

        # מאפס את המשפט ומתחיל חיפוש חדש
        if new_text.strip() == "#":
            current_query = ""
            print("\nStarted a new sentence.\n")
            continue

        if not new_text:
            continue

        # מוסיפים את הטקסט החדש למה שכבר הוקלד
        current_query = f"{current_query} {new_text.strip()}".strip()

        search_start = time.perf_counter()

        results = autocomplete.search(
            current_query,
            limit=5
        )

        search_time = time.perf_counter() - search_start

        print(f"\nSearch text: {current_query}")
        print(f"Search time: {search_time:.6f} seconds")

        if not results:
            print("No completions found.")

        for index, result in enumerate(results, start=1):
            print(
                f"{index}. {result.sentence.text}\n"
                f"   Score: {result.score} | "
                f"Source: {result.sentence.file_path}, "
                f"line {result.sentence.line_number}"
            )

        print()


if __name__ == "__main__":
    main()