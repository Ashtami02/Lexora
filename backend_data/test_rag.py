from src.rag_chain import LegalRAG

rag = LegalRAG()

response = rag.ask(
    question="What are the conditions for bail?",
    country="India",
    location="Delhi",
    category="Crime",
)

print("=" * 80)
print("LEGAL ANSWER")
print("=" * 80)

print(response["answer"])

print("\n" + "=" * 80)
print("\n" + "=" * 80)
print("SOURCES")
print("=" * 80)

for source in response["sources"]:
    print(
        f"Document : {source['document']}\n"
        f"Page     : {source['page']}\n"
        f"Category : {source['category']}\n"
        f"Location : {source['location']}\n"
    )