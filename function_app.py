import os
import logging
import azure.functions as func
from pymongo import MongoClient
from datetime import datetime, timedelta
import json

app = func.FunctionApp()

# Initialize MongoDB client with connection string
connection_string = "mongodb+srv://thilowiltsadmin:abc123abc123!@dataengprojectbatchdb.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"

# Store events in a list
events = []

try:
    logging.info('Attempting to create MongoClient')
    client = MongoClient(connection_string)
    logging.info('MongoClient created successfully')
    
    database_name = 'dataengprojectbatchdb'
    container_name = 'events'
    database = client[database_name]
    container = database[container_name]
    logging.info('Successfully created database and container clients')
except Exception as e:
    logging.error(f"Failed to create MongoClient: {e}")
    logging.error(f"Exception type: {type(e).__name__}")
    logging.error(f"Exception details: {e.args}")
    client = None
    database = None
    container = None

@app.event_grid_trigger(arg_name="azeventgrid")
def BatchGridTrigger(azeventgrid: func.EventGridEvent):
    if container is None:
        logging.error('Container client is not available. Skipping event processing.')
        return

    logging.info('Python EventGrid trigger processed an event')
    
    events.append(azeventgrid.get_json())

    # Check if 10 events have been collected
    if len(events) >= 10:
        try:
            # Store events in MongoDB
            container.insert_one({
                'id': str(datetime.utcnow()),
                'events': events
            })
            logging.info('Stored events in MongoDB')
        except Exception as e:
            logging.error(f"Failed to store events in MongoDB: {e}")
        
        logging.info('Clear events')
        events.clear()