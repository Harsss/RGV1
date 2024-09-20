from dotenv import load_dotenv
from datetime import datetime, timedelta
import multiprocessing
import pandas as pd
import numpy as np
load_dotenv()
import multiprocessing
import pandas as pd
import numpy as np


def process_product(product):
    
    extracted_data_list = []
    
    if 'user_intents' in product:
        for user_intent in product['user_intents']:
            extracted_data = {
                "intent": [],
                "mpn": '',
                "specs": {},
                "category": '',
                "brand": ''
            }
            if 'intent' in user_intent:
                if isinstance(user_intent['intent'], list):
                    extracted_data["intent"].extend(user_intent['intent'])
                else:
                    extracted_data["intent"].append(user_intent['intent'])

            for key in ['mpn', 'category', 'brand']:
                if key in user_intent:
                    extracted_data[key] = user_intent[key]

            if 'attribute_names' in user_intent:
                if (isinstance(user_intent["attribute_names"], str)):
                    extracted_data['specs'][user_intent["attribute_names"]] = ''
                else:
                    for attribute in user_intent['attribute_names']:
                        if isinstance(attribute, dict):
                            for attr_name, attr_detail in attribute.items():
                                if 'attribute_details' in attr_detail:
                                    extracted_data['specs'][attr_name] = attr_detail['attribute_details']
                                else:
                                    extracted_data['specs'][attr_name] = ''
                        else:
                            extracted_data['specs'][attribute] = ''

            extracted_data_list.append(extracted_data)
    return extracted_data_list


def decompose_intents(intents):
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    results = []
    products = []
    for intent_entry in intents:
        if 'product' in intent_entry:
            products.extend(intent_entry['product'])
            
    results_nested = pool.map(process_product, products)
    pool.close()
    pool.join()
    
    results = [item for sublist in results_nested for item in sublist]
    
    return results

def numpy_to_python_data_type(value):
    if isinstance(value, np.generic):
        return np.asscalar(value)
    return value

def process_group(group):
    details = {
        'mpn': group['rp_pd_specs_mpn'].iloc[0],
        'l3': group['rp_pd_specs_l3'].iloc[0],
        'data_type': group['rp_pd_specs_data_type'].iloc[0],
    }
    for _, row in group.iterrows():
        if pd.notna(row['value']) and row['value'] != "NaN":
            details[row['key']] = row['value']
        if pd.notna(row['rp_pd_specs_attribute_name']) and pd.notna(row['rp_pd_specs_display_value']):
            details[row['rp_pd_specs_attribute_name']] = row['rp_pd_specs_display_value']

    return details

def process_results(results):
    df_results = pd.DataFrame(results)
    df_results = df_results.applymap(numpy_to_python_data_type)
    df_results = df_results.groupby('int_pid').apply(process_group).reset_index(name='Details')
    list_of_results = df_results.to_dict(orient='records')
    
    return list_of_results


def check_time_difference(original_datetime):
    current_datetime = datetime.now()

    time_difference = abs(current_datetime - original_datetime)

    is_at_least_half_hour = time_difference >= timedelta(minutes=30)

    return is_at_least_half_hour, current_datetime




def map_intent_to_group(intent):
        intent_to_group = {
        "Price Request": "PD Details",
        "Lead Time Request": "PD Details",
        "Specifications Request/Question": "PD Details",
        "Availability": "PD Details",
        "Letter Request": "PD Details",
        "Certifications / Standards": "PD Details",
        "Alternate Product/s Request": "Alternate",
        "Cheaper Alternative Request": "Alternate",
        "Better Lead Time Request": "Alternate",
        "Brand Alternate Request": "Alternate",
        "Spare Request": "PD Links",
        "Kit Request": "PD Links",
        "Accessories Request": "PD Links",
        "Use": "How to",
        "Install": "How to",
        "Repair": "How to",
        "Use (Category)": "How to",
        "Install (Category)": "How to",
        "Repair (Category)": "How to",
        "Use (Category+Specs)": "How to",
        "Install (Category+Specs)": "How to",
        "Repair(Category+Specs)": "How to",
        "Requirement to category": "Generic requirement",
        "Category to subcategory/product": "Generic requirement",
        "Category+Specs to product": "Generic requirement",
        "Question (Generic MRO raptor question)": "Generic question",
        "Chit-Chat": "Generic question",
        "unhandled services (e.g. post quotation, pd warranty )": "misc."}
        return intent_to_group.get(intent, "misc.") 
    