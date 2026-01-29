"""
Sample Python Code for Documentation Testing
This file contains examples for the AI Documentation Generator.
"""


def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    return total / count


def sort_items_by_key(items, key, reverse=False):
    sorted_items = sorted(items, key=lambda x: x.get(key, 0), reverse=reverse)
    return sorted_items


def validate_email(email):
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


class DataProcessor:
    def __init__(self, data_source):
        self.data_source = data_source
        self.cache = {}
    
    def fetch_data(self, query):
        if query in self.cache:
            return self.cache[query]
        
        # Simulated data fetching
        result = f"Data for: {query}"
        self.cache[query] = result
        return result
    
    def clear_cache(self):
        self.cache.clear()
        return True


def process_text(text, lowercase=True, remove_punctuation=False):
    import string
    
    if lowercase:
        text = text.lower()
    
    if remove_punctuation:
        text = text.translate(str.maketrans('', '', string.punctuation))
    
    return text.strip()
