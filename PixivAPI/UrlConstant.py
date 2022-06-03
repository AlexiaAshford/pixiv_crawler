IMAGE_INFORMATION = "https://api.obfs.dev/api/pixiv/illust?id={}"
AUTHOR_INFORMATION = "https://api.obfs.dev/api/pixiv/member_illust?id={}&page={}"
FAVORITE_INFORMATION = "https://api.obfs.dev/api/pixiv/favorite?id={}"
FOLLOWING_INFORMATION = "user/following"
PIXIV_HOST = "https://app-api.pixiv.net/v1/"


def RANK_INFORMATION(page: int, mode="week") -> str:
    # rank_mode可选标签
    # "week" "day_male" "day_female" "week_original" "week_rookie"
    # "day_r18" "day_male_r18" "day_female_r18" "week_r18" "week_r18g"
    return f"https://api.obfs.dev/api/pixiv/rank?mode={mode}&page={page}&size=50"


def SEARCH_INFORMATION(
        word: str, page: int, mode="partial_match_for_tags", order="date_desc"
) -> str:
    """
    search_mode
    partial_match_for_tags	exact_match_for_tags    title_and_caption
    标签部分一致                  标签完全一致              标题说明文

    search_order
    date_desc	    date_asc    popular_desc
    按日期倒序        按日期正序    受欢迎降序(Premium功能)

    search_duration
    "within_last_day" "within_last_week" "within_last_month"
    """
    host = "https://api.obfs.dev/api/pixiv/search?"
    return f"{host}word={word}&mode={mode}&order={order}&page={page}&size=50"
