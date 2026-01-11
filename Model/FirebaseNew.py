import firebase_admin
from firebase_admin import credentials, firestore, storage #
import os
import json
import time

# 1. Firebase Configuration
# Replace 'your-project-id.appspot.com' with your actual bucket ID from Firebase Console
bucket_name = "Mr_Bin-7ec3f.appspot.com" 
firebase_cred_path = r"C:/Users/bps_r/Desktop/Mr_Bin/firebase-key.json" # Point to the actual file

# 2. Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_cred_path)
    firebase_admin.initialize_app(cred, {
        'storageBucket': bucket_name
    })

# Initialize Clients
firestore_client = firestore.client()
bucket = storage.bucket() #

# Already processed files (to avoid duplicates)
processed_files_Mr_Bin = set()
processed_files_camdetected = set()

def process_Mr_Bin_files():
    """Processes JSON reports from the 'userDetected/' folder in Firebase Storage"""
    global processed_files_Mr_Bin
    
    # List all blobs in the 'userDetected/' prefix
    blobs = bucket.list_blobs(prefix="userDetected/")

    for blob in blobs:
        file_key = blob.name

        # Skip directories or already processed files
        if file_key.endswith("/") or file_key in processed_files_Mr_Bin:
            continue

        file_name = os.path.basename(file_key)
        file_name_without_ext = os.path.splitext(file_name)[0]

        if file_name.endswith(".json"):
            try:
                # Download and parse JSON content directly from Firebase Storage
                file_data = blob.download_as_text()
                json_data = json.loads(file_data)

                # Extract username for document path
                username = json_data.get("user_metadata", {}).get("username")
                if not username:
                    print(f"Skipping {file_name}: 'username' field missing.")
                    continue

                # Upload data to Firestore
                doc_ref = (
                    firestore_client.collection("UserJson")
                    .document(username)
                    .collection("reports")
                    .document(file_name_without_ext)
                )
                doc_ref.set(json_data)

                processed_files_Mr_Bin.add(file_key)
                print(f"Synced {file_name} to Firestore (UserJson/{username})")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

def process_camdetected_files():
    """Processes metadata for images in the 'Camdetected/' folder in Firebase Storage"""
    global processed_files_camdetected

    blobs = list(bucket.list_blobs(prefix="Camdetected/"))
    
    # Sort by time updated (equivalent to LastModified in S3)
    blobs.sort(key=lambda x: x.updated, reverse=True)

    for blob in blobs:
        file_key = blob.name

        if file_key.endswith("/") or file_key in processed_files_camdetected:
            continue

        file_name = os.path.basename(file_key)
        file_name_without_ext = os.path.splitext(file_name)[0]

        try:
            # In Firebase, custom metadata is stored in the 'metadata' property
            custom_metadata = blob.metadata if blob.metadata else {}
            
            # Prepare data for Firestore
            report_data = {
                "LastModified": blob.updated.isoformat(),
                "ContentType": blob.content_type,
                "ContentLength": blob.size,
                "public_url": blob.public_url, # Useful for the dashboard
                **custom_metadata
            }

            camid = custom_metadata.get("camid", "unknown_camid")

            # Upload to Firestore
            doc_ref = (
                firestore_client.collection("Camjson")
                .document(camid)
                .collection("reports")
                .document(file_name_without_ext)
            )
            doc_ref.set(report_data)

            processed_files_camdetected.add(file_key)
            print(f"Synced metadata for {file_name} to Firestore (Camjson/{camid})")
            break # Only process the latest one as per original script logic
        except Exception as e:
            print(f"Error processing {file_name}: {e}")

def main():
    while True:
        print("\n--- Checking for new files in Firebase Storage ---")
        process_Mr_Bin_files()
        process_camdetected_files()
        time.sleep(10) # Wait 10 seconds between checks

if __name__ == "__main__":
    main()