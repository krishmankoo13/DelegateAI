import datetime
import re
from database import tasks_collection, contacts_collection
from config import elevenlabs_client, ELEVENLABS_AGENT_ID, ELEVENLABS_PHONE_NUMBER_ID

def execute_pending_calls():

    result = []

    for task in tasks_collection.find(
                {
                    'status':'pending', 
                    'action': 'call'
                }
                ):
        print('task:', task)
        contact = contacts_collection.find_one(
            {'name': re.compile(f"^{re.escape(task['name'])}$", re.IGNORECASE)}
        )

        if not contact:
            tasks_collection.update_one(
                {'_id': task['_id']},
                {'$set': {'status': 'failed', 'error':'contact not found'}}
            )
            result.append(f"Call Failed for {task['title']}. Contact Not Found {task['name']}")

        else:
            response = elevenlabs_client.conversational_ai.twilio.outbound_call(
                agent_id=ELEVENLABS_AGENT_ID,
                agent_phone_number_id=ELEVENLABS_PHONE_NUMBER_ID,
                to_number=contact['phone'],
                conversation_initiation_client_data={
                    'dynamic_variables':{
                        'contact_name':task['name'],
                        'task_summary':task['description'],
                    }
                }
            )

            tasks_collection.update_one(
                            {'_id': task['_id']},
                            {
                                '$set': {
                                    'status': 'calling', 
                                    'called_at': datetime.datetime.now(),
                                    'conversation_id': response.conversation_id
                                }
                            }
                        )

            result.append(f"Call Placed for {task['title']} to {task['name']}")

    return result if result else ["No Pending Calls"]


def fetch_conversation_status():

    result = []
        
    for task in tasks_collection.find(
                {
                    'status':'calling', 
                }
                ):

        print('task:', task)


        conversation = elevenlabs_client.conversational_ai.conversations.get(
            conversation_id=task['conversation_id']
        )

        if conversation.status == 'done':
            tasks_collection.update_one(
                                        {'_id': task['_id']},
                                        {
                                            '$set': {
                                                'status': 'completed', 
                                            }
                                        }
                                    )

        else:
            tasks_collection.update_one(
                                        {'_id': task['_id']},
                                            {
                                                '$set': {
                                                        'status': 'pending', 
                                                    }
                                                }
                                            )


    for task in tasks_collection.find(
                    {
                        'status':'completed', 
                    }
                    ):

        # result.append(conversation.status)
        result.append(f"Task Completed: {task['title']} - {task['description']} - Called {task['name']} at {task['called_at']}")

    return result