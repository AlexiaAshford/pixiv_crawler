from typing import Optional, List

from pydantic import BaseModel
from .user_info import UserInfoUser


class ImageUrls(BaseModel):
    square_medium: Optional[str] = None
    medium: Optional[str] = None
    large: Optional[str] = None


class ImageTags(BaseModel):
    name: Optional[str] = None
    translated_name: Optional[str] = None


class ImageMetaSinglePage(BaseModel):
    original_image_url: Optional[str] = None


class Illusts(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    type: Optional[str] = None
    image_urls: ImageUrls = None
    caption: Optional[str] = None
    restrict: Optional[int] = None
    user: UserInfoUser = None
    tags: List[ImageTags] = None
    tools: List[str]
    create_date: Optional[str] = None
    page_count: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    sanity_level: Optional[int] = None
    x_restrict: Optional[int] = None
    series: Optional[dict] = None
    meta_single_page: ImageMetaSinglePage = None
    meta_pages: Optional[List] = None
    total_view: Optional[int] = None
    total_bookmarks: Optional[int] = None
    is_bookmarked: Optional[bool] = None
    visible: Optional[bool] = None
    is_muted: Optional[bool] = None
    illust_ai_type: Optional[int] = None
    illust_book_style: Optional[int] = None
