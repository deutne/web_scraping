'''
Web Scraping Program
For IBE 151. Due: 5 November 2020
By: Dena E. Utne (Note: I am making an individual submission.)

Scrapes the web site https://xkcd.com. Collects the file names and sizes of
comic images that are in the standard format for the web site. Sorts the
images in descending order by file size. Prints a table containing the 10
largest files for the user. Asks the user to pick one image file to open.
Validates user input. Opens the image file.
'''

import sys

# Web scraping program.
# Write your code here. Have fun!
from scrape import scrape
from sort_lib import merge_sort_alg
from pick_and_show import interact_with_user


def main():
    '''
    Variables:  file_data is a list of tuples holding the image_name and
                    corresponding file_sizes.

                URL_OF_STIE is a string containing the url of the web site to
                scrape. It is a constant.

                URL_PATH_TO_IMAGES is a string containing the url path to the
                image files. It is a constant.

                NUMBER_FILES_TO_OUTPUT is an integer constant indicating the
                number of files to list in a message to the user.

    Opens log file.
    Calls scrape to collect unsorted file_data.

    Calls merge_sort_alg to obtain sorted file_data using a merge sort
    algorithm.

    Calls interact_with_user to list the largest files, have the user
    pick one, and open it.
    '''

    URL_OF_SITE = 'https://xkcd.com'
    URL_PATH_TO_IMAGES = "https://imgs.xkcd.com/comics"
    NUMBER_FILES_TO_OUTPUT = 10

    try:
        log_file = open('web_scraping_log_file.txt', 'w')
    except OSError as exc:
        print(f"Unable to open the log file and proceed with the program.\n"
              f"The error is: {exc}")
        sys.exit()
    else:
        file_data = scrape(URL_OF_SITE, URL_PATH_TO_IMAGES, log_file)
        file_data = merge_sort_alg(file_data)
        interact_with_user(file_data, NUMBER_FILES_TO_OUTPUT,
                           URL_PATH_TO_IMAGES)
        log_file.close()


main()
