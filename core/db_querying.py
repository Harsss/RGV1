from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import utils

import os
import psycopg2
import threading
import concurrent.futures

load_dotenv()

DB_PARAMS = {
    'host': os.getenv('DB_CONFIG_HOST'),
    'dbname': os.getenv('DB_CONFIG_DATABASE'),
    'user': os.getenv('DB_CONFIG_USER'),
    'password': os.getenv('DB_CONFIG_PASSWORD')
}

already_fetched_pds = set()
already_fetched_categories = set()
already_fetched_pds_lock = threading.Lock()
already_fetched_categories_lock = threading.Lock()

def get_db_connection():
    retry_count = 1
    while(retry_count < int(os.getenv('DB_RETRY_COUNT'))):
        try:
            conn = psycopg2.connect(**DB_PARAMS)
            return conn
        except Exception as e:
            retry_count += 1
        if retry_count == int(os.getenv('DB_RETRY_COUNT')):
            return None
        
def execute_query(connection, query, params):
    print(query, params)
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(query, params)
        results = cursor.fetchall()
        return utils.process_results(results)


def select_fields(fields=None):
    return f"SELECT {', '.join(fields) if fields else '*'}"

def limit_clause(limit):
    return f" LIMIT {limit}" if limit is not None and limit > 0 else ""

def join_tables(joins):
    join_query = ""
    for join in joins:
        join_table = f"{join['schema']}.{join['table']}" if 'schema' in join else join['table']
        join_query += f" {join['type'].upper()} JOIN {join_table} ON {join['on']}"
    return join_query

def where_clause(condition, params):
    return (f" WHERE {condition}", params) if condition else ("", [])

def having_clause(condition, params):
    return (f" HAVING {condition}", params) if condition else ("", [])

def order_by_clause(order):
    return f" ORDER BY {order}" if order else ""

def build_query(tables, select=None, joins=None, where=None, where_params=[], having=None, having_params=[], order_by=None, limit=None):
    initial_table = f"{tables[0]['schema']}.{tables[0]['table']}"
    query_parts = [select_fields(select), f"FROM {initial_table}"]
    params = []
    
    if joins:
        query_parts.append(join_tables(joins))
    
    if where:
        where_query, where_params = where_clause(where, where_params)
        query_parts.append(where_query)
        params.extend(where_params)
    
    if having:
        having_query, having_params = having_clause(having, having_params)
        query_parts.append(having_query)
        params.extend(having_params)
    
    if order_by:
        query_parts.append(order_by_clause(order_by))
    
    if limit:
        query_parts.append(limit_clause(limit))
    
    full_query = " ".join(query_parts)
    return full_query, params

def get_mpn_specs_query_params(mpn):
    tables = [{'schema': 'master_db', 'table': 'rp_pd_specs_rp_pd_data_view'}]
    where = "rp_pd_specs_rp_pd_data_view.rp_pd_specs_mpn = %s"
    where_params = [mpn]    
    query, params = build_query(tables=tables, where=where, where_params=where_params)
    return query, params

def get_category_specs_query_params(category):
    tables = [{'schema': 'master_db', 'table': 'rp_pd_specs_rp_pd_data_view'}]
    where = "rp_pd_specs_rp_pd_data_view.rp_pd_specs_l3 = %s"
    where_params = [category]
    query, params = build_query(
        tables=tables,
        where=where,
        where_params=where_params
    )
    return query, params

def get_query_results(queries):
    results = []
    connection = get_db_connection()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_query_result, intent, connection) for intent in queries]
        
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print("Error occurred:", e)
    
    global already_fetched_pds
    already_fetched_pds = set()
    global already_fetched_categories
    already_fetched_categories = set()
    
    return results


def get_query_result(intent, connection):
    results = {}
    try:
        if intent['mpn']:
            pd_mpn = intent['mpn'].lower()
            with already_fetched_pds_lock:
                if pd_mpn not in already_fetched_pds:
                    query, params = get_mpn_specs_query_params(pd_mpn)
                    results['mpn_details'] = execute_query(connection, query, params)
                    already_fetched_pds.add(pd_mpn)

        elif intent['category']:
            category = intent['category'].lower()
            with already_fetched_categories_lock:
                if category not in already_fetched_categories:
                    attributes = intent.get('specs', {})
                    brand = intent["brand"].lower()

                    query, params = get_category_specs_query_params(category)
                    
                    if brand:
                        query += " OR ( rp_pd_specs_rp_pd_data_view.key = %s AND rp_pd_specs_rp_pd_data_view.value = %s ) "
                        params.extend(['brand', brand])
                    
                    if(len(attributes)):
                        query += ' AND ( '
                    
                    or_count = 0
                    
                    for attribute_name, value in attributes.items():
                        
                        if (or_count > 0): 
                            query += ' OR '
                            
                        if value:
                            query += f" ( rp_pd_specs_rp_pd_data_view.rp_pd_specs_attribute_name = %s AND rp_pd_specs_rp_pd_data_view.rp_pd_specs_value1 = %s ) "
                            if(isinstance(value, list) and len(value) > 1):
                                params.extend([attribute_name.lower(), value[1].lower()])
                            else:
                                params.extend([attribute_name.lower(), value.lower()])
                        else:
                            query += f"( rp_pd_specs_rp_pd_data_view.rp_pd_specs_value1 = %s )"
                            params.append(attribute_name.lower())
                            
                        or_count += 1
                        
                    if(len(attributes)):
                        query += ' ) '
                    

                    results['category'] = execute_query(connection, query, params)
                    already_fetched_categories.add(category)

    except Exception as e:
        print(f"Error occurred in get_query_result: {e}")

    return results


'''

Database Schemas: sales and customer_data
Tables:
sales.order_details (contains order information)
customer_data.customers (contains customer information)
Query Goal: Retrieve all orders and their customer details where the order total is above $100,
            group by customer to calculate total sales, and fetch only customers with total sales above $500, 
            ordered by the customer name.


# Define the initial table (from schema and table)
tables = [{"schema": "sales", "table": "order_details"}]

# Define the JOIN
joins = [{
    "type": "inner",
    "schema": "customer_data",
    "table": "customers",
    "on": "customers.customer_id = order_details.customer_id"
}]

# Define the SELECT fields
select_fields = [
    "customers.customer_name",
    "customers.customer_id",
    "SUM(order_details.total) AS total_sales"
]

# Define the WHERE clause
where = "order_details.total > %s"
where_params = [100]

# Define the HAVING clause
having = "SUM(order_details.total) > %s"
having_params = [500]

# Define the ORDER BY clause
order_by = "customers.customer_name ASC"

# Build the query using the build_query function
query, params = build_query(
    tables, select=select_fields, joins=joins, 
    where=where, where_params=where_params,
    having=having, having_params=having_params, 
    order_by=order_by, limit=50
)

print(query)
print(params)

Tables and Schemas: The main table is sales.order_details, and we join it with customer_data.customers.
Select Fields: We're selecting the customer's name and ID, along with the sum of the order totals as total_sales.
Where Condition: We filter orders where the total is greater than $100.
Having Clause: After grouping (implicitly done by selecting with an aggregate function and not specifying a GROUP BY, assuming GROUP BY is handled outside this function if more granularity is needed), we filter groups where total sales are more than $500.
Order and Limit: We order the results by customer name in ascending order and limit the result to 50 entries.

'''