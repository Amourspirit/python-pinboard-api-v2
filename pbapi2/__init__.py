"""
Pinboard API V2 Python Client

A Python client for interacting with the Pinboard V2 API.

Copyright (c) 2025 :Barry-Thomas-Paul: Moss
Licensed under the MIT License - see LICENSE file for details.

API Reference: https://pinboard.in/api/v2/reference/
"""

from .pinboard_api import (
    # Main client class
    PinboardClient,
    # Exception classes
    PinboardAPIError,
    PinboardBadRequestError,
    PinboardUnauthorizedError,
    PinboardForbiddenError,
    PinboardNotFoundError,
    PinboardRateLimitExceededError,
    PinboardServerError,
)

# Define what gets imported with "from pbapi2 import *"
__all__ = [
    # Main client class
    "PinboardClient",
    # Exception classes
    "PinboardAPIError",
    "PinboardBadRequestError",
    "PinboardUnauthorizedError",
    "PinboardForbiddenError",
    "PinboardNotFoundError",
    "PinboardRateLimitExceededError",
    "PinboardServerError",
]

# Package metadata
__version__ = "0.0.3"
__author__ = ":Barry-Thomas-Paul: Moss"
__email__ = "pinboardapi2@pm.amourspirit.net"
__license__ = "MIT"
