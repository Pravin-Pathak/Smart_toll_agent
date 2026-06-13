import os
import sys
import chromadb
from llama_index.core.storage import storage_context

#from llama_index.core import chroma_collection, vector_store, index, query_engine
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

from llama_index.core import VectorStoreIndex,StorageContext,Document
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.core import Settings
from llama_index.core.agent.workflow import FunctionAgent

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.tools import calculate_speed_fine, mock_toll_wallet_deduction

app = FastAPI(tittle="Smart Toll AI Agent System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

API_KEY = "AIzaSyAK0VUcme-8-HpFMxNha69ecI_oC7QdxOk"
google_llm = GoogleGenAI(model="gemini-2.5-flash",api_key=API_KEY)
google_embed = GoogleGenAIEmbedding(model="models/text-embedding-004",api_key=API_KEY)
Settings.llm = google_llm
Settings.embed = google_embed

os.makedirs("data",exist_ok = True)
law_file_path =os.path.join("data","traffic_laws.csv")

if os.path.exists(law_file_path):
    with open(law_file_path,"r") as f:
        law_text_context = f.read()

else:
    law_text_context="No traffic laws found"

db_client = chromadb.PersistentClient(path="./chroma_db_storage")
chroma_collection= db_client.get_or_create_collection("isolated_traffic_laws_v2")

vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

print("[Backend] indexing traffic laws document into ChromaDB")

clean_document = Document(text=law_text_context,doc_id="static_smart_city_law_book")

index = VectorStoreIndex([clean_document],storage_context=storage_context,embed_model=google_embed)

query_engine = index.as_query_engine()
print("[Backend] ChromDB initialization complete")





def lookup_traffic_laws(violation_description:str) ->str:
    """
    Searches the official smart city traffic laws and penal code database .
    Use thsi to look up specific penalty sections, flat rates , and rules for a violation type.
    """

    return str(query_engine.query(violation_description))

agent = FunctionAgent(
    name="Toll_inspector_agent",
    description="An aintelligent traffic enforcement agent that evaluates vehicle logs, checks legal frameworks , and handles fine processing.",
    tools=[lookup_traffic_laws,calculate_speed_fine,mock_toll_wallet_deduction],
    llm=google_llm,
)




@app.post("/process-toll/")
async def process_toll(vehicle_id:str,file:UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        csv_data_string = df.to_string()

        execution_prompt = f""" 
You are acting aas the automated smart toll Scanner engine for vehicle
Id: {vehicle_id}.
Below is the raw telemetry sensor log matrix extracted from the vehicles """

        agent_response = await agent.run(execution_prompt)
        return {
            "status":"Success",
            "vehicle_id":vehicle_id,"report":str(agent_response),
        }
    except Exception as e:
        return {"status":"error","message":str(e)}

@app.get("/")
def read_root():
    return {"Status":"online","message":"Smart city Toll Server API is operating system normally"}
