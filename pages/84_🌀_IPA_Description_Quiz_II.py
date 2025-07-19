import streamlit as st
import random
import re

# --- IPA Consonant Dictionary ---
consonants = [
    {"symbol": "p", "voicing": "voiceless", "place": "bilabial", "oro_nasal": "oral", "centrality": "(central)", "manner": "plosive"},
    {"symbol": "b", "voicing": "voiced", "place": "bilabial", "oro_nasal": "oral", "centrality": "(central)", "manner": "plosive"},
    {"symbol": "t", "voicing": "voiceless", "place": "alveolar", "oro_nasal": "oral", "centrality": "(central)", "manner": "plosive"},
    {"symbol": "d", "voicing": "voiced", "place": "alveolar", "oro_nasal": "oral", "centrality": "(central)", "manner": "plosive"},
    {"symbol": "k", "voicing": "voiceless", "place": "velar", "oro_nasal": "oral", "centrality": "(central)", "manner": "plosive"},
    {"symbol": "g", "voicing": "voiced", "place": "velar", "oro_nasal": "oral", "centrality": "(central)", "manner": "plosive"},
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
    {"symbol": "m", "voicing": "voiced", "place": "bilabial", "oro_nasal": "nasal", "centrality": "(central)", "manner": "nasal"},
    {"symbol": "n", "voicing": "voiced", "place": "alveolar", "oro_nasal": "nasal", "centrality": "(central)", "manner": "nasal"},
    {"symbol": "ŋ", "voicing": "voiced", "place": "velar", "oro_nasal": "nasal", "centrality": "(central)", "manner": "nasal"},
    {"symbol": "l", "voicing": "voiced", "place": "alveolar", "oro_nasal": "oral", "centrality": "lateral", "manner": "approximant "},
    {"symbol": "ɹ", "voicing": "voiced", "place": "alveolar", "oro_nasal": "oral", "centrality": "(central)", "manner": "approximant"},
    {"symbol": "j", "voicing": "voiced", "place": "palatal", "oro_nasal": "oral", "centrality": "(central)", "manner": "glide"},
    {"symbol": "w", "voicing": "voiced", "place": "labio-velar", "oro_nasal": "oral", "centrality": "(central)", "manner": "glide"},
]


# --- UI Layout ---
tab1, tab2, tab3 = st.tabs(["Explore Sounds", "Identify Symbol", "Identify Feature"])

# ----------------- TAB 1 -----------------
with tab1:
    st.header("🎛️ Explore Consonants by Features")
    voicing = st.selectbox("Select voicing:", ["All", "voiced", "voiceless"])
    place = st.selectbox("Select place of articulation:", ["All"] + sorted(set(c['place'] for c in consonants)))
    oro_nasal = st.selectbox("Select oro-nasal process:", ["All"] + sorted(set(c['oro_nasal'] for c in consonants)))
    centrality = st.selectbox("Select centrality:", ["All"] + sorted(set(c['centrality'] for c in consonants)))
    manner = st.selectbox("Select manner of articulation:", ["All"] + sorted(set(c['manner'] for c in consonants)))

    filtered = consonants
    if voicing != "All":
        filtered = [c for c in filtered if c['voicing'] == voicing]
    if place != "All":
        filtered = [c for c in filtered if c['place'] == place]
    if oro_nasal != "All":
        filtered = [c for c in filtered if c['oro_nasal'] == oro_nasal]
    if centrality != "All":
        filtered = [c for c in filtered if c['centrality'] == centrality]
    if manner != "All":
        filtered = [c for c in filtered if c['manner'] == manner]

    st.write(f"### 🎯 {len(filtered)} sound(s) match your selection")
    st.write(", ".join(c['symbol'] for c in filtered))

# ----------------- TAB 2 -----------------
with tab2:
    st.header("🎲 Identify the Correct IPA Symbol")

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
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Check answer", key="tab2_check_btn"):
                if choice == st.session_state.answer:
                    st.success("✅ Correct!")
                else:
                    st.error("❌ Try again.")
        with col2:
            if st.button("Next", key="tab2_next_btn"):
                new_question()
                st.rerun()


# ----------------- TAB 3 -----------------
with tab3:
    st.header("🧠 Identify the Distinctive Feature")

    if 'contrast_pair' not in st.session_state:
        st.session_state.contrast_pair = None
        st.session_state.feature_answer = None
        st.session_state.feature_options = []
        st.session_state.feature_feedback = ""

    def new_pair():
        for _ in range(100):
            a, b = random.sample(consonants, 2)
            diffs = [k for k in ['voicing', 'place', 'oro_nasal', 'centrality', 'manner'] if a[k] != b[k]]
            if len(diffs) == 1:
                st.session_state.contrast_pair = (a, b)
                st.session_state.feature_answer = diffs[0]
                all_features = ['voicing', 'place', 'oro_nasal', 'centrality', 'manner']
                distractors = [f for f in all_features if f != diffs[0]]
                st.session_state.feature_options = random.sample(distractors, 4 - 1) + [diffs[0]]
                random.shuffle(st.session_state.feature_options)
                st.session_state.feature_feedback = ""
                break

    if st.button("Next", key="tab3_next") or st.session_state.contrast_pair is None:
        new_pair()

    pair = st.session_state.contrast_pair
    if pair:
        st.subheader(f"What is the key difference between: {pair[0]['symbol']} vs. {pair[1]['symbol']}?")
        feature_choice = st.radio("Choose the distinguishing feature:", st.session_state.feature_options, key="tab3_radio")

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Check answer", key="tab3_check"):
                if feature_choice == st.session_state.feature_answer:
                    st.success("✅ Correct! The key feature is indeed " + feature_choice)
                else:
                    st.error("❌ That's not the distinguishing feature. Try again.")
        with col2:
            st.button("Next", key="tab3_next_btn2", on_click=new_pair)
