from langchain_core.chat_history import InMemoryChatMessageHistory

#Store History Session wise
store = {}

def r_store():
    return store

def get_session_history(session_id:str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id] 
