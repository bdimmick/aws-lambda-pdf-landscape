#!/usr/bin/env bash

# Clean up from previous failed runs.
rm -rf ./package
rm -rf ./lambda_function.zip

# Install dependencies
pip install -r requirements.txt --target ./package --trusted-host pypi.python.org

# Package up Lambda
cd package
zip ../lambda_function.zip *
cd ..
rm -rf ./package
zip lambda_function.zip lambda_function.py
sleep 5