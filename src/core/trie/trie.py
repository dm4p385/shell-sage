from pytrie import Trie

class TrieSearch:
    def __init__(self, commands):
        self.command_list = commands
        self.trie = Trie({cmd: cmd for cmd in self.command_list})

    def search(self, prefix):
        """Return all commands starting with a given prefix."""
        return list(self.trie.values(prefix))
