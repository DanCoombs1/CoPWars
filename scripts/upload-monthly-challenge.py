#!/usr/bin/env python3
"""
Simple Monthly Challenge Upload Script
Edit the variables below and run this script to upload a new challenge to Firebase.
"""

import requests
import json
import os
from datetime import datetime
from typing import Optional

# Optional Google Auth imports (only required for Service Account OAuth)
try:
    from google.oauth2 import service_account  # type: ignore
    from google.auth.transport.requests import Request  # type: ignore
except Exception:
    service_account = None  # Lazy import fallback
    Request = None

# =============================================================================
# EDIT THESE VARIABLES FOR YOUR MONTHLY CHALLENGE
# =============================================================================

# Challenge ID (format: YYYY-MM)
CHALLENGE_ID = "2025-09"

# Challenge Details
TITLE = "First Missing Positive"
DESCRIPTION = """Problem Statement

Given an unsorted integer array nums. Return the smallest positive integer that is not present in nums.

You must implement an algorithm that runs in O(n) time and uses O(1) auxiliary space.

Constraints:
- 1 <= nums.length <= 10^5
- -2^31 <= nums[i] <= 2^31 - 1

Examples:
- Input: nums = [1,2,0], Output: 3
- Input: nums = [3,4,-1,1], Output: 2  
- Input: nums = [7,8,9,11,12], Output: 1"""

# Test Cases
TEST_CASES = [
    {
        "name": "Example 1",
        "input": "[1,2,0]",
        "expectedOutput": "3"
    },
    {
        "name": "Example 2", 
        "input": "[3,4,-1,1]",
        "expectedOutput": "2"
    },
    {
        "name": "Example 3",
        "input": "[7,8,9,11,12]",
        "expectedOutput": "1"
    },
    {
        "name": "All negatives",
        "input": "[-1,-2,-3]",
        "expectedOutput": "1"
    },
    {
        "name": "Large consecutive",
        "input": "[1,2,3,4,5]",
        "expectedOutput": "6"
    }
]

# Starter Code for each language
STARTER_CODE = {
    "python": "class Solution(object):\n    def firstMissingPositive(self, nums):\n        \"\"\"\n        :type nums: List[int]\n        :rtype: int\n        \"\"\"\n        # Your algorithm here\n        pass\n\n# Test your solution\nsol = Solution()\nnums = [1,2,0]\nresult = sol.firstMissingPositive(nums)\nprint(result)",
    "java": "class Solution {\n    public int firstMissingPositive(int[] nums) {\n        // Your algorithm here\n        return 1;\n    }\n}",
    "c++": "#include <vector>\nusing namespace std;\n\nclass Solution {\npublic:\n    int firstMissingPositive(vector<int>& nums) {\n        // Your algorithm here\n        return 1;\n    }\n};",
    "csharp": "public class Solution {\n    public int FirstMissingPositive(int[] nums) {\n        // Your algorithm here\n        return 1;\n    }\n}",
    "sql": "-- This problem is not applicable in SQL"
}

# Challenge Settings
DIFFICULTY = "Medium"
TIME_LIMIT = 5  # seconds
MEMORY_LIMIT = 128000  # KB

# =============================================================================
# DON'T EDIT BELOW THIS LINE
# =============================================================================

def _get_bearer_token() -> Optional[str]:
    """Return an OAuth bearer token if GOOGLE_APPLICATION_CREDENTIALS is set; otherwise None."""
    sa_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not sa_path:
        return None
    if service_account is None or Request is None:
        return None
    try:
        scopes = ["https://www.googleapis.com/auth/datastore"]
        creds = service_account.Credentials.from_service_account_file(sa_path, scopes=scopes)
        creds.refresh(Request())
        return creds.token
    except Exception:
        return None

