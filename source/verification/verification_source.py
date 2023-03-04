from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi import Path
from config import VERIFICATION_URL

verification_router = InferringRouter()

@cbv(verification_router)
class Verification:
    @verification_router.get(VERIFICATION_URL)
    async def verify(self,random_value:str=Path(min_length=16,max_length=16)):
        return {"random_value":random_value}
