import re
import sys

def strip_links(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # regex to find [Text](Link) and replace with Text
    # We want to keep the text inside the brackets
    new_content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        strip_links(sys.argv[1])
