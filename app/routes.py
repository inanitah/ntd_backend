from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from app import crud, schemas
from app.auth import get_current_user, authenticate_user, get_password_hash
from fastapi.security import OAuth2PasswordRequestForm
from app.consts import Status
from app.utils import perform_operation

router = APIRouter()


class CalculateRequest(BaseModel):
    operation_id: int


@router.post("/token", response_model=schemas.User)
def login_for_access_token(
    request: Request, form_data: OAuth2PasswordRequestForm = Depends()
):
    connection = request.state.db
    user = authenticate_user(connection, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    return user


@router.post("/users/", response_model=schemas.User)
def create_user(request: Request, user: schemas.UserCreate):
    connection = request.state.db
    db_user = crud.get_user_by_username(connection, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    return crud.create_user(
        connection, user=user, hashed_password=hashed_password, status=Status.ACTIVE
    )


@router.get("/operations/", response_model=list)
def read_operations(request: Request, skip: int = 0, limit: int = 10):
    connection = request.state.db
    operations = crud.get_operations(connection, skip=skip, limit=limit)
    return operations


@router.post("/operations/", response_model=schemas.Operation)
def create_operation(request: Request, operation: schemas.OperationCreate):
    connection = request.state.db
    operation_id = crud.create_operation(connection, operation=operation)
    created_operation = {
        "id": operation_id,
        "type": operation.type,
        "cost": operation.cost
    }
    return created_operation


@router.post("/calculate/", response_model=schemas.Record)
def calculate(
    request: Request, calc_request: CalculateRequest, user: dict = Depends(get_current_user)
):
    connection = request.state.db
    operations = crud.get_operations(connection)
    operation = next(
        (op for op in operations if op['id'] == calc_request.operation_id), None
    )
    if not operation:
        raise HTTPException(status_code=404, detail="Operation not found")

    if user['balance'] < operation['cost']:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    try:
        result = perform_operation(operation['type'])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    new_balance = user['balance'] - operation['cost']
    crud.update_user_balance(connection, user['id'], new_balance)

    record = schemas.RecordCreate(
        operation_id=operation['id'],
        user_id=user['id'],
        amount=operation['cost'],
        user_balance=new_balance,
        operation_response=result
    )
    record_id = crud.create_record(connection, record=record)
    record = crud.get_record(connection, record_id)
    return schemas.Record(**record)


@router.delete("/records/{id}", response_model=schemas.Record)
def delete_record(request: Request, id: int):
    connection = request.state.db
    record = crud.get_record(connection, record_id=id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    return crud.soft_delete_record(connection, record_id=id)


@router.get("/records/", response_model=list)
def read_records(
    request: Request, skip: int = 0, limit: int = 10, search: str = None, user: dict = Depends(get_current_user)
):
    connection = request.state.db
    records = crud.get_records(
        connection, skip=skip, limit=limit, search=search, user_id=user['id']
    )
    return records
