#!/usr/bin/env python3
"""
Security Test Script for AgriTech Firebase Configuration
This script verifies that sensitive information is properly secured.
"""

import os
import requests
import json
from dotenv import load_dotenv

def test_environment_variables():
    """Test that environment variables are properly loaded"""
    print("🔍 Testing Environment Variables...")
    
    load_dotenv()
    
    required_vars = [
        'FIREBASE_API_KEY',
        'FIREBASE_AUTH_DOMAIN', 
        'FIREBASE_PROJECT_ID',
        'FIREBASE_STORAGE_BUCKET',
        'FIREBASE_MESSAGING_SENDER_ID',
        'FIREBASE_APP_ID'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.environ.get(var)
        if not value or value == 'your_new_api_key_here':
            missing_vars.append(var)
        else:
            print(f"✅ {var}: {'*' * 10} (hidden)")
    
    if missing_vars:
        print(f"❌ Missing or placeholder environment variables: {missing_vars}")
        return False
    else:
        print("✅ All environment variables are properly set")
        return True

def test_firebase_config_endpoint():
    """Test that the Firebase config endpoint works and doesn't expose sensitive data"""
    print("\n🔍 Testing Firebase Config Endpoint...")
    
    try:
        # Start the Flask app (you'll need to run this separately)
        response = requests.get('http://localhost:5000/api/firebase-config', timeout=5)
        
        if response.status_code == 200:
            config = response.json()
            
            # Check that all required fields are present
            required_fields = ['apiKey', 'authDomain', 'projectId', 'storageBucket', 'messagingSenderId', 'appId']
            missing_fields = [field for field in required_fields if field not in config]
            
            if missing_fields:
                print(f"❌ Missing fields in config response: {missing_fields}")
                return False
            
            # Check that values are not placeholder values
            placeholder_values = ['your_new_api_key_here', 'your_project.firebaseapp.com', 'your_project_id']
            for field, value in config.items():
                if value in placeholder_values:
                    print(f"❌ Placeholder value found in {field}")
                    return False
            
            print("✅ Firebase config endpoint working correctly")
            print(f"✅ Config contains {len(config)} fields")
            return True
            
        else:
            print(f"❌ Endpoint returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask server. Make sure it's running on port 5000")
        return False
    except Exception as e:
        print(f"❌ Error testing endpoint: {e}")
        return False

def test_client_side_exposure():
    """Test that sensitive information is not exposed in client-side files"""
    print("\n🔍 Testing Client-Side File Security...")
    
    # Check firebase.js for hardcoded credentials
    try:
        with open('firebase.js', 'r') as f:
            content = f.read()
            
        # Look for common patterns that indicate hardcoded credentials
        suspicious_patterns = [
            'apiKey: "AIza',
            'projectId: "agritech',
            'apiKey: "YOUR_API_KEY"',
            'projectId: "YOUR_PROJECT_ID"'
        ]
        
        found_patterns = []
        for pattern in suspicious_patterns:
            if pattern in content:
                found_patterns.append(pattern)
        
        if found_patterns:
            print(f"❌ Found suspicious patterns in firebase.js: {found_patterns}")
            return False
        else:
            print("✅ No hardcoded credentials found in firebase.js")
            return True
            
    except FileNotFoundError:
        print("❌ firebase.js file not found")
        return False
    except Exception as e:
        print(f"❌ Error reading firebase.js: {e}")
        return False

def test_gitignore():
    """Test that .env file is properly ignored"""
    print("\n🔍 Testing .gitignore Configuration...")
    
    try:
        with open('.gitignore.txt', 'r') as f:
            content = f.read()
        
        if '.env' in content:
            print("✅ .env file is properly listed in .gitignore")
            return True
        else:
            print("❌ .env file is not in .gitignore")
            return False
            
    except FileNotFoundError:
        print("❌ .gitignore.txt file not found")
        return False
    except Exception as e:
        print(f"❌ Error reading .gitignore.txt: {e}")
        return False

def main():
    """Run all security tests"""
    print("🔒 AgriTech Firebase Security Test Suite")
    print("=" * 50)
    
    tests = [
        test_environment_variables,
        test_firebase_config_endpoint,
        test_client_side_exposure,
        test_gitignore
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Security Test Results:")
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ All {total} security tests PASSED")
        print("🎉 Your Firebase configuration is secure!")
    else:
        print(f"❌ {total - passed} out of {total} security tests FAILED")
        print("⚠️  Please address the failed tests before deploying")
    
    print("\n📝 Next Steps:")
    print("1. Create a .env file with your actual Firebase credentials")
    print("2. Regenerate Firebase API keys in the Firebase Console")
    print("3. Update Firebase security rules using firestore.rules")
    print("4. Test the application functionality")
    print("5. Monitor for any security issues")

if __name__ == "__main__":
    main()
