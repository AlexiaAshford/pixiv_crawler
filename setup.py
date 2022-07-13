from setuptools import setup

setup(
    name='pixivlib',
    version='1.2',
    packages=['src', 'src.PixivUtil', 'tools'],
    include_package_data=True,  # 自动打包文件夹内所有数据
    url='https://github.com/VeronicaAlexia/pixiv_crawler',
    license='MIT License',
    author='Alex',
    author_email='',
    entry_points={"console_scripts": ["pixivlib = src.__main__:main"]},
    description='download pixiv illustrations',
    zip_safe=True
)
