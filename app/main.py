# The Application Entry Point
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from schemas import models
import sys
load_dotenv()
sys.path.append("../")
from core import output_lnk

app = FastAPI(title="RGE Modules API", version="1.0.0", description="API for interacting with RGE")

class StripServicesMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/rge"):
            request.scope["path"] = request.url.path[len("/rge"):]
        response = await call_next(request)
        return response

# Add the middleware to the application
app.add_middleware(StripServicesMiddleware)
    

@app.post("/execute")
async def rge(input_data: models.InputQuery):
    sessionId = input_data.sessionId
    query = input_data.query
    if sessionId != '':
        results = output_lnk.manager_conversations(
            session_id = sessionId,
            query = query)
        results=str(results).strip('\n')
        results=str(results).replace('\n\n','\n').replace('html','').replace('`','').replace('<>','')
        results=str(results).replace('\n','<br>').replace(' **','<b>').replace('** ','</b>').replace('**','  ').replace('#','  ')              
        print('*'*50)
        print(results)          
        print('*'*50)
        return results
    else:        
        return {"result":'Some error occurred. Retry again after sometime'}
    
@app.post("/clear-session")
async def clear(input_data:models.sessionId):
    session_id = input_data.sessionId    
    result = output_lnk.update_sesssion_lst(session_id)
    if result == True:
        return {'message':'Cleared successfully'}
    else:
        return {'message':'Error in clearing chats'}

from fastapi.responses import FileResponse
from starlette.responses import Response
import os
import pandas as pd
import sqlite3
@app.get("/session-file/")
async def download_file():     
    # file_path = dir_path + '/session_logs.csv'
    # filename = 'rge_logs.csv'
    # return FileResponse(path=file_path, headers={"Content-Disposition": f"attachment; filename={filename}"})
    db_file = "new_session_logs.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Example query to fetch data (replace with your own query)
    cursor.execute("SELECT * FROM logs")
    rows = cursor.fetchall()
    columns = [i[0] for i in cursor.description]

    # Create a pandas DataFrame from the fetched data
    df = pd.DataFrame(rows, columns=columns)

    # Write DataFrame to an Excel file
    excel_filename = "logs.xlsx"
    df.to_excel(excel_filename, index=False)

    # Close database connection
    cursor.close()
    conn.close()

    # Prepare file response and return
    return FileResponse(path=excel_filename, filename=excel_filename, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')