from typing import Optional
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer(auto_error=False)

class User:
    def __init__(self, id: str, roles: list[str] = None):
        self.id = id
        self.roles = roles or []

class AuthProvider:
    def authenticate(self, request: Request) -> Optional[User]:
        raise NotImplementedError

class MockAuthProvider(AuthProvider):
    """
    Dummy provider for development. 
    Accepts any token and sets user_id to the token value.
    If token is 'dev-token', sets role to 'dev'.
    """
    def authenticate(self, request: Request) -> Optional[User]:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        token = auth_header.split(" ")[1]
        roles = ["dev"] if token == "dev-token" else []
        return User(id=token, roles=roles)

# For production, we would inject a JWT or Firebase or Auth0 provider here
auth_provider = MockAuthProvider()

def get_current_user(request: Request = None) -> Optional[User]:
    # Disabled auth for now
    return User(id="dev-user", roles=["dev"])

def require_current_user(user: Optional[User] = Depends(get_current_user)) -> User:
    # Always return user
    return user

def require_dev(user: User = Depends(require_current_user)) -> User:
    # Always return user
    return user
