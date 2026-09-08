import numpy as np
import os
from os.path import join
import pandas as pd
from sklearn.utils import shuffle
from random import randrange
import shutil

dataset_dir = "dataset"
audio_dir = join("extracted_files", "SUBESCO")

# NOTE: there is a single file which doesn't follow 
# the convention, since the last value '3]' isn't numeric:
if 'F_02_MONIKA_S_2_SURPRISE_3].wav' in os.listdir(audio_dir):
  os.rename(
      join(audio_dir,'F_02_MONIKA_S_2_SURPRISE_3].wav'),
      join(audio_dir,'F_02_MONIKA_S_2_SURPRISE_3.wav')
  )

# create DataFrame containing audio files
filenames = os.listdir(audio_dir)
df = pd.DataFrame(data={"file":filenames})

# define maps and functions to normalize labels
gender_map = {"M":"male","F":"female"}

emotion_map = {
    'SURPRISE' : 'surprise',
    'NEUTRAL' : 'neutral',
    'DISGUST' : 'disgust',
    'HAPPY' : 'happiness',
    'SAD' : 'sadness',
    'FEAR' : 'fear',
    'ANGRY' : 'anger',
}

# set columns
# NOTE: `.map(gender_map)` doesn't raise error if key isn't in dict => use lambda!
df["gender"] = df.file.str.split("_").map(lambda x: gender_map[x[0]])
df["speaker_number"] = df.file.str.split("_").str[0:2].str.join("_") # NOTE: see paper
df["speaker"] = df.file.str.split("_").str[2]
df["sentence"] = df.file.str.split("_").str[3:5].str.join("_")
df["emotion"] = df.file.str.split("_").str[5].map(lambda x: emotion_map[x])
df["take"] = df.file.str.split("_").str[6].str[0]

# create speaker-independent splits
speakers = df.speaker.unique()
print(speakers)
np.random.seed(42)
test_speakers = np.random.choice(speakers, size=4, replace=False)
train_speakers = [sp for sp in speakers if not sp in test_speakers]

# shuffle dataframe
shuffled_df = shuffle(df, random_state=42)

# split data into train/test dataframes
test_df = shuffled_df[shuffled_df.speaker.isin(test_speakers)]
train_df = shuffled_df[shuffled_df.speaker.isin(train_speakers)]

def move_files(dataframe, destination):
  if not os.path.exists(destination):
    os.makedirs(destination)
  for file in dataframe["file"]:
    src = join(audio_dir, file)
    shutil.copy2(src, destination)
    # shutil.move( join(src, file), audio_dir)   

train_dir = join("dataset", "train")
# move_files(train_df, train_dir)

test_dir = join("dataset", "test")
# move_files(test_df, test_dir)

# add file paths
test_df.file = test_df.file.map(lambda x: join("test", x))
train_df.file = train_df.file.map(lambda x: join("train", x))

# save tables as csv
test_df.to_csv("dataset/test.csv", index=False)
train_df.to_csv("dataset/train.csv", index=False)
