import firebase_admin
from firebase_admin import credentials, firestore, db
from app.config import settings
import logging

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

            if settings.FIREBASE_CREDENTIALS_PATH:
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                firebase_admin.initialize_app(cred, options)
                logger.info("Firebase Admin initialized with service account.")
            else:
                # Use default credentials (works on GCP, or if GOOGLE_APPLICATION_CREDENTIALS is set)
                # Note: options are still passed for things like storageBucket
                firebase_admin.initialize_app(options=options)
                logger.info("Firebase Admin initialized with default credentials.")
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {e}")
        raise e
