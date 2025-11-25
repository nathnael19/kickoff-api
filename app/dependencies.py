from fastapi import Header, HTTPException, status
from app.database import supabase

async def verify_admin(x_supabase_auth: str = Header(None)):
    """
    Verifies that the request comes from an authenticated admin user.
    In a real scenario, we would verify the JWT token.
    For now, we check if the header is present and valid via Supabase user retrieval.
    """
    if not x_supabase_auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
        )

    try:
        user = supabase.auth.get_user(x_supabase_auth)
        if not user:
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
        )
