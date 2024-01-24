import openai
import os
import pickle
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load PDF
loader = PyPDFLoader("/Users/bensolis-cohen/Projects/Chat with my data/data/iMessage Green Street Hooligans.pdf")
pages_pickle_file = 'data/pages.pickle'
if os.path.exists(pages_pickle_file):
    with open(pages_pickle_file, 'rb') as f:
        pages = pickle.load(f)
else:
    pages = loader.load()
    with open(pages_pickle_file, 'wb') as f:
        pickle.dump(pages, f)

# Split documents
# TODO(bensc): Fix problem where we have duplicate documents over multiple pages.
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splits = text_splitter.split_documents(pages)

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
template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer. 
{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

llm_name = "gpt-3.5-turbo"
llm = ChatOpenAI(model_name=llm_name, temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectordb.as_retriever(search_kwargs={"k": 10}),
    return_source_documents=True,
 #   chain_type="refine"#,
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)

while True:
    question = input("Please ask a question then press [enter]: ")
    result = qa_chain.invoke({"query": question})
    print(result["result"])
    print()