import faiss
import numpy as np
import os
import pickle
from sentence_transformers import SentenceTransformer
from src.prediction_engine.utils.logger import setup_logger

logger = setup_logger()

class FaissSearch:
    def __init__(self, commands, index_file="faiss_store/faiss_index.bin", mapping_file="faiss_store/commands.pkl"):
        self.commands = commands

        # Ensure full absolute paths
        self.index_file = os.path.abspath(index_file)
        self.mapping_file = os.path.abspath(mapping_file)

        # Automatically create the directory if it doesn't exist
        os.makedirs(os.path.dirname(self.index_file), exist_ok=True)
        os.makedirs(os.path.dirname(self.mapping_file), exist_ok=True)

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        if os.path.exists(self.index_file) and os.path.exists(self.mapping_file):
            logger.info("Loading existing FAISS index and command mapping...")
            self.index = faiss.read_index(self.index_file)
            with open(self.mapping_file, "rb") as f:
                self.command_map = pickle.load(f)
        else:
            logger.info("Building new FAISS index from command history...")
            self.build_index()
            self.save_index()

    def build_index(self):
        embeddings = np.array(
            self.model.encode(self.commands, normalize_embeddings=True)
        ).astype("float32")

        if embeddings.size == 0:
            raise ValueError("Cannot build FAISS index: No embeddings generated.")

        embedding_dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(embedding_dim)
        self.index.add(embeddings)

        self.command_map = {i: cmd for i, cmd in enumerate(self.commands)}
        logger.info(f"Built FAISS index with {len(self.commands)} commands.")

    def save_index(self):
        faiss.write_index(self.index, self.index_file)
        with open(self.mapping_file, "wb") as f:
            pickle.dump(self.command_map, f)
        logger.info(f"Saved FAISS index to '{self.index_file}' and command map to '{self.mapping_file}'.")

    def search(self, query, top_k=3):
        if not query.strip():
            logger.warning("Empty query received for FAISS search.")
            return []

        query_embedding = np.array(
            self.model.encode([query], normalize_embeddings=True)
        ).astype("float32")

        distances, indices = self.index.search(query_embedding, top_k)
        results = [self.command_map[i] for i in indices[0] if i in self.command_map]
        logger.debug(f"FAISS search for '{query}' returned {len(results)} results.")
        return results
