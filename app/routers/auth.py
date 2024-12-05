# imports libraries
import logging
import json

# Third party imports
from fastapi import APIRouter
from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse
from google.oauth2 import id_token
from google.auth.transport import requests
from authlib.integrations.starlette_client import OAuth

# Local imports
from app.settings import settings

# Local Utils imports
from app.utils.logging.logging_config import setup_logging

router = APIRouter(
    prefix="/auth",
    tags=["Auth APIs"],
)


# Logger Setup
setup_logging()
logger = logging.getLogger()


# Initiate Google OAuth2
oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    redirect_uri=settings.GOOGLE_REDIRECT_URL,
    access_token_url=settings.GOOGLE_ACCESS_TOKEN_URL,
    authorize_url=settings.GOOGLE_AUTHORIZE_URL,
    api_base_url=settings.GOOGLE_API_BASE_URL,
    client_kwargs={"scope": "openid profile email"},
    jwks_uri=settings.GOOGLE_JWKS_URI,
)


@router.get("/google/login")
async def login_with_google(request: Request):
    """
    ## API to login with Google.

    Initiates the Google OAuth2 login process by generating the Google authentication URL.

    Returns:
        JSONResponse: A JSON response containing the Google authentication URL.
    """
    try:
        # Generate redirect URI for Google authentication callback
        redirect_uri = request.url_for('auth_callback')
        response_obj = await oauth.google.authorize_redirect(request, redirect_uri)

        # Return the authentication URL in JSON response
        return JSONResponse(
            content={"success": True,  "message": "Auth URL created successfully", "data": response_obj._headers.get("location", '')}, status_code=status.HTTP_200_OK
        )
    except Exception as e:
        # Log any errors encountered during the login process
        logger.error(f"Error logging in with Google: {str(e)}")

        # Raise an HTTP exception for internal server error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/google/callback")
async def auth_callback(code: str, request: Request):
    """
    ## API to handle Google authentication callback.

    ## Parameters:
        `code`: The authorization code returned by Google.
        `request`: The FastAPI request object.

    ## Returns:
        `RedirectResponse`: A redirect response to the welcome page.
    """
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo")
        logger.info("User info: %s", user_info)
        return JSONResponse(
            content=user_info, status_code=status.HTTP_200_OK
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid id_token: {str(e)}")

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
