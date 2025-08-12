# Notes CRUD (FastAPI) + CLI Demo

A minimal FastAPI service that implements a simple in-memory **Notes** CRUD API, plus a tiny Python CLI client to drive the endpoints for a quick demo.

## Endpoints

- `POST /notes` — create a note
- `GET /notes` — list all notes
- `GET /notes/{id}` — get a note by id
- `PUT /notes/{id}` — update a note
- `DELETE /notes/{id}` — delete a note

Notes are kept **in memory** (cleared on server restart).

## Requirements

- Python 3.10+ recommended
- See `requirements.txt`

Install:
```bash
pip install -r requirements.txt
```

## Environment

The CLI client reads the API base URL from `.env`.

1. Copy `.env_template` to `.env`
2. Edit `BASE_URL` to point to your running API, e.g.:
   ```
   BASE_URL="http://localhost:8000"
   ```

> Only the CLI uses `BASE_URL`. The API itself doesn’t require any env vars.

## Run the API

```bash
uvicorn app:app --reload --port 8000
```

Console logging is enabled. You’ll see lines like:
```
2025-08-11 21:18:08 [INFO] POST /notes | Payload: {"title":"Test","content":"Hello"}
2025-08-11 21:18:08 [INFO] Created note 1
```

## Run the CLI

In a separate terminal:

```bash
python test_client.py
```

Menu:
```
1) POST /notes (create)
2) GET /notes (list all)
3) GET /notes/{id} (get one)
4) PUT /notes/{id} (update)
5) DELETE /notes/{id} (delete)
0) Exit
```

- At any input prompt, enter `0` to go **back** one step.
- On **PUT**, you can choose:
  - change title
  - change content
  - change both  
  After a successful update, you’re returned to the main menu.

## Project structure

```
.
├── app.py               # FastAPI service
├── test_client.py       # Interactive CLI tester
├── requirements.txt
├── .env_template
└── README.md
```

## Notes

- Data is in-memory by design.
- Logging middleware prints **method, path, and raw payload** for visibility.
