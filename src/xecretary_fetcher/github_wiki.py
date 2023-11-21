import os
import shutil
from git.repo import Repo

from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex


def trim_owner(url):
    return url.split("/")[3]


def trim_repo(url):
    return url.split("/")[4]


def remove_dir(path):
    shutil.rmtree(path)


class GithubWiki:
    def __init__(self, url: str):
        # URL example: https://github.com/torippy01/llm_poc/wiki/_Footer
        self.owner = trim_owner(url)
        self.repo = trim_repo(url)
        self.repo_url = f"https://github.com/{self.owner}/{self.repo}.wiki.git"
        self.index_id = f"{self.owner}.{self.repo}"
        self.tmp_url = f"tmp/{self.index_id}"
        if os.path.isdir(self.tmp_url):
            remove_dir(self.tmp_url)
        Repo.clone_from(self.repo_url, self.tmp_url)

    def create_index(self):
        # Wikiのテキストからindexを作成
        reader = SimpleDirectoryReader(input_dir=self.tmp_url)
        docs = reader.load_data()
        index = GPTVectorStoreIndex.from_documents(docs)

        # indexをstorage/*に保存
        index.set_index_id(self.index_id)
        persist_dir = f"storage/{self.index_id}"
        index.storage_context.persist(persist_dir)

        # clean up
        remove_dir(self.tmp_url)
