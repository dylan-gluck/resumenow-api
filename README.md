# ResumeNow: API

Backend service for the ResumeNow application.

## Endpoints

- `/api/parse` Parse a document into a type-safe Resume JSON object.
- `/api/format` Reformat a Resume object based on provided job description string.

## Running the API locally

```bash
uv run fastapi dev
```

## Running tests

```bash
uv run pytest
```
