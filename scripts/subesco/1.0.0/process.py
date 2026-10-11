import numpy as np
import os
from os.path import join
import pandas as pd
import sklearn
from random import randrange
import shutil

DATASET_DIR = "dataset"
AUDIO_DIR = join("extracted_files", "SUBESCO")

# NOTE: there is a single file which doesn't follow 
# the convention, since the last value '3]' isn't numeric:
if 'F_02_MONIKA_S_2_SURPRISE_3].wav' in os.listdir(AUDIO_DIR):
  os.rename(
      join(AUDIO_DIR,'F_02_MONIKA_S_2_SURPRISE_3].wav'),
      join(AUDIO_DIR,'F_02_MONIKA_S_2_SURPRISE_3.wav')
  )

# create DataFrame containing audio files
filenames = [f for f in os.listdir(AUDIO_DIR) if f.endswith(".wav")]
df = pd.DataFrame(data={"file":filenames})

# define maps
gender_map = {"M":"male", "F":"female"}

emotion_map = {
    "SURPRISE" : "surprise",
    "NEUTRAL" : "neutral",
    "DISGUST" : "disgust",
    "HAPPY" : "happiness",
    "SAD" : "sadness",
    "FEAR" : "fear",
    "ANGRY" : "anger",
}

# set columns
df["speaker"] = df.file.str.split("_").str[2]
df["sentence"] = df.file.str.split("_").str[4]
df["gender"] = df.file.str.split("_").map(lambda x: gender_map[x[0]])
df["speaker_number"] = df.file.str.split("_").str[0:2].str.join("_") # NOTE: see paper
df["emotion"] = df.file.str.split("_").str[5].map(lambda x: emotion_map[x])
df["take"] = df.file.str.split("_").str[6].str[0]

# create speaker-independent splits
speakers = df.speaker.unique()
np.random.seed(42)
test_speakers = np.random.choice(speakers, size=4, replace=False)
train_speakers = [sp for sp in speakers if not sp in test_speakers]

# shuffle dataframe
shuffled_df = sklearn.utils.shuffle(df, random_state=42)

# split data into train/test dataframes
test_df = shuffled_df[shuffled_df.speaker.isin(test_speakers)]
train_df = shuffled_df[shuffled_df.speaker.isin(train_speakers)]

# move files
def move_files(dataframe, destination):
  for file in dataframe["file"]:
    src = join(AUDIO_DIR, file)
    shutil.copy2(src, destination) # shutil.move

train_dir = join("dataset", "train")
test_dir = join("dataset", "test")

for destination in [train_dir, test_dir]:
  if not os.path.exists(destination):
      os.makedirs(destination)

move_files(train_df, train_dir)
move_files(test_df, test_dir)

# add file paths
test_df.file = test_df.file.map(lambda x: f"test/{x}")
train_df.file = train_df.file.map(lambda x: f"train/{x}")

# save tables as csv
test_path = join("dataset", "test.parquet")
test_df.to_parquet(test_path, index=False, engine="fastparquet")

train_path = join("dataset", "train.parquet")
train_df.to_parquet(train_path, index=False, engine="fastparquet")
