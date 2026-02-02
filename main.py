import streamlit as st
import pandas as pd
import random
import os

st.set_page_config(page_title="Ohio RE: Master Suite", layout="wide")

# 1. CHAPTER SELECTOR UI
st.sidebar.title("📚 Course Navigation")
chapter = st.sidebar.selectbox(
    "Select Chapter",
    ["Chapter 2: Real Property", "Chapter 3: Ownership", "Chapter 4: Legal Descriptions"]
)

# Mapping selection to filename
file_map = {
    "Chapter 2: Real Property": "chapter_2.csv",
    "Chapter 3: Ownership": "chapter_3.csv",
    "Chapter 4: Legal Descriptions": "chapter_4.csv"
}

target_file = file_map[chapter]

# 2. LOAD DATA
@st.cache_data
def load_data(file):
    if os.path.exists(file):
        return pd.read_csv(file).to_dict('records')
    return None

cards = load_data(target_file)

# 3. APP LOGIC
if cards:
    if f'idx_{chapter}' not in st.session_state:
        st.session_state[f'idx_{chapter}'] = 0
        random.shuffle(cards)
        st.session_state[f'deck_{chapter}'] = cards

    # Flashcard UI Logic goes here (Same as before, using st.session_state[f'deck_{chapter}'])
    st.success(f"Loaded {len(cards)} cards for {chapter}")
else:
    st.warning(f"⚠️ {target_file} not found in your GitHub. Please upload it to continue!")
