#!/bin/bash
echo "PROSPECTOR:" && prospector -0 backend && echo "BANDIT:" && bandit -r backend
