import glob
import operator
import os
import traceback

# directory where corpus is stored
CORPUS_DIRECTORY = "corpus"

N_GRAMS_MAPPING = {1: "unigram", 2: "bigram", 3: "trigram"}


def create_inverted_index(n):
    """creates inverted index for given n i.e. unigram, bigram, trigram etc"""
    inverted_index = {}
    doc_token_count_mapping = {}
    doc_id = 1
    # noinspection PyBroadException
    try:
        for filename in glob.glob(os.path.join(CORPUS_DIRECTORY, '*.txt')):
            with file(filename) as f:
                doc = f.read()
                doc_name = os.path.splitext(os.path.basename(filename))[0]
                print "Generating index for " + doc_name

                word_list = doc.split()
                terms_count = len(word_list) - n + 1
                doc_token_count_mapping[str(doc_id) + ":" + doc_name] = terms_count

                for i in range(terms_count):
                    if n == 1:
                        term = word_list[i]
                    elif n == 2:
                        term = word_list[i] + " " + word_list[i + 1]
                    else:
                        term = word_list[i] + " " + word_list[i + 1] + " " + word_list[i + 2]

                    if term not in inverted_index:
                        doc_tf_mapping = {doc_id: 1}
                        inverted_index[term] = doc_tf_mapping
                    elif doc_id in inverted_index[term]:
                        doc_tf_mapping = inverted_index[term]
                        value = doc_tf_mapping[doc_id]
                        value += 1
                        doc_tf_mapping[doc_id] = value
                    else:
                        doc_tf_mapping = {doc_id: 1}
                        inverted_index[term].update(doc_tf_mapping)
                f.close()
                doc_id += 1
        print "Token count:"
        print doc_token_count_mapping
    except:
        print "Error while creating index"
        print traceback.format_exc()
    return inverted_index


def generate_term_freq_table(inverted_index, ngram):
    """Generates term frequency table for given inverted index and sorts it from most to least frequent terms"""
    term_freq_mapping = {}

    for term in inverted_index:
        freq = 0
        doc_tf_mapping = inverted_index[term]
        for doc_id in doc_tf_mapping:
            freq += doc_tf_mapping[doc_id]
        term_freq_mapping[term] = freq

    sorted_term_freq_table = sorted(term_freq_mapping.items(), key=operator.itemgetter(1), reverse=True)
    write_term_freq_table(sorted_term_freq_table, ngram)


# noinspection PyBroadException
def write_term_freq_table(sorted_term_freq_table, ngram):
    """write sorted term freq table output to a file"""
    try:
        file_name = "term_freq_table_" + str(ngram) + ".txt"
        term_freq_table_file = open(file_name, 'w')
        for term_freq_pair in sorted_term_freq_table:
            term_freq_table_file.write(str(term_freq_pair[0]) + " ")
            term_freq_table_file.write(str(term_freq_pair[1]))
            term_freq_table_file.write("\n")
        term_freq_table_file.close()
    except:
        print "Error while writing term frequency table to the file"
        print traceback.format_exc()


def generate_doc_freq_table(inverted_index, ngram):
    """Generates doc frequency table for given inverted index and sorts it lexicographically on term"""
    doc_freq_mapping = {}

    for term in inverted_index:
        doc_list = []
        doc_tf_mapping = inverted_index[term]
        for doc_id in doc_tf_mapping:
            doc_list.append(doc_id)
        doc_freq_mapping[term] = doc_list

    sorted_doc_freq_table = sorted(doc_freq_mapping.items(), key=operator.itemgetter(0))
    write_doc_freq_table(sorted_doc_freq_table, ngram)


# noinspection PyBroadException
def write_doc_freq_table(sorted_doc_freq_table, ngram):
    """write sorted doc freq table output to a file"""
    try:
        file_name = "doc_freq_table_" + str(ngram) + ".txt"
        file_doc_freq_table = open(file_name, 'w')
        for doc_freq_pair in sorted_doc_freq_table:
            file_doc_freq_table.write(str(doc_freq_pair[0]) + " ")
            file_doc_freq_table.write(str(doc_freq_pair[1]) + " ")
            list_length = len(doc_freq_pair[1])
            file_doc_freq_table.write(str(list_length))
            file_doc_freq_table.write("\n")
        file_doc_freq_table.close()
    except:
        print "Error while writing doc frequency table to the file"
        print traceback.format_exc()


def main():
    """main function"""
    n = int(raw_input('Enter value of n for n-gram index:'))

    if n in range(1, 4):
        inverted_index = create_inverted_index(n)
        generate_term_freq_table(inverted_index, N_GRAMS_MAPPING[n])
        generate_doc_freq_table(inverted_index, N_GRAMS_MAPPING[n])
    else:
        print "Please enter a value in the range 1 to 3"


if __name__ == "__main__":
    main()
