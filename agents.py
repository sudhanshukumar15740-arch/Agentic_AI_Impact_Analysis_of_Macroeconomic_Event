from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from tools import search_news

# load_dotenv()
# llm = ChatGoogleGenerativeAI(
#     model="gemini-3.8-flash",   # check AI Studio for the current free-tier model names
#     temperature=0,
#     max_retries=1,              # auto-retries on rate-limit errors
# )
load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0,
    max_retries=3,
    timeout=60,
)

# load_dotenv()
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def to_text(content) -> str:
    """Convert LLM output (string or list of content blocks) to a plain string."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        return "".join(parts)
    return str(content)

# ---------- 1. Event Analysis Agent ----------
class EventAnalysis(BaseModel):
    summary: str = Field(description="2-3 sentence plain-English summary of the event")
    event_type: str = Field(description="e.g. trade policy, monetary policy, commodity shock")
    search_queries: list[str] = Field(description="3 focused web search queries")

def event_analysis_agent(state):
    structured_llm = llm.with_structured_output(EventAnalysis)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a macroeconomic analyst. Analyze the event and "
                   "produce search queries that focus on India-relevant impact."),
        ("human", "Event: {event}"),
    ])
    result = (prompt | structured_llm).invoke({"event": state["event"]})
    return {
        "event_summary": result.summary,
        "event_type": result.event_type,
        "search_queries": result.search_queries,
    }


# ---------- 2. Research node (uses the tool) ----------
def research_node(state):
    chunks = []
    for q in state["search_queries"]:
        chunks.append(f"### Query: {q}\n{search_news.invoke(q)}")
    return {"research": "\n\n".join(chunks)}


# ---------- 3. Impact Analysis Agent ----------
def impact_analysis_agent(state):
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a macro strategist focused on India. Using ONLY the event "
         "summary and research provided, identify:\n"
         "1. First-order effects\n"
         "2. Second-order effects (the knock-on consequences)\n"
         "3. Indian sectors likely helped or hurt, with reasoning\n"
         "Be explicit that these are possibilities, not certainties."),
        ("human", "Event: {summary}\n\nResearch:\n{research}"),
    ])
    out = (prompt | llm).invoke({
        "summary": state["event_summary"],
        "research": state["research"],
    })
    # return {"impact_analysis": out.content}
    return {"impact_analysis": to_text(out.content)}


# ---------- 4. Stock Analysis Agent ----------
def stock_analysis_agent(state):
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are an Indian equity research analyst. Based on the impact "
         "analysis, shortlist 5-8 NSE/BSE-listed companies that may be "
         "affected. For each give: company, ticker, positive/negative, the "
         "causal reason, and confidence (low/medium/high). Only name "
         "companies you are confident exist. Do not give buy/sell advice."),
        ("human", "Impact analysis:\n{impact}\n\nResearch:\n{research}"),
    ])
    out = (prompt | llm).invoke({
        "impact": state["impact_analysis"],
        "research": state["research"],
    })
    # return {"stock_analysis": out.content}
    return {"stock_analysis": to_text(out.content)}


# ---------- 5. Final Report ----------
def final_report_node(state):
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Write a clear markdown report with sections: Event Summary, "
         "First-Order Effects, Second-Order Effects, Affected Sectors, "
         "Stock Shortlist (table), Evidence (cite source URLs from the "
         "research), and a Disclaimer stating these are potential effects, "
         "not guaranteed outcomes or financial advice."),
        ("human",
         "Event summary: {summary}\n\nImpact: {impact}\n\n"
         "Stocks: {stocks}\n\nResearch: {research}"),
    ])
    out = (prompt | llm).invoke({
        "summary": state["event_summary"],
        "impact": state["impact_analysis"],
        "stocks": state["stock_analysis"],
        "research": state["research"],
    })
    # return {"final_report": out.content}
    return {"final_report": to_text(out.content)}