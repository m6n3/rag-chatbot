import os
import sys

import bs4
import gcp_llm

from langchain import document_loaders
from langchain import PromptTemplate
from langchain import text_splitter
from langchain.embeddings import google_palm
from langchain.llms import GooglePalm

from langchain.schema import runnable
from langchain.vectorstores import Chroma
import prompts
import requests

SITE_MAPS = [
    "https://cloud.google.com/healthcare-api/sitemap.xml",
]
MAX_PAGES = 1000

_singleton_chatbot_llm = None


def sitemaps_to_urls(sitemaps):
    urls = []
    for sitemap in sitemaps:
        resp = requests.get(sitemap)
        bs = bs4.BeautifulSoup(resp.content, "xml")
        urls += [e.text for e in bs.find_all("loc")]
    return [url for url in urls if "/reference/" not in url and "?hl" not in url]


def urls_to_docs(urls):
    loader = document_loaders.UnstructuredURLLoader(urls=urls)
    docs = loader.load()
    splitter = text_splitter.CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=100
    )
    doc_chunks = splitter.split_documents(docs)
    return doc_chunks


class ChatbotLLM:
    def __init__(self):
        self.urls = sitemaps_to_urls(SITE_MAPS)[:MAX_PAGES]
        docs = urls_to_docs(self.urls)
        db = Chroma.from_documents(docs, google_palm.GooglePalmEmbeddings())
        self.retriever = db.as_retriever()
        self.gcp_llm = gcp_llm.GCPLLM()
        self.template = prompts.CHATBOT_PROMPT
        self.cached_consent_store_summary = ""

    def run(self, user_query, consent_store_context):
        if len(self.cached_consent_store_summary) == 0:
            self.cached_consent_store_summary = self.gcp_llm.run(consent_store_context)
        query = self.template.safe_substitute(
            consent_store_summary=self.cached_consent_store_summary,
            urls=self.urls,
        )
        rag_chain = (
            {"context": self.retriever, "question": runnable.RunnablePassthrough()}
            | PromptTemplate.from_template(query)
            | GooglePalm(temperature=0.0)
        )
        return rag_chain.invoke(user_query)


def get_llm():
    global _singleton_chatbot_llm
    if _singleton_chatbot_llm is None:
        _singleton_chatbot_llm = ChatbotLLM()
    return _singleton_chatbot_llm
