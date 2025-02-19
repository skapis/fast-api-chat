from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import PERMISSIONS
from app.auth import get_current_user
from fastapi.responses import JSONResponse



class RoleMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            path = request.url.path
            method = request.method

            allowed_roles = PERMISSIONS.get(path, {}).get(method, [])

            if not allowed_roles:
                return await call_next(request)

            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Unauthorized")

            token = auth_header.split("Bearer ")[1]

            user = get_current_user(token)

            user_roles = user.get("roles", [])

            if not any(role['role_name'] in allowed_roles for role in user_roles):
                raise HTTPException(status_code=403, detail="Insufficient permissions")

            return await call_next(request)

        except HTTPException as http_exc:
            return JSONResponse(
                status_code=http_exc.status_code,
                content={"detail": http_exc.detail},
            )
