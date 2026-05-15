from datetime import datetime, timezone, UTC

# MongoDB mein user document ka structure
def user_model(name: str, email: str, hashed_password: str):
    return {
        "name": name,
        "email": email,
        "hashed_password": hashed_password,
        "created_at": datetime.now(UTC)
    }
    

