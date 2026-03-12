from query_engine import QueryEngine


engine = QueryEngine()

while True:

    question = input("\nAsk question (or type exit): ")

    if question.lower() == "exit":
        break

    engine.ask(question)