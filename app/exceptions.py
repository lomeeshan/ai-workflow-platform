class LLMServiceError(Exception):
    """
    Raised when the LLM provider fails or cannot return usable output.
    """
    pass


class InvalidLLMResponseError(Exception):
    """
    Raised when the LLM returns malformed JSON or data that does not match our schema.
    """
    pass


class DatabaseOperationError(Exception):
    """
    Raised when a database operation fails unexpectedly.
    """
    pass


