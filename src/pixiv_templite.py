from pydantic import BaseModel
from typing import List, Optional


class RefreshTokenUser(BaseModel):
    profile_image_urls: Optional[dict] = None
    id: Optional[str] = None
    name: Optional[str] = None
    account: Optional[str] = None
    mail_address: Optional[str] = None
    is_premium: Optional[bool] = None
    x_restrict: Optional[int] = None
    is_mail_authorized: Optional[bool] = None
    require_policy_agreement: Optional[bool] = None


class RefreshToken(BaseModel):
    access_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None
    scope: Optional[str] = None
    refresh_token: Optional[str] = None
    user: RefreshTokenUser = None
    response: Optional[dict] = None


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


"""{
    "illusts": [ 
    ],
    "contest_exists": false,
    "privacy_policy": {
        "version": "5-ja",
        "message": "pixivは2022年7月28日付けでプライバシーポリシーを改定しました",
        "url": "https://policies.pixiv.net/ja/privacy.html?appname=pixiv"
    },
    "next_url": "https://app-api.pixiv.net/v1/illust/recommended?include_ranking_illusts=false&include_privacy_policy=false&filter=for_android&min_bookmark_id_for_recent_illust=0&max_bookmark_id_for_recommend=-1&offset=30&viewed%5B0%5D=97971899&viewed%5B1%5D=97975937&viewed%5B2%5D=97974592&viewed%5B3%5D=97988150&viewed%5B4%5D=97985204&viewed%5B5%5D=97971099&viewed%5B6%5D=97973254&viewed%5B7%5D=97947474&viewed%5B8%5D=97993616&viewed%5B9%5D=97989312&viewed%5B10%5D=97991709&viewed%5B11%5D=97962585&viewed%5B12%5D=97972950&viewed%5B13%5D=97996595&viewed%5B14%5D=97965162&viewed%5B15%5D=97956937&viewed%5B16%5D=97963473&viewed%5B17%5D=97957534&viewed%5B18%5D=97974860&viewed%5B19%5D=97961596&viewed%5B20%5D=97972984&viewed%5B21%5D=97947509&viewed%5B22%5D=97981121&viewed%5B23%5D=97953674&viewed%5B24%5D=97974203&viewed%5B25%5D=97966254&viewed%5B26%5D=97962566&viewed%5B27%5D=97967493&viewed%5B28%5D=97971224&viewed%5B29%5D=97963521"
}"""


class ImageUrls(BaseModel):
    square_medium: Optional[str] = None
    medium: Optional[str] = None
    large: Optional[str] = None


class ImageTags(BaseModel):
    name: Optional[str] = None
    translated_name: Optional[str] = None


class ImageMetaSinglePage(BaseModel):
    original_image_url: Optional[str] = None


class  Illusts(BaseModel):
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
    series: Optional[str] = None
    meta_single_page: ImageMetaSinglePage = None
    meta_pages: Optional[List] = None
    total_view: Optional[int] = None
    total_bookmarks: Optional[int] = None
    is_bookmarked: Optional[bool] = None
    visible: Optional[bool] = None
    is_muted: Optional[bool] = None
    illust_ai_type: Optional[int] = None
    illust_book_style: Optional[int] = None


class RecommendImages(BaseModel):
    illusts: List[Illusts] = None
    contest_exists: Optional[bool] = None
    privacy_policy: Optional[dict] = None
    next_url: Optional[str] = None
