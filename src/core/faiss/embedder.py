from sentence_transformers import SentenceTransformer
import numpy as np
from src.utils.logger import setup_logger

logger = setup_logger()

class Embedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """Load a pre-trained sentence embedding model."""
        try:
            self.model = SentenceTransformer(model_name)
            logger.info(f"Loaded embedding model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to load model '{model_name}': {e}")
            raise

    def get_embedding(self, text, normalize=True):
        """Get the embedding for a single text input."""
        if not text.strip():
            logger.warning("Empty text provided to get_embedding.")
            return None
        embedding = self.model.encode([text], normalize_embeddings=normalize, convert_to_numpy=True)
        return np.array(embedding[0])

    def get_embeddings(self, texts, normalize=True):
        """Get embeddings for multiple text inputs."""
        if not texts:
            logger.warning("Empty list provided to get_embeddings.")
            return np.array([])
        return np.array(self.model.encode(texts, normalize_embeddings=normalize, convert_to_numpy=True))
