from fastapi import Request, Depends, HTTPException
from pydantic_core import ValidationError
from starlette import status
from starlette.responses import RedirectResponse

from src.settings import TEMPLATES
from src.users.dependencies import get_user_service
from src.users.exceptions import UsersBaseException
from src.users.interfaces import UserServiceInterface
from src.users.schemas import UserCreateSerializer


async def get_all_users_controller(
    request: Request,
    service: UserServiceInterface = Depends(get_user_service)
):
    users = await service.get_all()

    return TEMPLATES.TemplateResponse(
        request=request,
        name="users/users_list.html",
        context={"users": users}
    )


async def get_user_controller(
    request: Request,
    id: int,
    service: UserServiceInterface = Depends(get_user_service)
):
    try:
        user = await service.get_user(id=id)
    except UsersBaseException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exception)
        )

    return TEMPLATES.TemplateResponse(
        request=request,
        name="users/user_detail.html",
        context={"user": user}
    )


def get_sign_up_page(request: Request):
    return TEMPLATES.TemplateResponse(
        request=request,
        name="registration/register.html"
    )


async def create_user_controller(
    request: Request,
    service: UserServiceInterface = Depends(get_user_service)
):
    form = await request.form()
    try:
        user = UserCreateSerializer(
            email=form.get("email"),
            username=form.get("username"),
            full_name=form.get("full_name"),
            password=form.get("password"),
        )
    except ValidationError as validation_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(validation_error)
        )  # todo: refactor for beauty response

    try:
        new_user = await service.create_user(user)

        return RedirectResponse(
            url=f"/users/{new_user.id}/",
            status_code=status.HTTP_303_SEE_OTHER
        )
    except UsersBaseException as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exception)
        )
    except ValueError as value_exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(value_exc)
        )
