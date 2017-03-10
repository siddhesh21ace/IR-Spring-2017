import time
import Constants
from Helper import cleanup, crawl, setup


def main():
    """Main Method"""
    setup("Task1", "Task1_Crawled_Pages.txt")
    cleanup("Task1", "Task1_Crawled_Pages.txt")
    start_time = time.time()
    print "Crawling started for Task1 with Seed URL : " + Constants.DEFAULT_SEED_URL
    crawled_pages = set()
    crawl(Constants.DEFAULT_SEED_URL, False, crawled_pages)
    print "Time required in seconds : " + str(time.time() - start_time)
    print "Crawling completed."
    # printing the crawled pages list
    print crawled_pages


if __name__ == "__main__":
    main()


