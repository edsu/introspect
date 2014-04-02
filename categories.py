#!/usr/bin/env python

"""
Print out the categories of wikipedia articles you vist.
"""

import json

cat_counts = json.loads(open("categories.json").read())
cats = cat_counts.keys()
cats.sort(lambda a, b: cmp(cat_counts[b], cat_counts[a]))

for cat in cats:
    print ("%s - %s" % (cat, cat_counts[cat])).encode('utf8')

