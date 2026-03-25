from email import message
import requests
from pydantic import BaseModel

api_url='http://127.0.0.1:5000'
person_api_path="/maxrest/rest/mbo/person"
asset_api_path="/maxrest/rest/mbo/asset"
location_api_path="/maxrest/rest/mbo/location"

api_host='http://127.0.0.1:5000'
api_path='/maxrest/rest/mbo/'
# mbo_name=''

def get_all_data(mbo_name: str):
    response=requests.get(api_host+api_path+mbo_name.lower())
    if response.status_code==200:
        message=response.json()
    else:
        message={"Error in API Response"+str(response.status_code)}
    return message

def get_unique_data(mbo_name: str,uid: int):
    response=requests.get(api_host+api_path+mbo_name.lower()+"/"+str(uid))
    if response.status_code==200:
        message=response.json()
    else:
        message={"Error in API Response"+str(response.status_code)}
    return message

def add_data(mbo_name: str, data_json):
    """POST a record to the Maximo MBO REST endpoint for the given mbo name."""
    response=requests.post(api_host+api_path+mbo_name.lower(),json=data_json)
    if response.status_code==200:
        message=response.json()
    else:
        message={"Error in API Response"+str(response.status_code)}
    return message

def add_person(person_json):
    response=requests.post(api_url+person_api_path,json=person_json)
    print("Adding Person data" + str(person_json))
    if response.status_code==200:
        message=response.json()
        print("Successfuly added Person data" + str(person_json))
    else:
        message={"Error in API Response"+str(response.status_code)}

def add_asset(asset_json):
    response=requests.post(api_url+asset_api_path,json=asset_json)
    print("Adding Asset data" + str(asset_json))
    if response.status_code==200:
        message=response.json()
        print("Successfuly added Asset data" + str(asset_json))
    else:
        message={"Error in API Response"+str(response.status_code)}
    return message

def add_location(location_json):
    response=requests.post(api_url+location_api_path,json=location_json)
    print("Adding Location data" + str(location_json))
    if response.status_code==200:
        message=response.json()
        print("Successfuly added Location data" + str(location_json))
    else:
        message={"Error in API Response"+str(response.status_code)}
    return message
