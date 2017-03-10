import time
from Helper import load


def main():
    """Main Method"""
    file_name = raw_input("Enter file name ? ")
    start_time = time.time()
    print "Inlinks fetch started for file : " + file_name
    load(str(file_name))
    print "Time required in seconds : " + str(time.time() - start_time)
    print "Completed."


if __name__ == "__main__":
    main()
