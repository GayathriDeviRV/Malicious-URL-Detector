import re
import pandas as pd
import tldextract
from math import log2
from collections import Counter
from urllib.parse import urlparse


def calculate_entropy(url):
    p, lns = Counter(url), float(len(url))
    return -sum(count/lns * log2(count/lns) for count in p.values())


def extract_features(url):
    features = {}

    # Basic URL properties
    features['url_len'] = len(url)
    features['url_entropy'] = calculate_entropy(url)

    # Domain properties
    parsed_url = tldextract.extract(url)
    features['pdomain_len'] = len(parsed_url.domain)
    features['tld_len'] = len(parsed_url.suffix)
    features['subdomain_len'] = len(parsed_url.subdomain)

    # Parse the full URL to get path and query
    parsed_full_url = urlparse(url)
    path = parsed_full_url.path
    query = parsed_full_url.query

    # Count occurrences of certain characters
    features['url_count_dot'] = url.count('.')
    features['url_count_https'] = url.count('https')
    features['url_count_http'] = url.count('http')
    features['url_count_hyphen'] = url.count('-')
    features['url_count_www'] = url.count('www')
    features['url_count_atrate'] = url.count('@')
    features['url_count_hash'] = url.count('#')
    features['url_count_underscore'] = url.count('_')
    features['url_count_ques'] = url.count('?')
    features['url_count_equal'] = url.count('=')
    features['url_count_amp'] = url.count('&')

    # Character properties
    features['url_count_letter'] = sum(c.isalpha() for c in url)
    features['url_count_digit'] = sum(c.isdigit() for c in url)

    # Path properties
    features['path_len'] = len(path)
    features['path_count_no_of_dir'] = path.count('/')

    # Query properties
    features['query_len'] = len(query)
    features['query_count_components'] = query.count('&')

    # Ensure features are in the correct order and all features are present
    feature_order = [
        'url_len', 'url_entropy', 'url_count_dot', 'url_count_https', 'url_count_http',
        'url_count_hyphen', 'url_count_www', 'url_count_atrate', 'url_count_hash',
        'url_count_underscore', 'url_count_ques', 'url_count_equal', 'url_count_amp',
        'url_count_letter', 'url_count_digit', 'pdomain_len', 'tld_len', 'subdomain_len',
        'path_len', 'path_count_no_of_dir', 'query_len', 'query_count_components'
    ]
    features = {key: features.get(key, 0) for key in feature_order}

    return pd.DataFrame([features])
