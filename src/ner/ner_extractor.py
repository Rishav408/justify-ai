import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

class NERExtractor:
    def __init__(self, language: str = 'english'):
        self.language = language
        # Ensure NLTK resources for NER are available
        try:
            nltk.data.find('chunkers/maxent_ne_chunker')
            nltk.data.find('corpora/words')
        except LookupError:
            nltk.download('maxent_ne_chunker')
            nltk.download('words')

    def extract_entities(self, text: str) -> list:
        if self.language != 'english':
            # NLTK ne_chunk is primarily trained for English.
            # For low-resource languages, we return empty list in this baseline.
            return []
            
        # 1. Tokenize and POS Tag
        tokens = word_tokenize(text)
        tags = pos_tag(tokens)
        
        # 2. Extract NER Chunks
        chunks = ne_chunk(tags)
        
        entities = []
        for chunk in chunks:
            if isinstance(chunk, Tree):
                name = " ".join([token for token, pos in chunk.leaves()])
                label = chunk.label()
                entities.append({"name": name, "type": label})
                
        return entities

if __name__ == "__main__":
    extractor = NERExtractor('english')
    sample = "Rishav is working at Google in India."
    print("--- NER Discovery Test ---")
    print(extractor.extract_entities(sample))
