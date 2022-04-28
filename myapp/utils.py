from passlib.context import CryptContext

# telling passlib what is the default hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# hashing the password
def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):  # plain password -> password that user try to attempt
    return pwd_context.verify(plain_password, hashed_password)