from fastapi import APIRouter

from src.users.controllers import (
    get_all_users_controller,
    get_user_controller,
    get_sign_up_page,
    create_user_controller,
    get_login_page,
    login,
    logout,
)

router = APIRouter()

router.get("/users/", name="user-list")(get_all_users_controller)
router.get("/users/{id}/", name="user-detail")(get_user_controller)

router.get("/register/", name="get-sign-up")(get_sign_up_page)
router.post("/register/", name="post-sign-up")(create_user_controller)

router.get("/login/", name="get-login")(get_login_page)
router.post("/login/", name="post-login")(login)

router.get("/logout/", name="logout")(logout)
