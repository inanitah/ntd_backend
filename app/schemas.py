from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: int
    username: str
    balance: float
    status: str

    class Config:
        orm_mode = True


class OperationCreate(BaseModel):
    type: str
    cost: float


class Operation(BaseModel):
    id: int
    type: str
    cost: float

    class Config:
        orm_mode = True


class RecordCreate(BaseModel):
    operation_id: int
    user_id: int
    amount: float
    user_balance: float
    operation_response: str


class Record(BaseModel):
    id: int
    operation_id: int
    user_id: int
    amount: float
    user_balance: float
    operation_response: str
    deleted: Optional[bool] = False

    class Config:
        orm_mode = True
