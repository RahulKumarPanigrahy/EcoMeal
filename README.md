# EcoMeal AI - Local Backend

This is the local, non-AWS implementation of the EcoMeal AI backend using FastAPI and SQLite.

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   python -m uvicorn app:app --reload
   ```

3. View the API documentation:
   Open your browser and navigate to `http://127.0.0.1:8000/docs` to test the endpoints interactively.
