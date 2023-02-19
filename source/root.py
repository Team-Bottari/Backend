from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from config import MAIN_URL,VERSION
from fastapi_utils.inferring_router import InferringRouter
import os

root_router = InferringRouter()


@cbv(root_router)
class MainSource:
    @root_router.get(MAIN_URL)
    def get(self):
        return JSONResponse({"value":f"Version : {VERSION}"})

    


