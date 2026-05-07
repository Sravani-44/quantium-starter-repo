
#!/bin/bash

# Quantium - CI Test Runner Script
# Activates virtual environment and runs the test suite
# Returns 0 if all tests pass, 1 if anything fails

echo "Starting Quantium test suite..."

# Step 1: Activate virtual environment
source venv/Scripts/activate

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

echo "Virtual environment activated."

# Step 2: Run the test suite
python -m pytest test_dash.py -v

# Step 3: Capture result and return correct exit code
if [ $? -eq 0 ]; then
    echo "All tests passed!"
    exit 0
else
    echo "Some tests failed!"
    exit 1
fi