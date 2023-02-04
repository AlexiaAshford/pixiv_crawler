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
