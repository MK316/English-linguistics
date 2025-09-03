import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Allophonic Rules — CSV Quiz", page_icon="🔤", layout="centered")
st.markdown("#### (Not yet working) English Allophonic Rule practice")
st.caption("Choose a rule, select all items that exemplify it, then submit. Click “Show me another set of words” for new items.")

# --------------------------
# 1) Load the fixed CSV (set your RAW URL here)
# --------------------------
RAW_URL = "https://raw.githubusercontent.com/MK316/classmaterial/refs/heads/main/Phonetics/allophonic_rules_dataset.csv"

@st.cache_data
def load_rules(url: str):
    df = pd.read_csv(url)
    required = {"rule_label","description","set","option","item_text","is_correct"}
    if not required.issubset(df.columns):
        raise ValueError(f"CSV missing required columns. Found: {list(df.columns)}")

    # Normalize types
    df["set"] = df["set"].astype(int)
    df["option"] = df["option"].astype(int)
    df["is_correct"] = df["is_correct"].astype(int)

    # Build RULES dict in memory
    rules = {}
    for rule_label, g in df.groupby("rule_label", sort=False):
        desc = g["description"].iloc[0]
        sets = []
        for s, sg in g.sort_values(["set","option"]).groupby("set", sort=True):
            items = [{"text": row["item_text"], "is_correct": bool(row["is_correct"])} for _, row in sg.iterrows()]
            sets.append(items)
        rules[rule_label] = {"desc": desc, "sets": sets}
    return rules

RULES = load_rules(RAW_URL)

# --------------------------
# 2) State & helpers
# --------------------------
def ensure_state():
    if "started" not in st.session_state:
        st.session_state.started = False
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

def reset_current_set():
    # bump nonce so checkbox keys change -> clears selections on next render
    st.session_state.nonce += 1

def evaluate_selection(items, selected_flags):
    correct_flags = [it["is_correct"] for it in items]
    perfect = all(s == c for s, c in zip(selected_flags, correct_flags))
    must_select = [it["text"] for i, it in enumerate(items) if correct_flags[i] and not selected_flags[i]]
    should_uncheck = [it["text"] for i, it in enumerate(items) if (not correct_flags[i]) and selected_flags[i]]
    return perfect, must_select, should_uncheck

ensure_state()

# --------------------------
# 3) Start gate (one click)
# --------------------------
start_clicked = st.button("Start ▶️", disabled=st.session_state.started)
if start_clicked and not st.session_state.started:
    st.session_state.started = True
    if hasattr(st, "rerun"): st.rerun()
    elif hasattr(st, "experimental_rerun"): st.experimental_rerun()

if not st.session_state.started:
    st.info("Click **Start** to begin.")
    st.stop()

# --------------------------
# 4) Rule dropdown (from CSV rule_label)
# --------------------------
rule_options = list(RULES.keys())
st.selectbox(
    "Rule",
    options=rule_options,
    index=rule_options.index(st.session_state.rule_key),
    key="rule_key",
    on_change=on_rule_change
)


# --------------------------
# 6) Render current set — HORIZONTAL layout
# --------------------------
rk = st.session_state.rule_key
si = st.session_state.set_idx[rk]
items = RULES[rk]["sets"][si]
st.caption(f"Set {si + 1} of {len(RULES[rk]['sets'])}")

st.markdown(f"#### Rule Description: {RULES[rk]['desc']}")

# Arrange options horizontally in N columns (wraps to next row)
N_COLS = 3
cols = st.columns(N_COLS)

selected = []
for i, it in enumerate(items):
    col = cols[i % N_COLS]  # distribute left→right, wrap
    with col:
        selected.append(
            st.checkbox(it["text"], key=f"chk_{rk}_{si}_{i}_{st.session_state.nonce}")
        )

# --------------------------
# 5) Controls BEFORE rendering items (one-click behavior)
# --------------------------
c1, c2 = st.columns([1, 1])
with c1:
    st.button("✅ Show me another set of words", key="next_set_btn", on_click=next_set)
with c2:
    st.button("⁉️ Reset selections", key="reset_btn", on_click=reset_current_set)


st.divider()
colA, colB = st.columns([1, 1])
with colA:
    if st.button("Submit"):
        perfect, must_select, should_uncheck = evaluate_selection(items, selected)
        if perfect:
            st.success("🎉 Well done!")
        else:
            st.error("Not quite. See feedback:")
            if must_select:
                st.write("**You missed these correct items:** " + ", ".join(must_select))
            if should_uncheck:
                st.write("**These should not be selected:** " + ", ".join(should_uncheck))

with colB:
    st.caption("Tip: Use the buttons above to switch sets or clear selections.")
