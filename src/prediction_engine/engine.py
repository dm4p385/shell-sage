import asyncio
import time
from src.prediction_engine.core.trie.trie import TrieSearch
from src.prediction_engine.core.faiss.faiss_search import FaissSearch
from src.prediction_engine.ranking.ranking import Ranker
from src.prediction_engine.data.history_loader import DataLoader
from src.prediction_engine.core.llm.llm_completion import LLMCompletion
from src.prediction_engine.core.llm.faiss_cache import FaissCache
from src.prediction_engine.utils.logger import setup_logger  # assuming you created logger.py as discussed

logger = setup_logger()

class ShellSageCore:
    def __init__(self):
        self.data_loader = DataLoader()
        self.command_history = self.data_loader.commands
        self.trie_search = TrieSearch(self.command_history)
        self.faiss_search = FaissSearch(self.command_history)
        self.llm_completion = LLMCompletion()
        self.faiss_cache = FaissCache()
        self.ranker = Ranker()

    async def get_trie_results(self, query):
        start_time = time.time()
        results = self.trie_search.search(query)
        elapsed = time.time() - start_time
        logger.info(f"TrieSearch found {len(results)} results in {elapsed:.3f}s")
        return results

    async def get_faiss_results(self, query):
        start_time = time.time()
        results = self.faiss_search.search(query)
        elapsed = time.time() - start_time
        logger.info(f"FaissSearch found {len(results)} results in {elapsed:.3f}s")
        return results

    async def get_llm_results(self, query, candidates):
        if not candidates:
            return []
        candidates = list(dict.fromkeys(candidates))[:5]

        start_time = time.time()
        lookup_embedding = self.faiss_cache.generate_key_embedding(query, candidates)
        cached_results = self.faiss_cache.lookup(lookup_embedding)
        if cached_results:
            logger.info("Cache hit")
            elapsed = time.time() - start_time
            logger.info(f"LLMCompletion found {len(cached_results)} cached results in {elapsed:.3f}s")
            return cached_results

        logger.info("Cache miss")
        results = await self.llm_completion.refine(query, candidates)
        self.faiss_cache.add(lookup_embedding, results)
        self.faiss_cache.save()

        elapsed = time.time() - start_time
        logger.info(f"LLMCompletion found {len(results)} results in {elapsed:.3f}s")
        return results

    async def process_query(self, query):
        trie_task = self.get_trie_results(query)
        faiss_task = self.get_faiss_results(query)

        trie_results, faiss_results = await asyncio.gather(trie_task, faiss_task)
        llm_results = await self.get_llm_results(query, trie_results + faiss_results)

        final_suggestions = self.ranker.rank(trie_results, faiss_results, llm_results)

        logger.info("Final Ranked Suggestions:")
        if final_suggestions:
            for idx, suggestion in enumerate(final_suggestions, 1):
                logger.info(f"{idx}. {suggestion}")
        else:
            logger.warning("No relevant suggestions found.")

    async def run(self):
        while True:
            user_input = input("Enter command prefix (or type 'exit' to quit): ").strip()
            if user_input.lower() == "exit":
                logger.info("Exiting ShellSage. Goodbye!")
                break

            await self.process_query(user_input)


if __name__ == "__main__":
    asyncio.run(ShellSageCore().run())
