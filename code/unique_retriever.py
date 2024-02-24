from langchain_core.documents import Document
from langchain.chains import RetrievalQA
from langchain_core.retrievers import BaseRetriever
from langchain_core.pydantic_v1 import Field
from typing import List
from langchain_core.callbacks import (
    AsyncCallbackManagerForChainRun,
    CallbackManagerForChainRun,
    Callbacks,
)

class UniqueRetrievalQA(RetrievalQA):
    """RetrievalQA that returns unique documents
    """

    retriever: BaseRetriever = Field(exclude=True)

    def _get_docs(
        self,
        question: str,
        *,
        run_manager: CallbackManagerForChainRun,
    ) -> List[Document]:
        """Get docs."""
        docs = self.retriever.get_relevant_documents(
            question, callbacks=run_manager.get_child()
        )
        doc_set = set()
        unique_docs_list = []
        i = 0
        for doc in docs:
            doc_contents = doc.page_content
            if doc_contents not in doc_set:
                i += 1
                doc_set.add(doc_contents)
                unique_docs_list.append(doc)
            if i >= 7: # TODO(bensc): Get this externally
                break
        return unique_docs_list

    @property
    def _chain_type(self) -> str:
        """Return the chain type."""
        return "retrieval_qa_unique"