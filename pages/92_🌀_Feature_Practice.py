import streamlit as st

import streamlit as st
from st_aggrid import AgGrid
import pandas as pd
import random

tab1, tab2, tab3, tab4 = st.tabs(["🌀 Feature matrix","🌀 Consonant Practice","🌀 Vowel practice","🌀 Natural class"])

# IPA features dictionary with full feature names
ipa_features = {
    'p': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '-', 'anterior': '+', 'continuant': '-', 'nasal': '-', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '-'},
    'b': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '-', 'anterior': '+', 'continuant': '-', 'nasal': '-', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '+'},
    't': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '+', 'anterior': '+', 'continuant': '-', 'nasal': '-', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '-'},
    'd': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '+', 'anterior': '+', 'continuant': '-', 'nasal': '-', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '+'},
    'k': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '-', 'anterior': '-', 'continuant': '-', 'nasal': '-', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '-'},
    'g': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '-', 'anterior': '-', 'continuant': '-', 'nasal': '-', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '+'},
    'tʃ': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '+', 'anterior': '-', 'continuant': '-', 'nasal': '-', 'strident': '+', 'lateral': '-', 'delayed release': '+', 'voice': '-'},
    'dʒ': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '+', 'anterior': '-', 'continuant': '-', 'nasal': '-', 'strident': '+', 'lateral': '-', 'delayed release': '+', 'voice': '+'},
    'f': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '-', 'anterior': '+', 'continuant': '+', 'nasal': '-', 'strident': '+', 'lateral': '-', 'delayed release': '-', 'voice': '-'},
    'v': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '-', 'anterior': '+', 'continuant': '+', 'nasal': '-', 'strident': '+', 'lateral': '-', 'delayed release': '-', 'voice': '+'},
    'θ': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '+', 'anterior': '+', 'continuant': '+', 'nasal': '-', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '-'},
    'ð': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '+', 'anterior': '+', 'continuant': '+', 'nasal': '-', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '+'},
    's': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '+', 'anterior': '+', 'continuant': '+', 'nasal': '-', 'strident': '+', 'lateral': '-', 'delayed release': '-', 'voice': '-'},
    'z': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '+', 'anterior': '+', 'continuant': '+', 'nasal': '-', 'strident': '+', 'lateral': '-', 'delayed release': '-', 'voice': '+'},
    'ʃ': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '+', 'anterior': '-', 'continuant': '+', 'nasal': '-', 'strident': '+', 'lateral': '-', 'delayed release': '-', 'voice': '-'},
    'ʒ': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '+', 'anterior': '-', 'continuant': '+', 'nasal': '-', 'strident': '+', 'lateral': '-', 'delayed release': '-', 'voice': '+'},
    'h': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '-', 'anterior': '-', 'continuant': '+', 'nasal': '-', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '-'},
    'm': {'syllabic': '-', 'consonantal': '+', 'sonorant': '+', 'coronal': '-', 'anterior': '+', 'continuant': '-', 'nasal': '+', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '+'},
    'n': {'syllabic': '-', 'consonantal': '+', 'sonorant': '+', 'coronal': '+', 'anterior': '+', 'continuant': '-', 'nasal': '+', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '+'},
    'ŋ': {'syllabic': '-', 'consonantal': '+', 'sonorant': '+', 'coronal': '-', 'anterior': '-', 'continuant': '-', 'nasal': '+', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '+'},
    'l': {'syllabic': '-', 'consonantal': '+', 'sonorant': '+', 'coronal': '+', 'anterior': '+', 'continuant': '+', 'nasal': '-', 'strident': '-', 'lateral': '+', 'delayed release': '-', 'voice': '+'},
    'r': {'syllabic': '-', 'consonantal': '+', 'sonorant': '+', 'coronal': '+', 'anterior': '+', 'continuant': '+', 'nasal': '-', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '+'},
    'j': {'syllabic': '-', 'consonantal': '-', 'sonorant': '+', 'coronal': '-', 'anterior': '-', 'continuant': '+', 'nasal': '-', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '+'},
    'w': {'syllabic': '-', 'consonantal': '-', 'sonorant': '+', 'coronal': '-', 'anterior': '-', 'continuant': '+', 'nasal': '-', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '+'}
}

