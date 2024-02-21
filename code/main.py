import openai
import os
import pickle
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load messages
loader = TextLoader("/Users/bensolis-cohen/Projects/Chat with my data/data/messages.txt")
pages = loader.load()

# Split documents
# TODO(bensc): Fix problem where we have duplicate documents over multiple pages.
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
splits_raw = text_splitter.split_documents(pages)

splits = []
seen_texts = set()
i = 0

counters = {
    "num_non_dups" : 0,
    "total_docs" : 0,
}
for split in splits_raw:
    counters["total_docs"] += 1
    if split.page_content not in seen_texts:
        counters["num_non_dups"] += 1
        seen_texts.add(split.page_content)
        splits.append(split)

# Set up OpenAI and Chroma
openai.api_key = os.environ['OPENAI_API_KEY']
persist_directory = 'docs/chroma/'
embedding = OpenAIEmbeddings()

# Set up langchain
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.langchain.plus"

#vectordb = Chroma.from_documents(documents=splits, persist_directory=persist_directory, embedding=embedding)
#vectordb.persist()

vectordb = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding
)


# Build prompt
template = """Use the following pieces of context to answer the question at the end. Try to be a bit funny but make sure you convey all the information you can find.
{context}
Question: {question}
Informative Answer based on the chat conversation above:"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

llm_name = "gpt-3.5-turbo"
llm = ChatOpenAI(model_name=llm_name, temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectordb.as_retriever(search_kwargs={"k": 7}),
    return_source_documents=True,
 #   chain_type="refine"#,
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)

print(counters)

while True:
    question = input("Please ask a question then press [enter]: ")
    result = qa_chain.invoke({"query": question})
    print(result["result"])
    print()