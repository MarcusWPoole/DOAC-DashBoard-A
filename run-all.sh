#!/usr/bin/env bash
# run-all.sh

# Launch backend in the background
(cd backend && ./run.sh) &

# Give backend a moment to start (optional)
sleep 2

# Launch frontend
(cd frontend && npm run dev)
