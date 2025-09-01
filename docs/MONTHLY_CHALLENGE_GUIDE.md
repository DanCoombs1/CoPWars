# Monthly Challenge Upload Guide

This guide shows you how to upload a new monthly challenge to your coding platform.

## Quick Setup

No dependencies needed! The script uses only Python's built-in libraries.

## How to Upload a Monthly Challenge

### Step 1: Edit the Script
Open `upload-monthly-challenge.py` and edit these variables at the top:

```python
# Challenge ID (format: YYYY-MM)
CHALLENGE_ID = "2025-01"  # Change this each month

# Challenge Details
TITLE = "Your Challenge Title"
DESCRIPTION = """Your challenge description here..."""

# Test Cases
TEST_CASES = [
    {
        "name": "Test Case Name",
        "input": "test input",
        "expectedOutput": "expected output"
    }
]

# Starter Code
STARTER_CODE = {
    "javascript": "// Your JavaScript starter code",
    "python": "# Your Python starter code",
    # ... other languages
}

# Challenge Settings
DIFFICULTY = "Easy"  # Easy, Medium, Hard
TIME_LIMIT = 5  # seconds
MEMORY_LIMIT = 128000  # KB
```

### Step 2: Run the Script
```bash
python upload-monthly-challenge.py
```

The script will:
1. Show you a preview of your challenge
2. Ask for confirmation
3. Upload directly to Firebase Firestore
4. Make your challenge live on the website immediately
5. Save a backup JSON file

## Monthly Workflow

### For Each New Month:

1. **Copy the script** or edit the existing one
2. **Update the challenge ID** (e.g., "2025-01", "2025-02", etc.)
3. **Change the title and description**
4. **Update test cases** if needed
5. **Modify starter code** if needed
6. **Run the script**

### Example Monthly Updates:

**January 2025:**
```python
CHALLENGE_ID = "2025-01"
TITLE = "Find the Maximum Number"
```

**February 2025:**
```python
CHALLENGE_ID = "2025-02"
TITLE = "Palindrome Checker"
```

## Challenge Structure

### Test Cases Format:
```python
TEST_CASES = [
    {
        "name": "Descriptive test name",
        "input": "what the user types",
        "expectedOutput": "what should be output"
    }
]
```

### Starter Code Languages:
- `javascript` - Node.js code
- `python` - Python 3 code
- `java` - Java code
- `csharp` - C# code
- `sql` - SQL code (usually placeholder)

## Tips for Good Challenges

1. **Clear Requirements**: Make the problem easy to understand
2. **Multiple Test Cases**: Include edge cases and normal cases
3. **Good Starter Code**: Provide helpful comments and structure
4. **Appropriate Difficulty**: Start easy and increase complexity
5. **Interesting Problems**: Make it fun and engaging

## Troubleshooting

### Common Issues:

1. **Upload Failed:**
   - Check your internet connection
   - Verify the Firebase API key is correct
   - Make sure the challenge ID is valid (YYYY-MM format)

2. **Challenge Not Appearing:**
   - Check the challenge ID format (YYYY-MM)
   - Verify the Firebase path is correct
   - Ensure the challenge is marked as "active"
   - Wait a few seconds for Firebase to sync

3. **Test Cases Not Working:**
   - Make sure input/output match exactly
   - Check for extra spaces or newlines
   - Test your code manually first

## Example Challenge

Here's a complete example challenge:

```python
CHALLENGE_ID = "2025-01"
TITLE = "Count Vowels"
DESCRIPTION = """Write a program that counts the number of vowels in a string.

Requirements:
- Read a string from standard input
- Count vowels (a, e, i, o, u, both uppercase and lowercase)
- Output the total count

Example:
Input: Hello World
Expected Output: 3

Input: Programming
Expected Output: 3"""

TEST_CASES = [
    {
        "name": "Simple String",
        "input": "Hello World",
        "expectedOutput": "3"
    },
    {
        "name": "No Vowels",
        "input": "Rhythm",
        "expectedOutput": "0"
    },
    {
        "name": "All Vowels",
        "input": "aeiou",
        "expectedOutput": "5"
    }
]
```

This makes it super easy to create new monthly challenges! Just edit the variables and run the script.
