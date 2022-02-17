# PixivCrawler

| 功能           | 实现   |
|--------------|------|
| id下载插画       | ✅   |
| 命令行          | ✅   |
| 搜索插画          | ✅   |
| 下载收藏插画       | ✅  |
| 多线程 主要是担心封IP | ❌ |
| 异步 主要是担心封IP  | ❌ |
| 唤起浏览器获取token | ✅  |

### 目前Pixiv不支持login api进行账号登入，只能从web获取

## Pixiv API
### 感谢项目 [pixivpy](https://github.com/upbit/pixivpy) 提供的Pixiv API

## 使用方法
```bash
输入首字母
h | help               --- 显示说明
q | quit               --- 退出正在运作的程序
d | picture            --- 输入id或者url下载插画
t | recommend          --- 下载pixiv推荐插画
s | start              --- 下载账号收藏插画
n | tag name           --- 输入插画名或者表情名
```
## 运行脚本
```bash
python main.py
```
