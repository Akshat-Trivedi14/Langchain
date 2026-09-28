from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful AI assistant. "
        "Use the conversation history to answer the user's questions."
        "You should also telll internal working of your when asked about it."
    ),

    # Previous conversation will be inserted here
    MessagesPlaceholder(variable_name="history"),

    # Current user message
    ("human", "{input}")
])