import streamlit as st
import json
import os

# Path to save notes
NOTES_FILE = "notes.json"

# Load notes from file, converting any strings to dictionaries with "title" and "body"
def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as file:
            notes = json.load(file)
            # Convert any string notes to the new dictionary format
            return [{"title": note, "body": ""} if isinstance(note, str) else note for note in notes]
    return []

# Save notes to file
def save_notes(notes):
    with open(NOTES_FILE, "w") as file:
        json.dump(notes, file)

# Initialize session state to store notes and track edit mode
if 'notes' not in st.session_state:
    st.session_state.notes = load_notes()
if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None  # Tracks the index of the note currently in edit mode

# Function to add a new note
def add_note():
    # Adds a new note with empty title and body
    st.session_state.notes.append({"title": "", "body": ""})
    st.session_state.edit_index = len(st.session_state.notes) - 1  # Open the new note in edit mode
    save_notes(st.session_state.notes)

# Function to delete a note by index
def delete_note():
    if st.session_state.edit_index is not None:
        st.session_state.notes.pop(st.session_state.edit_index)
        st.session_state.edit_index = None  # Exit edit mode after deletion
        save_notes(st.session_state.notes)

# Function to update a note
def update_note(new_title, new_body):
    if st.session_state.edit_index is not None:
        st.session_state.notes[st.session_state.edit_index] = {"title": new_title, "body": new_body}
        save_notes(st.session_state.notes)

st.title("Ayani")

# Button to add a new note
if st.button("+ Add Note"):
    add_note()

# Define the number of columns for the grid layout
num_columns = 3
columns = st.columns(num_columns)

# Display notes in the grid layout
for index, note in enumerate(st.session_state.notes):
    # Calculate which column the note should go into
    col = columns[index % num_columns]
    with col:
        if st.session_state.edit_index == index:
            # Edit mode: Display title and body together in one "sticky note" style container
            with st.form(f"edit_form_{index}"):
                st.markdown(
                    """
                    <div style="background-color: #FFEB3B; padding: 1rem; border-radius: 8px; box-shadow: 2px 2px 8px rgba(0,0,0,0.1); color: #000000;">
                    """,
                    unsafe_allow_html=True
                )
                new_title = st.text_input("Title", value=note["title"], label_visibility="collapsed", placeholder="Title")
                new_body = st.text_area("Body", value=note["body"], label_visibility="collapsed", placeholder="Write your note here...")
                
                # Buttons inside the note
                save_button = st.form_submit_button("✔️ Save")
                delete_button = st.form_submit_button("🗑 Delete")
                
                if save_button:
                    update_note(new_title, new_body)
                    st.session_state.edit_index = None  # Exit edit mode after saving
                if delete_button:
                    delete_note()
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            # Display mode: Show note as a clickable button with title preview
            if st.button(
                label=f"📝 {note['title']}",
                key=f"note_{index}",
                help="Click to edit"
            ):
                st.session_state.edit_index = index  # Enter edit mode for this note
            st.markdown(
                f"""
                <div style="background-color: #FFEB3B; padding: 1rem; border-radius: 8px; box-shadow: 2px 2px 8px rgba(0,0,0,0.1); color: #000000; cursor: pointer;">
                    <strong>{note['title']}</strong><br>
                    {note['body'][:100]}...
                </div>
                """,
                unsafe_allow_html=True
            )


