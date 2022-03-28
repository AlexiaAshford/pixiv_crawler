from base64 import urlsafe_b64encode
from hashlib import sha256
from instance import *
from secrets import token_urlsafe
from urllib.parse import urlencode
from webbrowser import open as open_url
import requests


def s256(data):
    """S256 transformation method."""
    return urlsafe_b64encode(sha256(data).digest()).rstrip(b"=").decode("ascii")


def oauth_pkce(transform):
    """Proof Key for Code Exchange by OAuth Public Clients (RFC7636)."""
    code_verifier = token_urlsafe(32)
    code_challenge = transform(code_verifier.encode("ascii"))
    return code_verifier, code_challenge


def open_browser():
    code_verifier, code_challenge = oauth_pkce(s256)
    login_params = {
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "client": "pixiv-android",
    }
    open_url(f"https://app-api.pixiv.net/web/v1/login?{urlencode(login_params)}")
    return code_verifier


def login(code_verifier, code_information: str):
    response = requests.post(
        "https://oauth.secure.pixiv.net/auth/token",
        data={
            "client_id": "MOBrBDS8blbauoSck0ZfDbtuzpyT",
            "client_secret": "lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj",
            "code": code_information,
            "code_verifier": code_verifier,
            "grant_type": "authorization_code",
            "include_policy": "true",
            "redirect_uri": "https://app-api.pixiv.net/web/v1/users/auth/pixiv/callback",
        },
        headers={"User-Agent": "PixivAndroidApp/5.0.234 (Android 11; Pixel 5)"},
    ).json()
    if response.get("errors") is not None:
        print("errors:", response['errors']['system']['message'])
        return False
    else:
        save_token(response)


def refresh(refresh_token):
    response = requests.post(
        "https://oauth.secure.pixiv.net/auth/token",
        data={
            "client_id": "MOBrBDS8blbauoSck0ZfDbtuzpyT",
            "client_secret": "lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj",
            "grant_type": "refresh_token",
            "include_policy": "true",
            "refresh_token": refresh_token,
        },
        headers={"User-Agent": "PixivAndroidApp/5.0.234 (Android 11; Pixel 5)"},
    ).json()

    if response.get("errors") is not None:
        print("errors:", response['errors']['system']['message'])
        return False
    else:
        save_token(response)


def save_token(response):
    Vars.cfg.data["access_token"] = response["access_token"]
    Vars.cfg.data["refresh_token"] = response["refresh_token"]
    Vars.cfg.save()
