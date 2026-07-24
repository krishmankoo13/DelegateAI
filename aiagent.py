from database import DBHelper
from config import openai_client
import datetime
import json

# DB Initialization
db_helper = DBHelper()
db_helper.select_collection(collection_name='tasks')

# Save the Task in MongoDB
def save_task(task):
    # Adding 2 more keys in task
    task['status'] = 'pending'
    task['created_at'] = datetime.datetime.now()
    db_helper.save(task)

    result = (
        f"Task saved successfully as **pending** \n\n",
        f"**Action** {task['action']} \n\n",
        f"**Title** {task['title']} \n\n",
        f"**Contact Name** {task['name']} \n\n",
        f"**Description** {task['description']} \n\n"
    )

    return result

# 2. Define a list of callable tools for the model
tools = [
    {
        "type": "function",
        "name": "save_task",
        "description": "Save the task in MongoDB Atlas which a user will write",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Title of the Task",
                },
                "description": {
                    "type": "string",
                    "description": "Description of the Task",
                },
                "name": {
                    "type": "string",
                    "description": "Name of the contact person",
                },                
                "action": {
                    "type": "string",
                    "enum": ["call", "email", "message", "other"],
                    "description": "Action of the Task can be call, message or email",
                }
            },
            "required": ["title", "description", "action"],
        },
    },
]

def agentic_save(input_list):
    
    # Prompt the model with tools defined
    response = openai_client.responses.create(
        model="gpt-4o-mini",
        tools=tools,
        input=input_list,
    )  

    llm_output = response.model_dump_json(indent=2) # string
    print(llm_output)
    llm_output = json.loads(llm_output) # covert to dictionary
    arguments = json.loads(llm_output['output'][0]['arguments'])
    function_name = llm_output['output'][0]['name']
    type = llm_output['output'][0]['type']

    result = 'Sorry, I cannot process your request'

    if type == 'function_call':
        if function_name == 'save_task':
            # add original text written by user from input_list
            arguments['user_original_text'] = input_list[0]['content']
            result = save_task(arguments)
        elif function_name == 'update_task':
            pass
        elif function_name == 'delete_task':
            pass
        elif function_name == 'list_tasks':
            pass
    
    return result