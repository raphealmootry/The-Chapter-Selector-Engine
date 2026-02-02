import streamlit as st
import pandas as pd
import random
import os

st.set_page_config(page_title="Ohio RE Master Suite", layout="wide")

# --- 1. CONFIGURATION & NAVIGATION ---
st.sidebar.title("📚 Course Navigation")

# This list must match the keys in your file_map below
chapter_choice = st.sidebar.selectbox(
    "Select Chapter",
    ["Chapter 2", "Chapter 3", "Chapter 4", "Chapter 5"]
)

# MAP: This links the sidebar name to the EXACT filename in your GitHub
file_map = {
    "Chapter 2": "chapter_2.csv",
    "Chapter 3": "chapter_3.csv",
    "Chapter 4": "chapter_4.csv",
    "Chapter 5": "chapter_5.csv"
}

target_file = file_map[chapter_choice]

# --- 2. DATA LOADING ENGINE ---
@st.cache_data
def load_data(filename):
    if os.path.exists(filename):
        try:
            # Load CSV and fill empty 'Options' with empty strings to prevent errors
            df = pd.read_csv(filename).fillna("")
            return df.to_dict('records')
        except Exception as e:
            st.error(f"Error reading {filename}: {e}")
            return None
    return None

# --- 3. SESSION STATE INITIALIZATION ---
# We use chapter-specific keys so your progress is saved if you switch tabs
if f"deck_{chapter_choice}" not in st.session_state:
    data = load_data(target_file)
    if data:
        random.shuffle(data)
        st.session_state[f"deck_{chapter_choice}"] = data
        st.session_state[f"idx_{chapter_choice}"] = 0
        st.session_state[f"reveal_{chapter_choice}"] = False

# --- 4. MAIN INTERFACE ---
tab1, tab2 = st.tabs(["🎴 Flashcards", "⚙️ Deck Management"])

if f"deck_{chapter_choice}" in st.session_state:
    deck = st.session_state[f"deck_{chapter_choice}"]
    idx = st.session_state[f"idx_{chapter_choice}"]
    
    with tab1:
        st.title(f"Unit: {chapter_choice}")
        st.progress((idx + 1) / len(deck))
        st.write(f"**Card {idx + 1} of {len(deck)}**")
        
        curr = deck[idx]
        
        with st.container(border=True):
            # Display Question
            st.markdown(f"### {curr['Question']}")
            
            # Display Options ONLY if they exist (prevents KeyError/Empty boxes)
            if curr.get('Options') and str(curr['Options']).strip() != "":
                st.info(curr['Options'])
            
            # Reveal Logic
            if st.session_state[f"reveal_{chapter_choice}"]:
                st.divider()
                st.markdown(f"#### Answer: {curr['Answer']}")
                st.success(f"💡 **Explanation:** {curr['Explanation']}")

        # Navigation Buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⬅️ Previous"):
                st.session_state[f"idx_{chapter_choice}"] = (idx - 1) % len(deck)
                st.session_state[f"reveal_{chapter_choice}"] = False
                st.rerun()
        with col2:
            label = "🙈 Hide Answer" if st.session_state[f"reveal_{chapter_choice}"] else "👁️ Reveal Answer"
            if st.button(label, type="primary", use_container_width=True):
                st.session_state[f"reveal_{chapter_choice}"] = not st.session_state[f"reveal_{chapter_choice}"]
                st.rerun()
        with col3:
            if st.button("Next ➡️"):
                st.session_state[f"idx_{chapter_choice}"] = (idx + 1) % len(deck)
                st.session_state[f"reveal_{chapter_choice}"] = False
                st.rerun()

    with tab2:
        st.header("Deck Management")
        st.write(f"Current File: `{target_file}`")
        if st.button("🗑️ Reshuffle Current Unit"):
            random.shuffle(st.session_state[f"deck_{chapter_choice}"])
            st.session_state[f"idx_{chapter_choice}"] = 0
            st.rerun()
        
        st.dataframe(pd.DataFrame(deck), use_container_width=True)

else:
    st.warning(f"⚠️ **File Not Found:** Please ensure `{target_file}` is uploaded to your GitHub repository.")
    st.info("The filename must be all lowercase with an underscore (e.g., chapter_2.csv).")

# --- 5. SIDEBAR EXTRAS ---
st.sidebar.divider()
st.sidebar.video("https://www.youtube.com/watch?v=5yx6BWlEVcY")
