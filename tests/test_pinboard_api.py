"""
Tests for Pinboard API V2 Python Client

Copyright (c) 2025 :Barry-Thomas-Paul: Moss
Licensed under the MIT License - see LICENSE file for details.
"""

import pytest
import datetime
from unittest.mock import Mock, patch
import requests
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


class TestPinboardClient:
    """Test suite for PinboardClient class."""

    @pytest.fixture
    def client(self):
        """Create a PinboardClient instance for testing."""
        return PinboardClient("test_user:test_token")

    @pytest.fixture
    def test_client(self):
        """Create a PinboardClient instance in test mode."""
        return PinboardClient("test_user:test_token", test_mode=True)

    def test_init_production_mode(self):
        """Test client initialization in production mode."""
        client = PinboardClient("test_user:test_token")
        assert client.auth_token == "test_user:test_token"
        assert client.base_url == "https://api.pinboard.in/v2/"
        assert isinstance(client.session, requests.Session)

    def test_init_test_mode(self):
        """Test client initialization in test mode."""
        client = PinboardClient("test_user:test_token", test_mode=True)
        assert client.auth_token == "test_user:test_token"
        assert client.base_url == "https://api.test.pinboard.in/v2/"
        assert isinstance(client.session, requests.Session)

    @patch("requests.Session.get")
    def test_request_get_success(self, mock_get, client):
        """Test successful GET request."""
        mock_response = Mock()
        mock_response.json.return_value = {"result": "ok"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = client._request("GET", "hello")

        assert result == {"result": "ok"}
        mock_get.assert_called_once_with(
            "https://api.pinboard.in/v2/hello/",
            params={"auth_token": "test_user:test_token"},
        )

    @patch("requests.Session.post")
    def test_request_post_success(self, mock_post, client):
        """Test successful POST request."""
        mock_response = Mock()
        mock_response.json.return_value = {"result": "ok", "bookmark_id": "123"}
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        data = {"url": "https://example.com", "title": "Test"}
        result = client._request("POST", "bookmarks", data=data)

        assert result == {"result": "ok", "bookmark_id": "123"}
        mock_post.assert_called_once_with(
            "https://api.pinboard.in/v2/bookmarks/",
            params={"auth_token": "test_user:test_token"},
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

    @patch("requests.Session.get")
    def test_request_400_error(self, mock_get, client):
        """Test 400 Bad Request error handling."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response

        with pytest.raises(PinboardBadRequestError, match="Bad Request"):
            client._request("GET", "hello")

    @patch("requests.Session.get")
    def test_request_401_error(self, mock_get, client):
        """Test 401 Unauthorized error handling."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response

        with pytest.raises(PinboardUnauthorizedError, match="Unauthorized"):
            client._request("GET", "hello")

    @patch("requests.Session.get")
    def test_request_403_error(self, mock_get, client):
        """Test 403 Forbidden error handling."""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.text = "Forbidden"
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response

        with pytest.raises(PinboardForbiddenError, match="Forbidden"):
            client._request("GET", "hello")

    @patch("requests.Session.get")
    def test_request_404_error(self, mock_get, client):
        """Test 404 Not Found error handling."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response

        with pytest.raises(PinboardNotFoundError, match="Not Found"):
            client._request("GET", "hello")

    @patch("requests.Session.get")
    def test_request_429_error(self, mock_get, client):
        """Test 429 Rate Limit Exceeded error handling."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.text = "Rate Limit Exceeded"
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response

        with pytest.raises(PinboardRateLimitExceededError, match="Rate Limit Exceeded"):
            client._request("GET", "hello")

    @patch("requests.Session.get")
    def test_request_500_error(self, mock_get, client):
        """Test 500 Server Error handling."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response

        with pytest.raises(PinboardServerError, match="Server Error \\(500\\)"):
            client._request("GET", "hello")

    @patch("requests.Session.get")
    def test_request_network_error(self, mock_get, client):
        """Test network error handling."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

        with pytest.raises(PinboardAPIError, match="A network error occurred"):
            client._request("GET", "hello")

    def test_request_unsupported_method(self, client):
        """Test unsupported HTTP method."""
        with pytest.raises(ValueError, match="Unsupported HTTP method: PATCH"):
            client._request("PATCH", "hello")

    @patch.object(PinboardClient, "_request")
    def test_hello(self, mock_request, client):
        """Test hello method."""
        mock_request.return_value = {"result": "ok"}

        result = client.hello()

        assert result == {"result": "ok"}
        mock_request.assert_called_once_with("GET", "hello")

    @patch.object(PinboardClient, "_request")
    def test_last_update(self, mock_request, client):
        """Test last_update method."""
        expected_response = {
            "last_update": "2023-01-01T12:00:00Z",
            "last_update_notes": "2023-01-01T11:00:00Z",
        }
        mock_request.return_value = expected_response

        result = client.last_update()

        assert result == expected_response
        mock_request.assert_called_once_with("GET", "last_update")


class TestBookmarkMethods:
    """Test suite for bookmark-related methods."""

    @pytest.fixture
    def client(self):
        """Create a PinboardClient instance for testing."""
        return PinboardClient("test_user:test_token")

    @patch.object(PinboardClient, "_request")
    def test_get_bookmarks_default(self, mock_request, client):
        """Test get_bookmarks with default parameters."""
        expected_response = {"bookmarks": []}
        mock_request.return_value = expected_response

        result = client.get_bookmarks()

        assert result == expected_response
        mock_request.assert_called_once_with(
            "GET", "bookmarks", params={"count": 25, "offset": 0}
        )

    @patch.object(PinboardClient, "_request")
    def test_get_bookmarks_with_ids(self, mock_request, client):
        """Test get_bookmarks with bookmark IDs."""
        expected_response = {"bookmarks": []}
        mock_request.return_value = expected_response

        result = client.get_bookmarks(ids=["123", "456"])

        assert result == expected_response
        mock_request.assert_called_once_with(
            "GET", "bookmarks", params={"ids": "123,456"}
        )

    @patch.object(PinboardClient, "_request")
    def test_get_bookmarks_with_url(self, mock_request, client):
        """Test get_bookmarks with URL filter."""
        expected_response = {"bookmarks": []}
        mock_request.return_value = expected_response

        result = client.get_bookmarks(url="https://example.com")

        assert result == expected_response
        mock_request.assert_called_once_with(
            "GET", "bookmarks", params={"url": "https://example.com"}
        )

    @patch.object(PinboardClient, "_request")
    def test_get_bookmarks_with_filters(self, mock_request, client):
        """Test get_bookmarks with various filters."""
        expected_response = {"bookmarks": []}
        mock_request.return_value = expected_response

        start_date = datetime.datetime(2023, 1, 1)
        end_date = datetime.datetime(2023, 12, 31)

        result = client.get_bookmarks(
            tags=["python", "api"],
            start_date=start_date,
            end_date=end_date,
            filter_string="private",
            count=50,
            offset=10,
        )

        assert result == expected_response
        mock_request.assert_called_once_with(
            "GET",
            "bookmarks",
            params={
                "tags": "python,api",
                "start_date": "2023-01-01T00:00:00",
                "end_date": "2023-12-31T00:00:00",
                "filter": "private",
                "count": 50,
                "offset": 10,
            },
        )

    @patch.object(PinboardClient, "_request")
    def test_get_bookmarks_count_limit(self, mock_request, client):
        """Test get_bookmarks count is limited to 1000."""
        expected_response = {"bookmarks": []}
        mock_request.return_value = expected_response

        result = client.get_bookmarks(count=2000)

        assert result == expected_response
        mock_request.assert_called_once_with(
            "GET", "bookmarks", params={"count": 1000, "offset": 0}
        )

    @patch.object(PinboardClient, "_request")
    def test_get_all_bookmarks(self, mock_request, client):
        """Test get_all_bookmarks method."""
        expected_response = {"bookmarks": []}
        mock_request.return_value = expected_response

        result = client.get_all_bookmarks()

        assert result == expected_response
        mock_request.assert_called_once_with("GET", "bookmarks/all")

    @patch.object(PinboardClient, "_request")
    def test_get_bookmark_by_id(self, mock_request, client):
        """Test get_bookmark_by_id method."""
        expected_response = {"bookmark": {"id": "123", "url": "https://example.com"}}
        mock_request.return_value = expected_response

        result = client.get_bookmark_by_id("123")

        assert result == expected_response
        mock_request.assert_called_once_with("GET", "bookmarks/123")

    @patch.object(PinboardClient, "_request")
    def test_add_bookmark_minimal(self, mock_request, client):
        """Test add_bookmark with minimal parameters."""
        expected_response = {"result": "ok", "bookmark_id": "123"}
        mock_request.return_value = expected_response

        result = client.add_bookmark("https://example.com", "Test Title")

        assert result == expected_response
        mock_request.assert_called_once_with(
            "POST",
            "bookmarks",
            data={
                "url": "https://example.com",
                "title": "Test Title",
                "private": "no",
                "toread": "no",
                "exact_url": "no",
            },
        )

    @patch.object(PinboardClient, "_request")
    def test_add_bookmark_full(self, mock_request, client):
        """Test add_bookmark with all parameters."""
        expected_response = {"result": "ok", "bookmark_id": "123"}
        mock_request.return_value = expected_response

        created_date = datetime.datetime(2023, 1, 1, 12, 0, 0)

        result = client.add_bookmark(
            url="https://example.com",
            title="Test Title",
            description="Test Description",
            created=created_date,
            tags=["python", "api"],
            private=True,
            toread=True,
            exact_url=True,
        )

        assert result == expected_response
        mock_request.assert_called_once_with(
            "POST",
            "bookmarks",
            data={
                "url": "https://example.com",
                "title": "Test Title",
                "description": "Test Description",
                "created": "2023-01-01T12:00:00",
                "tags": "python,api",
                "private": "yes",
                "toread": "yes",
                "exact_url": "yes",
            },
        )

    @patch.object(PinboardClient, "_request")
    def test_update_bookmark_minimal(self, mock_request, client):
        """Test update_bookmark with minimal parameters."""
        expected_response = {"result": "ok"}
        mock_request.return_value = expected_response

        result = client.update_bookmark("123", title="New Title")

        assert result == expected_response
        mock_request.assert_called_once_with(
            "POST", "bookmarks/123", data={"title": "New Title"}
        )

    def test_update_bookmark_no_fields(self, client):
        """Test update_bookmark raises error when no fields provided."""
        with pytest.raises(ValueError, match="No fields provided for update"):
            client.update_bookmark("123")

    @patch.object(PinboardClient, "_request")
    def test_update_bookmark_full(self, mock_request, client):
        """Test update_bookmark with all parameters."""
        expected_response = {"result": "ok"}
        mock_request.return_value = expected_response

        created_date = datetime.datetime(2023, 1, 1, 12, 0, 0)

        result = client.update_bookmark(
            bookmark_id="123",
            url="https://newexample.com",
            title="New Title",
            description="New Description",
            created=created_date,
            tags=["new", "tags"],
            private=False,
            toread=False,
            exact_url=True,
        )

        assert result == expected_response
        mock_request.assert_called_once_with(
            "POST",
            "bookmarks/123",
            data={
                "url": "https://newexample.com",
                "title": "New Title",
                "description": "New Description",
                "created": "2023-01-01T12:00:00",
                "tags": "new,tags",
                "private": "no",
                "toread": "no",
                "exact_url": "yes",
            },
        )

    @patch.object(PinboardClient, "_request")
    def test_update_bookmark_empty_tags(self, mock_request, client):
        """Test update_bookmark with empty tags list."""
        expected_response = {"result": "ok"}
        mock_request.return_value = expected_response

        result = client.update_bookmark("123", tags=[])

        assert result == expected_response
        mock_request.assert_called_once_with("POST", "bookmarks/123", data={"tags": ""})

    @patch.object(PinboardClient, "_request")
    def test_delete_bookmark(self, mock_request, client):
        """Test delete_bookmark method."""
        expected_response = {"result": "ok"}
        mock_request.return_value = expected_response

        result = client.delete_bookmark("123")

        assert result == expected_response
        mock_request.assert_called_once_with("DELETE", "bookmarks/123")

    @patch.object(PinboardClient, "_request")
    def test_batch_delete_bookmarks(self, mock_request, client):
        """Test batch_delete_bookmarks method."""
        expected_response = {"result": "ok"}
        mock_request.return_value = expected_response

        result = client.batch_delete_bookmarks(["123", "456", "789"])

        assert result == expected_response
        mock_request.assert_called_once_with(
            "POST", "bookmarks/delete", data={"ids": "123,456,789"}
        )

    def test_batch_delete_bookmarks_empty_list(self, client):
        """Test batch_delete_bookmarks with empty list."""
        with pytest.raises(ValueError, match="Must provide 1 to 100 bookmark IDs"):
            client.batch_delete_bookmarks([])

    def test_batch_delete_bookmarks_too_many(self, client):
        """Test batch_delete_bookmarks with too many IDs."""
        bookmark_ids = [str(i) for i in range(101)]
        with pytest.raises(ValueError, match="Must provide 1 to 100 bookmark IDs"):
            client.batch_delete_bookmarks(bookmark_ids)


class TestTagMethods:
    """Test suite for tag-related methods."""

    @pytest.fixture
    def client(self):
        """Create a PinboardClient instance for testing."""
        return PinboardClient("test_user:test_token")

    @patch.object(PinboardClient, "_request")
    def test_get_tags_default(self, mock_request, client):
        """Test get_tags with default parameters."""
        expected_response = {"python": 10, "api": 5}
        mock_request.return_value = expected_response

        result = client.get_tags()

        assert result == expected_response
        mock_request.assert_called_once_with("GET", "tags", params={})

    @patch.object(PinboardClient, "_request")
    def test_get_tags_with_cutoff(self, mock_request, client):
        """Test get_tags with cutoff parameter."""
        expected_response = {"python": 10}
        mock_request.return_value = expected_response

        result = client.get_tags(cutoff=8)

        assert result == expected_response
        mock_request.assert_called_once_with("GET", "tags", params={"cutoff": 8})

    @patch.object(PinboardClient, "_request")
    def test_rename_tags(self, mock_request, client):
        """Test rename_tags method."""
        expected_response = {"result": "ok"}
        mock_request.return_value = expected_response

        result = client.rename_tags("old_tag", "new_tag")

        assert result == expected_response
        mock_request.assert_called_once_with(
            "POST", "tags/rename", data={"old": "old_tag", "new": "new_tag"}
        )

    @patch.object(PinboardClient, "_request")
    def test_delete_tags(self, mock_request, client):
        """Test delete_tags method."""
        expected_response = {"result": "ok"}
        mock_request.return_value = expected_response

        result = client.delete_tags(["tag1", "tag2", "tag3"])

        assert result == expected_response
        mock_request.assert_called_once_with(
            "POST", "tags/delete", data={"tags": "tag1,tag2,tag3"}
        )

    def test_delete_tags_empty_list(self, client):
        """Test delete_tags with empty list."""
        with pytest.raises(ValueError, match="Must provide 1 to 100 tags"):
            client.delete_tags([])

    def test_delete_tags_too_many(self, client):
        """Test delete_tags with too many tags."""
        tags = [f"tag{i}" for i in range(101)]
        with pytest.raises(ValueError, match="Must provide 1 to 100 tags"):
            client.delete_tags(tags)


class TestNoteMethods:
    """Test suite for note-related methods."""

    @pytest.fixture
    def client(self):
        """Create a PinboardClient instance for testing."""
        return PinboardClient("test_user:test_token")

    @patch.object(PinboardClient, "_request")
    def test_get_notes_default(self, mock_request, client):
        """Test get_notes with default parameters."""
        expected_response = {"notes": []}
        mock_request.return_value = expected_response

        result = client.get_notes()

        assert result == expected_response
        mock_request.assert_called_once_with(
            "GET", "notes", params={"count": 25, "offset": 0}
        )

    @patch.object(PinboardClient, "_request")
    def test_get_notes_with_params(self, mock_request, client):
        """Test get_notes with custom parameters."""
        expected_response = {"notes": []}
        mock_request.return_value = expected_response

        result = client.get_notes(count=50, offset=10)

        assert result == expected_response
        mock_request.assert_called_once_with(
            "GET", "notes", params={"count": 50, "offset": 10}
        )

    @patch.object(PinboardClient, "_request")
    def test_get_notes_count_limit(self, mock_request, client):
        """Test get_notes count is limited to 100."""
        expected_response = {"notes": []}
        mock_request.return_value = expected_response

        result = client.get_notes(count=200)

        assert result == expected_response
        mock_request.assert_called_once_with(
            "GET", "notes", params={"count": 100, "offset": 0}
        )

    @patch.object(PinboardClient, "_request")
    def test_get_note_by_id(self, mock_request, client):
        """Test get_note_by_id method."""
        expected_response = {"note": {"id": "123", "title": "Test Note"}}
        mock_request.return_value = expected_response

        result = client.get_note_by_id("123")

        assert result == expected_response
        mock_request.assert_called_once_with("GET", "notes/123")

    @patch.object(PinboardClient, "_request")
    def test_create_note_minimal(self, mock_request, client):
        """Test create_note with minimal parameters."""
        expected_response = {"result": "ok", "note_id": "123"}
        mock_request.return_value = expected_response

        result = client.create_note("Test Title", "Test Body")

        assert result == expected_response
        mock_request.assert_called_once_with(
            "POST",
            "notes",
            data={"title": "Test Title", "note": "Test Body", "use_markdown": "no"},
        )

    @patch.object(PinboardClient, "_request")
    def test_create_note_with_markdown(self, mock_request, client):
        """Test create_note with markdown enabled."""
        expected_response = {"result": "ok", "note_id": "123"}
        mock_request.return_value = expected_response

        result = client.create_note("Test Title", "# Test Body", use_markdown=True)

        assert result == expected_response
        mock_request.assert_called_once_with(
            "POST",
            "notes",
            data={"title": "Test Title", "note": "# Test Body", "use_markdown": "yes"},
        )

    @patch.object(PinboardClient, "_request")
    def test_update_note_minimal(self, mock_request, client):
        """Test update_note with minimal parameters."""
        expected_response = {"result": "ok"}
        mock_request.return_value = expected_response

        result = client.update_note("123", title="New Title")

        assert result == expected_response
        mock_request.assert_called_once_with(
            "POST", "notes/123", data={"title": "New Title"}
        )

    def test_update_note_no_fields(self, client):
        """Test update_note raises error when no fields provided."""
        with pytest.raises(ValueError, match="No fields provided for update"):
            client.update_note("123")

    @patch.object(PinboardClient, "_request")
    def test_update_note_full(self, mock_request, client):
        """Test update_note with all parameters."""
        expected_response = {"result": "ok"}
        mock_request.return_value = expected_response

        result = client.update_note(
            note_id="123", title="New Title", body="New Body", use_markdown=True
        )

        assert result == expected_response
        mock_request.assert_called_once_with(
            "POST",
            "notes/123",
            data={"title": "New Title", "note": "New Body", "use_markdown": "yes"},
        )

    @patch.object(PinboardClient, "_request")
    def test_delete_note(self, mock_request, client):
        """Test delete_note method."""
        expected_response = {"result": "ok"}
        mock_request.return_value = expected_response

        result = client.delete_note("123")

        assert result == expected_response
        mock_request.assert_called_once_with("DELETE", "notes/123")
