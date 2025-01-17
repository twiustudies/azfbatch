# Azure Function with MongoDB Integration

This repository contains an Azure Function that processes events from an Event Grid and stores them in a MongoDB database. The function collects events and stores them in batches of 10.

# Prerequisites

Python 3.8 or higher
Azure Functions Core Tools
MongoDB Atlas or any MongoDB instance
# Setup

Clone the repository:

git clone <repository-url>
cd <repository-directory>
Install dependencies:

pip install -r requirements.txt
Configure MongoDB connection:

Update the connection_string variable in the code with your MongoDB connection string.
# Function Details

## Event Grid Trigger

The function is triggered by Event Grid events. It collects events and stores them in a MongoDB collection once 10 events have been collected.

## Code Overview

MongoDB Initialization:

The MongoDB client is initialized with the provided connection string. If the connection fails, appropriate error messages are logged.

connection_string = "<your-mongodb-connection-string>"
client = MongoClient(connection_string)
database = client['dataengprojectbatchdb']
container = database['events']
Event Processing:

The function processes events from Event Grid and stores them in a list. Once 10 events are collected, they are inserted into the MongoDB collection.

@app.event_grid_trigger(arg_name="azeventgrid")
def BatchGridTrigger(azeventgrid: func.EventGridEvent):
    events.append(azeventgrid.get_json())
    if len(events) >= 10:
        container.insert_one({
            'id': str(datetime.utcnow()),
            'events': events
        })
        events.clear()
## Logging

The function logs important steps and errors to help with debugging and monitoring.

## Error Handling

If the MongoDB client or database connection fails, the function logs the error and skips event processing.

# License

This project is licensed under the MIT License.
