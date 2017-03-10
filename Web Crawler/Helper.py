import urllib2
import os
from os.path import exists
from bs4 import BeautifulSoup
import shutil
import Constants
import re
import traceback
import time
from urlparse import urlparse

# Counter for the saved crawled pages numbering
COUNTER = 1
# directory to hold crawled html pages/text
CRAWLED_PAGES_DIRECTORY = "Task1"
# file for the crawled URLs
CRAWLED_PAGES_LIST_FILE = "Task1_Crawled_Pages.txt"
# regex pattern for anchor text/link matching
LINK_REGEX = ""


def set_keyword_regex(keyword_regex):
    """initialize regex for the keyword"""
    global LINK_REGEX
    LINK_REGEX = keyword_regex


def setup(directory, filename):
    """set file, folder path for the crawled data"""
    global CRAWLED_PAGES_DIRECTORY, CRAWLED_PAGES_LIST_FILE
    CRAWLED_PAGES_DIRECTORY = directory
    CRAWLED_PAGES_LIST_FILE = filename


def get_redirected_url(page):
    """get actual URLs considering redirection and canonicalization"""
    opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
    request = opener.open(page)
    page = request.url
    soup = BeautifulSoup(request, "html.parser")
    data = soup.findAll('link', attrs={'rel': 'canonical'})
    for div in data:
        page = div.get('href')
    return page.encode("UTF-8"), soup


def merge(list1, list2):
    for element in list2:
        if element not in list1:
            list1.append(element)


def cleanup(directory, filename):
    """delete/create folder/file between crawl processes"""
    if os.path.exists(directory):
        shutil.rmtree(directory)
    if exists(filename):
        os.remove(filename)
    os.makedirs(directory)


def crawl(seed_url, is_focused, crawled_pages):
    """crawl logic"""
    frontier = [seed_url]
    next_depth = []
    depth = 1
    redirects_file = open('redirect.txt', 'a')

    while frontier and len(crawled_pages) < Constants.MAX_URL_COUNT and depth <= Constants.MAX_DEPTH:
        orig_page = frontier.pop(0)
        page, soup = get_redirected_url(orig_page)
        if orig_page != page:
            redirects_file.write(orig_page + '\n')
        if '#' in page:
            page = page[:page.index('#')]
        if page not in crawled_pages:
            # Politeness policy
            # time.sleep(1)
            if is_focused:
                urls = fetch_all_focused_urls(page, soup)
            else:
                urls = fetch_all_urls(page, soup)
            merge(next_depth, urls)
            crawled_pages.add(page)
            if not frontier:
                frontier, next_depth = next_depth, []
                depth = +1
    redirects_file.close()


def write_content(page, html_content):
    """writing URLs to file and saved web pages to folder"""
    global COUNTER
    filename = 'File_' + str(COUNTER) + '.html'
    content_file = open(CRAWLED_PAGES_DIRECTORY + '\\' + filename, 'w')
    # storing the URL along with the page content
    content_file.write(page + "\n" + html_content)
    crawled_urls_file = open(CRAWLED_PAGES_LIST_FILE, 'a')
    crawled_urls_file.write(str(COUNTER) + ' ' + page + '\n')
    COUNTER += 1
    content_file.close()
    crawled_urls_file.close()


def fetch_all_urls(page, soup):
    """fetch all urls for a page considering keywords, rules etc"""
    page_urls = []
    try:
        write_content(page, soup.prettify().encode("utf-8"))
        data = soup.findAll('div', attrs={'id': 'bodyContent'})
        for div in data:
            for link in div.findAll('a', {'href': re.compile('^/wiki/')}):
                href = link.get('href')
                # Avoid administrative pages having ':'
                if ':' in href:
                    continue
                if "Clinton_Foundation" in href:
                    print page
                url = Constants.WIKIPEDIA_BASE_URL + href
                # For '#' in url, extract the link up to '#'
                if '#' in url:
                    url = url[:url.index('#')]
                page_urls.append(url.encode("utf-8"))
    except:
        print "Error while fetching page URLs!"
        print traceback.format_exc()
    return page_urls


