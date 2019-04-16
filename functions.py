# pip install pandas
import re
import sys
import pandas as pd


def clean_text(text):
    """
    Utility function to clean text by removing links, special characters
    using simple regex statements. May not be needed.
    """
    return ''.join(re.sub(r'(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\ / \ / \S+)', '', text))
