import json
import sys
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.environ.get('BASE_URL')

def pretty(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))

def prompt(msg: str):
    """Prompt; return None if user enters 0 (meaning 'back')."""
    val = input(f"{msg} (0 to go back): ").strip()
    return None if val == "0" else val

def post_note():
    title = prompt("Title")
    if title is None:
        print("↩ back")
        return
    content = prompt("Content")
    if content is None:
        print("↩ back")
        return
    r = requests.post(f"{BASE_URL}/notes", json={"title": title, "content": content})
    print(f"Status: {r.status_code}")
    try: pretty(r.json())
    except: print(r.text)

def get_all():
    r = requests.get(f"{BASE_URL}/notes")
    print(f"Status: {r.status_code}")
    try: pretty(r.json())
    except: print(r.text)

def get_one():
    note_id = prompt("Note ID")
    if note_id is None:
        print("↩ back")
        return
    r = requests.get(f"{BASE_URL}/notes/{note_id}")
    print(f"Status: {r.status_code}")
    try: pretty(r.json())
    except: print(r.text)

def fetch_note(note_id: str):
    r = requests.get(f"{BASE_URL}/notes/{note_id}")
    if r.status_code == 200:
        try:
            return r.json()
        except Exception:
            return None
    return None

def put_note():
    # step 1: ask for note id; 0 -> back to main
    while True:
        note_id = prompt("Note ID to update")
        if note_id is None:
            print("↩ back to main")
            return

        # step 2: choose update option; 0 -> back to step 1
        while True:
            print("\nUpdate options")
            print("1) Change title")
            print("2) Change content")
            print("3) Change both")
            print("0) Back (choose another ID)")
            choice = input("> ").strip()

            if choice == "0":
                # back to step 1 (ask ID again)
                break

            # for partial updates, fetch current to preserve other field
            current = None
            if choice in ("1", "2"):
                current = fetch_note(note_id)
                if not current:
                    print("Note not found (cannot update).")
                    break  # go back to step 1

            # step 3: collect fields; any 0 -> back to step 2
            if choice == "1":
                new_title = prompt("New title")
                if new_title is None:
                    print("↩ back to update options")
                    continue
                payload = {"title": new_title, "content": current["content"]}

            elif choice == "2":
                new_content = prompt("New content")
                if new_content is None:
                    print("↩ back to update options")
                    continue
                payload = {"title": current["title"], "content": new_content}

            elif choice == "3":
                new_title = prompt("New title")
                if new_title is None:
                    print("↩ back to update options")
                    continue
                new_content = prompt("New content")
                if new_content is None:
                    print("↩ back to update options")
                    continue
                payload = {"title": new_title, "content": new_content}

            else:
                print("Invalid choice.")
                continue

            # perform update
            r = requests.put(f"{BASE_URL}/notes/{note_id}", json=payload)
            print(f"Status: {r.status_code}")
            try:
                pretty(r.json())
            except:
                print(r.text)

            # after a successful update, return to main menu
            return

def delete_note():
    note_id = prompt("Note ID to delete")
    if note_id is None:
        print("↩ back")
        return
    r = requests.delete(f"{BASE_URL}/notes/{note_id}")
    print(f"Status: {r.status_code}")
    try: pretty(r.json())
    except: print(r.text)

def notes_menu():
    while True:
        print("###############")
        print("Notes API")
        print("\n1) POST /notes (create)")
        print("2) GET /notes (list all)")
        print("3) GET /notes/{id} (get one)")
        print("4) PUT /notes/{id} (update)")
        print("5) DELETE /notes/{id} (delete)")
        print("0) Exit")
        print("###############")
        choice = input("> ").strip()

        if choice == "1":
            post_note()
        elif choice == "2":
            get_all()
        elif choice == "3":
            get_one()
        elif choice == "4":
            put_note()
        elif choice == "5":
            delete_note()
        elif choice == "0":
            print("Bye!")
            sys.exit(0)
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    notes_menu()
