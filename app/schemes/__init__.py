# from pydantic import BaseModel
# from typing import List
# from datetime import datetime
# from zoneinfo import ZoneInfo

# from app.config import settings

# # Zona elegida en deploy, e.g. "America/Argentina/Buenos_Aires"
# TZ = ZoneInfo(settings.TIMEZONE)

# class APIBaseModel(BaseModel):
#     model_config = {
#         "json_encoders": {
#             datetime: lambda dt: dt.astimezone(TZ).isoformat()
#         }
#     }
# class ErrorDetail(APIBaseModel):
#     loc: List[str]
#     msg: str
#     type: str

# class ErrorResponse(APIBaseModel):
#     detail: List[ErrorDetail]