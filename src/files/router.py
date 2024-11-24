from fastapi import APIRouter

from src.files.controllers import (
    create_file_controller,
    get_file_upload_page_controller,
    get_all_files_controller,
    remove_file,
    get_file_giving_access_page,
    update_users_file_access,
)

router = APIRouter()


router.get("/files/", name="file-list")(get_all_files_controller)
router.get("/files/upload/", name="get-upload-file")(
    get_file_upload_page_controller
)
router.post("/files/upload/", name="upload-file")(create_file_controller)
router.post("/files/{id}/delete/", name="file-remove")(remove_file)
router.get("/files/{file_id}/access/", name="get-file-access")(
    get_file_giving_access_page
)
router.post("/files/{file_id}/access/", name="file-access")(
    update_users_file_access
)
