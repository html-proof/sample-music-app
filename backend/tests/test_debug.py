import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_fastapi_security_isolation():
    """Verify fastapi.security works in isolation."""
    from fastapi.security import HTTPBearer
    assert HTTPBearer is not None

def test_app_security_import():
    """Verify importing app.security works."""
    # This might trigger the error
    from app.security import get_current_user
    assert get_current_user is not None
