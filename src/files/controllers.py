from fastapi import Request, HTTPException, Depends, UploadFile, File
from starlette import status
from starlette.responses import RedirectResponse

from src.files.dependencies import (
    get_file_service,
    get_allowed_files_for_user_service,
)
from src.files.interfaces import (
    FileServiceInterface,
    AllowedFilesForUserServiceInterface,
)
from src.settings import TEMPLATES, ALLOWED_EXTENSIONS
from src.utils.decorators import admin_only


@admin_only
async def get_file_upload_page_controller(
    request: Request
) -> TEMPLATES.TemplateResponse:
    allowed_extensions = ", ".join(ALLOWED_EXTENSIONS)
    return TEMPLATES.TemplateResponse(
        request=request,
        name="files/upload.html",
        context={"allowed_extensions": allowed_extensions}
    )


@admin_only
async def create_file_controller(
    request: Request,
    file: UploadFile = File(...),
    file_service: FileServiceInterface = Depends(get_file_service)
) -> RedirectResponse:
    try:
        await file_service.process_file_create(file)
    except ValueError as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exception)
        )

    return RedirectResponse(
        url="/files/",
        status_code=status.HTTP_302_FOUND
    )


@admin_only
async def get_all_files_controller(
    request: Request,
    file_service: FileServiceInterface = Depends(get_file_service)
):
    all_files = await file_service.get_all_files()

    return TEMPLATES.TemplateResponse(
        request=request,
        name="files/files_list.html",
        context={"files": all_files}
    )


@admin_only
async def remove_file(
    request: Request,
    id: int,
    file_service: FileServiceInterface = Depends(get_file_service)
) -> RedirectResponse:
    await file_service.remove_file(id=id)

    return RedirectResponse(
        url="/files/",
        status_code=status.HTTP_302_FOUND
    )


@admin_only
async def get_file_giving_access_page(
    request: Request,
    file_id: int,
    allowed_files_service: AllowedFilesForUserServiceInterface = Depends(
        get_allowed_files_for_user_service
    )
) -> TEMPLATES.TemplateResponse:
    users = await allowed_files_service.get_users_with_access_to_file(file_id)
    return TEMPLATES.TemplateResponse(
        request=request,
        name="files/give_file_access.html",
        context={"users": users, "file_id": file_id}
    )


@admin_only
async def update_users_file_access(
    request: Request,
    file_id: int,
    file_access_service: AllowedFilesForUserServiceInterface = Depends(
        get_allowed_files_for_user_service
    )
) -> RedirectResponse:
    form = await request.form()
    selected_user_ids = set(map(int, form.getlist("user_ids")))

    await file_access_service.update_file_access(file_id, selected_user_ids)

    return RedirectResponse(url="/files/", status_code=status.HTTP_302_FOUND)
