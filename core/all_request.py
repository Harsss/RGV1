import requests 
import json 




def send_dic_request(url, payload):
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        # Check if the request was successful
        if response.status_code == 200:
            # print("Request was successful")
            return response.json()
        else:
            # print(f"Request failed with status code: {response.status_code}")
            return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
    
    
    
def get_intent_entity_output(query,history=None):
        url = "https://www.mrompn.com/process/cid"
        if history:
            pass_history=history
        else:
            pass_history='[summary: \"\",chat_history:[user:,chatMRO:]]'
        payload = {
                "input_query": f"{query}",
                "history": f"history={pass_history}"
                }
        # Send the POST request
        response = send_dic_request(url, payload)        
        if response:
            return True, response
        else:
            return False, query

   
   
    
def get_mpn_data(mpn_list=[]):
    url = "https://chatmro.com/db_manager/elastic/get-mpn-data"

    payload = json.dumps({
      "mpns": mpn_list
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text




   
def fetch_k_product_on_cat(l3_list=[],k=2):
    url = "https://chatmro.com/db_manager/elastic/fetch-l3-products"

    payload = json.dumps({
      "l3s": l3_list,
      "k":k
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text






def get_pd_specs(specs_list=[]):
    url = "https://chatmro.com/db_manager/elastic/get-data-from-specs"

    payload = json.dumps(specs_list)
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text

    
    
    
    
def embedding_search(query='chatMRO'):
    url = "https://chatmro.com/db_manager/vector/search"

    payload = json.dumps({
      "search_query": query
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text
    
    




def l3_data(l3_lst=[]):
  url = "https://chatmro.com/db_manager/elastic/get-l3-data"

  payload = json.dumps({
    "l3s": l3_lst
  })
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  return response.text



def get_category_data(l3_list=[]):
    url = "https://chatmro.com/db_manager/elastic/get-l3-data"

    payload = json.dumps({
      "l3s": l3_list
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text




def get_mapping_data(unmaped):
  unmaped=json.dumps(unmaped)
  url = "https://mrompn.com/services/mapping"
  payload = json.dumps({
    "input_string": unmaped
  })
  headers = {
    'Content-Type': 'application/json'
  }
  response = requests.request("POST", url, headers=headers, data=payload)
  # return json.loads(response.text)
  # return json.loads(response.text)
  if response.status_code==200:
    return json.loads(response.text)
  else:
    unmaped=json.loads(unmaped)
  #   print(unmaped)
  #   return unmaped
  #   # response['mapped_category']=unmaped['category']
    # response['mapping status']=f'mapping fat gaya for' +  str(unmaped['category'])
    # return response




def get_alternate(mpn=None):
  mpn=mpn.lower()
  url = "https://www.mrompn.com/services/tools/fetch-alternate"
  payload = json.dumps({
    "mpn": str(mpn),
    "non_compromised_attr": {
      "additionalProp1": "string",
      "additionalProp2": "string",
      "additionalProp3": "string"
    },
    "fetch_generic": True,
    "fetch_brand": False,
    "fetch_price": False,
    "fetch_lead_time": False
  })
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  if response.status_code==200:
      # print(response.text)
      return response.text
  else:
      print(f'WE DONT HAVE THE EXACT ALTERNATE OF THIS {mpn} as of know, but TELL US YOUR REQUIREMENT WE WILL ARRANGE IT')
      return 'WE DONT HAVE THE EXACT ALTERNATE OF THIS {mpn} as of know, but TELL US YOUR REQUIREMENT WE WILL ARRANGE IT' 
    
    

def get_lead_time(mpns):
  ###########################################################################################################################################
  ########### if lead time not available dont return time to ware house return an empty list or give the email sale@raptorsuppiles.com or will see later ###############
  ########################################################################################################################################3
  url = "https://chatmro.com/db_manager/elastic/get_lead_time"
  payload = json.dumps({
    "mpns": mpns
  })
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  print(response.text)
