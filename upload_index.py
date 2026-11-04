import os
from huggingface_hub import HfApi

repo = "aanya09shukla/wiki-rag-index"
api = HfApi(token=os.environ["HF_TOKEN"])
api.create_repo(repo, repo_type="dataset", private=True, exist_ok=True)
api.upload_large_folder(folder_path=r"C:\rag\wiki_index", repo_id=repo, repo_type="dataset")
print("done")