# Pinboard API Python Wrapper

This package provides a convenient Python interface for interacting with the Pinboard V2 API. It abstracts away the low-level HTTP requests and offers a Pythonic way to manage your bookmarks, tags, and notes.

## ON HOLD

This project is on hold. API v2 remains in a draft or incomplete state. The documentation is insufficient, and the endpoints do not behave as described.
When I started this project I was not aware of the issues with the API v2. I have since learned that the API is not yet ready for production use. I will continue to monitor the API and may resume work on this project in the future.

More info [here](https://www.perplexity.ai/search/pinboard-in-verion-2-of-api-no-J4EGnZLaS0mG5RowFrda2g#0)

## Installation

**DO NOT USE THIS PACKAGE** Not currently published on PyPi

```bash
pip install pinboard-api-v2
```

## Usage

First, you need to get your Pinboard API token. You can find this on your Pinboard settings page (usually in the format username:hex_auth_token).

### Import Options

You can import the classes in several ways:

```python
# Option 1: Import specific classes (recommended)
from pbapi2 import PinboardClient, PinboardAPIError

# Option 2: Import all classes
from pbapi2 import (
    PinboardClient,
    PinboardAPIError,
    PinboardBadRequestError,
    PinboardUnauthorizedError,
    PinboardForbiddenError,
    PinboardNotFoundError,
    PinboardRateLimitExceededError,
    PinboardServerError,
)

# Option 3: Import everything (not recommended for production)
from pbapi2 import *

# Option 4: Import the module
import pbapi2
client = pbapi2.PinboardClient("your_token")
```

### Basic Example

```python
# example.py
import os
import datetime
from pbapi2 import PinboardClient, PinboardAPIError

# Replace with your actual auth token or use an environment variable
# It's recommended to use environment variables for sensitive information
# export PINBOARD_AUTH_TOKEN="your_username:your_hex_token"
AUTH_TOKEN = os.getenv("PINBOARD_AUTH_TOKEN", "YOUR_USERNAME:YOUR_HEX_TOKEN")

if AUTH_TOKEN == "YOUR_USERNAME:YOUR_HEX_TOKEN":
    print(
        "WARNING: Please set the PINBOARD_AUTH_TOKEN environment variable or replace the placeholder in example.py."
    )
    print(
        "You can find your token at https://pinboard.in/settings/password"
    )
    exit()

try:
    # Initialize the client
    # For testing, you can use test_mode=True
    client = PinboardClient(auth_token=AUTH_TOKEN, test_mode=False)

    print("--- Testing API Connectivity ---")
    hello_response = client.hello()
    print(f"Hello response: {hello_response}")

    print("\n--- Getting Last Update ---")
    last_update_response = client.last_update()
    print(f"Last update: {last_update_response}")

    print("\n--- Bookmarks Examples ---")

    # Add a new bookmark
    try:
        print("Adding a new bookmark...")
        new_bookmark_url = "https://www.example.com/test-pinboard-api"
        new_bookmark_title = "Test Pinboard API Bookmark"
        add_bookmark_response = client.add_bookmark(
            url=new_bookmark_url,
            title=new_bookmark_title,
            description="A test bookmark created via the Python API wrapper.",
            tags=["api", "test", "python"],
            private=True,
            toread=False,
        )
        print(f"Added bookmark: {add_bookmark_response}")
        # Extract the ID if the addition was successful
        if add_bookmark_response and add_bookmark_response.get("result") == "ok":
            bookmark_id = add_bookmark_response.get("bookmark_id")
            print(f"New bookmark ID: {bookmark_id}")

            # Retrieve the newly added bookmark by ID
            print(f"\nRetrieving bookmark by ID: {bookmark_id}...")
            retrieved_bookmark = client.get_bookmark_by_id(bookmark_id)
            print(f"Retrieved bookmark: {retrieved_bookmark}")

            # Update the bookmark
            print(f"\nUpdating bookmark {bookmark_id}...")
            update_response = client.update_bookmark(
                bookmark_id=bookmark_id,
                title="Updated Test Pinboard API Bookmark",
                tags=["api", "updated", "python", "newtag"],
                private=False,  # Make it public
            )
            print(f"Updated bookmark: {update_response}")

            # Delete the bookmark
            print(f"\nDeleting bookmark {bookmark_id}...")
            delete_response = client.delete_bookmark(bookmark_id)
            print(f"Deleted bookmark: {delete_response}")
        else:
            print(
                "Failed to add bookmark, skipping update and delete operations for this bookmark."
            )

    except PinboardAPIError as e:
        print(f"Error during bookmark operations: {e}")

    # Get a list of bookmarks (e.g., last 5)
    print("\n--- Getting a list of 5 bookmarks ---")
    bookmarks_list = client.get_bookmarks(count=5)
    for bookmark in bookmarks_list.get("bookmarks", []):
        print(
            f"- Title: {bookmark.get('title')}, URL: {bookmark.get('url')}, Tags: {bookmark.get('tags')}"
        )

    # Get all bookmarks (be mindful of rate limits!)
    # print("\n--- Getting all bookmarks (RATE LIMITED!) ---")
    # all_bookmarks = client.get_all_bookmarks()
    # print(f"Total bookmarks: {len(all_bookmarks.get('bookmarks', []))}")

    print("\n--- Tags Examples ---")

    # Get all tags with counts
    print("Getting all tags...")
    tags_response = client.get_tags()
    print(f"Tags: {tags_response}")

    # Example: Create a temporary tag for renaming/deletion test
    # This assumes you have at least one bookmark where you can add this tag
    # For a real test, you'd add a bookmark with this tag first.
    # For simplicity, we'll try to rename a non-existent tag for demonstration
    # You might get an error if the tag doesn't exist on your account.
    temp_old_tag = "oldtesttag"
    temp_new_tag = "newtesttag"
    try:
        print(f"\nRenaming tag '{temp_old_tag}' to '{temp_new_tag}'...")
        rename_response = client.rename_tags(old_tag=temp_old_tag, new_tag=temp_new_tag)
        print(f"Rename response: {rename_response}")
    except PinboardAPIError as e:
        print(f"Error renaming tag (expected if tag doesn't exist): {e}")

    # Delete a tag
    try:
        # Again, this will work if 'newtesttag' exists and is used by bookmarks
        print(f"\nDeleting tag '{temp_new_tag}'...")
        delete_tag_response = client.delete_tags(tags=[temp_new_tag])
        print(f"Delete tag response: {delete_tag_response}")
    except PinboardAPIError as e:
        print(
            f"Error deleting tag (expected if tag doesn't exist or already deleted): {e}"
        )

    print("\n--- Notes Examples ---")

    # Create a new note
    try:
        print("Creating a new note...")
        new_note_title = "My Test Note"
        new_note_body = "This is the **body** of my test note, written with Markdown."
        create_note_response = client.create_note(
            title=new_note_title, body=new_note_body, use_markdown=True
        )
        print(f"Created note: {create_note_response}")
        if create_note_response and create_note_response.get("id"):
            note_id = create_note_response["id"]
            print(f"New note ID: {note_id}")

            # Get the new note by ID
            print(f"\nRetrieving note by ID: {note_id}...")
            retrieved_note = client.get_note_by_id(note_id)
            print(f"Retrieved note: {retrieved_note}")

            # Update the note
            print(f"\nUpdating note {note_id}...")
            update_note_response = client.update_note(
                note_id=note_id,
                title="Updated Test Note Title",
                body="This is the *updated* body of the note.",
            )
            print(f"Updated note: {update_note_response}")

            # Delete the note
            print(f"\nDeleting note {note_id}...")
            delete_note_response = client.delete_note(note_id)
            print(f"Deleted note: {delete_note_response}")
        else:
            print(
                "Failed to create note, skipping update and delete operations for this note."
            )

    except PinboardAPIError as e:
        print(f"Error during note operations: {e}")

    # Get a list of notes
    print("\n--- Getting a list of notes ---")
    notes_list = client.get_notes(count=2)
    for note in notes_list.get("notes", []):
        print(f"- Title: {note.get('title')}, ID: {note.get('id')}")


except PinboardAPIError as e:
    print(f"An API error occurred: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

## Testing

This project includes comprehensive tests. To run them:

```bash
# Run all tests
python run_tests.py

# Or use pytest directly
python -m pytest tests/test_pinboard_api.py -v
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

:Barry-Thomas-Paul: Moss

## Acknowledgments

- [Pinboard](https://pinboard.in/) for providing the API
- The Python community for excellent libraries like `requests`