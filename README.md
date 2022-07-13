# PixivCrawler

### pixiv login.

- authentication method is no longer supported to pixiv .
- The Pixiv app now logs in through `https://accounts.pixiv.net/login`
- but this page is protected by Google reCAPTCHA, which seems impossible to circumvent.
- so, you can't use this crawler to with login account,but you can use this crawler to web get the account token to
  login.
- You can refer to the following [link](/docs) to get the account token.
- run `py mian.py` browser automatically login pixiv on startup **[1](/docs/1.png)**
- copy the `code`  **[2](/docs/2.png)**
- enter the `code` it to command terminal  **[3](/docs/3.png)**
- **Congratulations on your login success!**

## start crawler with command line arguments

```
h | help               --- show help information
q | quit               --- quit crawler and exit
d | picture            --- input picture id to download
t | recommend          --- download recommend picture
s | start              --- download all collect picture
u | read text pid      --- read text from picture id (only for pixiv)
n | tag name           --- search tag name and download all picture
```

## install

``` pip install pixivlib ```

## about command line arguments and usage

## NAME pixivlib

- **login account** 
  - ``` -l / --login```
- **download image** 
  - ```-d / --download <image_id> ```
- **download author illustrations**
  - ``` -a / --author <author_id> ```
- **change the thread number** 
  - ``` -m / --max ```
- **download collect illustrations**
  - ``` -s / --start ```
- **download recommend illustrations**
  - ``` -r / --recommend```
- **search illustrations** 
  - ``` -s / --search <search_word> ```
- **ranking illustrations** 
  - ``` -k / --rkaning ```
- **clear cache** 
  - ``` -c / --clear_cache```

| functions                                    | complete |
|----------------------------------------------|----------|
| download picture by image_id                 | ✅        |
| command line                                 | ✅        |
| download picture by image_name               | ✅        |
| download collect illustrations               | ✅        |
| download recommend illustrations             | ✅        |
| multi-threading                              | ✅        |
| asynchronous                                 | ❌        |
| browser automatically login pixiv on startup | ✅        |
| download illustrations by tag name           | ✅        |
