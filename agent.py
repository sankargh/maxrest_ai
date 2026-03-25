from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, trace
import api_tool
import gradio as gr
from pydantic import BaseModel
from person import Person
from asset import Asset
from location import Location

load_dotenv(override=True)

@function_tool
def get_all_persons():
    """ Get all Person data """
    return api_tool.get_all_persons()

@function_tool
def get_person(personid: int):
    """ Get person data using Person ID as paramater """
    return api_tool.get_person(personid)

@function_tool
def add_person(person: Person):
    """ Add Person Data """
    print("Model Dump data-->" +str(person.model_dump()))
    return api_tool.add_person(person.model_dump())


@function_tool
def get_all_assets():
    """ Get all Asset data """
    return api_tool.get_all_assets()


@function_tool
def get_asset(assetnum: str):
    """ Get asset data using Asset Number as parameter """
    return api_tool.get_asset(assetnum)


@function_tool
def add_asset(asset: Asset):
    """ Add Asset Data """
    print("Model Dump data-->" + str(asset.model_dump()))
    return api_tool.add_asset(asset.model_dump())

@function_tool
def get_all_locations():
    """ Get all Location data """
    return api_tool.get_all_locations()


@function_tool
def get_location(location: str):
    """ Get location data using Location as parameter """
    return api_tool.get_location(location)


@function_tool
def add_location(location: Location):
    """ Add Location Data """
    print("Model Dump data-->" + str(location.model_dump()))
    return api_tool.add_location(location.model_dump())


@function_tool
def get_all_data(mboname: str):
    """Get all records for the given mbo name."""
    return api_tool.get_all_data(mboname)


@function_tool
def get_unique_data(mboname: str, uid: int):
    """Get a single record for the given mbo name and uid."""
    return api_tool.get_unique_data(mboname, uid)

mbo_list={'asset','person','locations','asset','item'}
mbo_keys={'mboname':'mbokey', 'person':'personid','asset':'assetnum','locations':'location','item':'itemnum'}
# mbo_keys={'mboname':'uid', 'person':'personuid','asset':'assetuid','locations':'locationsuid','item':'itemuid'}

@function_tool
def get_mbokey(mbo_name: str):
    " Get mbo key for the given mbo name"
    return mbo_keys.get(mbo_name)

tools=[get_mbokey, get_all_data, get_unique_data,add_asset,add_location,add_person]

instructions="You are an agent to get, post data via API. Use only the tools provided. \
    Action: Get Data --> \
    1. First identify the mbo name from user input. \
    Example A: If the user asks, 'Get the location data', then search for the value matching 'location' in 'mbo_list' list\
    Example B: If the user asks, 'Get the asset detail, then search for the value matching 'asset' in 'mbo_list' list\
    2. Then, with that matching value/mbo name as argument, get mbo key using 'get_mbokey' tool\
    Then, proceed to next steps with mbo name, mbo_keys as parameter\
    For retrieving all person, convert data to 'Person' BaseModel, then call get_all_data() method\
    For retreiving a unique person record, convert data to 'Person' BaseModel, then call get_unique_data method    \
    If there is no matching data found, then proceed to next step\
    Ask user whether to create new data    \
    Action: Create data -->\
    If requests to create new data, get the details using BaseModel of Asset/Location/Person etc. as reference \
    Wait for user response\
    Once user provided all requesred details matching the BaseModel,   \
    Call relevant tools such as add_asset, add_location, add_person etc with details given by user\
       Example 1: If user asks, 'Add Asset data', then call add_asset tool with details given by user \
       Example 2: If user asks, 'Add Location data', then call add_location tool with details given by user \
    "
    
agent = Agent(
    name="Maximo REST API transactions to get, post data",
    instructions=instructions,
    tools=tools,
    model="gpt-4o-mini"
)

async def chat(user_input: str, history):
    with trace("Test API"):
        result = await Runner.run(agent,user_input)
    return result.final_output  
# gr.ChatInterface(chat,type="messages").launch()
gr.ChatInterface(chat).launch()