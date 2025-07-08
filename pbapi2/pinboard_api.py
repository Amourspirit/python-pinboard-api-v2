"""
Pinboard API V2 Python Client

A Python client for interacting with the Pinboard V2 API.

Copyright (c) 2025 :Barry-Thomas-Paul: Moss
Licensed under the MIT License - see LICENSE file for details.

API Reference: https://pinboard.in/api/v2/reference/
"""

from __future__ import annotations
import requests
import datetime
from typing import Dict, List, Optional


class PinboardAPIError(Exception):
    """Base exception for Pinboard API errors."""

    pass


class PinboardBadRequestError(PinboardAPIError):
    """Exception for 400 Bad Request errors."""

    pass


class PinboardUnauthorizedError(PinboardAPIError):
    """Exception for 401 Unauthorized errors."""

    pass


class PinboardForbiddenError(PinboardAPIError):
    """Exception for 403 Forbidden errors."""

    pass


class PinboardNotFoundError(PinboardAPIError):
    """Exception for 404 Not Found errors."""

    pass


class PinboardRateLimitExceededError(PinboardAPIError):
    """Exception for 429 Rate Limit Exceeded errors."""

    pass


class PinboardServerError(PinboardAPIError):
    """Exception for 5xx Server errors."""

    pass


class PinboardClient:
    """
    A Python client for interacting with the Pinboard V2 API.

    Attributes:
        base_url (str): The base URL for the Pinboard API.
        auth_token (str): The authentication token for API requests.
        session (requests.Session): The HTTP session for making requests.
    """

    def __init__(self, auth_token: str, test_mode: bool = False):
        """
        Initializes the PinboardClient.

        Args:
            auth_token (str): Your Pinboard API token (e.g., "username:hex_auth_token").
            test_mode (bool): If True, uses the test API endpoint. Defaults to False.
        """
        self.auth_token = auth_token
        self.base_url = (
            "https://api.test.pinboard.in/v2/"
            if test_mode
            else "https://api.pinboard.in/v2/"
        )
        self.session = requests.Session()

    def _request(
        self, method: str, endpoint: str, params: dict = None, data: dict = None
    ) -> dict:
        """
        Makes an HTTP request to the Pinboard API.

        Args:
            method (str): The HTTP method (GET, POST, PUT, DELETE).
            endpoint (str): The API endpoint (e.g., "hello", "bookmarks").
            params (dict, optional): Dictionary of query parameters. Defaults to None.
            data (dict, optional): Dictionary of form data for POST/PUT requests. Defaults to None.

        Returns:
            dict: The JSON response from the API.

        Raises:
            PinboardBadRequestError: If the request is malformed (400).
            PinboardUnauthorizedError: If authentication fails (401).
            PinboardForbiddenError: If access is forbidden (403).
            PinboardNotFoundError: If the resource is not found (404).
            PinboardRateLimitExceededError: If rate limit is exceeded (429).
            PinboardServerError: For 5xx server errors.
            PinboardAPIError: For other API-related errors.
        """
        url = f"{self.base_url}{endpoint}/"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Auth-Token": self.auth_token,
        }

        if params is None:
            params = {}
        # params["auth_token"] = self.auth_token

        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params)
            elif method.upper() == "POST":
                response = self.session.post(
                    url, params=params, data=data, headers=headers
                )
            elif method.upper() == "PUT":
                response = self.session.put(
                    url, params=params, data=data, headers=headers
                )
            elif method.upper() == "DELETE":
                response = self.session.delete(
                    url, params=params, data=data, headers=headers
                )
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.HTTPError:
            if response.status_code == 400:
                raise PinboardBadRequestError(f"Bad Request: {response.text}")
            elif response.status_code == 401:
                raise PinboardUnauthorizedError(f"Unauthorized: {response.text}")
            elif response.status_code == 403:
                raise PinboardForbiddenError(f"Forbidden: {response.text}")
            elif response.status_code == 404:
                raise PinboardNotFoundError(f"Not Found: {response.text}")
            elif response.status_code == 429:
                raise PinboardRateLimitExceededError(
                    f"Rate Limit Exceeded: {response.text}"
                )
            elif 500 <= response.status_code < 600:
                raise PinboardServerError(
                    f"Server Error ({response.status_code}): {response.text}"
                )
            else:
                raise PinboardAPIError(
                    f"An unexpected API error occurred ({response.status_code}): {response.text}"
                )
        except requests.exceptions.RequestException as e:
            raise PinboardAPIError(f"A network error occurred: {e}")

    def hello(self) -> dict:
        """
        Checks credentials and API reachability. Does not count against rate limits.

        Returns:
            dict: API response confirming connectivity and user.
        """
        return self._request("GET", "hello")

    def last_update(self) -> dict:
        """
        Returns timestamps of the last stateful changes to a user's bookmarks and notes.
        Useful for lightweight polling.

        Returns:
            dict: Dictionary with 'last_update' and 'last_update_notes' timestamps.
        """
        return self._request("GET", "last_update")

    ## Bookmarks

    def get_bookmarks(
        self,
        ids: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        start_date: Optional[datetime.datetime] = None,
        end_date: Optional[datetime.datetime] = None,
        filter_string: Optional[str] = None,
        url: Optional[str] = None,
        count: int = 25,
        offset: int = 0,
    ) -> Dict:
        """
        Retrieves a list of the user's bookmarks.

        Args:
            ids (list, optional): List of bookmark IDs (up to 50). If provided, other filters are ignored.
            tags (list, optional): List of tags (up to 3) to filter by.
            start_date (datetime.datetime, optional): Bookmarks created after this date.
            end_date (datetime.datetime, optional): Bookmarks created before this date.
            filter_string (str, optional): Filter by 'public', 'private', or 'read'.
            url (str, optional): Filter by a specific URL. If provided, other filters are ignored.
            count (int, optional): Number of bookmarks to return (default 25, max 1000).
            offset (int, optional): Offset for pagination.

        Returns:
            dict: A dictionary containing the list of bookmarks.
        """
        params = {}
        if ids:
            params["ids"] = ",".join(map(str, ids))
        elif url:
            params["url"] = url
        else:
            if tags:
                params["tags"] = ",".join(tags)
            if start_date:
                params["start_date"] = start_date.isoformat()
            if end_date:
                params["end_date"] = end_date.isoformat()
            if filter_string:
                params["filter"] = filter_string
            params["count"] = min(count, 1000)
            params["offset"] = offset
        return self._request("GET", "bookmarks", params=params)

    def get_all_bookmarks(self) -> dict:
        """
        Retrieves the full list of a user's bookmarks.
        This call is rate-limited to five calls an hour.

        Returns:
            dict: A dictionary containing the full list of bookmarks.
        """
        return self._request("GET", "bookmarks/all")

    def get_bookmark_by_id(self, bookmark_id: str) -> dict:
        """
        Retrieves a specific bookmark by its ID.

        Args:
            bookmark_id (str): The ID of the bookmark.

        Returns:
            dict: A dictionary containing the bookmark details.
        """
        return self._request("GET", f"bookmarks/{bookmark_id}")

    def add_bookmark(
        self,
        url: str,
        title: str,
        description: str = None,
        created: datetime.datetime = None,
        tags: list = None,
        private: bool = False,
        toread: bool = False,
        exact_url: bool = False,
    ) -> dict:
        """
        Creates a new bookmark.

        Args:
            url (str): The URL of the bookmark.
            title (str): The title of the bookmark.
            description (str, optional): The description of the bookmark.
            created (datetime.datetime, optional): The creation date of the bookmark.
            tags (list, optional): List of tags for the bookmark.
            private (bool, optional): If True, the bookmark is private. Defaults to False.
            toread (bool, optional): If True, marks the bookmark as toread. Defaults to False.
            exact_url (bool, optional): If True, matches the URL exactly. Defaults to False.

        Returns:
            dict: API response, typically with 'result' and 'bookmark_id'.
        """
        data = {
            "url": url,
            "title": title,
            "private": "yes" if private else "no",
            "toread": "yes" if toread else "no",
            "exact_url": "yes" if exact_url else "no",
        }
        if description:
            data["description"] = description
        if created:
            data["created"] = created.isoformat()
        if tags:
            data["tags"] = ",".join(tags)
        return self._request("POST", "bookmarks", data=data)

    def update_bookmark(
        self,
        bookmark_id: str,
        url: str = None,
        title: str = None,
        description: str = None,
        created: datetime.datetime = None,
        tags: list = None,
        private: bool = None,
        toread: bool = None,
        exact_url: bool = None,
    ) -> dict:
        """
        Updates an existing bookmark. Only explicitly provided fields are updated;
        an empty argument will erase existing data for that field.
        Changing the URL will change the bookmark ID.

        Args:
            bookmark_id (str): The ID of the bookmark to update.
            url (str, optional): The new URL of the bookmark.
            title (str, optional): The new title of the bookmark.
            description (str, optional): The new description of the bookmark.
            created (datetime.datetime, optional): The new creation date of the bookmark.
            tags (list, optional): List of new tags for the bookmark.
            private (bool, optional): If True, sets bookmark to private. If False, sets to public.
            toread (bool, optional): If True, marks as toread. If False, unmarks as toread.
            exact_url (bool, optional): If True, matches the URL exactly.

        Returns:
            dict: API response, typically with 'result' and 'bookmark_id'.
        """
        data = {}
        if url is not None:
            data["url"] = url
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if created is not None:
            data["created"] = created.isoformat()
        if tags is not None:
            data["tags"] = ",".join(tags) if tags else ""
        if private is not None:
            data["private"] = "yes" if private else "no"
        if toread is not None:
            data["toread"] = "yes" if toread else "no"
        if exact_url is not None:
            data["exact_url"] = "yes" if exact_url else "no"

        if not data:
            raise ValueError("No fields provided for update.")

        return self._request("POST", f"bookmarks/{bookmark_id}", data=data)

    def delete_bookmark(self, bookmark_id: str) -> dict:
        """
        Permanently deletes a specific bookmark.

        Args:
            bookmark_id (str): The ID of the bookmark to delete.

        Returns:
            dict: API response, typically with 'result': 'ok'.
        """
        return self._request("DELETE", f"bookmarks/{bookmark_id}")

    def batch_delete_bookmarks(self, bookmark_ids: list) -> dict:
        """
        Batch endpoint for deleting up to 100 bookmark IDs.

        Args:
            bookmark_ids (list): A list of bookmark IDs to delete (up to 100).

        Returns:
            dict: API response, typically with 'result': 'ok'.
        """
        if not bookmark_ids or len(bookmark_ids) > 100:
            raise ValueError("Must provide 1 to 100 bookmark IDs for batch deletion.")
        data = {"ids": ",".join(map(str, bookmark_ids))}
        return self._request("POST", "bookmarks/delete", data=data)

    ## Tags

    def get_tags(self, cutoff: int = None) -> dict:
        """
        Returns a full list of the user's tags with usage counts.
        This call is rate-limited to once a minute.

        Args:
            cutoff (int, optional): Minimum usage count for tags to be returned.

        Returns:
            dict: A dictionary where keys are tag names and values are their counts.
        """
        params = {}
        if cutoff:
            params["cutoff"] = cutoff
        return self._request("GET", "tags", params=params)

    def rename_tags(self, old_tag: str, new_tag: str) -> dict:
        """
        Renames one or more tags. Case changes are not supported.

        Args:
            old_tag (str): The old tag name (can be comma-delimited for multiple, up to 30).
            new_tag (str): The new single tag name.

        Returns:
            dict: API response, typically with 'result': 'ok'.
        """
        data = {"old": old_tag, "new": new_tag}
        return self._request("POST", "tags/rename", data=data)

    def delete_tags(self, tags: list) -> dict:
        """
        Deletes one or more tags (up to 100).

        Args:
            tags (list): A list of tag names to delete (up to 100).

        Returns:
            dict: API response, typically with 'result': 'ok'.
        """
        if not tags or len(tags) > 100:
            raise ValueError("Must provide 1 to 100 tags for deletion.")
        data = {"tags": ",".join(tags)}
        return self._request("POST", "tags/delete", data=data)

    ## Notes

    def get_notes(self, count: int = 25, offset: int = 0) -> dict:
        """
        Returns a list of the user's notes in reverse chronological order.

        Args:
            count (int, optional): Number of notes to return (default 25, max 100).
            offset (int, optional): Offset for pagination.

        Returns:
            dict: A dictionary containing the list of notes.
        """
        params = {"count": min(count, 100), "offset": offset}
        return self._request("GET", "notes", params=params)

    def get_note_by_id(self, note_id: str) -> dict:
        """
        Retrieves a specific note by its ID.

        Args:
            note_id (str): The ID of the note.

        Returns:
            dict: A dictionary containing the note details.
        """
        return self._request("GET", f"notes/{note_id}")

    def create_note(self, title: str, body: str, use_markdown: bool = False) -> dict:
        """
        Creates a new note.

        Args:
            title (str): The title of the note.
            body (str): The content of the note.
            use_markdown (bool, optional): If True, enables Markdown for the note. Defaults to False.

        Returns:
            dict: API response with the new note's identifier.
        """
        data = {
            "title": title,
            "note": body,
            "use_markdown": "yes" if use_markdown else "no",
        }
        return self._request("POST", "notes", data=data)

    def update_note(
        self,
        note_id: str,
        title: str = None,
        body: str = None,
        use_markdown: bool = None,
    ) -> dict:
        """
        Updates an existing note.

        Args:
            note_id (str): The ID of the note to update.
            title (str, optional): The new title of the note.
            body (str, optional): The new content of the note.
            use_markdown (bool, optional): If True, enables Markdown. If False, disables Markdown.

        Returns:
            dict: API response, typically with 'result': 'ok'.
        """
        data = {}
        if title is not None:
            data["title"] = title
        if body is not None:
            data["note"] = body
        if use_markdown is not None:
            data["use_markdown"] = "yes" if use_markdown else "no"

        if not data:
            raise ValueError("No fields provided for update.")

        return self._request("POST", f"notes/{note_id}", data=data)

    def delete_note(self, note_id: str) -> dict:
        """
        Deletes a specific note.

        Args:
            note_id (str): The ID of the note to delete.

        Returns:
            dict: API response, typically with 'result': 'ok'.
        """
        return self._request("DELETE", f"notes/{note_id}")
