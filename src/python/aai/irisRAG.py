from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_iris import IRISVector
from langchain_openai import OpenAIEmbeddings,ChatOpenAI
import os,iris



from langchain.chains.conversation.memory import ConversationSummaryMemory
from langchain.chat_models import ChatOpenAI
from sqlalchemy import create_engine



class RagOpr:
    def __init__(self, host='localhost', port=1972, namespace='USER', username='SuperUser', password='SYS') -> None:          
        self.CONNECTION_STRING = f"iris://{username}:{password}@{host}:{port}/{namespace}"
        self.engine = create_engine(self.CONNECTION_STRING)
        self.COLLECTION_NAME = "AgenticAIRAG"
        
       
    def ingestDoc(self):                
        #Check if document is defined, by selecting from table
        #If not defined then INGEST document, Otherwise back
        embeddings = OpenAIEmbeddings()	
        #Load the document based on the fle type
        loader = TextLoader("/irisdev/app/docs/IRIS2025-1-Release-Notes.txt", encoding='utf-8')      
        
        documents = loader.load()        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=0)
        
        texts = text_splitter.split_documents(documents)
                       
        #COLLECTION_NAME = "rag_document"
        db = IRISVector.from_documents(
            embedding=embeddings,
            documents=texts,
            collection_name = self.COLLECTION_NAME,
            connection_string=self.CONNECTION_STRING,
        )

        db = IRISVector.from_documents(embedding=embeddings,documents=texts, collection_name = self.COLLECTION_NAME, connection_string=self.CONNECTION_STRING,)
    
    def ragSearch(self,prompt):
        #Check if collections are defined or ingested done.
        # if not then call ingest method
        embeddings = OpenAIEmbeddings()	
        db2 = IRISVector (
            embedding_function=embeddings,    
            collection_name=self.COLLECTION_NAME,
            connection_string=self.CONNECTION_STRING,
        )
        docs_with_score = db2.similarity_search_with_score(prompt)
        relevant_docs = ["".join(str(doc.page_content)) + " " for doc, _ in docs_with_score]
        
        #Generate Template
        template = f"""
        Prompt: {prompt}

        Relevant Docuemnts: {relevant_docs}
        """
       
        return template

    #Check if Vectpr Search table is created, Return TRUE is created, otherwise return FALSE
    def check_VS_Table(self) -> bool:	
        iris.cls("%ZEmbedded.Utils").SetNameSpace("USER")    
        query = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'SQLUser' AND TABLE_NAME = 'AgenticAIRAG'"	
        statement = iris.sql.exec(query)
        if statement.ResultSet._GetRows() > 0:
            return True
        else:
            return False
        

