import os
from os.path import join
import shutil
import urllib.request

source="https://zenodo.org/records/4526477/files/SUBESCO.zip?download=1"

# download zip
zip_path = join("download","zip_files","subesco.zip")
if not os.path.exists(zip_path):
  os.makedirs(join("download","zip_files"), exist_ok=True)
  urllib.request.urlretrieve(source, zip_path)

download_dir = join("download","subesco")
audio_dir = join("audios","subesco")

# unpack zip
if not os.path.exists(download_dir):
  os.makedirs(download_dir)
  shutil.unpack_archive(zip_path, download_dir)

# move audio files to `./audios`
if not os.path.exists(audio_dir):
  os.makedirs(audio_dir)
  src=join(download_dir,"SUBESCO")
  for file in os.listdir(src):
    if not file.endswith(".wav"):
      print(f"{file} is not an audio file.")
      continue
    # shutil.copy2(join(src, file), audio_dir)
    shutil.move( join(src, file), audio_dir)   
