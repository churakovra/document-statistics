from uuid import UUID

from sqlalchemy.orm import Session

from app.exceptions.user_exceptions import UserNotFoundException, UserWrongPasswordException, UserAlreadyExistsException
from app.repositories.statistics_repository import StatisticsRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user.new_user import NewUserAccount
from app.schemas.user.user_account_response import UserCreds
from app.schemas.user.user_change_password import UserChangePassword
from app.schemas.user.user_dto import UserDTO
from app.services.app_service import AppService
from app.services.auth_service import AuthService
from app.services.collection_service import CollectionService
from app.services.document_service import DocumentService


class UserService:
    def __init__(self, session: Session):
        self.db = session

    def get_user(self, **credentials) -> UserDTO:
        user_repo = UserRepository(self.db)
        if "username" in credentials:  # TODO вынести строки в Enum
            username = credentials["username"]
            user = user_repo.get_user(username=username)
        elif "uuid" in credentials:
            uuid = credentials["uuid"]
            user = user_repo.get_user(uuid=uuid)
        elif "uuid_session" in credentials:
            uuid_session = credentials["uuid_session"]
            user = user_repo.get_user(uuid_session=uuid_session)
        else:
            raise ValueError("Требуется указать либо 'username', либо 'uuid'")
        if user is None:
            key = [str(key) for key in credentials.keys()][0]  # Получаем тип креда
            value = [str(value) for value in credentials.values()][0]  # Получаем значение
            raise UserNotFoundException(key=key, value=value)
        return user

    def register_user(self, user_creds: NewUserAccount):
        user_repo = UserRepository(self.db)
        try:
            self.get_user(username=user_creds.username)
            raise UserAlreadyExistsException(user_creds.username)
        except UserNotFoundException:
            password_hashed = AuthService.hash_pass(user_creds.password)
            user_creds.password = password_hashed
            user_repo.add_user(user_creds)
            new_user = self.get_user(username=user_creds.username)
            return UserCreds(
                uuid=new_user.uuid,
                username=new_user.username,
                dt_reg=new_user.dt_reg
            )

    def change_password(self, user_uuid: UUID, ucp: UserChangePassword):
        user_repository = UserRepository(self.db)
        user = self.get_user(uuid=user_uuid)
        if not AuthService.validate_pass(ucp.password_old, user.password_hashed):
            raise UserWrongPasswordException
        password_hashed_new = AuthService.hash_pass(ucp.password_new)
        user.password_hashed = password_hashed_new
        user_repository.set_new_pass(user)

    def delete_user(self, user: UserDTO):
        # Убиваем все сессии пользователя
        app_service = AppService(self.db)
        app_service.delete_user_sessions(user.uuid)

        # Удаляем коллекции, документы и статистику пользователя
        collection_service = CollectionService(self.db)
        document_service = DocumentService(self.db)
        statistics_repository = StatisticsRepository(self.db)

        deleted_collections_uuid = collection_service.delete_user_collections(user.uuid)
        deleted_documents_uuid = document_service.delete_user_documents(user)
        for uuid in deleted_collections_uuid:
            statistics_repository.delete_user_statistics(uuid)
        for uuid in deleted_documents_uuid:
            statistics_repository.delete_user_statistics(uuid)

        # Удаляем профиль пользователя
        user_repository = UserRepository(self.db)
        user_repository.delete_user(user.uuid)
