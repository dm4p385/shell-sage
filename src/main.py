import asyncio
import time
from core.trie.trie import TrieSearch
from core.faiss.faiss_search import FaissSearch
from ranking.ranking import Ranker
from data.history_loader import DataLoader
from core.llm.llm_completion import LLMCompletion


class ShellSage:
    def __init__(self):
        self.data_loader = DataLoader()
        self.command_history = self.data_loader.commands
        self.trie_search = TrieSearch(self.command_history)
        self.faiss_search = FaissSearch(self.command_history)
        self.llm_completion = LLMCompletion()
        self.ranker = Ranker()

    async def get_trie_results(self, query):
        start_time = time.time()
        results = self.trie_search.search(query)
        elapsed = time.time() - start_time
        print(f"🔍 TrieSearch found {len(results)} results in {elapsed:.3f}s")
        return results

    async def get_faiss_results(self, query):
        start_time = time.time()
        results = self.faiss_search.search(query)
        elapsed = time.time() - start_time
        print(f"📌 FaissSearch found {len(results)} results in {elapsed:.3f}s")
        return results

    async def get_llm_results(self, query, candidates):
        if not candidates:
            return []
        candidates = list(dict.fromkeys(candidates))[:5]  # deduplicate + truncate

        # candidates = candidates[:5]  # Limit LLM input to top 5 candidates
        start_time = time.time()

        results = await self.llm_completion.refine(query, candidates)

        elapsed = time.time() - start_time
        print(f"🤖 LLMCompletion found {len(results)} results in {elapsed:.3f}s")
        return results

    async def process_query(self, query):
        trie_task = self.get_trie_results(query)
        faiss_task = self.get_faiss_results(query)

        # Run Trie & Faiss in parallel
        trie_results, faiss_results = await asyncio.gather(trie_task, faiss_task)

        # Run LLM only if Trie/Faiss return results
        llm_results = await self.get_llm_results(query, trie_results + faiss_results)

        # Rank and display results
        final_suggestions = self.ranker.rank(trie_results, faiss_results, llm_results)

        print("\n🎯 **Final Ranked Suggestions:**")
        if final_suggestions:
            for idx, suggestion in enumerate(final_suggestions, 1):
                print(f"   {idx}. {suggestion}")
        else:
            print("⚠️ No relevant suggestions found.")

    async def run(self):
        while True:
            user_input = input("\n🔹 Enter command prefix (or type 'exit' to quit): ").strip()
            if user_input.lower() == "exit":
                print("🚀 Exiting ShellSage. Goodbye!")
                break

            await self.process_query(user_input)


if __name__ == "__main__":
    asyncio.run(ShellSage().run())
