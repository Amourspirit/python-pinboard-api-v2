# Pinboard API Tests

This directory contains comprehensive tests for the Pinboard API Python wrapper.

## Test Structure

The tests are organized into several test classes:

- **`TestPinboardClient`**: Tests for the main client class initialization and core functionality
- **`TestBookmarkMethods`**: Tests for all bookmark-related operations
- **`TestTagMethods`**: Tests for tag management operations  
- **`TestNoteMethods`**: Tests for note management operations

## Running Tests

### Basic Test Run

```bash
# From the project root directory
python -m pytest tests/test_pinboard_api.py -v
```

### Using the Test Runner Script

```bash
# Basic test run
python run_tests.py

# With coverage report
python run_tests.py --coverage
```

### Running Specific Test Classes

```bash
# Run only bookmark tests
python -m pytest tests/test_pinboard_api.py::TestBookmarkMethods -v

# Run only tag tests
python -m pytest tests/test_pinboard_api.py::TestTagMethods -v

# Run only note tests
python -m pytest tests/test_pinboard_api.py::TestNoteMethods -v
```

### Running Individual Tests

```bash
# Run a specific test
python -m pytest tests/test_pinboard_api.py::TestPinboardClient::test_hello -v
```

## Test Coverage

The test suite covers:

### Core Functionality
- ✅ Client initialization (production and test modes)
- ✅ HTTP request handling (GET, POST, DELETE)
- ✅ Error handling for all HTTP status codes (400, 401, 403, 404, 429, 5xx)
- ✅ Network error handling
- ✅ Authentication token handling

### Bookmark Operations
- ✅ Get bookmarks with various filters
- ✅ Get all bookmarks
- ✅ Get bookmark by ID
- ✅ Add bookmarks (minimal and full parameters)
- ✅ Update bookmarks (with validation)
- ✅ Delete individual bookmarks
- ✅ Batch delete bookmarks (with validation)

### Tag Operations
- ✅ Get tags with optional cutoff
- ✅ Rename tags
- ✅ Delete tags (with validation)

### Note Operations
- ✅ Get notes with pagination
- ✅ Get note by ID
- ✅ Create notes (with and without markdown)
- ✅ Update notes (with validation)
- ✅ Delete notes

### Utility Methods
- ✅ Hello endpoint (connectivity check)
- ✅ Last update timestamps

## Test Features

- **Mocking**: All tests use mocks to avoid making real API calls
- **Error Testing**: Comprehensive error condition testing
- **Parameter Validation**: Tests for input validation and edge cases
- **Response Validation**: Ensures correct API calls are made with proper parameters

## Dependencies

The tests require:
- `pytest` - Testing framework
- `unittest.mock` - For mocking HTTP requests (built into Python)

Optional for coverage:
- `pytest-cov` - For coverage reports

## Test Data

All tests use mock data and don't require real Pinboard API credentials. The tests verify:
- Correct API endpoints are called
- Proper HTTP methods are used
- Parameters are formatted correctly
- Error conditions are handled appropriately

## Adding New Tests

When adding new functionality to the Pinboard API client:

1. Add the corresponding test method to the appropriate test class
2. Use `@patch.object(PinboardClient, '_request')` to mock the HTTP request
3. Test both success and error conditions
4. Verify the correct API endpoint and parameters are used
5. Run the full test suite to ensure no regressions
