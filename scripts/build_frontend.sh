#!/usr/bin/env bash
set -e

cd frontend
npm ci --legacy-peer-deps || npm ci
npm run build
# Export static site to frontend/out (may be no-op if not supported)
npx next export || true
