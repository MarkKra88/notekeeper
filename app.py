import logging
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Notes CRUD API")

class NoteBase(BaseModel):
    title: str
    content: str

class Note(NoteBase):
    id: int

# In-memory store
notes: List[Note] = []
next_id = 1

# Middleware to log all incoming requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    body = await request.body()
    logger.info(f"{request.method} {request.url.path} | Payload: {body.decode('utf-8') or 'No body'}")
    response = await call_next(request)
    return response

@app.post("/notes", response_model=Note)
def create_note(note: NoteBase):
    global next_id
    new_note = Note(id=next_id, **note.dict())
    notes.append(new_note)
    next_id += 1
    logger.info(f"Created note {new_note.id}")
    return new_note

@app.get("/notes", response_model=List[Note])
def list_notes():
    print(f"Listing {len(notes)} notes")
    return notes

@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: int):
    for note in notes:
        if note.id == note_id:
            print(f"Fetched note {note_id}")
            return note
    raise HTTPException(status_code=404, detail="Note not found")

@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: int, updated: NoteBase):
    for idx, note in enumerate(notes):
        if note.id == note_id:
            notes[idx] = Note(id=note_id, **updated.dict())
            print(f"Updated note {note_id}")
            return notes[idx]
    raise HTTPException(status_code=404, detail="Note not found")

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    for idx, note in enumerate(notes):
        if note.id == note_id:
            deleted_note = notes.pop(idx)
            print(f"Deleted note {note_id}")
            return {"status": "deleted", "note": deleted_note}
    raise HTTPException(status_code=404, detail="Note not found")