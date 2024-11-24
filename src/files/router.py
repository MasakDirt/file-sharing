from fastapi import APIRouter

from src.files.controllers import (
    create_file_controller,
    get_file_upload_page_controller,
    get_all_files_controller,
)

router = APIRouter()

router.get("/files/upload/", name="get-upload-file")(
    get_file_upload_page_controller
)
router.post("/files/upload/", name="upload-file")(create_file_controller)

router.get("/files/", name="file-list")(get_all_files_controller)
