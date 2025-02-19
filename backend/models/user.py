from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserDB(UserBase):
    id: int
    balance: float

    class Config:
        orm_mode = True

class User:
    @staticmethod
    def get(db, user_id: int):
        result = db.execute("SELECT * FROM users WHERE id = ?;", (user_id,)).fetchall()
        if result:
            row = result[0]
            return UserDB(id=row[0], username=row[1], balance=row[3])
        return None

    @staticmethod
    def get_by_username(db, username: str):
        result = db.execute("SELECT * FROM users WHERE username = ?;", (username,)).fetchall()
        if result:
            row = result[0]
            return UserDB(id=row[0], username=row[1], balance=row[3])
        return None

    @staticmethod
    def create(db, user: UserCreate):
        hashed_password = user.password + "notreallyhashed"
        db.execute("INSERT INTO users (username, hashed_password, balance) VALUES (?, ?, ?);",
                   (user.username, hashed_password, 1000.0))
        new_id = db.execute("SELECT MAX(id) FROM users;").fetchone()[0]
        return User.get(db, new_id) 