import streamlit as st
import random

# --- IPA Consonant Dictionary ---
consonants = [
    {"symbol": "p", "voicing": "voiceless", "place": "bilabial", "manner": "plosive"},
    {"symbol": "b", "voicing": "voiced", "place": "bilabial", "manner": "plosive"},
    {"symbol": "t", "voicing": "voiceless", "place": "alveolar", "manner": "plosive"},
    {"symbol": "d", "voicing": "voiced", "place": "alveolar", "manner": "plosive"},
    {"symbol": "k", "voicing": "voiceless", "place": "velar", "manner": "plosive"},
    {"symbol": "g", "voicing": "voiced", "place": "velar", "manner": "plosive"},
    {"symbol": "f", "voicing": "voiceless", "place": "labiodental", "manner": "fricative"},
    {"symbol": "v", "voicing": "voiced", "place": "labiodental", "manner": "fricative"},
    {"symbol": "θ", "voicing": "voiceless", "place": "dental", "manner": "fricative"},
    {"symbol": "ð", "voicing": "voiced", "place": "dental", "manner": "fricative"},
    {"symbol": "s", "voicing": "voiceless", "place": "alveolar", "manner": "fricative"},
    {"symbol": "z", "voicing": "voiced", "place": "alveolar", "manner": "fricative"},
    {"symbol": "ʃ", "voicing": "voiceless", "place": "post-alveolar", "manner": "fricative"},
    {"symbol": "ʒ", "voicing": "voiced", "place": "post-alveolar", "manner": "fricative"},
    {"symbol": "h", "voicing": "voiceless", "place": "glottal", "manner": "fricative"},
    {"symbol": "tʃ", "voicing": "voiceless", "place": "post-alveolar", "manner": "affricate"},
    {"symbol": "dʒ", "voicing": "voiced", "place": "post-alveolar", "manner": "affricate"},
    {"symbol": "m", "voicing": "voiced", "place": "bilabial", "manner": "nasal"},
    {"symbol": "n", "voicing": "voiced", "place": "alveolar", "manner": "nasal"},
    {"symbol": "ŋ", "voicing": "voiced", "place": "velar", "manner": "nasal"},
    {"symbol": "l", "voicing": "voiced", "place": "alveolar", "manner": "approximant (lateral)"},
    {"symbol": "ɹ", "voicing": "voiced", "place": "alveolar", "manner": "approximant (non-lateral)"},
    {"symbol": "j", "voicing": "voiced", "place": "palatal", "manner": "glide"},
    {"symbol": "w", "voicing": "voiced", "place": "labio-velar", "manner": "glide"},
]

# --- UI Layout ---
tab1, tab2, tab3 = st.tabs(["Explore Sounds", "Identify Symbol", "Identify Feature"])

# ----------------- TAB 1 -----------------
with tab1:
    st.header("🎛️ Explore Consonants by Features")
    voicing = st.selectbox("Select voicing:", ["All", "voiced", "voiceless"])
    place = st.selectbox("Select place of articulation:", ["All"] + sorted(set(c['place'] for c in consonants)))
    manner = st.selectbox("Select manner of articulation:", ["All"] + sorted(set(c['manner'] for c in consonants)))

    filtered = consonants
    if voicing != "All":
        filtered = [c for c in filtered if c['voicing'] == voicing]
    if place != "All":
        filtered = [c for c in filtered if c['place'] == place]
    if manner != "All":
        filtered = [c for c in filtered if c['manner'] == manner]

    st.write(f"### 🎯 {len(filtered)} sound(s) match your selection")
    st.write(", ".join(c['symbol'] for c in filtered))

# ----------------- TAB 2 -----------------
with tab2:
    st.header("🎲 Identify the Correct IPA Symbol")

    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
        st.session_state.options = []
        st.session_state.answer = None
        st.session_state.feedback = ""

    def new_question():
        st.session_state.current_question = random.choice(consonants)
        distractors = random.sample([c for c in consonants if c != st.session_state.current_question], 4)
        options = distractors + [st.session_state.current_question]
        random.shuffle(options)
        st.session_state.options = options
        st.session_state.answer = st.session_state.current_question['symbol']
        st.session_state.feedback = ""

    if st.button("Next") or st.session_state.current_question is None:
        new_question()

    question = st.session_state.current_question
    if question:
        desc = f"{question['voicing']} {question['place']} {question['manner']}"
        st.subheader(f"Which symbol matches: *{desc}*?")
        choice = st.radio("Choose one:", [c['symbol'] for c in st.session_state.options], key="tab2_choice")

        if st.button("Check answer", key="tab2_check"):
            if choice == st.session_state.answer:
                st.success("✅ Correct!")
            else:
                st.error("❌ Try again.")

# ----------------- TAB 3 -----------------
with tab3:
    st.header("🧠 Identify the Distinctive Feature")

    if 'contrast_pair' not in st.session_state:
        st.session_state.contrast_pair = None
        st.session_state.feature_answer = None
        st.session_state.feature_options = []
        st.session_state.feature_feedback = ""

    def new_pair():
        # Generate a pair of symbols that differ by only one feature
        for _ in range(100):
            a, b = random.sample(consonants, 2)
            diffs = [k for k in ['voicing', 'place', 'manner'] if a[k] != b[k]]
            if len(diffs) == 1:
                st.session_state.contrast_pair = (a, b)
                st.session_state.feature_answer = diffs[0]
                all_features = ['voicing', 'place', 'manner']
                distractors = [f for f in all_features if f != diffs[0]]
                st.session_state.feature_options = random.sample(distractors, 2) + [diffs[0]]
                random.shuffle(st.session_state.feature_options)
                st.session_state.feature_feedback = ""
                break

    if st.button("Next", key="tab3_next") or st.session_state.contrast_pair is None:
        new_pair()

    pair = st.session_state.contrast_pair
    if pair:
        st.subheader(f"What is the key difference between: {pair[0]['symbol']} vs. {pair[1]['symbol']}?")
        feature_choice = st.radio("Choose the distinguishing feature:", st.session_state.feature_options, key="tab3_radio")

        if st.button("Check answer", key="tab3_check"):
            if feature_choice == st.session_state.feature_answer:
                st.success("✅ Correct! The key feature is indeed " + feature_choice)
            else:
                st.error("❌ That's not the distinguishing feature. Try again.")
