import streamlit as st

st.set_page_config(page_title="English Allophonic Rules — Quiz", page_icon="🔤", layout="centered")

st.title("English Allophonic Rules — Practice Quiz")
st.caption("Select a rule, choose all words that illustrate it, then submit. Use “Show me another set of words” to get new items.")

# -----------------------
# Data model
# -----------------------
# Each rule has 5 sets; each set is a list of dicts: {"text": "...", "is_correct": True/False}
RULES = {
    "R#1 — Aspirated voiceless stops (except after /s/)":
        {
            "desc": "Voiceless stops /p, t, k/ are aspirated when they are stressed, except when they follow /s/.",
            "sets": [
                [ # Set 1
                    {"text": "pie",  "is_correct": True},
                    {"text": "tie",  "is_correct": True},
                    {"text": "kite", "is_correct": True},
                    {"text": "spy",  "is_correct": False},
                    {"text": "sty",  "is_correct": False},
                    {"text": "sky",  "is_correct": False},
                ],
                [ # Set 2
                    {"text": "pool",  "is_correct": True},
                    {"text": "tool",  "is_correct": True},
                    {"text": "cool",  "is_correct": True},
                    {"text": "school","is_correct": False},
                    {"text": "stool", "is_correct": False},
                    {"text": "spool", "is_correct": False},
                ],
                [ # Set 3
                    {"text": "panda",  "is_correct": True},
                    {"text": "taco",   "is_correct": True},
                    {"text": "cabin",  "is_correct": True},
                    {"text": "spray",  "is_correct": False},
                    {"text": "stare",  "is_correct": False},
                    {"text": "scare",  "is_correct": False},
                ],
                [ # Set 4
                    {"text": "pie",    "is_correct": True},
                    {"text": "port",   "is_correct": True},
                    {"text": "team",   "is_correct": True},
                    {"text": "spy",    "is_correct": False},
                    {"text": "sport",  "is_correct": False},
                    {"text": "steam",  "is_correct": False},
                ],
                [ # Set 5
                    {"text": "cream",  "is_correct": True},   # aspiration persists (not an /s/ cluster)
                    {"text": "tall",   "is_correct": True},
                    {"text": "king",   "is_correct": True},
                    {"text": "screen", "is_correct": False},  # /s/ + stop
                    {"text": "stall",  "is_correct": False},  # /s/ + stop
                    {"text": "skit",   "is_correct": False},  # /s/ + stop
                ],
            ]
        },

    "R#2a — Syllabic nasals after obstruent (word-final)":
        {
            "desc": "Nasals /m, n/ are syllabic at the end of a word when immediately after an obstruent.",
            "sets": [
                [
                    {"text": "leaden", "is_correct": True},
                    {"text": "chasm",  "is_correct": True},
                    {"text": "film",   "is_correct": False},
                    {"text": "kiln",   "is_correct": False},
                    {"text": "open",   "is_correct": False},
                    {"text": "lemon",  "is_correct": False},
                ],
                [
                    {"text": "hidden", "is_correct": True},
                    {"text": "sadden", "is_correct": True},
                    {"text": "seven",  "is_correct": True},   # counting style often syllabic final /n/
                    {"text": "cabin",  "is_correct": False},
                    {"text": "siren",  "is_correct": False},
                    {"text": "oven",   "is_correct": False},
                ],
                [
                    {"text": "prism",  "is_correct": True},
                    {"text": "chasm",  "is_correct": True},
                    {"text": "prison", "is_correct": True},
                    {"text": "salmon", "is_correct": False},
                    {"text": "human",  "is_correct": False},
                    {"text": "wagon",  "is_correct": False},
                ],
                [
                    {"text": "leaden", "is_correct": True},
                    {"text": "burden", "is_correct": True},
                    {"text": "happen", "is_correct": False},
                    {"text": "garden", "is_correct": False},
                    {"text": "autumn", "is_correct": False},
                    {"text": "woman",  "is_correct": False},
                ],
                [
                    {"text": "chasm",  "is_correct": True},
                    {"text": "rhythm", "is_correct": True},
                    {"text": "column", "is_correct": False},
                    {"text": "basin",  "is_correct": False},
                    {"text": "siren",  "is_correct": False},
                    {"text": "cumin",  "is_correct": False},
                ],
            ]
        },

    "R#2b — Syllabic liquids /l, r/ after consonant (word-final)":
        {
            "desc": "Liquids /l, r/ are syllabic at the end of a word when immediately after a consonant.",
            "sets": [
                [
                    {"text": "little", "is_correct": True},
                    {"text": "bottle", "is_correct": True},
                    {"text": "razor",  "is_correct": True},  # vocalic r
                    {"text": "real",   "is_correct": False},
                    {"text": "allow",  "is_correct": False},
                    {"text": "lily",   "is_correct": False},
                ],
                [
                    {"text": "whistle", "is_correct": True},
                    {"text": "paddle",  "is_correct": True},
                    {"text": "hammer",  "is_correct": True},
                    {"text": "yellow",  "is_correct": False},
                    {"text": "early",   "is_correct": False},
                    {"text": "ruler",   "is_correct": False},
                ],
                [
                    {"text": "kennel",  "is_correct": True},
                    {"text": "channel", "is_correct": True},
                    {"text": "tailor",  "is_correct": True},
                    {"text": "royal",   "is_correct": False},
                    {"text": "alloy",   "is_correct": False},
                    {"text": "oral",    "is_correct": False},
                ],
                [
                    {"text": "barrel",  "is_correct": True},
                    {"text": "snarl",   "is_correct": True},
                    {"text": "solder",  "is_correct": False},
                    {"text": "solar",   "is_correct": False},
                    {"text": "rely",    "is_correct": False},
                    {"text": "relay",   "is_correct": False},
                ],
                [
                    {"text": "little",  "is_correct": True},
                    {"text": "bottle",  "is_correct": True},
                    {"text": "tailor",  "is_correct": True},
                    {"text": "lunar",   "is_correct": False},
                    {"text": "rural",   "is_correct": False},
                    {"text": "real",    "is_correct": False},
                ],
            ]
        },

    "R#3 — Velarized (dark) /l/ in coda or syllabic /l/":
        {
            "desc": "The lateral /l/ is velarized after a vowel or before a consonant at the end of a word (coda) or when /l/ is syllabic.",
            "sets": [
                [
                    {"text": "feel", "is_correct": True},
                    {"text": "milk", "is_correct": True},
                    {"text": "silk", "is_correct": True},
                    {"text": "leaf", "is_correct": False},
                    {"text": "lady", "is_correct": False},
                    {"text": "lily", "is_correct": False},
                ],
                [
                    {"text": "full",  "is_correct": True},
                    {"text": "cold",  "is_correct": True},
                    {"text": "bold",  "is_correct": True},
                    {"text": "light", "is_correct": False},
                    {"text": "allow", "is_correct": False},
                    {"text": "loyal", "is_correct": False},
                ],
                [
                    {"text": "pearl", "is_correct": True},
                    {"text": "paddle","is_correct": True},  # syllabic /l/ possible
                    {"text": "whistle","is_correct": True},
                    {"text": "leafy", "is_correct": False},
                    {"text": "alone", "is_correct": False},
                    {"text": "lunar", "is_correct": False},
                ],
                [
                    {"text": "meal", "is_correct": True},
                    {"text": "cool", "is_correct": True},
                    {"text": "coal", "is_correct": True},
                    {"text": "lean", "is_correct": False},
                    {"text": "laser","is_correct": False},
                    {"text": "level","is_correct": False},  # first /l/ onset light
                ],
                [
                    {"text": "real", "is_correct": True},
                    {"text": "dull", "is_correct": True},
                    {"text": "pale", "is_correct": True},
                    {"text": "lute", "is_correct": False},
                    {"text": "leaf", "is_correct": False},
                    {"text": "lilt", "is_correct": False},
                ],
            ]
        },

    "R#4 — Alveolar stop → tap between vowels (2nd unstressed)":
        {
            "desc": "Alveolar stops /t, d/ become a voiced tap between vowels when the second vowel is unstressed.",
            "sets": [
                [
                    {"text": "butter", "is_correct": True},
                    {"text": "city",   "is_correct": True},
                    {"text": "water",  "is_correct": True},
                    {"text": "attack", "is_correct": False},
                    {"text": "detail", "is_correct": False},
                    {"text": "hotel",  "is_correct": False},
                ],
                [
                    {"text": "rider",  "is_correct": True},
                    {"text": "writer", "is_correct": True},
                    {"text": "witty",  "is_correct": True},
                    {"text": "retire", "is_correct": False},
                    {"text": "Italian","is_correct": False},
                    {"text": "routine","is_correct": False},
                ],
                [
                    {"text": "cater",  "is_correct": True},
                    {"text": "data",   "is_correct": True},
                    {"text": "ladder", "is_correct": True},
                    {"text": "rotate", "is_correct": False},
                    {"text": "edit",   "is_correct": False},
                    {"text": "attain", "is_correct": False},
                ],
                [
                    {"text": "credit", "is_correct": True},
                    {"text": "editor", "is_correct": True},
                    {"text": "petal",  "is_correct": True},
                    {"text": "today",  "is_correct": False},
                    {"text": "canoe",  "is_correct": False},
                    {"text": "detail", "is_correct": False},
                ],
                [
                    {"text": "beauty", "is_correct": True},
                    {"text": "duty",   "is_correct": True},
                    {"text": "petite", "is_correct": True},
                    {"text": "attack", "is_correct": False},
                    {"text": "retake", "is_correct": False},
                    {"text": "debate", "is_correct": False},
                ],
            ]
        },

    "R#5 — Unreleased stop before another stop":
        {
            "desc": "Consecutive stops overlap; a stop is often unreleased when it occurs immediately before another stop.",
            "sets": [
                [
                    {"text": "apt",    "is_correct": True},
