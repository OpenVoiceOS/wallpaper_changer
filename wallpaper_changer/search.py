import bs4
import feedparser
import requests
from requests_cache import CachedSession
from datetime import timedelta, datetime

_expire_after = timedelta(hours=1)
_session = CachedSession(backend='memory', expire_after=_expire_after)


def latest_reddit(sub="wallpapers"):
    feed = "https://www.reddit.com/r/{sub}/.rss"\
        .format(sub=sub.replace("/r/", ""))
    entries = feedparser.parse(feed)["entries"]
    wallpapers = []
    for e in entries:
        data = {
            "author": e.get("author", sub),
            "title": e.get("title", sub),
            "imgLink": "",

        }
        html = e["summary"]
        soup = bs4.BeautifulSoup(html, "html.parser")
        for url in soup.find_all("a"):
            url = url["href"]
            if ".jpg" not in url or "thumbs.redditmedia" in url:
                continue
            data["imgLink"] = url
        if data["imgLink"]:
            wallpapers.append(data)
    return wallpapers


def latest_wpcraft(cat=None, n_pages=1):
    base_url = "https://wallpaperscraft.com"
    categories = [
        '3d', 'abstract', 'animals', 'anime', "art", "black", "cars", 'city',
        'dark', 'fantasy', 'flowers', 'food', 'holidays', 'love', 'macro',
        'minimalism', 'motorcycles', 'music', 'nature', 'other', 'smilies',
        'space', 'sport', 'hi-tech', 'textures', 'vector', 'words',
        '60_favorites'
    ]
    if cat:
        assert cat in categories
        base_url = base_url + "/catalog/" + cat

    wallpapers = []
    n = 0
    for i in range(1, n_pages + 1):
        try:
            if i > 1:
                url = base_url + "/page" + str(i)
            else:
                url = base_url
            html = _session.get(url).text
            soup = bs4.BeautifulSoup(html, 'html.parser')
            if not n:
                n = soup.find("li", {"class": "pager__item "
                                              "pager__item_last-page"}).find(
                    "a")

                n = int(n["href"].split("/")[-1].replace("page", ""))
            if n < i:
                break  # end of pages

            div = soup.find('ul', {'class': 'wallpapers__list'})
            for wp in div.find_all("li", {"class": "wallpapers__item"}):
                data = {}
                wp = wp.find("a", {"class": "wallpapers__link"})
                res = wp.find("span", {"class": "wallpapers__info"})
                tags = wp.find_all("span", {"class": "wallpapers__info"})[1]
                data["tags"] = tags.text.split(", ")
                data["url"] = base_url + wp["href"]
                data["res"] = \
                    [r.strip() for r in res.text.split("\n") if r.strip()][1]
                try:
                    data["rating"] = float(res.find("span",
                                                    {
                                                        "class": "wallpapers__info-rating"})
                                           .text)
                except:
                    pass
                im_id = wp["href"].split("/")[-1]
                data[
                    "imgLink"] = "https://images.wallpaperscraft.com/image/{image_id}_{res}.jpg" \
                    .format(image_id=im_id, res=data["res"])
                wallpapers.append(data)
        except:
            pass  # TODO debug random failures
    return wallpapers


def random_unsplash(cat=None, size='1920x1080'):
    url = 'https://source.unsplash.com/' + size + '/' + '?'
    tags = ["random"]
    if cat:
        url += cat
        tags = [cat]
    # notice usage of requests, not cache session
    r = requests.get(url)
    return {"imgLink": r.url, "tags": tags}


def latest_unsplash(cat=None, size='1920x1080', n=5):
    images = []
    if n < 1:
        n = 1
    for i in range(n):
        image = random_unsplash(cat, size)
        if image not in images:
            images.append(image)
    return images

