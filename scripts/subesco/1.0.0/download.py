import os
from os.path import join
import shutil
import urllib.request

source="https://zenodo.org/records/4526477/files/SUBESCO.zip?download=1"
zip_path = "subesco.zip"
extracted_files_dir = "extracted_files"

# download zip
if not os.path.exists(zip_path):
  urllib.request.urlretrieve(source, zip_path)

# unpack zip
if not os.path.exists(extracted_files_dir):
  os.makedirs(extracted_files_dir)
  shutil.unpack_archive(zip_path, extracted_files_dir)
