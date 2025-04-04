from collections import Counter
from src.prediction_engine.utils.logger import setup_logger  # Assumes you’ve created logger.py

logger = setup_logger()

class Ranker:
    def __init__(self, weights=None):
        self.weights = weights if weights else {"trie": 1.0, "faiss": 1.5, "llm": 2.0}
        logger.info(f"Initialized Ranker with weights: {self.weights}")

    def rank(self, trie_results, faiss_results, llm_results):
        """Merge results from all sources and rank them."""
        logger.info(f"Ranking {len(trie_results)} trie, {len(faiss_results)} faiss, and {len(llm_results)} llm results.")

        all_results = trie_results + faiss_results + llm_results
        scores = Counter()

        for cmd in all_results:
            if cmd in trie_results:
                scores[cmd] += self.weights["trie"]
            if cmd in faiss_results:
                scores[cmd] += self.weights["faiss"]
            if cmd in llm_results:
                scores[cmd] += self.weights["llm"]

        ranked = [cmd for cmd, _ in scores.most_common()]
        logger.info(f"Top ranked suggestions: {ranked[:5]}")
        return ranked
