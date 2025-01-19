from assistant.graph import run_graph
from dotenv import load_dotenv
load_dotenv()


if __name__ == "__main__":
    query = input("Ask a question: ")
    print(run_graph(query))
