#!/bin/sh

set -e

rm -rf ./test-venv

virtualenv --no-site-packages ./test-venv
echo 'Installing packages...'
./test-venv/bin/pip -q install --download-cache "${HOME}/bundles/${JOB_NAME}" -r test-requirements.txt

echo 'Running tests...'
PYTHONPATH=. ./test-venv/bin/nosetests

echo 'Done'
rm -rf ./test-venv
exit 0
