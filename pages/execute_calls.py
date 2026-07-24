import streamlit as st
from calleragent import execute_pending_calls
from database import tasks_collection

# function to execute calls
def page_calls():
    st.title('Execute Calls')

    st.subheader('Task Board')
    
    for task in tasks_collection.find():
        st.write(f"{task['title']} - {task['status']} - {task['action']} - {task['name']}")    

    st.divider()

    if st.button('Start Pending Calls'):
        result = execute_pending_calls()

        for line in result:
            st.write(line)


    