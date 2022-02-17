"""
Programmer: Sam Pickell
Date: February 13, 2022
Filename: debian_architecture_parse.py
Description: Canonical technical assessment.
    Develop a Python commandline tool that
    takes an architecture as an argument and
    downloads the corresponding contents file
    from a Debian mirror. Then, output the
    top 10 packages that have the most files
    associated with them.
"""

import sys
import shutil
import gzip
import os
import operator
import requests


def download_package(arch_name):
    """
    Function to obtain the debian package
    associated with the passed in architecture
    name.

    :param
    arch_name: string
        Name of the architecture the user input
    :return:
        void
    """

    # Attempt to obtain the user specified
    # architecture from Debian mirror and save
    # to a file
    contents_file = requests.get("http://ftp.uk.debian.org/debian/dists/stable/main/Contents-"
                                 + arch_name + ".gz")

    with open("Contents-" + arch_name + ".gz", "wb") as my_archive:
        my_archive.write(contents_file.content)
    my_archive.close()

    # Extract the file from the gz archive
    with gzip.open("Contents-" + arch_name + ".gz", "rb") as gz_file:
        with open("Contents-" + arch_name, "wb") as new_file:
            shutil.copyfileobj(gz_file, new_file)
    gz_file.close()
    new_file.close()

    # Remove the gz archive
    os.remove("Contents-" + arch_name + ".gz")


def file_parse(filename):
    """
    Parses the downloaded Contents file, adds packages and filecount
    to a dictionary, and prints out the top 10 packages based on filecount

    :param
    filename: string
        Name of the contents file
    :return:
        void
    """

    # Create a dictionary to store package names and file counts
    package_dictionary = {}

    # Open the downloaded contents file
    with open(filename, "r") as content_file:
        # Find package(s), and increment count (or add to dictionary)
        for curr_line in content_file:
            # Keep on the packages listed on the line
            curr_line = curr_line.split()[-1]

            # Store this line of packages in a list
            curr_line_packages = curr_line.split(",")

            # Add each package in the current line package list
            # to the dictionary, or update an existing package's count
            for i, my_enum in enumerate(curr_line_packages):
                if curr_line_packages[i] in package_dictionary:
                    package_dictionary[my_enum] = \
                        package_dictionary[my_enum] + 1
                else:
                    package_dictionary[curr_line_packages[0]] = 1
    content_file.close()

    # Sort the dictionary, and print the top 10 packages and their file count:
    sorted_packages = dict(reversed(sorted(package_dictionary.items(), key=operator.itemgetter(1))))
    sorted_list = list(sorted_packages)[:10]

    for i in range(10):
        print(str(i+1) + ". " + sorted_list[i] + " " + str(sorted_packages[sorted_list[i]]))


def main():
    """
    The main driver function. Asks for user input (architecture),
    downloads the appropriate contents file, and then parses the file.

    :return:
        void
    """

    # Obtain the architecture from user input
    user_input = (sys.argv[1])

    # Download contents package
    download_package(user_input)

    # Output to the terminal
    print()
    print("Top 10 packages based on number of associated files for architecture: " + user_input)
    print()

    # Parse and display the top 10 packages
    file_parse("Contents-" + user_input)
    print()


main()
