import src
from tools import *
from src.PixivUtil import UrlConstant


def refresh_pixiv_token(error_info: str = "") -> None:
    if error_info != "" and error_info is not None:
        print("[error]:", error_info)
    if PixivLogin.refresh(Vars.cfg.data.get("refresh_token")):
        print("refresh token success, new token:", Vars.cfg.data.get("access_token"))
    else:
        print("refresh token failed, please login again")


class PixivApp:

    @staticmethod
    def get_user_info(show_start: bool = False) -> bool:
        params = {"user_id": Vars.cfg.data.get("user_info", {}).get("id")}
        response = src.get(api_url=UrlConstant.ACCOUNT_INFORMATION, params=params).get('user')
        if response is not None:
            if show_start is True:
                print(f"用户名：{response.get('name')}\t\t用户id：{response.get('id')}")
            return True

    @staticmethod
    def images_information(works_id: str) -> dict:
        response = src.get(UrlConstant.IMAGE_INFORMATION, params={'id': works_id}, head="web")
        if isinstance(response, dict) and response.get('illust') is not None:
            return response["illust"]
        else:
            print(response)

    @staticmethod
    def start_images(
            api_url: str = UrlConstant.BOOKMARK_INFORMATION,
            user_id: [int, str] = None,
            restrict: str = "public",
            params_clear: bool = False,
            max_retry: int = 3
    ) -> [list, str, None]:  # get account start information and return a list of p_id
        if user_id is None:  # if user_id is None, get the user_id from config file
            user_id = Vars.cfg.data['user_info']['id']

        if api_url != UrlConstant.BOOKMARK_INFORMATION:  # if api_url is not bookmark, clear to params dict
            params_clear = True
        response = src.get(api_url=api_url, params={"user_id": user_id, "restrict": restrict}, params_clear=params_clear)
        if response.get('illusts') is not None:
            return response.get('illusts'), response.get('next_url')
        if max_retry <= 3:
            refresh_pixiv_token(response.get("error").get("message"))  # refresh token
            PixivApp.start_images(api_url, user_id, restrict)  # if get error, try to refresh token and retry
            max_retry += 1

    @staticmethod
    def recommend_images(
            api_url: str = UrlConstant.RECOMMENDED_INFORMATION,
            params_clear: bool = False,
            include_ranking_illusts: str = "true",
            include_privacy_policy: str = "true",
            max_retry: int = 3
    ) -> [list, str, None]:  # get account recommend images and return a list of p_id

        if api_url != UrlConstant.RECOMMENDED_INFORMATION:  # if api_url is not recommended, clear to params dict
            params_clear = True

        params = {"include_ranking_illusts": include_ranking_illusts, "include_privacy_policy": include_privacy_policy}
        response: dict = src.get(api_url=api_url, params=params, params_clear=params_clear)
        if response.get('illusts') is not None:
            return response.get("illusts"), response.get('next_url')
        if max_retry <= 3:  # if max_retry is less than 3, try to refresh token and retry
            refresh_pixiv_token(response.get("error").get("message"))  # refresh token
            PixivApp.recommend_images(api_url=api_url)  # if get error, try to refresh token and retry
            max_retry += 1  # add retry count

    @staticmethod
    def follow_information(
            api_url: str = UrlConstant.FOLLOWING_INFORMATION,
            user_id: [int, str] = None,
            restrict: str = "public",
            params_clear: bool = False,
            max_retry: int = 3
    ) -> [list, str]:  # get account follow information and return a list of AUTHOR_ID
        """获取指定 user_id 关注的所有画师信息"""
        if user_id is None:  # if user_id is None, get the user_id from config file
            user_id = Vars.cfg.data['user_info']['id']  # get user_id from config file and set to user_id
        if api_url != UrlConstant.FOLLOWING_INFORMATION:  # if api_url is not recommended, clear to params dict
            params_clear = True
        response = src.get(api_url=api_url, params={"user_id": user_id, "restrict": restrict}, params_clear=params_clear)
        if response.get('user_previews') is not None:
            return response["user_previews"], response.get('next_url')
        if max_retry <= 3:
            refresh_pixiv_token(response.get("error").get("message"))  # refresh token
            PixivApp.follow_information(user_id, restrict)  # if get error, try to refresh token and retry
            max_retry += 1

    @staticmethod
    def author_information(
            api_url: str = UrlConstant.AUTHOR_INFORMATION,
            author_id: str = "",
            params_clear: bool = False,
            max_retry: int = 3
    ) -> [list, str, None]:  # get author information and return a list of p_id

        if api_url != UrlConstant.AUTHOR_INFORMATION:  # if api_url is not author, clear to params dict
            params_clear = True
        response = src.get(api_url=api_url, params={"user_id": author_id, "type": "illust"}, params_clear=params_clear)
        if response.get('illusts') is not None:  # get success, return a list of p_id and next_url (if not None)
            return response.get('illusts'), response.get('next_url')
        if max_retry <= 3:
            refresh_pixiv_token(response.get("error").get("message"))  # refresh token
            PixivApp.author_information(api_url=api_url, author_id=author_id)  # try to refresh token and retry
            max_retry += 1

    @staticmethod
    def get_ranking_info(
            api_url: str = UrlConstant.RANKING_INFORMATION,
            params_clear: bool = False,
            max_retry: int = 5
    ) -> [list, str]:  # 作品排行信息
        mode_list = [
            "day", "week", "month", "day_male",
            "day_female", "week_original", "week_rookie",
            "day_manga", "day_r18", "day_male_r18",
            "day_female_r18", "week_r18", "week_r18g"
        ]
        if api_url == UrlConstant.RANKING_INFORMATION:  # if api_url is not author, clear to params dict
            for index, mode in enumerate(mode_list):  # for each mode, get the ranking information
                print("index:", index, "\t\tmode_name:", mode)  # print mode_name
            mode_type = mode_list[functions.input_int(">", len(mode_list))]  # input mode_type from user
        else:
            params_clear, mode_type = True, None  # clear to params dict and set mode_type to None
        response = src.get(api_url=api_url, params={"mode": mode_type}, params_clear=params_clear)
        if response.get('illusts') is not None:
            return response.get('illusts'), response.get('next_url')
        if max_retry <= 3:  # if max_retry is less than 3, try to refresh token and retry
            refresh_pixiv_token(response.get("error").get("message"))  # refresh token
            PixivApp.get_ranking_info(api_url=api_url)  # if get error, try to refresh token and retry
            max_retry += 1  # add retry count to max_retry


