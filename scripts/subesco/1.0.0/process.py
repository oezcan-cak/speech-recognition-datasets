import numpy as np
import os
from os.path import join
import pandas as pd
from sklearn.utils import shuffle
from random import randrange

audio_dir = join("audios","subesco")

# NOTE: there is a single file which doesn't follow 
# the convention, since the last value '3]' isn't numeric:
if 'F_02_MONIKA_S_2_SURPRISE_3].wav' in os.listdir(audio_dir):
  os.rename(
      join(audio_dir,'F_02_MONIKA_S_2_SURPRISE_3].wav'),
      join(audio_dir,'F_02_MONIKA_S_2_SURPRISE_3.wav')
  )

# create DataFrame containing audio files
index = pd.Index(os.listdir(audio_dir))
df = pd.DataFrame(index=index)


# define maps to normalize labels
gender_map={"M":"male","F":"female"}

emotion_map={
    'SURPRISE' : 'surprise',
    'NEUTRAL' : 'neutral',
    'DISGUST' : 'disgust',
    'HAPPY' : 'happiness',
    'SAD' : 'sadness',
    'FEAR' : 'fear',
    'ANGRY' : 'anger',
}

get_take=lambda x: int(x.replace(".wav",""))

# set columns
df["gender"]=df.index.str.split("_").str[0].map(gender_map)
df["speaker_number"]=df.index.str.split("_").str[0:2].str.join("_") # see paper
df["speaker"]=df.index.str.split("_").str[2]
df["sentence"]=df.index.str.split("_").str[3:5].str.join("_")
df["emotion"]=df.index.str.split("_").str[5].map(emotion_map)
df["take"]=df.index.str.split("_").str[6].map(get_take)

# create tables dir
tables_dir = "tables"
if not os.path.exists(tables_dir):
  os.makedirs(tables_dir)

# save files table
df.to_csv(join("tables","subesco_files.csv"))

print(df.head())


#################
# create splits #
#################

dimensions = ["arousal", "valence", "dominance"]

# select speakers randomly
speakers = df.speaker.unique()
seed = randrange(1, 10_000)
np.random.seed(seed)
test_speakers = np.random.choice(speakers, size=2, replace=False)
train_speakers = [sp for sp in speakers if not sp in test_speakers]

# shuffle dataframe
random_state = randrange(1, 10_000)
shuffled_df = shuffle(df, random_state=random_state)

# split data into train/test dataframes
test_df = shuffled_df[shuffled_df.speaker.isin(test_speakers)]
train_df = shuffled_df[shuffled_df.speaker.isin(train_speakers)]

# save tables as csv
test_df["emotion"].to_csv(join("tables","subesco_emotions_test.csv"))
train_df["emotion"].to_csv(join("tables","subesco_emotions_train.csv"))
