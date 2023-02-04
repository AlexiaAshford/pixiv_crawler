from typing import List, Optional

from pydantic import BaseModel
from .image_info import Illusts


class RecommendImages(BaseModel):
    illusts: List[Illusts] = None
    contest_exists: Optional[bool] = None
    privacy_policy: Optional[dict] = None
    next_url: Optional[str] = None
