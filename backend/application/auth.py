from flask_jwt_extended import get_jwt, verify_jwt_in_request, get_jwt_identity
from functools import wraps
from flask import jsonify, current_app
import logging

logger = logging.getLogger(__name__)

def admin_required(fn):
    """
    A decorator to ensure that only admin users can access the decorated route.
    
    - Verifies JWT token is present
    - Checks if the user has admin privileges
    - Logs unauthorized access attempts
    """
    @wraps(fn)
    def decorator(*args, **kwargs):
        try:
            # Verify JWT token is present and valid
            verify_jwt_in_request()
            
            # Get claims from the JWT token
            claims = get_jwt()
            
            # Get the identity (now a string - user email) and additional claims
            user_email = get_jwt_identity()  # This is now the email string
            is_admin = claims.get('is_admin', False)
            
            # Check if user is an admin
            if not is_admin:
                # Log unauthorized access attempt
                logger.warning(
                    f"Unauthorized admin access attempt. "
                    f"User email: {user_email}"
                )
                
                return jsonify({
                    "message": "Unauthorized. Admin access required.",
                    "error": "ADMIN_ACCESS_REQUIRED"
                }), 403
            
            # If admin, proceed with the route function
            return fn(*args, **kwargs)
        
        except Exception as e:
            # Log any unexpected errors during admin check
            logger.error(f"Admin access check error: {str(e)}")
            
            return jsonify({
                "message": "An error occurred while checking admin access.",
                "error": "ADMIN_ACCESS_ERROR"
            }), 500
    
    return decorator