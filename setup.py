from setuptools import setup

setup(
    name='wallpaper_finder',
    version='0.1.2',
    packages=['wallpaper_changer'],
    url='https://github.com/JarbasAl/wallpaper_changer',
    install_requires=["requests", "bs4", "feedparser", "requests-cache"],
    license='Apache2.0',
    author='jarbasAI',
    author_email='jarbasai@mailfence.com',
    description='platform wallpaper changer'
)
