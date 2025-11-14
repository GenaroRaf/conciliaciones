from pydantic import BaseModel


class ReportSheet(BaseModel):
    name: str
    redis_key: str
