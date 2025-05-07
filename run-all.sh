#!/usr/bin/env bash
# run-all.sh

# Launch backend in the background
(cd back-end && ./run.sh) &

# Give backend a moment to start (optional)
sleep 2

# Launch frontend
(cd front-end && npm install && npm run dev)