def fetch_all_focused_urls(page, soup):
    """fetching urls for Focused crawling"""
    page_urls = []
    try:
        write_content(page, soup.prettify().encode("utf-8"))
        data = soup.findAll('div', attrs={'id': 'bodyContent'})
        for div in data:
            for link in div.findAll('a', {'href': re.compile('^/wiki/')}):
                href = link.get('href')
                anchor_text = link.text.encode("utf-8")
                # Avoid administrative links having ':'
                if ':' in href:
                    continue
                url = Constants.WIKIPEDIA_BASE_URL + href
                # For '#' in url, extract the link up to '#'
                if '#' in url:
                    url = url[:url.index('#')]
                # Regex for the link matching to the given keyword
                link_match = re.search(LINK_REGEX, '"'+str(url)+'"', re.IGNORECASE)
                anchor_text_match = re.search(LINK_REGEX, '"'+anchor_text+'"', re.IGNORECASE)
                # Add to the frontier iff the keyword is present in the anchor text or the link text
                if anchor_text_match or link_match:
                    page_urls.append(url.encode("utf-8"))
    except:
        print "Error while fetching page URLs!"
        print traceback.format_exc()
    return page_urls


def dfs_focused_crawl(base_url, depth, crawled_pages):
    """Crawl logic for depth first crawler"""
    if depth > Constants.MAX_DEPTH or len(crawled_pages) == Constants.MAX_URL_COUNT:
        return
    base_url, soup = get_redirected_url(base_url)
    if base_url in crawled_pages:
        return
    time.sleep(1)
    urls = fetch_all_focused_urls(base_url, soup)
    crawled_pages.add(base_url)
    for page in urls:
        dfs_focused_crawl(page, depth + 1, crawled_pages)


def load(url_file):
    file_page_mapping = {}
    page_inlinks_mapping = {}
    pages = set()
    redirects = set()
    file_content = open(url_file, 'r')
    for line in file_content.readlines():
        words = line.split()
        file_no = words[0]
        url = words[1]
        url_parts = urlparse(url)

        page = url_parts.path.split('/')[-1]
        file_page_mapping[file_no] = page
        page_inlinks_mapping[page] = set()
        pages.add(page)
    file_content.close()

    print "Graph File content parsed."

    file_content = open('redirect.txt', 'r')
    for line in file_content.readlines():
        redirects.add(line.splitlines()[0])
    file_content.close()

    print redirects
    print "Redirects File content parsed."

    counter = 0
    for file_no in file_page_mapping:
        print counter
        page_title = file_page_mapping[file_no]
        filename = 'File_' + file_no + '.html'
        page_titles = fetch_all_page_titles(filename, redirects)
        for p in page_titles.intersection(pages):
            if p == page_title:
                continue
            page_inlinks_mapping[p].add(page_title)
        counter += 1

    filename = 'G1_Graph.txt'
    page_inlinks_file = open(filename, 'a')

    for p in page_inlinks_mapping:
        page_inlinks_file.write(p + " " + " ".join(page_inlinks_mapping[p]) + '\n')
    page_inlinks_file.close()


def fetch_all_page_titles(filename, redirects):
    page_titles = set()
    soup = BeautifulSoup(open(CRAWLED_PAGES_DIRECTORY + '\\' + filename), "html.parser")
    data = soup.findAll('div', attrs={'id': 'bodyContent'})
    for div in data:
        for link in div.findAll('a', {'href': re.compile('^/wiki/')}):
            href = link.get('href')
            # Avoid administrative pages having ':'
            if ':' in href:
                continue
            url = Constants.WIKIPEDIA_BASE_URL + href
            if '#' in href:
                url = url[:url.index('#')]
            if url in redirects:
                print "before :" + url
                url, dummy_soup = get_redirected_url(url)
                print "after :" + url
                print "------------------------------------------"
            url_parts = urlparse(url)
            title = url_parts.path.split('/')[-1]
            page_titles.add(title)
    return page_titles



