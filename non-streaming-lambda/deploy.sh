#!/bin/bash

# Create deployment package
echo "Creating Lambda deployment package..."

# Create temporary directory
mkdir -p lambda-package

# Copy app.py
cp app.py lambda-package/

# Install dependencies to package directory
pip install -r requirements.txt -t lambda-package/

# Create zip file
cd lambda-package
zip -r ../nova-lambda.zip .
cd ..

# Clean up
rm -rf lambda-package