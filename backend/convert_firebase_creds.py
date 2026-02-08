#!/usr/bin/env python3
"""
Firebase Credentials to Base64 Converter
Converts Firebase service account JSON to base64 for Railway environment variables
"""
import base64
import json
import sys

def convert_to_base64(json_file_path):
    """Convert Firebase JSON to base64 string"""
    try:
        with open(json_file_path, 'rb') as f:
            json_bytes = f.read()
        
        # Convert to base64
        base64_string = base64.b64encode(json_bytes).decode('utf-8')
        
        print("=" * 60)
        print("✅ Firebase Credentials Converted Successfully!")
        print("=" * 60)
        print("\nCopy the following base64 string to Railway:")
        print("\nVariable Name: FIREBASE_CREDENTIALS_BASE64")
        print("\nVariable Value:")
        print("-" * 60)
        print(base64_string)
        print("-" * 60)
        
        # Save to file for easy copying
        with open('firebase_credentials_base64.txt', 'w') as f:
            f.write(base64_string)
        
        print("\n✅ Also saved to: firebase_credentials_base64.txt")
        print("\n📋 Next Steps:")
        print("1. Go to Railway → Your Service → Variables")
        print("2. Add variable: FIREBASE_CREDENTIALS_BASE64")
        print("3. Paste the base64 string above")
        print("4. Redeploy your service")
        print("=" * 60)
        
        return base64_string
        
    except FileNotFoundError:
        print(f"❌ Error: File not found: {json_file_path}")
        print("\nUsage: python convert_firebase_creds.py <path-to-serviceAccountKey.json>")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_firebase_creds.py <path-to-serviceAccountKey.json>")
        print("\nExample:")
        print("  python convert_firebase_creds.py musicapp-2a106-firebase-adminsdk.json")
        sys.exit(1)
    
    json_file = sys.argv[1]
    convert_to_base64(json_file)
