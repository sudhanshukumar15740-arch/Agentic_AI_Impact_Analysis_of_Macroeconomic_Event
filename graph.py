from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from agents import (
    event_analysis_agent, research_node, impact_analysis_agent,
    stock_analysis_agent, final_report_node,
)

class State(TypedDict, total=False):
    event: str
    event_summary: str
    event_type: str
    search_queries: list[str]
    research: str
    impact_analysis: str
    stock_analysis: str
    final_report: str

def build_graph():
    g = StateGraph(State)

    g.add_node("event_analysis", event_analysis_agent)
    g.add_node("research", research_node)
    g.add_node("impact_analysis", impact_analysis_agent)
    g.add_node("stock_analysis", stock_analysis_agent)
    g.add_node("final_report", final_report_node)

    g.add_edge(START, "event_analysis")
    g.add_edge("event_analysis", "research")
    g.add_edge("research", "impact_analysis")
    g.add_edge("impact_analysis", "stock_analysis")
    g.add_edge("stock_analysis", "final_report")
    g.add_edge("final_report", END)

    return g.compile()