import time
from Helper import cleanup, crawl, setup

SEED_URL = "https://en.wikipedia.org/wiki/Solar_power"


def main():
    """Main Method"""
    setup("Task3", "Task3_Crawled_Pages.txt")
    cleanup("Task3", "Task3_Crawled_Pages.txt")
    start_time = time.time()
    print "Crawling started for Task3 with Seed URL : " + SEED_URL
    crawled_pages = set()
    crawl(SEED_URL, False, crawled_pages)
    print "Time required in seconds : " + str(time.time() - start_time)
    print "Crawling completed."
    # printing the crawled pages list
    print crawled_pages


if __name__ == "__main__":
    main()
