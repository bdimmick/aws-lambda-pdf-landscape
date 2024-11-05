#!/usr/bin/env bash

rm -rf ./package
rm -rf ./lambda_function.zip

pip install -r requirements.txt --target ./package --trusted-host pypi.python.org
cd package
zip ../lambda_function.zip *
cd ..
# rm -rf ./package
zip lambda_function.zip lambda_function.py
sleep 5