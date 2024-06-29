from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app import crud, schemas
from app.auth import get_current_user, authenticate_user, get_password_hash
from fastapi.security import OAuth2PasswordRequestForm

from app.crud import connection

router = APIRouter()


@router.post("/token", response_model=schemas.User)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate):
    db_user = crud.get_user_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    return crud.create_user(user=user, hashed_password=hashed_password)


@router.get("/operations/", response_model=list)
def read_operations(skip: int = 0, limit: int = 10):
    operations = crud.get_operations(skip=skip, limit=limit)
    return operations


@router.post("/operations/", response_model=schemas.Operation)
def create_operation(operation: schemas.OperationCreate):
    operation_id = crud.create_operation(operation=operation)
    created_operation = {
        "id": operation_id,
        "type": operation.type,
        "cost": operation.cost
    }
    return created_operation


class CalculateRequest(BaseModel):
    operation_id: int


@router.post("/calculate/", response_model=schemas.Record)
def calculate(request: CalculateRequest, user: schemas.User = Depends(get_current_user)):
    operations = crud.get_operations()
    operation = next((op for op in operations if op['id'] == request.operation_id), None)
    if not operation:
        raise HTTPException(status_code=404, detail="Operation not found")

    if user['balance'] < operation['cost']:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    if operation['type'] == "addition":
        result = 1 + 1  # Placeholder, should be replaced with actual logic
    elif operation['type'] == "subtraction":
        result = 1 - 1  # Placeholder, should be replaced with actual logic
    elif operation['type'] == "multiplication":
        result = 1 * 1  # Placeholder, should be replaced with actual logic
    elif operation['type'] == "division":
        result = 1 / 1  # Placeholder, should be replaced with actual logic
    elif operation['type'] == "square_root":
        result = 1 ** 0.5  # Placeholder, should be replaced with actual logic
    elif operation['type'] == "random_string":
        import requests
        response = requests.get("https://www.random.org/strings/?num=1&len=8&digits=on&upperalpha=on&loweralpha=on&unique=on&format=plain&rnd=new")
        result = response.text.strip()
    else:
        raise HTTPException(status_code=400, detail="Invalid operation type")

    user['balance'] -= operation['cost']
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET balance = %s WHERE id = %s", (user['balance'], user['id']))
    connection.commit()

    record = schemas.RecordCreate(
        operation_id=operation['id'],
        user_id=user['id'],
        amount=operation['cost'],
        user_balance=user['balance'],
        operation_response=str(result)
    )
    record_id = crud.create_record(record=record)
    record = crud.get_record(record_id)
    return schemas.Record(**record)

