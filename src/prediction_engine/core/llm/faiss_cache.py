from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import pickle
import os
from src.prediction_engine.utils.logger import setup_logger

logger = setup_logger()


class FaissCache:
    def __init__(self, dim=384, cache_path="llm_cache/cache"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.cache_path = cache_path
        self.index, self.outputs = self._load_cache(dim)

    def _load_cache(self, dim):
        index_path = f"{self.cache_path}.index"
        mapping_path = f"{self.cache_path}.pkl"

        if os.path.exists(index_path) and os.path.exists(mapping_path):
            try:
                index = faiss.read_index(index_path)
                with open(mapping_path, "rb") as f:
                    outputs = pickle.load(f)
                logger.info("Loaded FAISS cache successfully.")
            except Exception as e:
                logger.error(f"Failed to load FAISS cache: {e}")
                index = faiss.IndexFlatIP(dim)
                outputs = []
        else:
            index = faiss.IndexFlatIP(dim)
            outputs = []
            logger.info("No FAISS cache found, initialized fresh.")

        return index, outputs

    def _save_cache(self):
        try:
            os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
            faiss.write_index(self.index, f"{self.cache_path}.index")
            with open(f"{self.cache_path}.pkl", "wb") as f:
                pickle.dump(self.outputs, f)
            logger.info("FAISS cache saved successfully.")
        except Exception as e:
            logger.error(f"Failed to save FAISS cache: {e}")

    def generate_key_embedding(self, query, candidates):
        text = query + " | " + " || ".join(candidates)
        return self.model.encode([text], normalize_embeddings=True)[0]

    def lookup(self, embedding, threshold=0.9):
        if self.index.ntotal == 0:
            logger.debug("Cache is empty, cannot lookup.")
            return None

        D, I = self.index.search(np.array([embedding]), 1)
        logger.debug(f"Lookup score: {D[0][0]:.4f}")

        if D[0][0] >= threshold:
            logger.info("Cache hit.")
            return self.outputs[I[0][0]]

        logger.info("Cache miss.")
        return None

    def add(self, embedding, output):
        self.index.add(np.array([embedding]))
        self.outputs.append(output)
        logger.debug("New entry added to FAISS cache.")

    def save(self):
        self._save_cache()
