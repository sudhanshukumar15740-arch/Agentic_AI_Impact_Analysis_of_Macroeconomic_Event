# Agentic_AI_Impact_Analysis_of_Macroeconomic_Event
Build an Agentic AI system that takes a macroeconomic/geopolitical event, analyzes its second-order effects on the Indian economy, identifies affected sectors, and then identifies the Indian stocks most exposed to those effects.
Agentic AI for Second-Order Impact Analysis of Macroeconomic Events on Indian Equities

Objective:
Build an Agentic AI system that takes a macroeconomic/geopolitical event, analyzes its second-order effects on the Indian economy, identifies affected sectors, and then identifies the Indian stocks most exposed to those effects.
OUTLINE:
A Multi-Agent Workflow Built with LangGraph, LangChain, Google Gemini and Tavily Search
Output: 
Enter one economic event and receive a reasoned explanation of itssecond-order effects together with a shortlist of potentially affected Indian stocks.
Project Report
Sudhanshu kumar
github link: 

Idea: First-Order vs Second-Order Effects
First-order effect : The immediate, direct consequence (example: Fuel import bill for India rises; petrol/diesel costs go up)
Second-order effect : A consequence of the first-order effect (example: Airline and logistics costs rise, paint and chemical input costs rise, margins come under pressure, inflation expectations move)

Skill Used
Skill
Role in project
Python
Programming language for all code.
Langchain
Provides prompt templates,
LangGraph
Connects the steps into a graph with shared state
Google Gemini API(free trail)
The LLM used by every reasoning step: understanding the event, analysing impact, shortlisting stocks.
Tavily Search API 
Web search built for AI applications. Returns clean news 
Pydantic
Defines the exact shape of the event-analysis output
python-dotenv 
Loads API keys from the .env
Steamlit
For frontend at local host







System Architecture
The system follows a layered architecture. The user enters a macroeconomic event. The LangGraph workflow engine passes that event through five processing nodes that share a common state. The nodes use the Google Gemini LLM for reasoning and the Tavily Search API for retrieving news. The final markdown report is displayed.
Step
Node
Type
Reads from State
Writes to State
1
event_analysis
LLM (structured output)
event
event_summary, event_type, search_queries
2
research
Tool (Tavily)
search_queries
research
3
impact_analysis
LLM
event_summary, research
Impact_analysis
4
stock_analysis
LLM
impact_analysis, research
Stock Analysis
5
Final_report
LLM
event_summary, impact_analysis, 
stock_analysis, research
Final reporting
Architecture layers
Layer
Component
Technology
Responsibility
Presentation Layer
app.py (and main.py for terminal)
Streamlit
Accepts the event from the user and displays the report, research.
Orchestration Layer
graph.py
LangGraph (StateGraph)
Defines the State, registers the nodes, and connects them with edges in a fixed order.
Processing Layer
agents.py
Python, LangChain
Contains five nodes: Event Analysis, Research, Impact Analysis, Stock Analysis and Final Report.
Tool Layer
tools.py
LangChain @tool, Tavily client
Provides the search_news tool that retrieves recent news with source URLs.
AI Model Layer
ChatGoogleGenerativeAI
Google Gemini API
Performs understanding, reasoning, stock shortlisting and report writing.
Configuration Layer
.env
python-dotenv
Stores GOOGLE_API_KEY and TAVILY_API_KEY securely.

stock_impact_agent/
├── app.py         (the Streamlit)
├── main.py       (terminal version)
├── agents.py
├── tools.py
├── graph.py
└── .env
Result:
 
# Market Analysis: Impact of 50% US Tariffs on Indian Exports

## Event Summary
The United States has implemented a 50% tariff on a broad range of Indian imports. This policy, partially driven by geopolitical tensions regarding India’s energy trade with Russia and broader trade deficit concerns, represents a significant escalation in protectionism. The move has disrupted bilateral trade flows, forced Indian manufacturers into "survival mode," and triggered a strategic pivot toward alternative export markets.

