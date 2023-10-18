'''This module provides utility functions for
parsing JSON data and searching for keywords within JSON fields.'''

import json


def func(required_field, keyword):
    return (required_field, keyword)


def parse_json(json_str: str, required_fields=None, keywords=None, keyword_callback=None):
    """Parse a JSON string, search for specified keywords in specified fields,
    and trigger a callback function for each found keyword."""

    if None in (required_fields, keywords, keyword_callback):
        return

    json_doc = json.loads(json_str)

    for field in required_fields:
        if json_doc.get(field):
            words = json_doc[field].lower().split()
            for keyword in keywords:
                if keyword.lower() in words:
                    keyword_callback(required_field=field, keyword=keyword)
    return
