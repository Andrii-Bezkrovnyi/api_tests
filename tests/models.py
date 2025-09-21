from typing import List
from pydantic import BaseModel, Field, HttpUrl, field_validator


class Image(BaseModel):
    """Hero image model with a validated URL."""

    url: HttpUrl = Field(alias='url')
    model_config = {"populate_by_name": True}


class Biography(BaseModel):
    """Biography details of a hero."""
    full_name: str = Field(alias='full-name')
    alter_egos: str = Field(alias='alter-egos')
    aliases: List[str]
    place_of_birth: str = Field(alias='place-of-birth')
    first_appearance: str = Field(alias='first-appearance')
    publisher: str
    alignment: str

    model_config = {"populate_by_name": True}

    @field_validator('full_name', 'alter_egos', 'place_of_birth', 'first_appearance',
                     'publisher', 'alignment')
    def non_empty_strings(cls, value):
        if not value.strip():
            raise ValueError('Field must not be empty')
        return value

    @field_validator('aliases')
    def aliases_not_empty(cls, value):
        if not value:
            raise ValueError('Aliases list must not be empty')
        return value


class Appearance(BaseModel):
    """Physical appearance attributes of a hero."""
    gender: str
    race: str
    height: List[str]
    weight: List[str]
    eye_color: str = Field(alias='eye-color')
    hair_color: str = Field(alias='hair-color')

    model_config = {"populate_by_name": True}

    @field_validator('gender', 'race', 'eye_color', 'hair_color')
    def non_empty_strings(cls, value):
        if not value.strip():
            raise ValueError('Field must not be empty')
        return value

    @field_validator('height', 'weight')
    def non_empty_lists(cls, value):
        if not value or not all(isinstance(i, str) and i.strip() for i in value):
            raise ValueError('Height and weight lists must contain non-empty strings')
        return value


class Work(BaseModel):
    """Work information about a hero."""
    occupation: str
    base: str

    model_config = {"populate_by_name": True}

    @field_validator('occupation', 'base')
    def non_empty_strings(cls, value):
        if not value.strip():
            raise ValueError('Field must not be empty')
        return value


class Connections(BaseModel):
    """Connections and relationships of a hero."""
    group_affiliation: str = Field(alias='group-affiliation')
    relatives: str

    model_config = {"populate_by_name": True}

    @field_validator('group_affiliation', 'relatives')
    def non_empty_strings(cls, value):
        if not value.strip():
            raise ValueError('Field must not be empty')
        return value


class Powerstats(BaseModel):
    """Hero power statistics, must be non-negative integers."""
    intelligence: int
    strength: int
    speed: int
    durability: int
    power: int
    combat: int

    model_config = {"populate_by_name": True}

    @field_validator('*', mode='before')
    def check_positive(cls, value):
        if int(value) < 0:
            raise ValueError('Powerstats values must be >= 0')
        return int(value)


class Hero(BaseModel):
    """Top-level hero model."""
    id: int
    name: str
    powerstats: Powerstats
    biography: Biography
    appearance: Appearance
    work: Work
    connections: Connections
    image: Image

    model_config = {"populate_by_name": True}

    @field_validator('name')
    def name_not_empty(cls, value):
        if not value.strip():
            raise ValueError('Hero name must not be empty')
        return value


class HeroSearchResponse(BaseModel):
    """Search response model for heroes."""
    response: str
    results_for: str = Field(alias='results-for')
    results: List[Hero]

    model_config = {"populate_by_name": True}

    @field_validator('response', 'results_for')
    def non_empty_strings(cls, value):
        if not value.strip():
            raise ValueError('Field must not be empty')
        return value
