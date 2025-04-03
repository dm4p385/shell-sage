import logging
import os
import chardet
import yaml

class DataLoader:
    def __init__(self, shell_history_path=None):
        self.shell_history_path = os.path.expanduser(shell_history_path or "~/.local/share/fish/fish_history")
        self.commands = []  # Store loaded commands

        if not os.path.exists(self.shell_history_path):
            logging.warning(f"Fish history file not found at {self.shell_history_path}!")
        self.load()

    def detect_encoding(self, file_path):
        """Detect the encoding of a file."""
        with open(file_path, "rb") as f:
            raw_data = f.read(10000)  # Read a sample
            result = chardet.detect(raw_data)
            return result.get("encoding", "utf-8")  # Default to utf-8 if detection fails

    def load(self):
        """Load shell history and store commands."""
        try:
            with open(self.shell_history_path, "r", encoding="utf-8", errors="ignore") as f:
                history = yaml.safe_load(f)
                if not isinstance(history, list):
                    raise ValueError("Invalid Fish history format: Expected a list!")

                for entry in history:
                    if isinstance(entry, dict) and "cmd" in entry:
                        command = entry["cmd"].strip()
                        self.commands.append(command)  # Store commands
            logging.info("Fish history loaded successfully.")
        except FileNotFoundError:
            logging.error(f"Fish history file does not exist: {self.shell_history_path}")
        except yaml.YAMLError as e:
            logging.error(f"Error reading Fish history file: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
