import time
from reader import load_corpus_from_zip

ZIP_PATH = "data/Archive.zip"

def main():
    # --- PHASE 1: OFFLINE (Chargement et Indexation) ---
    index = load_corpus_from_zip(ZIP_PATH)
    
    print("\n" + "="*50)
    print("Système d'autocomplétion prêt (Version Naïve PoC)")
    print("Tapez un mot puis appuyez sur Entrée.")
    print("Pour réinitialiser/quitter la recherche sur un mot, tapez '#'.")
    print("="*50 + "\n")

    # --- PHASE 2: ONLINE (Interactions utilisateur) ---
    while True:
        query = input("Entrez votre recherche > ").strip()
        
        if query == "#":
            print("Fin de la session.")
            break
        
        if not query:
            continue

        normalized_query = query.lower()

        # Mesure du temps de recherche
        search_start = time.time()
        results = index.get(normalized_query, [])
        search_time = (time.time() - search_start) * 1000 # Converti en ms

        # Récupération des 5 premiers résultats
        top_5 = results[:5]

        print(f"\n[Temps de recherche: {search_time:.4f} ms | Résultats trouvés: {len(results)}]")
        print("Top 5 des propositions :")
        for idx, sentence in enumerate(top_5, start=1):
            print(f"  {idx}. {sentence.text} (Fichier: {sentence.file_path}, Ligne: {sentence.line_number})")
        print("-" * 50)

if __name__ == "__main__":
    main()