class Tag:
    """
    search_target
    partial_match_for_tags	exact_match_for_tags    title_and_caption
    标签部分一致                  标签完全一致              标题说明文

    sort
    date_desc	    date_asc    popular_desc
    按日期倒序        按日期正序    受欢迎降序(Premium功能)

    search_duration
    "within_last_day" "within_last_week" "within_last_month"
    """

    @staticmethod
    def search_tag_information(png_name: str, sort: str = "popular_desc", max_retry: int = 5) -> list:
        params = {
            "include_translated_tag_results": "true",
            "merge_plain_keyword_results": "true",
            "word": png_name,
            "sort": sort,
            "search_target": "exact_match_for_tags",
        }
        response = src.get(api_url=UrlConstant.SEARCH_INFORMATION, params=params)
        if response.get('illusts') is not None:
            return response["illusts"]
        if max_retry <= 3:
            refresh_pixiv_token(response.get("error").get("message"))
            Tag.search_tag_information(png_name, sort)
            max_retry += 1

    @staticmethod
    def search_information(png_name: str, sort: str = "date_desc", max_retry: int = 5) -> list:
        params = {
            "include_translated_tag_results": "true",
            "merge_plain_keyword_results": "true",
            "word": png_name,
            "sort": sort,
            "search_target": "partial_match_for_tags",
        }
        response = src.get(api_url=UrlConstant.SEARCH_INFORMATION, params=params)
        if response.get('illusts') is not None:
            return response["illusts"]
        if max_retry <= 3:
            refresh_pixiv_token(response.get("error").get("message"))
            Tag.search_information(png_name, sort)
            max_retry += 1


class PixivLogin:

    @staticmethod
    def oauth_pkce() -> [str, str]:
        from secrets import token_urlsafe
        from base64 import urlsafe_b64encode
        from hashlib import sha256
        """S256 transformation method. Proof Key for Code Exchange by OAuth Public Clients (RFC7636)."""
        code_verifier = token_urlsafe(32)  # generate code_verifier from secrets.token_urlsafe
        code_challenge = urlsafe_b64encode(sha256(code_verifier.encode("ascii")).digest()). \
            rstrip(b"=").decode("ascii")  # remove padding characters from base64 encoding and decode to ascii
        return code_verifier, code_challenge

    @staticmethod
    def open_browser(client: str = "pixiv-android") -> [str, None]:
        from webbrowser import open as open_url
        from urllib.parse import urlencode
        code_verifier, code_challenge = PixivLogin.oauth_pkce()
        login_params = {"code_challenge": code_challenge, "code_challenge_method": "S256", "client": client}
        return code_verifier, open_url(f"https://app-api.pixiv.net/web/v1/login?{urlencode(login_params)}")

    @staticmethod
    def login(code_verifier: str, code_information: str) -> bool:  # login with code_information
        response = src.get(
            api_url="https://oauth.secure.pixiv.net/auth/token",
            head="login",
            method="POST",
            params={
                "client_id": "MOBrBDS8blbauoSck0ZfDbtuzpyT",
                "client_secret": "lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj",
                "code": code_information,
                "code_verifier": code_verifier,
                "grant_type": "authorization_code",
                "include_policy": "true",
                "redirect_uri": "https://app-api.pixiv.net/web/v1/users/auth/pixiv/callback",
            },
        )
        if response.get("errors") is not None:  # if get error, return False and print error message
            print("errors:", response['errors'])
        else:
            PixivLogin.save_token(response)
            return True

    @staticmethod
    def refresh(refresh_token: str) -> bool:  # refresh token and save to file
        response = src.get(
            api_url="https://oauth.secure.pixiv.net/auth/token",
            head="login",
            method="POST",
            params={
                "client_id": "MOBrBDS8blbauoSck0ZfDbtuzpyT",
                "client_secret": "lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj",
                "grant_type": "refresh_token",
                "include_policy": "true",
                "refresh_token": refresh_token,
            }
        )

        if response.get("errors") is not None:
            print("errors:", response['errors'])
        else:
            PixivLogin.save_token(response)
            return True

    @staticmethod
    def save_token(response: dict) -> None:  # save token to file for later use
        if isinstance(response, dict):  # if response is a dict
            Vars.cfg.data["user_info"] = response["user"]  # save user_id to config
            Vars.cfg.data["access_token"] = response["access_token"]  # save access_token to config
            Vars.cfg.data["refresh_token"] = response["refresh_token"]  # save refresh_token to config
            Vars.cfg.save()  # save config to file
            print("login success, user_id:", response["user"]["id"], "access_token:", response["access_token"])
        else:
            print("response is not dict type")
