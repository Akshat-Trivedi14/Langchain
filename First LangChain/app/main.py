import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.runnables.history import RunnableWithMessageHistory

from prompt import prompt
from memory import get_session_history,r_store


load_dotenv()

# Create the LLM

llm = ChatGroq(model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"), temperature=0.4)

# Create Chain

chain = prompt | llm

#Add history to the chain

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    #Current user message 
    input_messages_key="input",
    #Previous conversation 
    history_messages_key="history"
)


def chat(session_id: str, user_input: str):

    response = chain_with_history.invoke(
        {
            "input": user_input
        },
        config={
            "configurable": {
                "session_id": session_id
            }
        }
    )

    return response.content


if __name__ == "__main__":
    # Ask which session (user) this terminal belongs to.
    # Different ids keep separate histories; the same id shares history.
    session_id = input("Session ID (e.g. alice): ").strip() or "session_1"
    print(f"Started session '{session_id}'. Type 'exit' to quit, 'switch' to change session.")

    while True:
        user_input = input(f"[{session_id}] User: ")

        if user_input.lower() == "exit":
            break

        if user_input.lower() == "switch":
            session_id = input("Switch to Session ID: ").strip() or session_id
            print(f"Now in session '{session_id}'.")
            continue

        response = chat(session_id, user_input)
        print("AI Response:", response)

