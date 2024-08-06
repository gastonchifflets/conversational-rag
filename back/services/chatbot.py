import bs4
from langchain import hub
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders.merge import MergedDataLoader
from langchain_openai import ChatOpenAI

def makeIaCall(input):
  llm = ChatOpenAI(model="gpt-3.5-turbo")

  # 1. Load, chunk and index the contents of the blog to create a retriever.
  web_loader = WebBaseLoader(["https://www.promtior.ai/","https://www.promtior.ai/service","https://www.promtior.ai/use-cases"])

  pdf_loader = PyPDFLoader("../sources/AI-Engineer.pdf")

  loader_all = MergedDataLoader(loaders=[web_loader, pdf_loader])
  docs = loader_all.load()

  text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
  splits = text_splitter.split_documents(docs)
  vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
  retriever = vectorstore.as_retriever()

  # 2. Incorporate the retriever into a question-answering chain.
  system_prompt = (
      "You are an assistant for question-answering tasks. "
      "Use the following pieces of retrieved context to answer "
      "the question. If you don't know the answer, say that you "
      "don't know. Use three sentences maximum and keep the "
      "answer concise."
      "\n\n"
      "{context}"
  )

  prompt = ChatPromptTemplate.from_messages(
      [
          ("system", system_prompt),
          ("human", "{input}"),
      ]
  )

  question_answer_chain = create_stuff_documents_chain(llm, prompt)
  rag_chain = create_retrieval_chain(retriever, question_answer_chain)

  response = rag_chain.invoke({"input": input})
  return response["answer"]