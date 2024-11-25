from fastapi import Request, Depends, HTTPException
from fastapi_csrf_protect import CsrfProtect
from pydantic_core import ValidationError
from starlette import status
from starlette.responses import RedirectResponse

from src.utils.decorators import (
    admin_only,
    set_csrf_token,
    validate_csrf_token,
)
from src.settings import TEMPLATES
from src.users.dependencies import get_user_service, get_auth_service
from src.users.exceptions import UsersBaseException
from src.users.interfaces import UserServiceInterface, AuthServiceInterface
from src.users.schemas import UserCreateSerializer, UserLoginSerializer


@admin_only
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


async def get_me_controller(
    request: Request,
    service: UserServiceInterface = Depends(get_user_service)
) -> TEMPLATES.TemplateResponse:
    auth_user = request.state.user

    try:
        user = await service.get_user(id=auth_user.id)
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


@set_csrf_token
async def get_sign_up_page(
    request: Request,
    csrf_protect: CsrfProtect = Depends(),
) -> TEMPLATES.TemplateResponse:
    return TEMPLATES.TemplateResponse(
        request=request,
        name="registration/register.html",
        context={"csrf_token": request.state.csrf_token}
    )


@validate_csrf_token
async def create_user_controller(
    request: Request,
    csrf_protect: CsrfProtect = Depends(),
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
        )

    try:
        await service.create_user(user)

        return RedirectResponse(
            url="/",
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


@set_csrf_token
async def get_login_page(
    request: Request,
    csrf_protect: CsrfProtect = Depends(),
) -> TEMPLATES.TemplateResponse:
    return TEMPLATES.TemplateResponse(
        request=request,
        name="registration/login.html",
        context={"csrf_token": request.state.csrf_token}
    )


@validate_csrf_token
async def login(
    request: Request,
    csrf_protect: CsrfProtect = Depends(),
    service: AuthServiceInterface = Depends(get_auth_service)
) -> RedirectResponse:
    form = await request.form()
    login_data = UserLoginSerializer(
        email=form.get("email"),
        password=form.get("password"),
    )
    remember_me = bool(form.get("remember"))

    try:
        token = await service.login(
            login_data=login_data,
            remember_me=remember_me
        )
    except UsersBaseException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exception)
        )

    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

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
