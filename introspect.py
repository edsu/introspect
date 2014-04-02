#!/usr/bin/env python

"""
Attempts to open your Chrome history, find wikipedia URLs and
look up information about them.
"""

import os
import re
import json
import urllib
import sqlite3
import urlparse


def get_articles(dbfile):
    """
    Returns a list of wikipedia articles you've visted.
    """
    db = sqlite3.connect(dbfile)
    q = "SELECT url, visit_count FROM urls ORDER BY visit_count DESC"
    articles = []
    for url, visit_count in db.execute(q):
        u = urlparse.urlparse(url)
        if 'en.wikipedia.org' in u.netloc and u.path.startswith('/wiki/'):
            title = u.path.replace('/wiki/', '')
            articles.append({
                'url': url,
                'title': title,
                'visits': visit_count
            })
    db.close()
    return articles


def get_categories(title):
    """
    Returns a list of Wikipedia categories the an article is in.
    """
    cat_url = ('https://en.wikipedia.org/w/api.php?action=query&format=json&clshow=!hidden&cllimit=500&prop=categories&titles=%s' % title).encode('utf8')
    r = json.loads(urllib.urlopen(cat_url).read())
    page_id, cat_data = r['query']['pages'].items()[0]
    if 'categories' in cat_data:
        return [c['title'] for c in cat_data['categories']]
    return []


def category_counts(dbfile):
    """
    Returns a mapping of categories and the number of times you visited
    an article in that category.
    """
    cat_counts = {}
    articles = get_articles(dbfile)
    open("articles.json", "w").write(json.dumps(articles))
    for article in articles:
        print article
        for cat in get_categories(article['title']):
            # ignore administrative looking categories
            if 'articles' in cat.lower() or 'wikipedia' in cat.lower() \
                    or 'pages' in cat.lower():
                continue
            cat_counts[cat] = cat_counts.get(cat, 0) + article['visits']
    return cat_counts


def add_broader(categories):
    for cat, count in categories.items():
        for broader in get_categories(cat):
            print ("%s <- %s" % (cat, broader)).encode('utf8')
            categories[broader] = categories.get(broader, 0) + count


def main():
    """
    print out categories of wikipdia pages visited.
    """
    home = os.path.expanduser("~")
    dbfile = home + "/Library/Application Support/Google/Chrome/Default/History"
    dbfile = "History"

    categories = category_counts(dbfile)
    add_broader(categories)
    open("categories.json", "w").write(json.dumps(categories, indent=2))



if __name__ == "__main__":
    main()
