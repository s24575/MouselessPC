import kaggle
import os
from PIL import Image

def download():
    # https://www.kaggle.com/datasets/gti-upm/leapgestrecog
    print("Downloading dataset...")
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files('gti-upm/leapgestrecog', path='./model/data/', unzip=True)

def show(filepath: str):
    image = Image.open(filepath)
    image.show()

if __name__ == '__main__':
    data_path = "./model/data"
    if not os.path.isdir(data_path):
        os.mkdir(data_path)
        download()
    else:
        print(f"Using existing dataset located in {data_path}")

    # gesture_dir_mapping = {
    #     "0":
    # }

    # test_dir = os.path.join(data_path, "test/test")
    # test_sign_dirnames = os.listdir(test_dir)
    # for test_sign_dirname in test_sign_dirnames:
    #     test_sign_dir_path = os.path.join(test_dir, test_sign_dirname)
    #     for (dirpath, dirnames, filenames) in os.walk(test_sign_dir_path):
    #         for filename in filenames:
    #             filename_path = os.path.join(test_sign_dir_path, filename)
    #             print(filename)
    #             show(filename_path)
    #             break