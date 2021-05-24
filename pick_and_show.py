'''
pick_and_show.py contains the functions related to ouputing an image to
the user.
These include listing files for the user to pick from, receiving and
validating the user's input, and showing the chosen image to the user.

By: Dena E. Utne
'''

import requests
import sys
import os
from PIL import Image


def list_largest_files(sorted_file_data, NUMBER_FILES_TO_OUTPUT):
    '''
    Input:  sorted_file_data is a pointer to the sorted list containing
            tuples holding the image_name and corresponding file_size.

            NUMBER_FILES_TO_OUTPUT is an integer constant indicating
            the number of files to list in a message to the user.

    Prints a table containing the 10 largest image files from largest to
    smallest.

    Returns: None
    '''

    print("\nThe 10 largest comic image files from largest to \
            smallest are as follows:\n")
    print(f"{'File nr.':<12}{'Image name':<40}{'Image size (bytes)':<20}")
    print(f"{'':_<70}\n")

    for i in range(NUMBER_FILES_TO_OUTPUT):
        print(f"{i + 1:>2}{'':<10}{sorted_file_data[i][0]:<40}\
                {sorted_file_data[i][1]:>8}")


def get_file_choice(sorted_file_data, NUMBER_FILES_TO_OUTPUT):
    '''
    Input:      sorted_file_data is a pointer to the sorted file_data list
                containing tuples holding the image_name and corresponding
                file_size.

                NUMBER_FILES_TO_OUTPUT is a constant indicating the number of
                files to list in a message to the user.
    Asks the user to pick a file by number. Validates user input.

    Returns:    index (integer) to the tuple in sorted_file_data containing
                the image file to open.
    '''
    input_error_message = f"Invalid input. You may only enter integers "\
                          f"from 1 to {NUMBER_FILES_TO_OUTPUT} inclusive!"
    input_ok = False        # Flag. Is True when user input is acceptable.
    while not input_ok:
        input_str = input("\nPlease enter the file number of the file you "
                          "would like me to open: ")

        if not input_str.isdigit():
            print(input_error_message)
        elif (int(input_str) > NUMBER_FILES_TO_OUTPUT) or (int(input_str) < 1):
            print(input_error_message)
        else:
            input_ok = True

    # Tuple number is one less than file number size list indices start at
        # 0 and file numbers start at 1.
    return int(input_str)-1


def put_image_in_res(image_name, URL_PATH_TO_IMAGES):
    '''
    Input:      image_name is a string containing the name of the image file
                to open.

                URL_PATH_TO_IMAGES is a string containing the url path to the
                image files. It is a constant.
    Tries to open the web page indicated by URL_PATH_TO_IMAGES and iamge_name.
    Saves the response as a response object res.
    The function is supposed to make a graceful exit if an error is
    encountered, but nothing I tried to do to catch the error entirely
    gracefully worked.

    Returns: Repsonse object res.
    '''
    print("Downloading " + URL_PATH_TO_IMAGES + "/" + image_name)
    res = requests.get(URL_PATH_TO_IMAGES + "/" + image_name)
    res.raise_for_status()
    return res


def write_image(res, image_name):
    '''
    Input:      res is a response object.

                image_name is a string containing the file name of the image
                file to write.

    Makes the subdirectory ./xkcd.
    Tries to create and write a local file named image_name.
    Prints an error to the user if uable to write the output file named
    image_name.
    '''
    os.makedirs('xkcd', exist_ok=True)

    try:
        image_file = open('xkcd/' + image_name, 'wb')
    except OSError as exc:
        print(f"Unable to open a local file to copy the image and "
              f"proceed with the program.\nThe error is: {exc}")
        sys.exit()
    else:
        for chunk in res.iter_content(100000):
            image_file.write(chunk)
        image_file.close()


def copy_image(image_name, URL_PATH_TO_IMAGES):
    '''
    Input:      image_name is a string containing the name of the image file
                to open.

                URL_PATH_TO_IMAGES is a string containing the url path to the
                image files. It is a constant.
    Calls put_image_in_res function to get a response object. Then calls
    write_image function to write the image to disk.

    Variables:  res is a response object.

    Returns:    None
    '''
    res = put_image_in_res(image_name, URL_PATH_TO_IMAGES)
    write_image(res, image_name)


def show_image(image_name):
    '''
    Input:      image_name is a string containing the name of the image
                file to open.

    Uses the PIL Image module to open the file indicated by image_name.
    Displays the image file for the user.

    Source for some of the code here:
    https://stackoverflow.com/questions/35286540/display-an-image-with-python/35286593

    Returns:    None
    '''
    image_file = Image.open(r"xkcd/" + image_name)
    image_file.show()
    image_file.close()


def interact_with_user(file_data, NUMBER_FILES_TO_OUTPUT, URL_PATH_TO_IMAGES):
    '''
    Input:      file_data is a list of tuples holding the image_name and
                corresponding file_sizes.

                NUMBER_FILES_TO_OUTPUT is an integer contstant indicating the
                number of files to list in a message to the user.

                URL_PATH_TO_IMAGES is a string containing the url path to the
                image files. It is a constant.

    Calls the function list_largest_files to list the largest n files where
    n = NUMBER_FILES_TO_OUTPUT.

    Calls the function tuple_to_open to obtain user's choice.
    Calls the function copy_image to download the user's chosen image.
    Calls the function show_image to display the user's chosen image.
    '''

    list_largest_files(file_data, NUMBER_FILES_TO_OUTPUT)
    tuple_to_open = get_file_choice(file_data, NUMBER_FILES_TO_OUTPUT)
    copy_image(file_data[tuple_to_open][0], URL_PATH_TO_IMAGES)
    show_image(file_data[tuple_to_open][0])
