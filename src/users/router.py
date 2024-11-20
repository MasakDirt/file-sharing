from fastapi import APIRouter

from src.users.controllers import (
    get_all_users_controller,
    get_user_controller,
    get_sign_up_page,
    create_user_controller,
)

router = APIRouter()

router.get("/users/")(get_all_users_controller)
router.get("/users/{id}/")(get_user_controller)

router.get("/signUp/")(get_sign_up_page)
router.post("/signUp/")(create_user_controller)
