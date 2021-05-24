'''
scrape.py contains the web scraping functions of the web scraping program.
By: Dena E. Utne
'''

import requests
import lxml
from bs4 import BeautifulSoup
from json import dump
import sys


def dnl_web_page_into_soup(url, log_file):
    '''
    Input:      url is a string indicating the url of page to try to download.
                log_file is the log_file to output to.

    Receives a url, writes a message to the log_file indicating which page the
    function is trying to download.

    Tries to opens the web site at the url. Prints error message to user if
    unable to gain acess to the web site.

    If the function can open the url, it uses lxml to parse the web page and
    save it as a BeautifulSoup object.

    Returns:    res: response object from web server.
                soup: BeautifulSoup object.
    '''
    log_file.write(f"Attempting to download the page {url}.\t")

    try:
        res = requests.get(url)
    except Exception as exc:
        print(f"There was a problem gaining access to the web site at {url}. "
              f"The program is terminating.")
        sys.exit()
    else:
        soup = BeautifulSoup(res.text, 'lxml')
        return res, soup


def get_image_name(soup, log_file):
    '''
    Input:      soup is a BeautifulSoup object.
                log_file is the log file to output to.

    Finds the html tags for of the comic image file indicated by css selector
    (#comic img) from the soup object.

    Uses the src attribute to find the URL of comic image file and extracts the
    file name from the end of the URL.

    Returns:    Name of the comic image file to download. Empty string if the
    file is out-of-format.
    '''
    comic_img_tag = soup.select('#comic img')
    if comic_img_tag == []:
        log_file.write(f"\nI HAVE TO SKIP THIS FILE.\n")
        return ""

    # Takes the string associated with src and splits it into a
    # list of strings called image_url.
    image_url = str(comic_img_tag[0].get('src')).split("/")
    return image_url[len(image_url)-1]


def get_image_file_size(url):
    '''
    Input:  url is a string indicating the url of the image file.

    Uses the Content-length component of the image file's header to obtain the
    file size.

    Source for code in this function:
    https://stackoverflow.com/questions/14270698/get-file-size-using-python-requests-while-only-getting-the-header

    Returns: an integer indicating the size of the image file in bytes.

    '''
    return int(requests.get(url, stream=True).headers['Content-length'])


def find_url_of_prev(soup, url_of_site):
    '''
    Input:      soup is a BeautifulSoup object.
                url_of_site is the url of the web site being scraped.
    Determines the url of the comic prior to the comic in soup.

    Uses the rel="prev" attribute in html <a> tags to locate the reference to
    the prior comic.

    Determines the complete url to the prior comic by getting the 'href'
    attribute of the prior comic and concatenating it to the end of
    url_of_site.

    Source for first line:  Sweigart, Al "Automate the Boring Stuff with
                            Python", 2e, p. 289.

    Returns:    String containing complete url to the prior comic.
    '''
    prevLink = soup.select('a[rel="prev"]')[0]
    url_of_prev = url_of_site + prevLink.get('href')
    return url_of_prev


def output_json(file_data, json_ouput_file_name):
    '''
    Input:      A pointer to file_data: a list of tuples holding image_name
                and its corresponding file_size for all of the scraped comic
                images.

                json_ouput_file_name is a string containing the name of the
                json output file.
    '''
    with open(json_ouput_file_name, 'w') as json_file:
        dump(file_data, json_file)


def scrape(URL_OF_SITE, URL_PATH_TO_IMAGES, log_file):
    '''
    Input:      URL_OF_SITE is a string containing the base url of the web site
                to scrape. It is a constant.

                URL_PATH_TO_IMAGES is a string containing the url path to the
                image files. It is a constant.

                log_file is the log file to output to.

    Variables:  url_to_dnl is a string containing the current web page to
                download.

                url_to_start_with is a string containing the first web page to
                download if one is not beginning the scrape at the main page.
                It is for debugging purposes.

                res is a response object from a web server.

                soup is a BeatufiulSoup object made by parsing url_to_dnl.

                image_name is a string containing the name of a comic image
                files extracted from soup.

                file_size is an integer indicating the size of the comic
                image image_name in bytes.

                file_data is a list of tuples holding image_name and its
                corresponding file_size for all of the scraped comic images.

                url_to_start_with is for debugging purposes. It is a string and
                can be used for having the web scraping start much closer to
                the end of the sequence of pages to scrape. When put into use,
                it should be assigned to url_to_dnl before the while loop is
                entered.

     The scrape function loops through the url's of web pages to download using
     a while loop.
     In each iteration of the while loop, the following steps occur:
        Call dnl_web_page_into_soup function to try to open a url and download
        the web page into a soup object.

        Call get_image_name function to get the name of the comic image in
        soup.

        Write the image_name to the log file.

        If image_name is not an empty string, then the image file is in the
        expected format.
            Call get_image_file_size function to get the file size of the
            image,and save image_name and file_size as a tuple in the
            list file_data.
            It is worth noting that the headers of the comic image files
            are read, but the images themselves are not downloaded at this
            point.

        Otherwise, the image file is NOT in the expected format.
            Print a message to the user, and skip determing the image file's
            size and recording its name and size in file_data.

        Call the find_url_of_prev function to get the prior page's url and
        reassign url_to_dnl to this web page.

        Close the response object res.
    The while loop terminates when the url_to_dnl ends in '#'.

    output_json is called to ouput file_data in json format.

    Returns: file_data
    '''

    # url_to_start_with = 'https://xkcd.com/10'  # For debugging purposes.
    url_to_dnl = URL_OF_SITE
    # url_to_dnl = url_to_start_with            # For debugging purposes.
    file_data = []

    # If the URL ends in '#', the final image has already been downloaded.
    while url_to_dnl[-1] != "#":

        # Call function to try to open a url and download the web page
        # into a soup object.
        res, soup = dnl_web_page_into_soup(url_to_dnl, log_file)

        # Call funtion to get the name of the comic image in soup.
        image_name = get_image_name(soup, log_file)
        log_file.write(f"The image name is {image_name}.\n")
        log_file.flush()

        # If image_name is not an empty string, then the image file
        # is in the expected format.
        # Call a function to get the file size of the image, and
        # save image_name and file_size in the dictionary file_data.
        if image_name != "":
            file_size = get_image_file_size(URL_PATH_TO_IMAGES +
                                            "/" + image_name)
            file_data.append((image_name, file_size))

        else:   # The image file is NOT in the expected format.
            print(f"Image file named {url_to_dnl} is a different format. "
                    f"Skipping.")

        # Call a function to get the prior page's url.
        url_to_dnl = find_url_of_prev(soup, URL_OF_SITE)

        res.close()

    # Call a functiion to output json data.
    output_json(file_data, "file_data.json")
    return(file_data)
