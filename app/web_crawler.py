from langchain_community.document_loaders import RecursiveUrlLoader
from bs4 import BeautifulSoup


def extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    # remove useless sections
    for tag in soup(["script", "style", "noscript", "header", "footer"]):
        tag.extract()

    return soup.get_text(separator=" ", strip=True)


def load_site():
    loader = RecursiveUrlLoader(
        "https://rathod-vaibhav.github.io/",
        max_depth=3,
        extractor=extract_text
    )
    return loader.load()
