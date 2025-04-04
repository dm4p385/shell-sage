import os
import chardet
import yaml
from src.prediction_engine.utils.logger import setup_logger

logger = setup_logger()

class DataLoader:
    def __init__(self, shell_history_path=None):
        self.shell_history_path = os.path.expanduser(shell_history_path or "~/.local/share/fish/fish_history")
        self.commands = []

        if not os.path.exists(self.shell_history_path):
            logger.warning(f"Fish history file not found at {self.shell_history_path}")
        self.load()

    def detect_encoding(self, file_path):
        """Detect the encoding of a file."""
        with open(file_path, "rb") as f:
            raw_data = f.read(10000)
            result = chardet.detect(raw_data)
            return result.get("encoding", "utf-8")

    def load(self):
        """Load shell history and store commands."""
        try:
            with open(self.shell_history_path, "r", encoding="utf-8", errors="ignore") as f:
                history = yaml.safe_load(f)
                if not isinstance(history, list):
                    raise ValueError("Invalid Fish history format: Expected a list")

                for entry in history:
                    if isinstance(entry, dict) and "cmd" in entry:
                        command = entry["cmd"].strip()
                        self.commands.append(command)

            logger.info(f"Loaded {len(self.commands)} commands from shell history.")
        except FileNotFoundError:
            logger.error(f"Fish history file not found: {self.shell_history_path}")
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error in fish history file: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while loading shell history: {e}")
