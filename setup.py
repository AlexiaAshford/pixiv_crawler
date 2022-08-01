from setuptools import setup

setup(
    name='pixiv',
    version='1.4',
    packages=['src', 'src.PixivUtil', 'tools'],
    include_package_data=True,  # 自动打包文件夹内所有数据
    url='https://github.com/VeronicaAlexia/pixiv_crawler',
    license='MIT License',
    author='Alex',
    author_email='',
    entry_points={
        "console_scripts": ["pixiv = src.__main__:main"]
    },
    description='download pixiv illustrations',
    zip_safe=True
)