def upload_challenge():
    """Upload the challenge to Firebase Firestore using REST API."""
    
    # Firebase project ID and API key (from your frontend config)
    project_id = "cop-codewars"
    api_key = "YOUR_FIREBASE_WEB_API_KEY_HERE" # Replace if using API key auth
    
    # Create challenge document
    challenge_data = {
        "title": TITLE,
        "description": DESCRIPTION,
        "testCases": TEST_CASES,
        "starterCode": STARTER_CODE,
        "difficulty": DIFFICULTY,
        "timeLimit": TIME_LIMIT,
        "memoryLimit": MEMORY_LIMIT,
        "createdAt": datetime.now().isoformat() + "Z",
        "active": True
    }
    
    # Decide auth mode
    bearer = _get_bearer_token()
    if bearer:
        url = (
            f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/"
            f"artifacts/{project_id}/public/data/challenges/{CHALLENGE_ID}"
        )
        headers = {
            "Authorization": f"Bearer {bearer}",
            "Content-Type": "application/json",
        }
        auth_mode = "oauth"
    else:
        url = (
            f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/"
            f"artifacts/{project_id}/public/data/challenges/{CHALLENGE_ID}?key={api_key}"
        )
        headers = {"Content-Type": "application/json"}
        auth_mode = "api_key"
    
    # Convert to Firestore document format
    firestore_doc = {
        "fields": {
            "title": {"stringValue": challenge_data["title"]},
            "description": {"stringValue": challenge_data["description"]},
            "testCases": {"arrayValue": {"values": [
                {
                    "mapValue": {
                        "fields": {
                            "name": {"stringValue": tc["name"]},
                            "input": {"stringValue": tc["input"]},
                            "expectedOutput": {"stringValue": tc["expectedOutput"]}
                        }
                    }
                } for tc in challenge_data["testCases"]
            ]}},
            "starterCode": {"mapValue": {
                "fields": {
                    lang: {"stringValue": code} for lang, code in challenge_data["starterCode"].items()
                }
            }},
            "difficulty": {"stringValue": challenge_data["difficulty"]},
            "timeLimit": {"integerValue": str(challenge_data["timeLimit"])},
            "memoryLimit": {"integerValue": str(challenge_data["memoryLimit"])},
            "createdAt": {"timestampValue": challenge_data["createdAt"]},
            "active": {"booleanValue": challenge_data["active"]}
        }
    }
    
    try:
        print(f"📤 Uploading to Firebase using {auth_mode}...")
        
        response = requests.patch(url, headers=headers, json=firestore_doc)
        
        if response.status_code in [200, 201]:
            print(f"✅ Successfully uploaded challenge: {TITLE} ({CHALLENGE_ID})")
            print(f"🚀 Your challenge is now live on the website!")
            
            with open(f"challenge-{CHALLENGE_ID}.json", "w") as f:
                json.dump(challenge_data, f, indent=2)
            print(f"📄 Backup saved to: challenge-{CHALLENGE_ID}.json")
            
            return True
        else:
            print(f"❌ Failed to upload challenge. Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            with open(f"challenge-{CHALLENGE_ID}.json", "w") as f:
                json.dump(challenge_data, f, indent=2)
            print(f"📄 Challenge data saved to: challenge-{CHALLENGE_ID}.json for manual upload")
            return False
            
    except Exception as e:
        print(f"❌ Failed to upload challenge: {e}")
        
        try:
            with open(f"challenge-{CHALLENGE_ID}.json", "w") as f:
                json.dump(challenge_data, f, indent=2)
            print(f"📄 Challenge data saved to: challenge-{CHALLENGE_ID}.json for manual upload")
        except:
            pass
        
        return False

def preview_challenge():
    """Preview the challenge data before uploading."""
    print("📋 Challenge Preview:")
    print("=" * 50)
    print(f"ID: {CHALLENGE_ID}")
    print(f"Title: {TITLE}")
    # ... preview logic ...
    print("=" * 50)

if __name__ == "__main__":
    print("🎯 Monthly Challenge Upload Script")
    # ... main logic ...
    response = input("\n❓ Do you want to upload this challenge to Firebase? (y/N): ").strip().lower()
    
    if response in ['y', 'yes']:
        success = upload_challenge()
        # ... completion logic ...
    else:
        print("\n❌ Upload cancelled.")

