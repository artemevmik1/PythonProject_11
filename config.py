from pathlib import Path

CURRENT_FILE = Path(__file__).resolve().parent
operations_json = CURRENT_FILE / "data/operations.json"
print(operations_json)
