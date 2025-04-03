from collections import Counter


class Ranker:
    def __init__(self, weights=None):
        self.weights = weights if weights else {"trie": 1.0, "faiss": 1.5, "llm": 2.0}

    def rank(self, trie_results, faiss_results, llm_results):
        """Merge results from all sources and rank them."""
        all_results = trie_results + faiss_results + llm_results
        scores = Counter()

        for cmd in all_results:
            if cmd in trie_results:
                scores[cmd] += self.weights["trie"]
            if cmd in faiss_results:
                scores[cmd] += self.weights["faiss"]
            if cmd in llm_results:
                scores[cmd] += self.weights["llm"]

        return [cmd for cmd, _ in scores.most_common()]
