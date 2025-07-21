import streamlit as st
import random
import re

# ---- Score display

# Initialize per-session score tracking
if "tab2_score" not in st.session_state:
    st.session_state.tab2_score = 0
if "tab2_total" not in st.session_state:
    st.session_state.tab2_total = 0



# --- IPA Consonant Dictionary ---
consonants = [
    {"symbol": "p", "voicing": "voiceless", "place": "bilabial", "oro_nasal": "oral", "centrality": "(central)", "manner": "stop"},
    {"symbol": "b", "voicing": "voiced", "place": "bilabial", "oro_nasal": "oral", "centrality": "(central)", "manner": "stop"},
    {"symbol": "t", "voicing": "voiceless", "place": "alveolar", "oro_nasal": "oral", "centrality": "(central)", "manner": "stop"},
    {"symbol": "d", "voicing": "voiced", "place": "alveolar", "oro_nasal": "oral", "centrality": "(central)", "manner": "stop"},
    {"symbol": "k", "voicing": "voiceless", "place": "velar", "oro_nasal": "oral", "centrality": "(central)", "manner": "stop"},
    {"symbol": "g", "voicing": "voiced", "place": "velar", "oro_nasal": "oral", "centrality": "(central)", "manner": "stop"},
    {"symbol": "f", "voicing": "voiceless", "place": "labiodental", "oro_nasal": "oral", "centrality": "(central)", "manner": "fricative"},
    {"symbol": "v", "voicing": "voiced", "place": "labiodental", "oro_nasal": "oral", "centrality": "(central)", "manner": "fricative"},
    {"symbol": "θ", "voicing": "voiceless", "place": "dental", "oro_nasal": "oral", "centrality": "(central)", "manner": "fricative"},
    {"symbol": "ð", "voicing": "voiced", "place": "dental", "oro_nasal": "oral", "centrality": "(central)", "manner": "fricative"},
    {"symbol": "s", "voicing": "voiceless", "place": "alveolar", "oro_nasal": "oral", "centrality": "(central)", "manner": "fricative"},
    {"symbol": "z", "voicing": "voiced", "place": "alveolar", "oro_nasal": "oral", "centrality": "(central)", "manner": "fricative"},
    {"symbol": "ʃ", "voicing": "voiceless", "place": "post-alveolar", "oro_nasal": "oral", "centrality": "(central)", "manner": "fricative"},
    {"symbol": "ʒ", "voicing": "voiced", "place": "post-alveolar", "oro_nasal": "oral", "centrality": "(central)", "manner": "fricative"},
    {"symbol": "h", "voicing": "voiceless", "place": "glottal", "oro_nasal": "oral", "centrality": "(central)", "manner": "fricative"},
    {"symbol": "tʃ", "voicing": "voiceless", "place": "post-alveolar", "oro_nasal": "oral", "centrality": "(central)", "manner": "affricate"},
    {"symbol": "dʒ", "voicing": "voiced", "place": "post-alveolar", "oro_nasal": "oral", "centrality": "(central)", "manner": "affricate"},
    {"symbol": "m", "voicing": "voiced", "place": "bilabial", "oro_nasal": "nasal", "centrality": "(central)", "manner": "stop"},
    {"symbol": "n", "voicing": "voiced", "place": "alveolar", "oro_nasal": "nasal", "centrality": "(central)", "manner": "stop"},
    {"symbol": "ŋ", "voicing": "voiced", "place": "velar", "oro_nasal": "nasal", "centrality": "(central)", "manner": "stop"},
    {"symbol": "l", "voicing": "voiced", "place": "alveolar", "oro_nasal": "oral", "centrality": "lateral", "manner": "approximant"},
    {"symbol": "ɹ", "voicing": "voiced", "place": "alveolar", "oro_nasal": "oral", "centrality": "(central)", "manner": "approximant"},
    {"symbol": "j", "voicing": "voiced", "place": "palatal", "oro_nasal": "oral", "centrality": "(central)", "manner": "approximant"},
    {"symbol": "w", "voicing": "voiced", "place": "labio-velar", "oro_nasal": "oral", "centrality": "(central)", "manner": "approximant"},
]

# Clean all trailing spaces from data
for c in consonants:
    for k in c:
        if isinstance(c[k], str):
            c[k] = c[k].strip()

def display_score(tab_label):
    score = st.session_state[f"{tab_label}_score"]
    total = st.session_state[f"{tab_label}_total"]
    st.markdown(f"**Score: {score} / {total}**")


# --- UI Layout ---
tab1, tab2 = st.tabs(["[1] Explore Sounds", "[2] Identify Symbol"])

