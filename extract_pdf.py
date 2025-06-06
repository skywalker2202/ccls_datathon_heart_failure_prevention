from pydantic import BaseModel, Field
from agno.embedder.azure_openai import AzureOpenAIEmbedder
from agno.models.azure import AzureOpenAI
from agno.agent import Agent
import os
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader

class Relevent_Data(BaseModel):
    age: float = Field(description="age of patient")
    SBP: float = Field(description="systolic blood pressure")
    BP_med: int = Field(description="use of blood pressure medication")
    LVH_ECG: int = Field(description="left ventricular hypertrophy in the ECG")
    Gender: str = Field (description="gender (female of male)")
    BMI: float = Field (description="BMI (body mass index in kg/m^2)")
    Heart_Rate: float = Field (description="heart rate in beats per minute")
    PMI:int = Field(description="previous myocardial infarction")
    VHD: int = Field(description="ventricular heart disease")

class Relevant_Data_List(BaseModel):
    relevant_data: list[Relevent_Data] = Field(description="List of relevant data")

def extract_data_from_pdf (path):
    model_name = "gpt-4.1-mini"
    api_version="2025-04-01-preview"
    endpoint = "https://workshopccls.openai.azure.com/"
    api_key = "2xoDaxJZ8Z6oBzXl9UhxryKoHiAY9uetTdCeUfxmbRt58GZmOCbvJQQJ99BEACfhMk5XJ3w3AAABACOGkc4n"

    os.environ["AZURE_OPENAI_API_KEY"] = api_key
    os.environ["AZURE_OPENAI_ENDPOINT"] = endpoint
    os.environ["OPENAI_API_VERSION"] = api_version

    vector_db = ChromaDb(
        collection="ccls",
        embedder=AzureOpenAIEmbedder(id='text-embedding-3-small')
    )
    print(vector_db.collection_name)

    knowledge_base = PDFKnowledgeBase(
        path=path,
        vector_db=vector_db,
        reader=PDFReader(chunk=True),
    )
    print(knowledge_base.vector_db)

    agent = Agent(
    model=AzureOpenAI(id=model_name),
    knowledge=knowledge_base,
    instructions=[
        "Cite the exact phrases and section titles from the sources in your response.",
        "Use enumerations to organize your response.",
        "Do not write any other text than the response.",
    ],
    response_model=Relevant_Data_List,
    search_knowledge=True,
)
    agent.knowledge.load()

    res = agent.run("List the relevant data from the doctor's note.")

    data_dict = res.content.relevant_data[0].model_dump()
    print(data_dict)

#extract_data_from_pdf("/Users/suchanda/Desktop/CCLS-Datathon-2025/proj/data/fictional_doctors_note.pdf")