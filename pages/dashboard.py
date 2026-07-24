import streamlit as st
from calleragent import fetch_conversation_status

# function to display dashboard
def page_dashboard():
    st.title('Dashboard')
    
    if st.button('Fetch Conversation Status'):
        result = fetch_conversation_status()
    
        for line in result:
            st.write(line)
    