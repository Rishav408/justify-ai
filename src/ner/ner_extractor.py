import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

class NERExtractor:
    def __init__(self, language: str = 'english'):
        self.language = language
        self._ensure_nltk_resources()

    def _safe_download(self, package: str) -> None:
        """Try downloading an NLTK package without crashing startup."""
        try:
            nltk.download(package, quiet=True)
        except Exception:
            # Runtime should keep working even if download fails (offline env, etc.)
            pass

    def _ensure_nltk_resources(self) -> None:
        """Ensure required tokenization/POS/NER resources are present when possible."""
        required_paths = [
            'tokenizers/punkt',
            'taggers/averaged_perceptron_tagger',
            'chunkers/maxent_ne_chunker',
            # Newer NLTK versions may require this extra table resource.
            'chunkers/maxent_ne_chunker_tab',
            'corpora/words',
        ]
        missing = False
        for path in required_paths:
            try:
                nltk.data.find(path)
            except LookupError:
                missing = True

        if not missing:
            return

        for package in [
            'punkt',
            'averaged_perceptron_tagger',
            'maxent_ne_chunker',
            'maxent_ne_chunker_tab',
            'words',
        ]:
            self._safe_download(package)

    def extract_entities(self, text: str) -> list:
        if self.language != 'english':
            # NLTK ne_chunk is primarily trained for English.
            # For low-resource languages, we return empty list in this baseline.
            return []

        try:
            # 1. Tokenize and POS Tag
            tokens = word_tokenize(text)
            tags = pos_tag(tokens)

            # 2. Extract NER Chunks
            chunks = ne_chunk(tags)
        except LookupError:
            # Missing runtime model/resource should not fail the whole API.
            return []
        except Exception:
            # Any unexpected NER parsing issue should degrade gracefully.
            return []

        entities = []
        for chunk in chunks:
            if isinstance(chunk, Tree):
                name = " ".join([token for token, _ in chunk.leaves()])
                label = chunk.label()
                entities.append({"name": name, "type": label})

        return entities

if __name__ == "__main__":
    extractor = NERExtractor('english')
    sample = "Rishav is working at Google in India."
    print("--- NER Discovery Test ---")
    print(extractor.extract_entities(sample))
