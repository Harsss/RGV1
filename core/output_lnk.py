import sys
sys.path.append("../core")
import os 
import csv
import logging
import final_res
from final_res import Controller 
import datetime
import logging
import json
import pickle
import os
import logging
import sqlite3

all_sessions={}




def append_to_sql(session_id, log_dict,model):
    # Establish a connection to the SQLite database
    conn = sqlite3.connect('new_session_logs_llm.db')
    cursor = conn.cursor()
    
    # Create table if it does not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            session_id TEXT,
            query TEXT,
            dic_out TEXT,
            data_prepared_with_mapping TEXT,
            all_data_for_context TEXT,
            final_response TEXT,
            history TEXT,
            total_rge_time Text,
            total_dic_time Text,
            total_llm_response_time Text,
            llm_used Text
        )
    ''')
    
    # Insert the log data into the database
    cursor.execute('''
        INSERT INTO logs (session_id, query, dic_out,data_prepared_with_mapping, all_data_for_context, final_response, history, total_rge_time, total_dic_time, total_llm_response_time, llm_used)
        VALUES (?, ?, ?, ?, ?, ?,?,?,?,?,?)
    ''', (str(session_id), str(log_dict.get('query', '')),
        str(log_dict.get('dic_output', '')), 
        str(log_dict.get('data_preperad_for_db_fetching', '')),
        str(log_dict.get('all_Data_context', '')), 
        str(log_dict.get('final_response', '')),
        str(log_dict.get('hist', '')), 
        str(log_dict.get('total_rge_time', '')),
        str(log_dict.get('total_dic_time', '')),
        str(log_dict.get('total_response_llm_time', '')),
        str(model)))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    





    
    
def save_conversation(session_id, conversation, directory='sessions'):
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = os.path.join(directory, f'{session_id}.pkl')
    with open(filename, 'wb') as f:
        pickle.dump(conversation, f)

def load_conversation(session_id, directory='sessions'):
    filename = os.path.join(directory, f'{session_id}.pkl')
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

def manager_conversations(session_id, model,query, directory='sessions'):
    try:
        # Load existing conversation for the session_id
        conversation = load_conversation(session_id, directory)
        
        if conversation is None:
            conversation = Controller(query=query)
            query_output,log_dict = conversation.process_query(ads_status=1,llm_used=model)
        else:
            if isinstance(conversation, Controller):
                query_output,log_dict = conversation.handle_new_query(query,llm_used=model)
            else:
                logging.error('Unexpected object type in session.')
                raise ValueError('Unexpected object type in session.')
        
        # Save the updated conversation back to its pickle file
        save_conversation(session_id, conversation, directory)
        append_to_sql(session_id=session_id, log_dict=log_dict,model=model)

    
        developer_mode_output= {
                'session_id': session_id,
                'query': log_dict.get('query', ''),
                'dic_out': log_dict.get('dic_output', ''),
                'data_with_mapped_ent': log_dict.get('data_preperad_for_db_fetching', ''),
                'history': log_dict.get('hist', ''),
                'total_rge_time':log_dict.get('total_rge_time'),
                'total_dic_time':log_dict.get('total_dic_time'),
                'total_response_llm_time':log_dict.get('total_response_llm_time'),
                'llm_used':model

        }
    
    except Exception as e:
        logging.error(f'Error occurred: {e}')
        print(f'eeor at this point {e}')
        developer_mode_output= {
            'session_id':session_id,
            'query':query,
            'dic_out':'not found',
            'history':'not found'
        }
        
        print('Call someone to fix the issue')
        query_output='There is some error in the process please try again \n sincere Request from ChatMRO'
        # query_output='This question is out of scope. Phela scope define nhi kiya tha. Ab ise agli iteration me dekhenge '
    
    
    
    return {"query_output" : query_output,
        "developer_mode_output" : developer_mode_output
        }

        

def update_sesssion_lst(session_id):
    global all_sessions    
    if session_id in all_sessions:
        try:        
            del all_sessions[session_id]
            return True 
        except Exception as e:
            print('error in removing ')
            logging.log(e)
    else:
        return False
    