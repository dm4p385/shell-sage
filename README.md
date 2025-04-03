ShellSage/
│── src/                                # Main source code  
│   ├── __init__.py                     # Package init  
│   ├── main.py                          # CLI entry point  
│   ├── config.py                        # Configuration settings  
│   │  
│   ├── core/                            # Core autocomplete logic  
│   │   ├── __init__.py                  
│   │   ├── trie.py                      # Trie-based prefix search  
│   │   ├── faiss_search.py              # FAISS for context search  
│   │   ├── llm_completion.py            # LLM-based command prediction  
│   │   ├── hybrid_ranker.py             # Merging Trie, FAISS, and LLM  
│   │  
│   ├── data/                            # Data management  
│   │   ├── __init__.py  
│   │   ├── history_loader.py            # Fetch and store shell history  
│   │   ├── prebuilt_commands.json       # Preloaded common shell commands  
│   │  
│   ├── ranking/                         # Ranking algorithms  
│   │   ├── __init__.py  
│   │   ├── trie_ranker.py                # Rank Trie results  
│   │   ├── faiss_ranker.py               # Rank FAISS results  
│   │   ├── hybrid_ranker.py              # Final ranking strategy  
│   │  
│   ├── utils/                           # Utility functions  
│   │   ├── __init__.py  
│   │   ├── cache.py                      # Caching to reduce latency  
│   │   ├── async_utils.py                # Async processing helpers  
│   │   ├── logging.py                    # Custom logger  
│   │  
│   ├── cli/                             # Interactive CLI components  
│   │   ├── __init__.py  
│   │   ├── shellsage_cli.py              # Handles CLI interactions  
│   │   ├── ui.py                         # Terminal UI for displaying suggestions  
│   │  
│── tests/                               # Unit & integration tests  
│   ├── test_trie.py  
│   ├── test_faiss.py  
│   ├── test_llm.py  
│   ├── test_ranking.py  
│   ├── test_cli.py  
│  
│── scripts/                             # Helper scripts  
│   ├── install_dependencies.sh           # Install requirements  
│   ├── build_index.py                    # Precompute embeddings for FAISS  
│  
│── docs/                                # Documentation  
│   ├── README.md  
│   ├── architecture.md                   # System design overview  
│   ├── api_reference.md                  # API Documentation  
│  
│── .env                                 # Environment variables  
│── requirements.txt                     # Python dependencies  
│── setup.py                             # Installable Python package  
│── Dockerfile                           # Containerization for deployment  
│── .gitignore                           # Git ignored files  