## First-Order Effects
*   **Export Contraction:** A sharp decline in goods exports to the US, which historically accounted for ~18–20% of India’s total goods exports.
*   **Manufacturing Slowdown:** India’s Manufacturing PMI has hit a nine-month low as production volumes drop and new export orders stagnate.
*   **Margin Compression:** Exporters are facing a binary crisis: absorbing tariff costs, which erodes profitability, or passing them to US consumers, which reduces market competitiveness.
*   **Policy Recalibration:** The Indian government is accelerating efforts to finalize trade frameworks with the EU, UK, and UAE to mitigate the loss of US market access.

## Second-Order Effects
*   **Supply Chain Reconfiguration:** Firms are aggressively diversifying export destinations (e.g., China, Spain, Bangladesh) to bypass US protectionism.
*   **Labor Market Stress:** High-exposure, labor-intensive sectors (textiles, leather, gems) face potential mass layoffs as SMEs struggle to maintain operations.
*   **Geopolitical Friction:** The tariffs have created a "trade-security" dilemma, straining the US-India strategic partnership and potentially leading to retaliatory domestic protectionism in India.
*   **Macroeconomic Volatility:** Persistent uncertainty regarding trade policy is dampening long-term capital expenditure and domestic investment.

## Affected Sectors
*   **Textiles & Apparel:** Highly vulnerable; facing "survival mode" and factory shutdowns.
*   **Gems & Jewelry:** Significant export volume to the US; growth has slowed to near-zero.
*   **Steel & Auto Components:** Hit by the steepest tariffs (up to 50% for steel, 35% for auto parts).
*   **Shrimp/Seafood:** US prices have risen 15–20%, threatening the viability of Indian exporters.
*   **IT Services:** **Neutral/Insulated**; currently not targeted by goods-based tariffs.
*   **Electronics:** **Resilient**; sector growth remains strong (50.5%), showing lower dependence on targeted goods.

## Stock Shortlist
*The following companies are identified based on high exposure to US export markets in the most severely impacted sectors.*

| Company | Ticker | Impact | Causal Reason | Confidence |
| :--- | :--- | :--- | :--- | :--- |
| **Gokaldas Exports** | GOKEX | Negative | High reliance on US apparel retail; margin compression risk. | High |
| **Titan Company** | TITAN | Negative | Significant US exposure in jewelry; demand slowdown. | Medium |
| **Tata Steel** | TATASTEEL | Negative | Steel exports hit by 50% tariff; price competitiveness lost. | High |
| **Bharat Forge** | BHARATFORG | Negative | 35% tariff on auto/industrial components; volume impact. | High |
| **Apex Frozen Foods** | APEX | Negative | US is primary market for shrimp; supply chain viability at risk. | High |

***
**Disclaimer:** *This report is for informational purposes only and does not constitute financial, investment, or trading advice. The effects described are potential outcomes based on current market data and expert projections; they are not guaranteed. Please conduct your own due diligence before making any investment decisions.*

MOST IMPORTANT
Improvement scope
    1. Let the agent decide what to search. Right now the code runs three fixed searches (due to Limitation of Free API). A better version would let the AI read the first results, notice what is missing, and search again by itself until it has enough information. 
    • llm = ChatGoogleGenerativeAI(
    • model="gemini-3.1-flash-lite",
    • temperature=0,
    • max_retries=3,
    • timeout=60,
    • )
       
    2. Check the stocks with real market data. The AI can sometimes suggest a wrong company name or ticker. If we add a tool that checks real prices and tickers from the stock market, the shortlist becomes more trustworthy.
    3. Add a reviewer agent. After the report is written, a separate agent can read it and check whether every claim is supported by the news. If something looks weak, it sends the report back to be fixed. 
    4. Use specialist agents for each sector. Instead of one agent analysing everything, we can have separate agents for banking, oil and gas, IT, pharma and so on. Each one knows its own area better, and a main agent combines their answers. 
    5. Add memory and past events.

