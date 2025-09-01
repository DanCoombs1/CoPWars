#!/usr/bin/env python3
"""
Automated Monthly Winners Script
This script automatically saves the top 3 winners from the previous month.
Can be run manually or scheduled to run automatically.
"""

import requests
import json
from datetime import datetime, timedelta
import sys

# =============================================================================
# CONFIGURATION
# =============================================================================

# Firebase project ID and API key
PROJECT_ID = "cop-codewars"
API_KEY = "AIzaSyDQ_qPKNKsxJ9azV5TehHo8S43gSAjRENk"

# =============================================================================
# DON'T EDIT BELOW THIS LINE
# =============================================================================

def get_previous_month():
    """Get previous month in YYYY-MM format."""
    today = datetime.now()
    # Go back one month
    if today.month == 1:
        previous_month = today.replace(year=today.year - 1, month=12)
    else:
        previous_month = today.replace(month=today.month - 1)
    return f"{previous_month.year}-{previous_month.month:02d}"

def get_month_winners(month):
    """Get top 3 winners for a specific month."""
    print(f"📊 Fetching winners for {month}...")
    
    # Get all users
    users_url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/artifacts/cop-codewars/users?key={API_KEY}"
    
    try:
        response = requests.get(users_url)
        if response.status_code != 200:
            print(f"❌ Failed to get users: {response.status_code}")
            return []
        
        users_data = response.json()
        if 'documents' not in users_data:
            print("❌ No users found")
            return []
        
        winners = []
        
        # For each user, get their best score for the month
        for user_doc in users_data['documents']:
            user_id = user_doc['name'].split('/')[-1]
            
            # Get user's best score for the month
            best_score_url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/artifacts/cop-codewars/users/{user_id}/bestScores/{month}?key={API_KEY}"
            
            score_response = requests.get(best_score_url)
            if score_response.status_code == 200:
                score_data = score_response.json()
                if 'fields' in score_data:
                    fields = score_data['fields']
                    score = int(fields.get('score', {}).get('integerValue', 0))
                    
                    if score > 0:  # Only include users with valid scores
                        winner = {
                            'userId': user_id,
                            'displayName': fields.get('displayName', {}).get('stringValue', f'Agent-{user_id[:6]}'),
                            'score': score,
                            'executionTime': float(fields.get('executionTime', {}).get('doubleValue', 0)),
                            'memory': int(fields.get('memory', {}).get('integerValue', 0)),
                            'hairColor': int(fields.get('hairColor', {}).get('integerValue', 0)),
                            'skinColor': int(fields.get('skinColor', {}).get('integerValue', 0)),
                            'topColor': int(fields.get('topColor', {}).get('integerValue', 0)),
                            'accessory': int(fields.get('accessory', {}).get('integerValue', 0))
                        }
                        winners.append(winner)
        
        # Sort by score and take top 3
        winners.sort(key=lambda x: x['score'], reverse=True)
        return winners[:3]
        
    except Exception as e:
        print(f"❌ Error fetching winners: {e}")
        return []

def save_monthly_winners(month, winners):
    """Save monthly winners to Firebase."""
    if not winners:
        print(f"❌ No winners to save for {month}")
        return False
    
    print(f"🏆 Saving {len(winners)} winners for {month}...")
    
    # Prepare the document data
    winners_data = {
        'month': month,
        'winners': winners,
        'savedAt': datetime.now().isoformat() + 'Z',
        'totalWinners': len(winners)
    }
    
    # Convert to Firestore format
    firestore_doc = {
        'fields': {
            'month': {'stringValue': winners_data['month']},
            'savedAt': {'timestampValue': winners_data['savedAt']},
            'totalWinners': {'integerValue': winners_data['totalWinners']},
            'winners': {
                'arrayValue': {
                    'values': [
                        {
                            'mapValue': {
                                'fields': {
                                    'userId': {'stringValue': winner['userId']},
                                    'displayName': {'stringValue': winner['displayName']},
                                    'score': {'integerValue': winner['score']},
                                    'executionTime': {'doubleValue': winner['executionTime']},
                                    'memory': {'integerValue': winner['memory']},
                                    'hairColor': {'integerValue': winner['hairColor']},
                                    'skinColor': {'integerValue': winner['skinColor']},
                                    'topColor': {'integerValue': winner['topColor']},
                                    'accessory': {'integerValue': winner['accessory']}
                                }
                            }
                        } for winner in winners_data['winners']
                    ]
                }
            }
        }
    }
    
    # Save to Firebase
    url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/artifacts/cop-codewars/public/data/monthlyWinners/{month}?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.patch(url, headers=headers, json=firestore_doc)
        
        if response.status_code in [200, 201]:
            print(f"✅ Successfully saved monthly winners for {month}")
            print(f"🥇 1st Place: {winners[0]['displayName']} - {winners[0]['score']} pts")
            if len(winners) > 1:
                print(f"🥈 2nd Place: {winners[1]['displayName']} - {winners[1]['score']} pts")
            if len(winners) > 2:
                print(f"🥉 3rd Place: {winners[2]['displayName']} - {winners[2]['score']} pts")
            
            # Save backup JSON
            with open(f"monthly-winners-{month}.json", "w") as f:
                json.dump(winners_data, f, indent=2)
            print(f"📄 Backup saved to: monthly-winners-{month}.json")
            
            return True
        else:
            print(f"❌ Failed to save winners. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error saving winners: {e}")
        return False

def main():
    """Main function."""
    print("🤖 Automated Monthly Winners Script")
    print("=" * 50)
    
    # Get previous month
    month = get_previous_month()
    print(f"📅 Target month: {month}")
    
    # Get winners
    winners = get_month_winners(month)
    
    if not winners:
        print(f"❌ No winners found for {month}")
        return
    
    print(f"🎯 Found {len(winners)} winners:")
    for i, winner in enumerate(winners, 1):
        print(f"   {i}. {winner['displayName']} - {winner['score']} pts")
    
    # Automatically save (no user confirmation needed)
    success = save_monthly_winners(month, winners)
    if success:
        print(f"\n🎉 Monthly winners saved successfully!")
    else:
        print(f"\n💥 Failed to save monthly winners!")

if __name__ == "__main__":
    main()
