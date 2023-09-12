####################################################################################################
#
# This file prepares the datasets for training and testing.
# Using the kaggle dataset for cats and dogs.
#
####################################################################################################

import os
import urllib.request
import path_util
import zipfile
import shutil

# Dataset: https://www.microsoft.com/en-us/download/details.aspx?id=54765
kaggle_dataset = "https://download.microsoft.com/download/3/E/1/3E1C3F21-ECDB-4869-8368-6DEBA77B919F/kagglecatsanddogs_5340.zip"


# Download dataset save to /tmp in app project
def download_dataset():
    # Download dataset and display progress
    print("Downloading dataset...")
    urllib.request.urlretrieve(
        kaggle_dataset,
        "{}/kagglecatsanddogs_5340.zip".format(path_util.get_tmp()),
        reporthook=lambda blocknum, blocksize, totalsize: print(
            "Downloading: {}%".format(int(blocknum * blocksize * 100 / totalsize)),
            end="\r",
        ),
    )
    print("Download complete.")

    # Extract dataset
    print("Extracting dataset...")
    with zipfile.ZipFile(
        "{}/kagglecatsanddogs_5340.zip".format(path_util.get_tmp()), "r"
    ) as zip_ref:
        zip_ref.extractall(path_util.get_tmp())
    print("Extraction complete.")

    # Renaming folders to lowercase for consistency folder structure
    print("Renaming folders to lowercase...")
    # Rename PetImages to petimages
    os.rename(
        "{}/PetImages".format(path_util.get_tmp()),
        "{}/petimages".format(path_util.get_tmp()),
    )
    # Rename Cat to cat
    os.rename(
        "{}/petimages/Cat".format(path_util.get_tmp()),
        "{}/petimages/cat".format(path_util.get_tmp()),
    )
    # Rename Dog to dog
    os.rename(
        "{}/petimages/Dog".format(path_util.get_tmp()),
        "{}/petimages/dog".format(path_util.get_tmp()),
    )
    print("Renaming complete.")

    # Initialize train and test datasets folders
    print("Initializing train and test datasets folders...")
    for folder in ["train", "test"]:
        if not os.path.exists("{}/datasets/{}".format(path_util.get_root, folder)):
            os.makedirs("{}/datasets/{}".format(path_util.get_root(), folder))
            print("Created {} folder.".format(folder))
        else:
            print("Folders {} already exist.".format(folder))
    print("Initialization train and test datasets folders complete.")


# Split dataset into train and test datasets
def split_dataset():
    # Split dataset
    print("Splitting dataset...")
    for folder in ["cat", "dog"]:
        for i, file in enumerate(
            os.listdir("{}/petimages/{}".format(path_util.get_tmp(), folder))
        ):
            # Split dataset into 80% train and 20% test
            if i < 10000:
                os.rename(
                    "{}/petimages/{}/{}".format(path_util.get_tmp(), folder, file),
                    "{}/datasets/train/{}_{}".format(
                        path_util.get_root(), folder, file
                    ),
                )
            else:
                os.rename(
                    "{}/petimages/{}/{}".format(path_util.get_tmp(), folder, file),
                    "{}/datasets/test/{}_{}".format(path_util.get_root(), folder, file),
                )
    print("Splitting dataset complete.")


# Clean up tmp folder
def clean_up():
    # Clean up tmp folder
    print("Cleaning up tmp folder...")
    for folder in os.listdir(path_util.get_tmp()):
        if folder != ".gitignore":
            if os.path.isdir("{}/{}".format(path_util.get_tmp(), folder)):
                shutil.rmtree("{}/{}".format(path_util.get_tmp(), folder))
            else:
                os.remove("{}/{}".format(path_util.get_tmp(), folder))
    print("Cleaning up tmp folder complete.")
    print("Dataset preparation complete.")


# Clean up datasets folder
def clean_dataset():
    print("Cleaning up datasets folder...")
    if os.path.exists("{}/datasets".format(path_util.get_root())):
        for folder in os.listdir("{}/datasets".format(path_util.get_root())):
            if folder != ".gitignore":
                if os.path.isdir("{}/datasets/{}".format(path_util.get_root(), folder)):
                    shutil.rmtree("{}/datasets/{}".format(path_util.get_root(), folder))
                else:
                    os.remove("{}/datasets/{}".format(path_util.get_root(), folder))
    print("Cleaning up datasets folder complete.")


# Main function
if __name__ == "__main__":
    # Help argument
    if "--help" in os.sys.argv:
        print("Usage: python datasets_prep.py [--clean]")
        print("  --clean: Clean up tmp folder")
        print("  --clean-all: Clean up tmp folder and datasets folder")
        os.sys.exit()

    # If user have --clean argument, clean up tmp folder
    if "--clean" in os.sys.argv:
        clean_up()
        os.sys.exit()

    # Clean datasets/** and tmp folder
    if "--clean-all" in os.sys.argv:
        clean_dataset()
        clean_up()
        os.sys.exit()

    # Ask user if they want to prepare the dataset
    while True:
        answer = input("Do you want to prepare the dataset? (y/n): ")
        if answer == "y":
            # clean up datasets and tmp folder
            clean_dataset()
            clean_up()
            # start preparing dataset
            download_dataset()
            split_dataset()
            clean_up()
            break
        elif answer == "n":
            print("Dataset preparation skipped.")
            break
        else:
            print("Please answer y or n.")
