from passlib.context import CryptContext


class PwdHelper:
    pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)


pwd_hepler: PwdHelper = PwdHelper()
