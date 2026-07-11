from Services.ragservice import ask_assistant
result = ask_assistant("What do customers say about delivery?")
print(result["answer"])
print(result["sources"])