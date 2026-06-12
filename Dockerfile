# Build frontend with Node, then build runtime image with Python
FROM node:20-alpine AS node_builder
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json* ./frontend/
COPY frontend/ ./frontend/
WORKDIR /app/frontend
RUN npm ci --legacy-peer-deps || npm ci
RUN npm run build || true
# Try to export static site; some Next.js configs may not support export.
RUN npx next export || true

FROM python:3.11-slim
WORKDIR /app
COPY . /app
# Copy built frontend static files from node build stage
COPY --from=node_builder /app/frontend/out /app/frontend/out

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r backend/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