# Grouped features based on previous dictionary
grouped_features = {
    '[+voice]': ['b', 'd', 'g', 'dʒ', 'v', 'ð', 'z', 'ʒ', 'm', 'n', 'ŋ', 'l', 'r', 'j', 'w'],
    '[-voice]': ['p', 't', 'k', 'tʃ', 'f', 'θ', 's', 'ʃ', 'h'],
    '[+anterior]': ['p', 'b', 't', 'd', 'f', 'v', 'θ', 'ð', 's', 'z', 'm', 'n', 'l', 'r'],
    '[+coronal]': ['t', 'd', 'tʃ', 'dʒ', 'θ', 'ð', 's', 'z', 'ʃ', 'ʒ', 'n', 'l', 'r'],
    '[+delayed release]': ['tʃ', 'dʒ'],
    '[+sonorant]': ['m', 'n', 'ŋ', 'l', 'r', 'j', 'w'],
    '[+strident]': ['tʃ', 'dʒ', 'f', 'v', 's', 'z', 'ʃ', 'ʒ'],
    '[+nasal]': ['m', 'n', 'ŋ'],
    '[+continuant]': ['f', 'v', 'θ', 'ð', 's', 'z', 'ʃ', 'ʒ', 'h', 'l', 'r', 'j', 'w'],
}


# Define vowel features
vowel_features = {
    '[i]': {'[high]': '+', '[low]': '-', '[front]': '+', '[back]': '-', '[rounded]': '-', '[tense]': '+'},
    '[ɪ]': {'[high]': '+', '[low]': '-', '[front]': '+', '[back]': '-', '[rounded]': '-', '[tense]': '-'},
    '[ɛ]': {'[high]': '-', '[low]': '-', '[front]': '+', '[back]': '-', '[rounded]': '-', '[tense]': '-'},
    '[æ]': {'[high]': '-', '[low]': '+', '[front]': '+', '[back]': '-', '[rounded]': '-', '[tense]': '-'},
    '[ə]': {'[high]': '-', '[low]': '-', '[front]': '-', '[back]': '-', '[rounded]': '-', '[tense]': '-'},
    '[u]': {'[high]': '+', '[low]': '-', '[front]': '-', '[back]': '+', '[rounded]': '+', '[tense]': '+'},
    '[ʊ]': {'[high]': '+', '[low]': '-', '[front]': '-', '[back]': '+', '[rounded]': '+', '[tense]': '-'},
    '[ʌ]': {'[high]': '-', '[low]': '-', '[front]': '-', '[back]': '+', '[rounded]': '-', '[tense]': '-'},
    '[ɔ]': {'[high]': '-', '[low]': '-', '[front]': '-', '[back]': '+', '[rounded]': '+', '[tense]': '+'},
    '[ɑ]': {'[high]': '-', '[low]': '+', '[front]': '-', '[back]': '+', '[rounded]': '-', '[tense]': '+'}
}

# Dictionary comprehension to modify keys to include brackets
modified_ipa_features = {phoneme: {'[' + feature + ']': value for feature, value in features.items()} for phoneme, features in ipa_features.items()}

# Now modified_ipa_features contains the updated keys
# print(modified_ipa_features)

with tab1:
    def create_feature_matrix(ipa_features):
        # Convert the dictionary to a DataFrame
        df = pd.DataFrame(ipa_features)  # Transpose to make symbols columns and features rows
        return df
    
    def app():
        st.markdown('#### 🐣 Consonant Feature Matrix')
        st.write('This matrix displays the distinctive features for 24 English consonants in IPA.')
    
        # Generate the feature matrix DataFrame
        feature_matrix = create_feature_matrix(modified_ipa_features)
    
        # Display the feature matrix
        st.dataframe(feature_matrix, height=440, use_container_width=True)
    
    if __name__ == "__main__":
        app()

