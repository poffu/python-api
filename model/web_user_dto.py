from pydantic import BaseModel


class LoginDto(BaseModel):
    email: str = ''
    password: str = ''


class InsertDto(BaseModel):
    email: str = ''
    name: str = ''
    password: str = ''
    tel: str = ''


class UpdateDto(BaseModel):
    userId: int = 0
    email: str = ''
    name: str = ''
    password: str = ''
    tel: str = ''


class ListUserDto(BaseModel):
    name: str = ''
