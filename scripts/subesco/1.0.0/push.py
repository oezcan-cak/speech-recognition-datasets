from datasets import load_dataset
import pandas as pd
from huggingface_hub import HfApi, login

login()

# push dataset to Huggingface
dataset = load_dataset("audiofolder", data_dir="dataset")
dataset.push_to_hub("oezcan-cak/subecso", private=True)

# add version tag
api = HfApi()
api.create_tag(
    repo_id="oezcan-cak/subecso",
    tag="1.0.0",
    repo_type="dataset",
    tag_message="Initial release",
)
