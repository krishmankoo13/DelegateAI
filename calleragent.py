import datetime
from database import tasks_collection, contacts_collection
from config import elevenlabs_client, ELEVENLABS_AGENT_ID, ELEVENLABS_PHONE_NUMBER_ID

def execute_pending_calls():

    for task in tasks_collection.find(
                {'status':'pending'},
                {'action': 'call'}
                ):
        contact = contacts_collection.find_one({'name': task['name'].lower()})

        if not contact:
            tasks_collection.update_one(
                {'_id': task['_id']},
                {'$set': {'status': 'failed', 'error':'contact not found'}}
            )
        else:
            elevenlabs_client.conversational_ai.twilio.outbound_call(
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
                            {'$set': {'status': 'calling', 'called_at': datetime.datetime.now()}}
                        )