with tab2:
    st.markdown('### 🐾 Distinctive Feature Practice Apps')
    st.write('Applications to train yourself with distinctive features in phonology')

    st.caption("""
    Here is a selection of applications designed to enhance feature matrix learning through interactive and innovative tools.
    """)

    # Columns for buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <a href="https://mk-316-featureapp01.hf.space/" target="_blank">
            <button style="
                background-color: #FF8C42;
                color: white;
                padding: 10px 15px;
                font-size: 14px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                width: 100%;
            ">
                App 1: Distinctive Features
            </button>
        </a>
        <p style="font-size:13px">Basic level - Sound lists by feature marking</p>
        <p style="font-size:12px; color: gray">Updated on: 2024.10.15</p>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <a href="https://mk-316-feature-practice.hf.space/" target="_blank">
            <button style="
                background-color: #0d47a1;
                color: white;
                padding: 10px 15px;
                font-size: 14px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                width: 100%;
            ">
                App 2: Feature Quiz 1
            </button>
        </a>
        <p style="font-size:13px">Basic level - Feature marking for individual segments</p>
        <p style="font-size:12px; color: gray">Updated on: 2024.10.14</p>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <a href="https://feature-quiz02.streamlit.app/" target="_blank">
            <button style="
                background-color: #7e57c2;
                color: white;
                padding: 10px 15px;
                font-size: 14px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                width: 100%;
            ">
                App 3: Feature Quiz 2
            </button>
        </a>
        <p style="font-size:13px">Level 1 - Distinctive feature quiz (choose)</p>
        <p style="font-size:12px; color: gray">Updated on: 2024.11.6</p>
        """, unsafe_allow_html=True)

with tab3: 
    def create_feature_matrix(vowel_features):
        # Convert the dictionary to a DataFrame and transpose it
        df = pd.DataFrame(vowel_features)  # Transpose to make symbols columns and features rows
        return df
    
    def app():
        st.markdown('#### 🐣 Vowel Feature Matrix')
        st.write('This matrix displays the distinctive features for English vowels in IPA.')

        # Generate the feature matrix DataFrame
        feature_matrix = create_feature_matrix(vowel_features)
    
        # Display the feature matrix
        st.dataframe(feature_matrix, height=260, use_container_width=True)

        st.info("Note 1: The vowel [ʌ] is phonologically marked as [+back], even though it is phonetically pronounced more centrally. This distinction may not be crucial for the TCE exam.")
        
        st.info("Note 2: The vowel [ɔ] is marked as [+tense] here. You may encounter different descriptions in various textbooks.")

    if __name__ == "__main__":
        app()




# Function to generate question sets
# Updated function: only selects sound groups, not a fixed answer
# def generate_questions(num_sets):
#     all_sets = []
#     used_sets = set()
#     features = list(grouped_features.items())

#     while len(all_sets) < num_sets:
#         feature, sounds = random.choice(features)
#         if len(sounds) >= 3:
#             selected = sorted(random.sample(sounds, min(4, len(sounds))))
#             if tuple(selected) not in used_sets:
#                 all_sets.append(selected)
#                 used_sets.add(tuple(selected))
#     return all_sets

def generate_questions(num_sets, sounds_per_set=4):
    all_sets = []
    used_sets = set()
    features = list(grouped_features.items())

    while len(all_sets) < num_sets:
        feature, sounds = random.choice(features)
        if len(sounds) >= sounds_per_set:
            selected = sorted(random.sample(sounds, sounds_per_set))
            if tuple(selected) not in used_sets:
                all_sets.append(selected)
                used_sets.add(tuple(selected))
    return all_sets


def get_all_matching_features(sound_list):
    if not sound_list:
        return []

    # Start with features of the first sound
    common = set(ipa_features[sound_list[0]].items())

    # Intersect with features of the rest
    for sound in sound_list[1:]:
        common &= set(ipa_features[sound].items())

    # Return BOTH [+] and [-] features
    return [f"[{val}{feat}]" for feat, val in common]


with tab4:
    with st.expander("**Instructions**"):
        st.info("""
        **Consider the following features only:**  
        [+voice], [-voice], [+anterior], [+coronal], [+delayed release],  
        [+sonorant], [+strident], [+nasal], [+continuant]  
        Write answers in square brackets, like `[+voice]` or `[+nasal]`.
        """)
    st.caption("📌 Do not use [+consonantal], [-nasal], or [-lateral], most of which are uninformative to group sounds")
    st.markdown("---")

    # Initialize session state
    if 'questions' not in st.session_state:
        st.session_state['questions'] = []
    if 'current_question' not in st.session_state:
        st.session_state['current_question'] = 0
    if 'score' not in st.session_state:
        st.session_state['score'] = 0
    if 'answered' not in st.session_state:
        st.session_state['answered'] = False

    # Ask user how many sets
    if not st.session_state['questions']:
        num_sets = st.number_input("How many sets would you like to practice?", min_value=1, max_value=10, value=1)
        sounds_per_set = st.number_input("How many sounds per set?", min_value=2, max_value=6, value=4)
        
        if st.button("Start Practice"):
            st.session_state['questions'] = generate_questions(num_sets, sounds_per_set)
            st.session_state['current_question'] = 0
            st.session_state['score'] = 0
            st.session_state['answered'] = False
            st.rerun()

    # Main question loop
    if st.session_state['questions']:
        sounds = st.session_state['questions'][st.session_state['current_question']]
        possible_answers = get_all_matching_features(sounds)

        st.markdown(f"#### 🐳 **Identify ONE Common Feature.**")
        st.write(f"⚪ **Sounds:** [{', '.join(sounds)}]")

        user_answer = st.text_input("Write feature with +/- value (e.g., [+voice], [+nasal]):", value="")

        # if st.button("Check Answer"):
        #     cleaned_user = user_answer.strip().replace(" ", "")
        #     cleaned_valids = [f.strip().replace(" ", "") for f in possible_answers]

        #     if cleaned_user in cleaned_valids:
        #         st.success(f"✅ Correct! **{cleaned_user}** is one of the possible correct answers.")
        #         st.session_state['score'] += 1
        #     else:
        #         st.error(f"❌ Incorrect. The correct answers could be: {', '.join(possible_answers)}")

        #     st.session_state['answered'] = True
        
        if st.button("Check Answer"):
            user_inputs = [ans.strip().replace(" ", "") for ans in user_answer.split(",") if ans.strip()]
            cleaned_valids = [f.strip().replace(" ", "") for f in possible_answers]
        
            correct_answers = [ans for ans in user_inputs if ans in cleaned_valids]
            incorrect_answers = [ans for ans in user_inputs if ans not in cleaned_valids]
        
            if correct_answers and not incorrect_answers:
                st.success(f"✅ Correct! Your answer(s): {', '.join(correct_answers)}")
                st.info(f"All possible correct answers: {', '.join(possible_answers)}")
                st.session_state['score'] += len(set(correct_answers))
            elif correct_answers and incorrect_answers:
                st.warning(f"⚠️ Partially correct. You got {len(set(correct_answers))} right, "
                           f"but these were wrong: {', '.join(incorrect_answers)}")
                st.info(f"All possible correct answers: {', '.join(possible_answers)}")
                st.session_state['score'] += len(set(correct_answers))
            else:
                st.error(f"❌ Incorrect. None of your answers matched.")
                st.info(f"All possible correct answers: {', '.join(possible_answers)}")
                # score stays the same (no points added)
        
            # Always show current score after each check
            st.write(f"**Current score: {st.session_state['score']} / {len(st.session_state['questions'])}**")
        
            # Allow next or completion
            st.session_state['answered'] = True
        
        # Navigation & Completion
        if st.session_state['answered']:
            if st.session_state['current_question'] < len(st.session_state['questions']) - 1:
                if st.button("Next Question"):
                    st.session_state['current_question'] += 1
                    st.session_state['answered'] = False
                    st.rerun()
            else:
                st.success("🎉 **Practice Completed!**")
                st.write(f"**Your final score: {st.session_state['score']} / {len(st.session_state['questions'])}**")
        
                # 🎈 Balloons only if perfect score
                if st.session_state['score'] == len(st.session_state['questions']):
                    st.balloons()
        
                if st.button("Restart Practice"):
                    st.session_state['questions'] = []
                    st.session_state['current_question'] = 0
                    st.session_state['score'] = 0
                    st.session_state['answered'] = False
                    st.rerun()
