import re
import time
import Constants
from Helper import cleanup, crawl, set_keyword_regex, setup


def main():
    """Main Method"""
    setup("Task2A", "Task2A_Crawled_Pages.txt")
    cleanup("Task2A", "Task2A_Crawled_Pages.txt")
    seed_url = raw_input('Enter the Seed URL (Press 1 for default seed URL): ')
    keyword = raw_input('Enter the keyword: ')
    if seed_url == "1":
        seed_url = Constants.DEFAULT_SEED_URL
    keyword_regex = r'.*' + re.escape(keyword) + r'.*'
    set_keyword_regex(keyword_regex)
    start_time = time.time()
    print "Crawling started for Task2A with Seed URL : " + seed_url
    crawled_pages = set()
    crawl(seed_url, True, crawled_pages)
    print "Time required in seconds : " + str(time.time() - start_time)
    print "Crawling completed."
    # printing the crawled pages list
    print crawled_pages


if __name__ == "__main__":
    main()
