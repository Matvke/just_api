from sqlalchemy.exc import SQLAlchemyError
from app.repository import UserRepository
from app.schema import SignInResponse, GetUserResponse, SignInRequest, SignUpRequest
from app.core.exceptions import NotCreatedException, NotFoundException, UserAlreadyExistsException


class AuthService():
    def __init__(self, repository: UserRepository):
        self.repository = repository


    async def sign_in(self, user_data: SignInRequest) -> SignInResponse:
        try:
            user = await self.repository.get_one_by_filters(email=user_data.email, password=user_data.password)
            if not user:
                raise NotFoundException("Incorrect login or password.")
            return SignInResponse.model_validate(user)
        except SQLAlchemyError as e:
            raise e


    async def sign_up(self, user_data: SignUpRequest) -> GetUserResponse:
        data = user_data.model_dump()
        try:
            if await self.repository.get_one_by_filters(email=user_data.email):
                raise UserAlreadyExistsException(f"User with email {user_data.email} already exist.")
            new_user = await self.repository.create(data)
            if not new_user:
                raise NotCreatedException(f"User with email {user_data.email} not found.")
            return GetUserResponse.model_validate(new_user)
        except SQLAlchemyError as e:
            raise e