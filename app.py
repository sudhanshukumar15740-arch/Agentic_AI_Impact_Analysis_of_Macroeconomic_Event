import streamlit as st
from graph import build_graph

st.set_page_config(page_title="Macro Event to Indian Stocks",
                   page_icon="📈", layout="wide")

# Human-readable names for each graph node
STEPS = {
    "event_analysis": "Event analysed, search queries created",
    "research": "News research collected",
    "impact_analysis": "First- and second-order effects identified",
    "stock_analysis": "Indian stocks shortlisted",
    "final_report": "Final report written",
}

EXAMPLES = [
    "Crude oil prices spike 20% suddenly",
    "RBI cuts repo rate by 50 bps",
    "US imposes 50% tariffs on Chinese imports",
]


@st.cache_resource
def get_app():
    return build_graph()   # build the graph once, reuse on every rerun


def set_example(text):
    st.session_state["event_text"] = text


# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Try an example")
    for ex in EXAMPLES:
        st.button(ex, on_click=set_example, args=(ex,), use_container_width=True)
    st.divider()
    st.caption("Output shows *potential* effects based on AI analysis of "
               "news. It is not guaranteed and not financial advice.")

# ---------------- Main page ----------------
st.title("📈 Macro Event → Second-Order Effects → Indian Stocks")
st.write("Enter a macroeconomic event to see its knock-on effects and "
         "potentially affected Indian companies.")

event = st.text_area("Macroeconomic event", key="event_text", height=90,
                     placeholder="e.g. The US increases tariffs on Chinese products")
run = st.button("Analyze", type="primary")

# ---------------- Run the workflow ----------------
if run:
    if not event.strip():
        st.warning("Please enter an event first.")
    else:
        app = get_app()
        state = {"event": event.strip()}
        with st.status("Running analysis...", expanded=True) as status:
            try:
                for chunk in app.stream({"event": event.strip()},
                                        stream_mode="updates"):
                    for node, update in chunk.items():
                        state.update(update)
                        st.write(f"✅ {STEPS.get(node, node)}")
                status.update(label="Analysis complete", state="complete",
                              expanded=False)
                st.session_state["result"] = state
            except Exception as e:
                status.update(label="Analysis failed", state="error")
                st.error(f"Something went wrong: {e}")
                st.info("503 or 429 errors from Google are usually temporary. "
                        "Wait a minute and try again.")

# ---------------- Show results ----------------
result = st.session_state.get("result")
if result:
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📄 Final Report", "🔎 Research", "🧠 Impact Analysis", "🏢 Stocks"])

    with tab1:
        st.markdown(result.get("final_report", ""))
        st.download_button("Download report (.md)",
                           data=result.get("final_report", ""),
                           file_name="stock_impact_report.md",
                           mime="text/markdown")

    with tab2:
        st.subheader("Search queries used")
        for q in result.get("search_queries", []):
            st.write(f"- {q}")
        with st.expander("Raw research text"):
            st.text(result.get("research", ""))

    with tab3:
        st.write(f"**Event type:** {result.get('event_type', '')}")
        st.write(f"**Summary:** {result.get('event_summary', '')}")
        st.markdown(result.get("impact_analysis", ""))

    with tab4:
        st.markdown(result.get("stock_analysis", ""))