from pytrie import Trie
from src.utils.logger import setup_logger

logger = setup_logger()


class TrieSearch:
    def __init__(self, commands):
        self.command_list = commands
        self.trie = Trie({cmd: cmd for cmd in self.command_list})
        logger.info(f"Trie initialized with {len(commands)} commands.")

    def search(self, prefix):
        """Return all commands starting with a given prefix."""
        results = list(self.trie.values(prefix))
        logger.debug(f"Found {len(results)} results for prefix '{prefix}'")
        return results
