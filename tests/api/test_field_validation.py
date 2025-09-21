import pytest

from tests.models import HeroSearchResponse
from tests.utils import build_search_url


class TestFieldValidation:

    @pytest.mark.validation
    def test_search_hero_success(self, session, base_url, access_token):
        """
            Test: Search for a hero by name (Batman).

            Purpose:
                Validate that the search endpoint returns a successful response
                and the results contain at least one matching hero.

            Steps:
                1. Build the search URL for 'Batman'.
                2. Send GET request to the API.
                3. Validate response status code (200).
                4. Parse JSON into `HeroSearchResponse`.
                5. Verify the response indicates success and results are non-empty.

            Expected Result:
                - Status code is 200.
                - `response` field is "success".
                - Results list contains at least one hero.
        """
        url = build_search_url(base_url, access_token, "Batman")
        response = session.get(url)

        # Check that the response is successful
        assert response.status_code == 200, "API returned an error"

        # Validate the response model
        response_model = HeroSearchResponse.model_validate(response.json())
        assert response_model.response == "success", "Search was not successful"
        assert len(response_model.results) > 0, "No results returned"

    @pytest.mark.validation
    def test_field_level_validation(self, session, base_url, access_token):
        """
            Test: Validate hero fields in search results (Superman).

            Purpose:
                Ensure that all critical fields returned for each hero
                are present, correctly typed, and valid.

            Steps:
                1. Search for "Superman".
                2. Parse response into `HeroSearchResponse`.
                3. For each hero in results:
                    - Powerstats: all values are integers >= 0.
                    - Biography:
                        * aliases is a non-empty list.
                        * publisher is a non-empty string.
                    - Appearance:
                        * gender in ["Male", "Female", "-", "Other"].
                        * race is a non-empty string.
                        * height and weight are non-empty lists.
                    - Work:
                        * occupation is a non-empty string.
                    - Connections:
                        * group_affiliation is a non-empty string.
                    - Image:
                        * url starts with "http".

            Expected Result:
                All fields pass validation checks for every hero.
        """
        url = build_search_url(base_url, access_token, "Superman")
        response = session.get(url)

        # Parse response into model
        response_model = HeroSearchResponse.model_validate(response.json())

        for hero in response_model.results:
            # 1. Powerstats
            for stat_name, stat_value in hero.powerstats.model_dump().items():
                assert isinstance(stat_value, int) and stat_value >= 0, \
                    f"{stat_name} must be >=0, got {stat_value} for hero {hero.name}"

            # 2. Biography
            assert isinstance(hero.biography.aliases, list) and len(
                hero.biography.aliases) > 0, \
                f"aliases must be a non-empty list for hero {hero.name}"
            assert isinstance(
                hero.biography.publisher,
                str
            ) and hero.biography.publisher.strip() != "", \
                f"publisher must be a non-empty string for hero {hero.name}"

            # 3. Appearance
            assert hero.appearance.gender in ["Male", "Female", "-", "Other"], \
                f"Invalid gender value: {hero.appearance.gender}"
            assert isinstance(
                hero.appearance.race,
                str
            ) and hero.appearance.race.strip() != "", \
                "race must be a non-empty string"
            assert isinstance(hero.appearance.height, list) and len(
                hero.appearance.height) > 0, \
                f"height must contain at least one entry for {hero.name}"
            assert isinstance(hero.appearance.weight, list) and len(
                hero.appearance.weight) > 0, \
                f"weight must contain at least one entry for {hero.name}"

            # 4. Work
            assert isinstance(
                hero.work.occupation,
                str
            ) and hero.work.occupation.strip() != "", \
                "occupation must be a non-empty string"

            # 5. Connections
            assert isinstance(
                hero.connections.group_affiliation,
                str
            ) and hero.connections.group_affiliation.strip() != "", \
                "group_affiliation must be a non-empty string"

            # 6. Image
            assert str(hero.image.url).startswith("http"), \
                f"Invalid image URL for hero {hero.name}: {hero.image.url}"
