from passlib.context import CryptContext

pass_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto",
)


class AuthService:
    @staticmethod
    def validate_pass(pwd: str, pwd_hashed: str) -> bool:
        return pass_context.verify(pwd, pwd_hashed)

    @staticmethod
    def hash_pass(pwd: str) -> str:
        return pass_context.hash(pwd)