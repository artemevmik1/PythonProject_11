from pathlib import Path

CURRENT_FILE = Path(__file__).resolve().parent
operations_json = CURRENT_FILE / "data/operations.json"
filename_csv = CURRENT_FILE / "data/transactions.csv"
filename_excel = CURRENT_FILE / "data/transactions_excel.xlsx"
