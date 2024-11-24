from fastapi import Request, HTTPException, Depends, UploadFile, File
from starlette import status
from starlette.responses import RedirectResponse

from src.files.dependencies import get_file_service
from src.files.interfaces import FileServiceInterface
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
        url="/files/upload/",
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
