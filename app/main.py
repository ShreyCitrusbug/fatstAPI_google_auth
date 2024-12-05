# Third party imports
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

# Local imports
from app.settings import settings

# Local imports
from app.routers.auth import router as auth_router

# Initialize FastAPI
app = FastAPI(title=settings.APP_NAME,
              version=settings.APP_VERSION, debug=settings.DEBUG)


@app.get("/", include_in_schema=False)
def health_check():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"success": "ok"})


# add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origin_settings.get("allowed_origins"),
    allow_credentials=True,
    allow_methods=settings.get_allowed_origin_settings.get("allowed_methods"),
    allow_headers=settings.get_allowed_origin_settings.get("allowed_headers"),
)


# Session Middleware for Google OAuth2
app.add_middleware(SessionMiddleware,secret_key="")

# Include routers
app.include_router(auth_router)
