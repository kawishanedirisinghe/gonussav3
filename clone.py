
import os
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
import pickle

STATE_FILE = "/home/runner/workspace/clone_state.pkl"

def save_state(visited, to_visit):
    with open(STATE_FILE, 'wb') as f:
        pickle.dump({'visited': visited, 'to_visit': to_visit}, f)

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'rb') as f:
            return pickle.load(f)
    return None


class LinkExtractor(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.links = set()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    url = urljoin(self.base_url, value)
                    url = url.split('#')[0] # Remove fragment
                    if urlparse(self.base_url).netloc == urlparse(url).netloc:
                        self.links.add(url)

def download_page(url, path):
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read()
        with open(path, 'wb') as f:
            f.write(content)
        return content.decode('utf-8', 'ignore')
    except Exception as e:
        print(f"Could not download {url}: {e}")
        return None

def clone_website(start_url, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    state = load_state()
    if state:
        visited_pages = state['visited']
        pages_to_visit = state['to_visit']
    else:
        visited_pages = set()
        pages_to_visit = {start_url}

    base_url = start_url
    
    count = 0
    while pages_to_visit and count < 5:
        url = pages_to_visit.pop()
        if url in visited_pages:
            continue

        visited_pages.add(url)
        
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip('/').split('/')
        if not path_parts or not path_parts[-1]:
            file_name = 'index.html'
        else:
            file_name = path_parts[-1]

        if not file_name.endswith(('.html', '.htm')):
             file_name += '.html'

        file_path = os.path.join(output_dir, file_name)

        print(f"Downloading {url} to {file_path}...")
        html_content = download_page(url, file_path)

        if html_content:
            parser = LinkExtractor(base_url)
            parser.feed(html_content)
            for link in parser.links:
                if link not in visited_pages:
                    pages_to_visit.add(link)
        
        count += 1

    save_state(visited_pages, pages_to_visit)
    
    if not pages_to_visit:
        print("Cloning complete.")
        if os.path.exists(STATE_FILE):
            os.remove(STATE_FILE)
    else:
        print(f"Batch complete. {len(pages_to_visit)} pages remaining.")


if __name__ == "__main__":
    website_url = "https://seglobal.b12sites.com/"
    clone_folder = "/home/runner/workspace/111"
    clone_website(website_url, clone_folder)
