import pytest

from tests.utils import build_search_url, is_not_found_error, get_invalid_tokens


class TestSearchEndpoint:

    @pytest.mark.search_test
    @pytest.mark.parametrize(
        "name, expected_substring",
        [
            ("Batman", "Batman"),
            ("Iron Man", "Iron Man"),
            ("Black Panther", "Panther"),
        ],
        ids=["batman", "iron_man", "black_panther"]
    )
    def test_valid_name_search(self, session, base_url, access_token, name,
                               expected_substring):
        """Positive test: valid hero names return results."""
        url = build_search_url(base_url, access_token, name)
        resp = session.get(url)
        assert resp.status_code == 200, \
            f"Status code != 200 for name '{name}', got {resp.status_code}"
        data = resp.json()
        assert "results" in data, f"'results' key missing in response for name '{name}'"
        assert any(
            expected_substring.lower() in hero.get(
                "name",
                ""
            ).lower() for hero in data["results"]
        ), (
            f"Expected substring '{expected_substring}"
            f"' not found in any result for name '{name}'"
        )

    @pytest.mark.search_test
    @pytest.mark.parametrize(
        "name",
        [
            "NonExistentHeroNameXYZ",
            "",
            "1234567890",
            "😀😂🤣",
            "       ",
            "!@#$%^&*()",
        ],
        ids=["no_such_name", "empty_string", "digits_only", "emojis", "spaces_only",
             "special_symbols"]
    )
    def test_no_results_error_message(self, session, base_url, access_token, name):
        """
        Negative test: invalid hero names
         should return 'character not found' error.
         """
        url = build_search_url(base_url, access_token, name)
        resp = session.get(url)
        data = resp.json()
        assert is_not_found_error(data), \
            f"Expected not found error for name '{name}', got {data}"

    @pytest.mark.search_test
    @pytest.mark.parametrize(
        "name",
        [
            "!@#$%^&*()_+-=[]{};':,./<>?",
            "test!@#",
            "名前",
            "John_Doe",
            "Name-With-Hyphens",
        ],
        ids=["special_chars", "special_ascii", "unicode_chars", "underscore", "hyphens"]
    )
    def test_special_characters_error(self, session, base_url, access_token, name):
        """Negative test: special characters or unusual names should return an error."""
        url = build_search_url(base_url, access_token, name)
        resp = session.get(url)
        data = resp.json()
        assert is_not_found_error(data), \
            f"Expected not found error for special name '{name}', got {data}"

    @pytest.mark.search_test
    @pytest.mark.parametrize(
        "invalid_token",
        [
            "0000000000000000",
            "invalidtoken12345",
            "",
            "null",
            "@#$%^&*",
        ],
        ids=["all_zeroes", "random_string", "empty_token", "null_token",
             "special_chars_token"]
    )
    def test_invalid_token(self, session, base_url, invalid_token):
        """Negative test: invalid token should return an error."""
        name = "Batman"
        url = build_search_url(base_url, invalid_token, name)
        resp = session.get(url)
        data = resp.json()
        assert get_invalid_tokens(data), \
            f"Expected error response for bad token '{invalid_token}', got {data}"

    @pytest.mark.search_test
    @pytest.mark.parametrize(
        "name_segment",
        [
            None,
            "",
            "   ",
            "!@#",
        ],
        ids=["segment_none", "segment_empty", "segment_spaces", "segment_special_chars"]
    )
    def test_missing_or_invalid_name_segment(
            self,
            session,
            base_url,
            access_token,
            name_segment
    ):
        """
        Negative test: missing or invalid name segment
         in URL should return an error.
         """
        if name_segment is None:
            url = f"{base_url}/{access_token}/search/"
        else:
            url = build_search_url(base_url, access_token, name_segment)
        resp = session.get(url)
        data = resp.json()
        assert is_not_found_error(data), \
            f"Expected error response for name segment '{name_segment}', got {data}"
