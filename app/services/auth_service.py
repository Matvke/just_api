from datetime import datetime, timedelta, timezone
import jwt
from app.repository import UserRepository
from app.schemas import SignUpRequest
from app.core.security import SECRET_KEY, ALGORITHM, pwd_context
from app.model.models import User
from app.exceptions.service_exceptions import NotCreatedException


class AuthService():
    def __init__(self, repository: UserRepository):
        self.repository = repository


    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)


    def get_password_hash(self, password):
        return pwd_context.hash(password)
    

    async def authenticate_user(self, username: str, password: str) :
        user = await self.repository.get_one_by_filters(username=username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user


    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    

    async def sign_up(self, form_data: SignUpRequest) -> User:
        if await self.repository.get_one_by_filters(email=form_data.email):
            raise NotCreatedException(f"Email {form_data.email} already taken")
        
        if await self.repository.get_one_by_filters(username=form_data.username):
            raise NotCreatedException(f"Username {form_data.username} already taken")
        
        user_data = form_data.model_dump(exclude={"password"})
        user_data["hashed_password"] = self.get_password_hash(form_data.password)
        
        try: 
            user = await self.repository.create(user_data)
            await self.repository.session.commit()
            return user
        except Exception as e:
            await self.repository.session.rollback()
            raise e