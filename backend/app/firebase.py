import firebase_admin
from firebase_admin import credentials, firestore, db
from app.config import settings
import logging
import base64
import json
import tempfile
import os

logger = logging.getLogger(__name__)

def initialize_firebase():
    """Initializes Firebase Admin SDK"""
    try:
        if not firebase_admin._apps:
            options = {}
            if settings.FIREBASE_STORAGE_BUCKET:
                options['storageBucket'] = settings.FIREBASE_STORAGE_BUCKET
            if settings.FIREBASE_PROJECT_ID:
                options['projectId'] = settings.FIREBASE_PROJECT_ID

            # Priority 1: Base64 encoded credentials (Railway deployment)
            if settings.FIREBASE_CREDENTIALS_BASE64:
                try:
                    # Decode base64 credentials
                    cred_json = base64.b64decode(settings.FIREBASE_CREDENTIALS_BASE64)
                    cred_dict = json.loads(cred_json)
                    cred = credentials.Certificate(cred_dict)
                    firebase_admin.initialize_app(cred, options)
                    logger.info("Firebase Admin initialized with base64 credentials.")
                    return
                except Exception as e:
                    logger.error(f"Failed to decode base64 credentials: {e}")
                    raise

            # Priority 2: File path to credentials
            if settings.FIREBASE_CREDENTIALS_PATH:
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                firebase_admin.initialize_app(cred, options)
                logger.info("Firebase Admin initialized with service account file.")
            else:
                # Priority 3: Default credentials (GCP environment)
                firebase_admin.initialize_app(options=options)
                logger.info("Firebase Admin initialized with default credentials.")
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {e}")
        raise e
