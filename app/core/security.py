import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt
from fastapi.security import OAuth2PasswordBearer


# Hash password logic

def hash_password(password:str):

    # Encode the password converting it into bytes
    pw_bytes = password.encode('utf-8')

    # Generate the salt
    salt = bcrypt.gensalt(rounds=12)

    # Hash the password
    hashed_password = bcrypt.hashpw(pw_bytes, salt)

    return hashed_password





# Verify password
def verify_password(plain_password, hashed):
    encoded_incoming_password = plain_password.encode('utf-8')
    encoded_stored_password = hashed.encode('utf-8')

    try:

        return bcrypt.checkpw(encoded_incoming_password, encoded_stored_password)


    except (ValueError, TypeError, AttributeError):
        return False



# JWT Token Logic


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "2a782a3bb64b4351543bd672ffe9bdda01fd0f5c3651c853e96200c1b1c2e26d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Creating the token for user's authentication

def create_token(data:dict, expires_delta:timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt






















