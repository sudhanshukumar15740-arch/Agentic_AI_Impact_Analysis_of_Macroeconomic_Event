from graph import build_graph

if __name__ == "__main__":
    event = input("Enter a macroeconomic event: ")
    app = build_graph()
    result = app.invoke({"event": event})
    print("\n" + result["final_report"])