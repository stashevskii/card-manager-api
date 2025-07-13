from fastapi import APIRouter, Depends, status
from app.schemas import BlockRequestFilter, BlockRequestResponse, BlockRequestCreate, BlockRequestReplace, BlockRequestUpdate
from app.utils import handle_business_errors
from app.dependencies import BlockRequestServiceDep, AdminDep, CurrentUserDep

router = APIRouter(prefix="/block-requests", tags=["Block requests"])


@router.get("/", summary="Get list of block requests by query. For admin only")
@handle_business_errors
def get_users_by_query(
        _: AdminDep,
        service: BlockRequestServiceDep,
        schema: BlockRequestFilter = Depends()
) -> list[BlockRequestResponse]:
    return service.get(schema)


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create block requests")
@handle_business_errors
def create_user(
        user: CurrentUserDep,
        service: BlockRequestServiceDep,
        schema: BlockRequestCreate
) -> BlockRequestResponse:
    return service.create(user, schema)


@router.get("/{id}", summary="Get block request by id. For admin only")
@handle_business_errors
def get_user_by_id(_: AdminDep, service: BlockRequestServiceDep, id: int) -> BlockRequestResponse:
    return service.get_by_id(id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete block request. For admin only")
@handle_business_errors
def delete_user(_: AdminDep, service: BlockRequestServiceDep, id: int):
    return service.delete(id)


@router.put("/{id}", summary="Replace block request. For admin only")
@handle_business_errors
def replace_user(
        _: AdminDep,
        service: BlockRequestServiceDep,
        id: int,
        schema: BlockRequestReplace
) -> BlockRequestResponse:
    return service.replace(id, schema)


@router.patch("/{id}", summary="Update block request. For admin only")
@handle_business_errors
def update_user(
        _: AdminDep,
        service: BlockRequestServiceDep,
        id: int, schema: BlockRequestUpdate
) -> BlockRequestResponse:
    return service.update(id, schema)
