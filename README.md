# API Testing Project
Automated tests for the [Superhero API](https://superheroapi.com/), 
built with **pytest** and **Pydantic** for response schema validation.

## Project Structure
```
api-testing-project/
├── tests/
│   ├── api/
│   │   ├── test_field_validation.py
│   │   └── test_search.py
│   ├── conftest.py
│   ├── utils.py
│   └── models.py
├── .env.example
├── reports/
│   └── (generated test reports)
├── pytest.ini
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup Instructions
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Andrii-Bezkrovnyi/api_tests.git
    cd api-tests
    ```
2. **Create a virtual environment**:
    ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables**:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
     - Add your Superhero API access token to the `.env` file:
       ```
       ACCESS_TOKEN=your_access_token_here
       ```
5. **Run tests**:
    ```bash
    pytest
    ```
6. Run tests only for search name endpoint:
    ```bash
    pytest -m search_test
    ``` 
7. Run tests only for field validation:
    ```bash
    pytest -m validation
    ```
8. Check the report in the `reports/` directory after test execution.
