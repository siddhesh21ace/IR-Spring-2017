import glob
import re
import traceback
import urllib2
import os
from urlparse import urlparse
import time
from bs4 import BeautifulSoup
import shutil

# downloaded pages from HW1 Task 1
RAW_PAGES_DIRECTORY = "raw_pages"
# directory where corpus is stored
CORPUS_DIRECTORY = "corpus"


# noinspection PyBroadException
def generate_corpus():
    """Process raw Wikipedia articles from HW1 to generate clean corpus"""
    try:
        for filename in glob.glob(os.path.join(RAW_PAGES_DIRECTORY, '*.txt')):
            with file(filename) as f:
                url = f.readline()
                url_parts = urlparse(url)
                article_name = url_parts.path.split('/')[-1]
                article_name = urllib2.unquote(article_name).decode("utf-8")
                # remove - and _ from the title
                article_name = re.sub(ur'[-_\u2013\u005F]', '', article_name.strip())

                print "Processing file: " + f.name

                content = f.read()
                content = content.lower()

                soup = BeautifulSoup(content, "html.parser")
                soup.prettify().encode("utf-8")

                # remove title of contents and other meta tags
                remove_elements('id', 'toc', soup)
                remove_elements('id', 'sitesub', soup)
                remove_elements('id', 'contentsub', soup)
                remove_elements('id', 'jump-to-nav', soup)
                remove_elements('class', 'metadata', soup)
                remove_elements('class', 'mw-editsection', soup)
                remove_elements('class', 'external free', soup)
                remove_elements('class', 'reference', soup)

                # remove see_also, reference tags etc
                see_also_tag = soup.find('span', attrs={'id': 'see_also'})
                references_tag = soup.find('span', attrs={'id': 'references'})

                if see_also_tag and see_also_tag.parent:
                    remove_following_elements(see_also_tag)
                elif references_tag and references_tag.parent:
                    remove_following_elements(references_tag)

                header = soup.find('h1').get_text().encode("utf-8")
                data = soup.findAll('div', attrs={'id': 'bodycontent'})

                body = ""
                for div in data:
                    body += div.get_text().encode("utf-8")
                content = header + body
                content = transform(content)
                write(content, article_name)
                f.close()
    except:
        print "Error while processing of raw html content"
        print traceback.format_exc()


def remove_following_elements(tag):
    """this function removes all the tags after the given tag from the page"""
    tokens = tag.parent.find_all_next()
    for token in tokens:
        token.decompose()


def remove_elements(attr_name, attr_value, soup):
    """remove tags like see also, references etc from the html content"""
    for token in soup.find_all(attrs={attr_name: attr_value}):
        token.decompose()


def is_english(word):
    """do not consider non-english words"""
    try:
        word.decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def transform(content):
    """text transformation on the content"""
    content = re.sub(ur'[@_!\s^&*?#=+$~%:;\\/|<>(){}[\]"\'\u2019]', ' ', content.decode("utf-8"))
    content = content.encode("utf-8")
    content_word_list = []
    for word in content.split():
        if not is_english(word):
            continue
        word = handle_punctuation(word)
        if word != '' or word != ' ':
            word = handle_punctuation(word)
            content_word_list.append(word.strip())
    content = " ".join(content_word_list)
    return content


def handle_punctuation(word):
    """handles starting and trailing punctuations in the words"""
    if word[-1:] == "." and numeric(word[:-1]):
        word = word[:-1]
        return word

    if numeric(word):
        return word

    if len(word) > 3 and word[0].isalnum() and word[-1:] == "." and word[1] == ".":
        return word

    while word[-1:] == "-" or word[-1:] == "," or word[-1:] == ".":
        word = word[:-1]

    while word[:1] == "-" or word[:1] == "," or word[:1] == ".":
        word = word[1:]

    return word


def numeric(word):
    return re.match(r'^[\-]?[0-9,]*\.?[0-9]+$', word)


# noinspection PyBroadException
def write(content, file_name):
    """write content to the file"""
    try:
        terms_file = open(CORPUS_DIRECTORY + '\\' + file_name + ".txt", 'w')
        terms_file.write(content)
        terms_file.close()
    except:
        print "Error while writing content to the file"
        print traceback.format_exc()


def setup():
    if os.path.exists(CORPUS_DIRECTORY):
        shutil.rmtree(CORPUS_DIRECTORY)
    os.mkdir(CORPUS_DIRECTORY)


def main():
    """Main function"""
    print "Corpus generation started."

    start_time = time.time()
    generate_corpus()
    print "Time required in seconds : " + str(time.time() - start_time)


if __name__ == "__main__":
    main()
