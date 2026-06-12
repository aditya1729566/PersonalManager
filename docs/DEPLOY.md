# Deployment

This repository includes a Dockerfile for the FastAPI backend and a Next.js frontend. The GitHub Actions workflow `.github/workflows/ci-build-and-publish.yml` will build a Docker image and push it to GitHub Container Registry (GHCR) when you push to `main` or `clean-main`.

Quick steps to make the build publish succeed:

1. In the repository settings, enable Actions to allow `packages: write` for the `GITHUB_TOKEN` (default is usually fine).
2. Push to `clean-main` or `main` to trigger the workflow; the image will be published as:

   `ghcr.io/<your-github-username>/<repo-name>:latest`

Deploying the image to a hosting provider (Render / Fly / Railway / DigitalOcean App Platform):

- Create a new web service on your provider and select "Deploy from a container registry" (or point it to a Dockerfile).
- Use the image URL from GHCR (example: `ghcr.io/aditya1729566/PersonalManager:latest`).
- Set environment variables (example `.env.example`):

  - `DATABASE_URL` — e.g. `sqlite:////data/kanban.db` or a PostgreSQL URL
  - `OPENROUTER_API_KEY` — (if you want AI features)
  - Any other secrets your deployment needs

Notes and next steps:

- For a one-click deploy, Render can use the Dockerfile in the repo and will build the image on their side; you can also point it to the GHCR image above.
- Consider switching password hashing to `bcrypt` for production.
- Remove any large test artifacts (`frontend/.ms-playwright`, `frontend/test-results`, `data/kanban.db`) from the published history if you care about repository size; consider using `git filter-repo` or the BFG repo cleaner to rewrite history.
