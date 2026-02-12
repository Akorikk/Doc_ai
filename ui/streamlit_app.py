import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("Ultra Doc AI")

st.write("Upload a logistics document and interact with it.")

# -------- Upload --------

uploaded_file = st.file_uploader("Upload Document", type=["pdf", "docx", "txt"])

if uploaded_file and st.button("Upload"):

    files = {"file": uploaded_file.getvalue()}

    response = requests.post(
        f"{API_URL}/upload",
        files={"file": (uploaded_file.name, uploaded_file.getvalue())}
    )

    st.success("Document uploaded and processed")

# -------- Ask Question --------

question = st.text_input("Ask a question")

if st.button("Get Answer"):

    res = requests.post(
        f"{API_URL}/ask",
        json={"question": question}
    ).json()

    st.write("Answer:", res["answer"])
    st.write("Confidence:", res["confidence"])
    st.write("Sources:", res["sources"])

# -------- Extraction --------

if uploaded_file and st.button("Extract Data"):

    res = requests.post(
        f"{API_URL}/extract",
        files={"file": (uploaded_file.name, uploaded_file.getvalue())}
    ).json()

    st.write(res)
