LangChain — Message History

A basic LangChain implementation demonstrating conversational memory using RunnableWithMessageHistory, InMemoryChatMessageHistory, MessagesPlaceholder, and session-based history.

Project Structure

First LangChain/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── memory.py
│   └── prompt.py
│
├── .gitignore
└── requirements.txt

Architecture

The application separates the prompt, memory, and application logic.

flowchart TD
    A[User] --> B[chain_with_history.invoke]
    B --> C[RunnableWithMessageHistory]

    C --> D[session_id]
    D --> E[get_session_history]
    E --> F[InMemoryChatMessageHistory]

    C --> G[Actual Chain]
    G --> H[Prompt Template]
    F --> I[history]
    I --> J[MessagesPlaceholder]
    J --> H
    H --> K[LLM]
    K --> L[AI Response]

    L --> F
    B --> M[input]
    M --> H

Message History Flow

The important idea is that the current input and the session identifier have different responsibilities.

flowchart LR
    A["Current input<br/>{input: 'Hello'}"] --> B[Prompt]
    C["configurable<br/>session_id: 'user_123'"] --> D[get_session_history]
    D --> E[Previous messages]
    E --> F["MessagesPlaceholder('history')"]
    F --> B
    B --> G[LLM]
    G --> H[AI Response]
    H --> I[Update session history]
    A --> I

Core Concepts

1. MessagesPlaceholder

MessagesPlaceholder(variable_name="history")

MessagesPlaceholder does not store messages. It provides a location in the prompt where previously stored messages can be inserted.

2. InMemoryChatMessageHistory

store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()

    return store[session_id]

This stores conversation messages in memory.

Different session IDs maintain different conversations:

user_123 → History A
user_456 → History B

3. RunnableWithMessageHistory

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

It connects the session ID, history store, and actual chain.

Its basic responsibility is:

session_id
    ↓
retrieve history
    ↓
put history under "history"
    ↓
MessagesPlaceholder("history")
    ↓
run chain
    ↓
store new messages

4. Feeding Input

response = chain_with_history.invoke(
    {"input": "What is LangChain?"},
    config={
        "configurable": {
            "session_id": "user_123"
        }
    }
)

Here:

input = current user message

session_id = identifies which conversation to use

history = retrieved automatically by RunnableWithMessageHistory

Why is session_id inside configurable?

The session ID is not part of the user's actual message. It is runtime configuration used to determine which conversation history should be loaded.

input
  → what the chain should process

configurable.session_id
  → which conversation state should be used

For example:

chain_with_history.invoke(
    {"input": "Hello"},
    config={
        "configurable": {
            "session_id": "chat_1"
        }
    }
)

and:

chain_with_history.invoke(
    {"input": "Hello"},
    config={
        "configurable": {
            "session_id": "chat_2"
        }
    }
)

use the same chain but maintain separate conversation histories.

Current Limitation

This project uses:

InMemoryChatMessageHistory

Therefore, the history exists only while the application is running. Restarting the application clears the in-memory conversations.

For a production application, the history can be moved to persistent storage such as PostgreSQL or Redis.

Learning Outcome

After completing this example, you should understand:

ChatPromptTemplate

MessagesPlaceholder

InMemoryChatMessageHistory

get_session_history()

RunnableWithMessageHistory

input_messages_key

history_messages_key

session_id

configurable

How current input and previous conversation are combined before reaching the LLM

Next Topics

Message History
      ↓
Prompt Templates
      ↓
Output Parsers / Structured Output
      ↓
Runnables + LCEL
      ↓
Chains
      ↓
Tool Calling
      ↓
Agents
      ↓
RAG
      ↓
LangGraph