# ----------------- TAB 1 -----------------
with tab1:
    st.header("🔎 IPA Sound Filter")

    voicing = st.selectbox("Voicing", ["Any", "voiced", "voiceless"])
    place = st.selectbox("Place of articulation", ["Any", "bilabial", "labiodental", "dental", "alveolar", "post-alveolar", "palatal", "labio-velar", "velar", "glottal"])
    oro_nasal = st.selectbox("Oro-nasal process", ["Any", "oral", "nasal"])
    centrality = st.selectbox("Centrality", ["Any", "(central)", "lateral"])
    manner = st.selectbox("Manner of articulation", ["Any", "plosive", "nasal", "fricative", "affricate", "approximant (lateral)", "approximant (non-lateral)", "glide"])

    # Define place articulation order
    place_order = {
        "bilabial": 1,
        "labiodental": 2,
        "dental": 3,
        "alveolar": 4,
        "post-alveolar": 5,
        "palatal": 6,
        "labio-velar": 7,
        "velar": 8,
        "glottal": 9
    }

    # Filter consonants
    filtered = [
        c for c in consonants
        if (voicing == "Any" or c["voicing"] == voicing)
        and (place == "Any" or c["place"] == place)
        and (oro_nasal == "Any" or c["oro_nasal"] == oro_nasal)
        and (centrality == "Any" or c["centrality"] == centrality)
        and (manner == "Any" or c["manner"] == manner)
    ]

    # Sort by place of articulation
    filtered.sort(key=lambda c: place_order.get(c["place"], 99))

    st.markdown(f"### 🎯 {len(filtered)} result(s):")

    if filtered:
        # Sort by place of articulation (following typical order)
        place_order = [
            "bilabial", "labiodental", "dental", "alveolar",
            "post-alveolar", "palatal", "labio-velar", "velar", "glottal"
        ]

        place_groups = {}
        for c in filtered:
            place = c["place"]
            if place not in place_groups:
                place_groups[place] = []
            place_groups[place].append(c["symbol"])

        # Display grouped sounds by place in the defined order
        for place in place_order:
            if place in place_groups:
                symbols = ", ".join([f"<span style='font-size:1.6em'>{s}</span>" for s in place_groups[place]])
                st.markdown(f"{symbols} <span style='color:gray'>({place})</span><br>", unsafe_allow_html=True)
    else:
        st.info("No matching sounds found.")




# ----------------- TAB 2 -----------------
with tab2:
    
    st.header("🌳 Identify the Correct IPA Symbol")

    display_score("tab2")

    # Initialize session state
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
    if "options" not in st.session_state:
        st.session_state.options = []
    if "answer" not in st.session_state:
        st.session_state.answer = None

    def new_question():
        st.session_state.current_question = random.choice(consonants)
        correct = st.session_state.current_question
        distractors = random.sample([c for c in consonants if c != correct], 4)
        options = distractors + [correct]
        random.shuffle(options)
        st.session_state.options = options
        st.session_state.answer = correct['symbol']

    # Trigger new question at start or after "Next"
    if st.session_state.current_question is None:
        new_question()

    question = st.session_state.current_question

    if question:
        # Format manner
        if question["manner"] == "nasal":
            desc = f"{question['place']} ({question['oro_nasal']}) nasal (stop)"
        else:
            manner_display = question["manner"]
            # Drop centrality if manner includes 'lateral'
            centrality_display = "" if "lateral" in manner_display else question["centrality"]
            desc_parts = [
                question["voicing"],
                question["place"],
                f"({question['oro_nasal']})",
                centrality_display,
                manner_display
            ]
            desc = " ".join([part for part in desc_parts if part])

        # Style bracketed text gray
        import re
        desc_html = re.sub(r"\((.*?)\)", r"<span style='color:gray'>(\1)</span>", desc)
        st.markdown(f"#### Which symbol matches: *{desc_html}*?", unsafe_allow_html=True)

        # Show options
        choice = st.radio("Choose one:", [c['symbol'] for c in st.session_state.options], key="tab2_choice_radio")

        # Buttons
# Buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("Check answer", key="tab2_check_btn"):
                st.session_state.tab2_total += 1
                if choice == st.session_state.answer:
                    st.session_state.tab2_score += 1
                    st.success("✅ Correct!")
                else:
                    st.error("❌ Try again.")

                        # 🎉 Trigger balloons if user reaches 20/20
                if st.session_state.tab2_score == 20 and st.session_state.tab2_total == 20:
                    st.balloons()
        
        with col2:
            if st.button("Next", key="tab2_next_btn"):
                new_question()
                st.rerun()
        
        with col3:
            if st.button("🔁 Reset Session", key="tab2_reset_btn"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
           
