def build_search_url(base_url: str, access_token: str, name: str) -> str:
    """
    Build the full search URL for querying the Superhero API.

    Args:
        base_url (str): Base URL of the API ("https://www.superheroapi.com/api.php").
        access_token (str): API access token for authentication.
        name (str): Name of the superhero to search for.

    Returns:
        str: A formatted URL string that can be used to perform the API request.
    """
    return f"{base_url}/{access_token}/search/{name}"


def is_not_found_error(data: dict) -> bool:
    """
    Check if the given API response corresponds to an error when
    a character name cannot be found or the search request is invalid.

    Args:
        data (dict): The JSON response from the API.

    Returns:
        bool: True if the response matches the expected "not found" or
              "bad name" error formats, False otherwise.
    """
    expected_character_error = {
        "response": "error",
        "error": "character with given name not found"
    }
    expected_name_error = {
        "response": "error",
        "error": "bad name search request"
    }
    return data == expected_character_error or data == expected_name_error


def get_invalid_tokens(data: dict) -> bool:
    """
       Check if the given API response corresponds to an invalid
       or unauthorized access token.

       Args:
           data (dict): The JSON response from the API.

       Returns:
           bool: True if the response matches the expected "access denied" error,
                 False otherwise.
       """
    expected_result = {"response": "error", "error": "access denied"}
    return data == expected_result
