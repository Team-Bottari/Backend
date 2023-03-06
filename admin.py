from fastapi.requests import Request
from sqladmin.authentication import AuthenticationBackend
from settings import ADMIN_ID,ADMIN_PASSWORD


class MyBackend(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        if (username==ADMIN_ID) and (password==ADMIN_PASSWORD):
            request.session.update({"token": "..."})
            return True
        else:
            return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        return True