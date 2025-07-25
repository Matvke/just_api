from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


SECRET_KEY = "44cd7841827c1add075a4c4a122683b1d85c4a654b8f767da8937da3922c1f93"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")







