from sentence_transformers import SentenceTransformer
import numpy as np

class Embedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """Load a pre-trained sentence embedding model."""
        self.model = SentenceTransformer(model_name)

    def get_embedding(self, text):
        """Get the embedding for a single text input."""
        return np.array(self.model.encode([text], convert_to_numpy=True))

    def get_embeddings(self, texts):
        """Get embeddings for multiple text inputs."""
        return np.array(self.model.encode(texts, convert_to_numpy=True))
