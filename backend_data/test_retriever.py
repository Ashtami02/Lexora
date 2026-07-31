from pprint import pprint

from src.retriever import LegalRetriever


def main():

    retriever = LegalRetriever()

    docs = retriever.retrieve_context(
        question="What are the conditions for bail?",
        country="india",
        location="delhi",
        category="crime",
        k=5,
    )

    pprint(docs)


if __name__ == "__main__":
    main()