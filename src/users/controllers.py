from fastapi import Request, Depends, HTTPException
from pydantic_core import ValidationError
from starlette import status
from starlette.responses import RedirectResponse

from src.settings import TEMPLATES
from src.users.dependencies import get_user_service, get_auth_service
from src.users.exceptions import UsersBaseException
from src.users.interfaces import UserServiceInterface, AuthServiceInterface
from src.users.schemas import UserCreateSerializer, UserLoginSerializer


async def get_all_users_controller(
    request: Request,
    service: UserServiceInterface = Depends(get_user_service)
) -> TEMPLATES.TemplateResponse:
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
) -> TEMPLATES.TemplateResponse:
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


def get_sign_up_page(request: Request) -> TEMPLATES.TemplateResponse:
    return TEMPLATES.TemplateResponse(
        request=request,
        name="registration/register.html"
    )


async def create_user_controller(
    request: Request,
    service: UserServiceInterface = Depends(get_user_service)
) -> RedirectResponse:
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


async def get_login_page(request: Request) -> TEMPLATES.TemplateResponse:
    return TEMPLATES.TemplateResponse(
        request=request,
        name="registration/login.html"
    )


async def login(
    request: Request,
    service: AuthServiceInterface = Depends(get_auth_service)
) -> RedirectResponse:
    form = await request.form()
    login_data = UserLoginSerializer(
        email=form.get("email"),
        password=form.get("password"),
    )
    remember_me = bool(form.get("remember"))
    print(remember_me)

    token = await service.login(login_data=login_data, remember_me=remember_me)

    response = RedirectResponse(url="/", status_code=302)

    response.set_cookie(
        key="session",
        value=token,
        httponly=True,
        secure=False,
    )

    return response


async def logout(
    request: Request,
    service: AuthServiceInterface = Depends(get_auth_service)
) -> RedirectResponse:
    session_token = request.cookies.get("session")
    await service.logout(session_token)

    response = RedirectResponse(url="/login/", status_code=302)
    response.delete_cookie(key="session")

    return response
