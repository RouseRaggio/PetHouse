from pydantic import BaseModel
from typing import List


class AssignPermissions(BaseModel):
    permission_ids: List[int]