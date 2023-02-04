from pydantic import BaseModel
from typing import List, Optional


class UserInfoUser(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    account: Optional[str] = None
    profile_image_urls: Optional[dict] = None
    comment: Optional[str] = None
    is_followed: Optional[bool] = None
    is_access_blocking_user: Optional[bool] = None


class UserInfoProfile(BaseModel):
    webpage: Optional[str] = None
    gender: Optional[str] = None
    birth: Optional[str] = None
    birth_day: Optional[str] = None
    birth_year: Optional[int] = None
    region: Optional[str] = None
    address_id: Optional[int] = None
    country_code: Optional[str] = None
    job: Optional[str] = None
    job_id: Optional[int] = None
    total_follow_users: Optional[int] = None
    total_mypixiv_users: Optional[int] = None
    total_illusts: Optional[int] = None
    total_manga: Optional[int] = None
    total_novels: Optional[int] = None
    total_illust_bookmarks_public: Optional[int] = None
    total_illust_series: Optional[int] = None
    total_novel_series: Optional[int] = None
    background_image_url: Optional[str] = None
    twitter_account: Optional[str] = None
    twitter_url: Optional[str] = None
    pawoo_url: Optional[str] = None
    is_premium: Optional[bool] = None
    is_using_custom_profile_image: Optional[bool] = None


class UserInfoProfilePublicity(BaseModel):
    gender: Optional[str] = None
    region: Optional[str] = None
    birth_day: Optional[str] = None
    birth_year: Optional[str] = None
    job: Optional[str] = None
    pawoo: Optional[bool] = None


class UserInfoWorkspace(BaseModel):
    pc: Optional[str] = None
    monitor: Optional[str] = None
    tool: Optional[str] = None
    scanner: Optional[str] = None
    tablet: Optional[str] = None
    mouse: Optional[str] = None
    printer: Optional[str] = None
    desktop: Optional[str] = None
    music: Optional[str] = None
    desk: Optional[str] = None
    chair: Optional[str] = None
    comment: Optional[str] = None
    workspace_image_url: Optional[str] = None


class UserInfo(BaseModel):
    user: UserInfoUser = None
    profile: UserInfoProfile = None
    profile_publicity: UserInfoProfilePublicity = None
    workspace: UserInfoWorkspace = None

