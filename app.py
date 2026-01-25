import streamlit as st
import asyncio
from dotenv import load_dotenv
load_dotenv()
from src.agent.workflow import app as agent_app
from src.utils.metrics import start_metrics_server, SEARCH_QUERIES
import networkx as nx
import matplotlib.pyplot as plt
from src.graph.manager import KnowledgeGraphManager

# UI Config
st.set_page_config(page_title="Autonomous Research Agent", layout="wide")

# Start metrics on load (singleton pattern roughly)
if "metrics_started" not in st.session_state:
    start_metrics_server(8000)
    st.session_state.metrics_started = True

st.title("🤖 Autonomous Research Agent")
st.markdown("### Multi-step reasoning with Knowledge Graph & Citations")

# Sidebar
st.sidebar.header("Configuration")
model_choice = st.sidebar.selectbox("Model", ["gemini-3-flash-preview", "gemini-2.5-flash"])
max_steps = st.sidebar.number_input("Max Steps", min_value=1, value=3)

# Main Input
topic = st.text_input("Enter a research topic:", "The impact of Quantum Computing on Cryptography")

async def run_research(topic, model_name):
    initial_state = {"task": topic, "model_name": model_name}
    container = st.empty()
    status_text = st.empty()
    
    # Initialize Graph Manager locally for this run (visualization only)
    # Note: real graph is built into state triples, we recreate it here for Vis.
    kg = KnowledgeGraphManager()
    
    # Stream events
    final_output = None
    
    async for event in agent_app.astream(initial_state):
        for key, value in event.items():
            status_text.text(f"Current Agent Node: {key}")
            
            if key == "planner":
                st.write("📋 **Plan Generated:**")
                st.write(value.get("plan", []))
                
            elif key == "researcher":
                st.write(f"🔍 **Researching Step:** {value.get('current_step')}")
                SEARCH_QUERIES.inc()
                with st.expander("See Research Results"):
                    st.write(value.get("research_results", [])[-1])
                    
            elif key == "extractor":
                triplets = value.get("graph_triplets", [])
                st.write(f"🧠 **Extracted {len(triplets)} facts**")
                for t in triplets:
                    kg.add_triplet(t.get("subject"), t.get("predicate"), t.get("object"))
                
                # Update Graph Vis
                if triplets:
                    fig, ax = plt.subplots(figsize=(4, 3))
                    pos = nx.shell_layout(kg.graph)
                    nx.draw(kg.graph, pos, ax=ax, with_labels=True, node_size=300, font_size=7, node_color="skyblue", edge_color="gray")
                    st.pyplot(fig)
                    
            elif key == "reporter":
                final_output = value.get("final_report")
    
    return final_output

if st.button("Start Research"):
    with st.spinner("Agent is working..."):
        # Run async loop in streamlit
        final_answer = asyncio.run(run_research(topic, model_choice))
        
        if final_answer:
            st.success("Research Complete!")
            st.markdown("## 📝 Final Report")
            st.markdown(final_answer)
            
            st.download_button(
                label="Download Report as MD",
                data=final_answer,
                file_name=f"research_report_{topic.replace(' ', '_').lower()}.md",
                mime="text/markdown"
            )
            
            # Word Doc Download
            from src.utils.word_generator import create_word_report
            docx_file = create_word_report(final_answer, topic)
            
            st.download_button(
                label="Download Report as Word Doc",
                data=docx_file,
                file_name=f"research_report_{topic.replace(' ', '_').lower()}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

