import streamlit as st
import pandas as pd

st.set_page_config(page_title="Allophonic Rules — CSV-driven Quiz", page_icon="🔤", layout="centered")
st.title("English Allophonic Rules — CSV-driven Quiz")
st.caption("Load the dataset from a GitHub Raw URL or upload a CSV. Then pick a rule and practice.")

# --------------------------
# Data loading
# --------------------------
default_url = ""  # paste your Raw GitHub CSV URL here when ready
url = st.text_input("GitHub RAW CSV URL (optional)", value=default_url, placeholder="https://raw.githubusercontent.com/MK316/classmaterial/refs/heads/main/Phonetics/allophonic_rules_dataset.csv")
uploaded = st.file_uploader("Or upload the CSV", type=["csv"])

@st.cache_data
def load_df_from_url(u: str):
    return pd.read_csv(u)

@st.cache_data
def load_df_from_bytes(b):
    return pd.read_csv(b)

df = None
if url:
    try:
        df = load_df_from_url(url)
        st.success("Loaded CSV from URL.")
    except Exception as e:
        st.warning(f"Could not load from URL: {e}")
if df is None and uploaded is not None:
    try:
        df = load_df_from_bytes(uploaded)
        st.success("Loaded CSV from upload.")
    except Exception as e:
        st.error(f"Could not read uploaded CSV: {e}")

if df is None:
    st.info("Provide a GitHub RAW URL or upload the CSV to begin.")
    st.stop()

# Validate schema
required_cols = {"rule_label","description","set","option","item_text","is_correct"}
if not required_cols.issubset(set(df.columns)):
    st.error(f"CSV missing required columns. Found: {list(df.columns)}")
    st.stop()

# Normalize types
df["set"] = df["set"].astype(int)
df["option"] = df["option"].astype(int)
df["is_correct"] = df["is_correct"].astype(int)

# --------------------------
# Build in-memory dataset
# --------------------------
RULES = {}
for rule_label, g in df.groupby("rule_label", sort=False):
    desc = g["description"].iloc[0]
    sets = []
    for s, sg in g.sort_values(["set","option"]).groupby("set", sort=True):
        items = [{"text": row["item_text"], "is_correct": bool(row["is_correct"])} for _, row in sg.iterrows()]
        sets.append(items)
    RULES[rule_label] = {"desc": desc, "sets": sets}

# --------------------------
# State & callbacks
# --------------------------
def ensure_state():
    if "rule_key" not in st.session_state:
        st.session_state.rule_key = list(RULES.keys())[0]
    if "set_idx" not in st.session_state:
        st.session_state.set_idx = {k: 0 for k in RULES.keys()}
    if "nonce" not in st.session_state:
        st.session_state.nonce = 0

def on_rule_change():
    rk = st.session_state.rule_key
    st.session_state.set_idx[rk] = 0
    st.session_state.nonce += 1

def next_set():
    rk = st.session_state.rule_key
    total = len(RULES[rk]["sets"])
    st.session_state.set_idx[rk] = (st.session_state.set_idx[rk] + 1) % total
    st.session_state.nonce += 1

def evaluate_selection(items, selected_flags):
    correct_flags = [it["is_correct"] for it in items]
    perfect = all(s == c for s, c in zip(selected_flags, correct_flags))
    must_select = [it["text"] for i, it in enumerate(items) if correct_flags[i] and not selected_flags[i]]
    should_uncheck = [it["text"] for i, it in enumerate(items) if not correct_flags[i] and selected_flags[i]]
    return perfect, must_select, should_uncheck

ensure_state()

# --------------------------
# UI: select rule + next set button
# --------------------------
rule_options = list(RULES.keys())
st.selectbox("Rule", rule_options,
             index=rule_options.index(st.session_state.rule_key),
             key="rule_key",
             on_change=on_rule_change)

st.button("Show me another set of words", key="next_set_btn", on_click=next_set)

# Read current set and render
rk = st.session_state.rule_key
si = st.session_state.set_idx[rk]
items = RULES[rk]["sets"][si]

st.markdown(f"**Description:** {RULES[rk]['desc']}")
st.caption(f"Set {si + 1} of {len(RULES[rk]['sets'])}")

selected = []
for i, it in enumerate(items):
    selected.append(st.checkbox(it["text"], key=f"chk_{rk}_{si}_{i}_{st.session_state.nonce}"))

# Submit & feedback
colA, colB = st.columns([1,1])
with colA:
    if st.button("Submit"):
        perfect, must_select, should_uncheck = evaluate_selection(items, selected)
        if perfect:
            st.success("🎉 Well done!")
        else:
            st.error("Not quite. Check the feedback below.")
            if must_select:
                st.write("**You missed these correct items:** " + ", ".join(must_select))
            if should_uncheck:
                st.write("**These should not be selected:** " + ", ".join(should_uncheck))

with colB:
    st.caption("Tip: Change the rule or click 'Show me another set of words' for fresh items.")
