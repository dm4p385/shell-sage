import faiss
import numpy as np
import os
import pickle
from sentence_transformers import SentenceTransformer

class FaissSearch:
    def __init__(self, commands, index_file="faiss_index.bin", mapping_file="commands.pkl"):
        self.commands = commands
        self.index_file = index_file
        self.mapping_file = mapping_file
        self.model = SentenceTransformer("all-MiniLM-L6-v2")  # Good balance of speed & accuracy

        if os.path.exists(self.index_file) and os.path.exists(self.mapping_file):
            print("Loading existing FAISS index and command mapping...")
            self.index = faiss.read_index(self.index_file)
            with open(self.mapping_file, "rb") as f:
                self.command_map = pickle.load(f)
        else:
            print("Building new FAISS index...")
            self.build_index()
            self.save_index()

    def build_index(self):
        embeddings = np.array(self.model.encode(self.commands, normalize_embeddings=True)).astype("float32")
        embedding_dim = embeddings.shape[1]  # Get embedding size

        # Create FAISS index with Inner Product
        self.index = faiss.IndexFlatIP(embedding_dim)
        self.index.add(embeddings)  # Add embeddings

        # Store command mapping (to retrieve text from FAISS indices)
        self.command_map = {i: cmd for i, cmd in enumerate(self.commands)}

    def save_index(self):
        """Saves FAISS index and command mapping to disk."""
        faiss.write_index(self.index, self.index_file)
        with open(self.mapping_file, "wb") as f:
            pickle.dump(self.command_map, f)
        print(f"Index and command map saved to {self.index_file} & {self.mapping_file}")

    def search(self, query, top_k=3):
        """Performs semantic search using FAISS."""
        query_embedding = np.array(self.model.encode([query], normalize_embeddings=True)).astype("float32")
        distances, indices = self.index.search(query_embedding, top_k)

        return [self.command_map[i] for i in indices[0] if i in self.command_map]
