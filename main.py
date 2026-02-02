import streamlit as st
import pandas as pd
import random
import os

st.set_page_config(page_title="Ohio RE Master Suite", layout="wide")

# --- 1. CONFIGURATION & NAVIGATION ---
st.sidebar.title("📚 Course Navigation")

# 1. Update the selectbox to include Chapter 1
chapter_choice = st.sidebar.selectbox(
    "Select Chapter",
    ["Chapter 1", "Chapter 2", "Chapter 3", "Chapter 4", "Chapter 5"]
)

# 2. Update the map so the engine knows where to look
file_map = {
    "Chapter 1": "chapter_1.csv",  # <--- ADD THIS LINE
    "Chapter 2": "chapter_2.csv",
    "Chapter 3": "chapter_3.csv",
    "Chapter 4": "chapter_4.csv",
    "Chapter 5": "chapter_5.csv"
}

target_file = file_map[chapter_choice]

# --- 2. DATA LOADING ENGINE ---
@st.cache_data(show_spinner=False)
def load_data(filename):
    base_path = os.path.dirname(__file__)
    full_path = os.path.join(base_path, filename)
    
    if os.path.exists(full_path):
        try:
            df = pd.read_csv(full_path).fillna("")
            return df.to_dict('records')
        except Exception as e:
            st.error(f"Error reading {filename}: {e}")
            return None
    return None

# --- 3. SESSION STATE INITIALIZATION ---
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
        
        curr = deck[idx]
        
        with st.container(border=True):
            st.markdown(f"### {curr['Question']}")
            
            if curr.get('Options') and str(curr['Options']).strip() != "":
                clean_options = str(curr['Options']).replace("\\n", "\n")
                st.info(clean_options)
            
            if st.session_state[f"reveal_{chapter_choice}"]:
                st.divider()
                st.markdown(f"#### Answer: {curr['Answer']}")
                st.success(f"💡 **Explanation:** {curr['Explanation']}")

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
        st.write(f"Currently viewing: `{target_file}`")
        if st.button("🗑️ Reshuffle & Force Sync"):
            st.cache_data.clear()
            del st.session_state[f"deck_{chapter_choice}"]
            st.rerun()
        st.dataframe(pd.DataFrame(deck), use_container_width=True)

else:
    st.error(f"⚠️ **File Not Found:** `{target_file}`")
    if st.button("🔄 Try Re-scanning Repository"):
        st.cache_data.clear()
        st.rerun()

# --- 5. SIDEBAR EXTRAS (The Vibes) ---
st.sidebar.divider()
st.sidebar.markdown("### 🎧 Study Beats")
st.sidebar.video("https://www.youtube.com/watch?v=5yx6BWlEVcY")

if st.sidebar.checkbox("Show Debug Mode"):
    st.sidebar.write("Visible Files:", os.listdir("."))
