import streamlit as st
from crew import run_crew

# WHY: Streamlit = fastest way to demo GenAI product

st.set_page_config(page_title="Multi-Agent Research Tool")

st.title("🔎 Multi-Agent Research Pipeline")
st.write("Enter a topic and generate a research report using AI agents.")

topic = st.text_input("Research Topic")

if st.button("Run Research"):
    if topic:
        with st.spinner("Agents are researching..."):
            result = run_crew(topic)

        st.success("Research Completed!")

        # WHY: Markdown rendering for readable report
        st.markdown(result)
    else:
        st.warning("Please enter a topic.")