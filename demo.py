import random

def fake_ai_response(user_input):
    """Simulates AI by responding based on memory retrieval."""
    
    # Step 1: Retrieve relevant memories
    recalled_memories = retrieve_memories(user_input)
    
    # Step 2: If memory exists, respond based on it
    if recalled_memories:
        return f"Ari: I remember! {random.choice(recalled_memories)}"

    # Step 3: If no memory exists, "learn" from the user
    return "Ari: I don’t recall that yet. Want to tell me?"

# Simulated chat
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    print(fake_ai_response(user_input))
