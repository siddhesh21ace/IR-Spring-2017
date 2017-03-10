from math import log
from time import time
from operator import itemgetter

# Global Variables

# Mapping of pages to their corresponding in-links
PAGE_INLINKS_MAPPING = {}
# Mapping of pages to their corresponding number of out-links
PAGE_OUTLINKS_MAPPING = {}
# Initial PageRank values
PAGE_RANK_MAPPING = {}
# Revised PageRank values
NEW_PAGE_RANK_MAPPING = {}
# Set of all pages
PAGES = set()
# Set of sink pages who don't have outgoing links
SINK_PAGES = set()
# PageRank Damping/Teleportation factor
TELEPORT_FACTOR = 0.85
# Max consecutive iterations count for convergence
ITERATIONS_COUNT = 4
# NO. of pages
N = 1
# Top PageRank Pages count
NO_OF_TOP_PAGES_BY_RANKS = 50
# Top Inlink Pages count
NO_OF_TOP_PAGES_BY_INLINKS = 5


def load(graph_file):
    """parses the graph file given to it and calls functions to populate all the mappings"""
    global N
    file_content = open(graph_file, 'r')
    counter = 0
    for line in file_content.readlines():
        words = line.split()
        populate_page_inlinks_mapping(words)
        populate_pages(words)
        counter += 1
    file_content.close()
    N = len(PAGES)
    populate_page_outlinks_mapping()
    populate_sink_pages()


def populate_page_inlinks_mapping(words):
    """populates the page-inlinks mapping"""
    page = words[0]
    inlinks = set(words[1:])
    PAGE_INLINKS_MAPPING[page] = inlinks
    if page in PAGE_INLINKS_MAPPING:
        PAGE_INLINKS_MAPPING[page] = inlinks.union(PAGE_INLINKS_MAPPING[page])
    else:
        PAGE_INLINKS_MAPPING[page] = inlinks


def populate_pages(words):
    """populates the list for pages"""
    PAGES.add(words[0])


def populate_page_outlinks_mapping():
    """populates the page-outlinks mapping"""
    for page in PAGE_INLINKS_MAPPING:
        for inlink in PAGE_INLINKS_MAPPING[page]:
            if inlink in PAGE_OUTLINKS_MAPPING:
                PAGE_OUTLINKS_MAPPING[inlink] += 1
            else:
                PAGE_OUTLINKS_MAPPING[inlink] = 1


def populate_sink_pages():
    """populates the list for sink pages"""
    for page in PAGES:
        if page not in PAGE_OUTLINKS_MAPPING:
            SINK_PAGES.add(page)


def initialize_pagerank():
    """populates initial page rank values for pages"""
    for page in PAGES:
        PAGE_RANK_MAPPING[page] = 1.0 / N


def calculate_perplexity():
    """calculates Perplexity of the PageRank Distribution"""
    entropy = 0
    for page in PAGES:
        entropy += PAGE_RANK_MAPPING[page] * log(PAGE_RANK_MAPPING[page], 2)
    return 2 ** -entropy


def calculate_pagerank():
    """calculates page rank for pages"""
    counter = 0
    perplexity = 0
    iteration = 0

    initialize_pagerank()
    while counter < ITERATIONS_COUNT:
        sink_page_rank = 0
        for page in SINK_PAGES:
            sink_page_rank += PAGE_RANK_MAPPING[page]
        for page in PAGES:
            NEW_PAGE_RANK_MAPPING[page] = float(1 - TELEPORT_FACTOR) / N
            NEW_PAGE_RANK_MAPPING[page] += TELEPORT_FACTOR * (float(sink_page_rank) / N)
            for inlinks in PAGE_INLINKS_MAPPING[page]:
                NEW_PAGE_RANK_MAPPING[page] += TELEPORT_FACTOR * float(PAGE_RANK_MAPPING[inlinks]) / float(
                    PAGE_OUTLINKS_MAPPING[inlinks])
        for page in PAGES:
            PAGE_RANK_MAPPING[page] = NEW_PAGE_RANK_MAPPING[page]
        new_perplexity = calculate_perplexity()
        if abs(new_perplexity - perplexity) < 1:
            counter += 1
        else:
            counter = 0
        perplexity = new_perplexity
        iteration += 1
        print("Perplexity after iteration " + str(iteration) + " : " + str(perplexity))


def list_top_pages_by_rank():
    """sorts page ranks and prints top n values"""
    sorted_mapping = sorted(NEW_PAGE_RANK_MAPPING.items(), key=itemgetter(1), reverse=True)
    count = 0
    while count < NO_OF_TOP_PAGES_BY_RANKS and count < len(sorted_mapping):
        print sorted_mapping[count]
        count += 1


def list_top_pages_by_inlinks():
    """sorts page inlinks and prints top n values"""
    page_inlinks_count_mapping = {}
    for page in PAGE_INLINKS_MAPPING:
        page_inlinks_count_mapping[page] = len(PAGE_INLINKS_MAPPING.get(page))
    sorted_mapping = sorted(page_inlinks_count_mapping.items(), key=itemgetter(1), reverse=True)
    count = 0
    while count < NO_OF_TOP_PAGES_BY_INLINKS and count < len(sorted_mapping):
        print sorted_mapping[count]
        count += 1


def get_source_count():
    """counts the number of pages with no inlinks (sources)"""
    counter = 0
    for page in PAGE_INLINKS_MAPPING:
        if not PAGE_INLINKS_MAPPING[page]:
            counter += 1
            print page
    return counter


def main():
    """Main method"""
    filename = raw_input('Enter the filename: ')
    load(str(filename))
    start_time = time()
    print "<--------------------PageRank Calculation Started-------------------->"
    calculate_pagerank()
    print "<--------------------PageRank Calculation Complete-------------------->"
    print "Time required in second : " + str(time() - start_time)
    print "<--------------------Top 50 pages by PageRank-------------------->"
    list_top_pages_by_rank()
    print "<--------------------Top 5 pages by Inlink counts--------------->"
    list_top_pages_by_inlinks()
    print "<---------------------Statistics--------------------->"
    print "Total number of pages in the graph are : " + str(N)
    print "Total number of pages in the graph with no out-links (sinks) are : " + str(len(SINK_PAGES))
    print "Total number of pages in the graph with no in-links (sources) are : " + str(
        get_source_count())


if __name__ == "__main__":
    main()
