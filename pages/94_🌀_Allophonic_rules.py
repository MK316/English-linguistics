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
                    {"text": "act",    "is_correct": True},
                    {"text": "packed", "is_correct": True},
                    {"text": "cap",    "is_correct": False},
                    {"text": "bag",    "is_correct": False},
                    {"text": "tap",    "is_correct": False},
                ],
                [
                    {"text": "kept",   "is_correct": True},
                    {"text": "fact",   "is_correct": True},
                    {"text": "doctor", "is_correct": True},  # /kt/
                    {"text": "back",   "is_correct": False},
                    {"text": "tack",   "is_correct": False},
                    {"text": "cave",   "is_correct": False},
                ],
                [
                    {"text": "script", "is_correct": True},
                    {"text": "abduct", "is_correct": True},
                    {"text": "uptake", "is_correct": True},
                    {"text": "cab",    "is_correct": False},
                    {"text": "sad",    "is_correct": False},
                    {"text": "buy",    "is_correct": False},
                ],
                [
                    {"text": "hotdog", "is_correct": True},  # /td/
                    {"text": "subpar", "is_correct": True},  # /bp/
                    {"text": "laptop", "is_correct": True},  # /pt/
                    {"text": "topic",  "is_correct": False},
                    {"text": "rapid",  "is_correct": False},
                    {"text": "paper",  "is_correct": False},
                ],
                [
                    {"text": "kept quiet", "is_correct": True},  # /tq/
                    {"text": "act fast",   "is_correct": True},  # /tf/
                    {"text": "apt choice", "is_correct": True},  # /tch/
                    {"text": "cap it",     "is_correct": False},
                    {"text": "bag it",     "is_correct": False},
                    {"text": "pop it",     "is_correct": False},
                ],
            ]
        },

    "R#6 — Final voiceless stop with glottalization":
        {
            "desc": "In many accents, syllable-final voiceless stops /p, t, k/ are accompanied by an overlapping glottal stop; final /t/ may surface as a pure glottal stop.",
            "sets": [
                [
                    {"text": "cat",  "is_correct": True},
                    {"text": "tip",  "is_correct": True},
                    {"text": "back", "is_correct": True},
                    {"text": "cab",  "is_correct": False},
                    {"text": "bad",  "is_correct": False},
                    {"text": "bag",  "is_correct": False},
                ],
                [
                    {"text": "kick", "is_correct": True},
                    {"text": "hat",  "is_correct": True},
                    {"text": "pack", "is_correct": True},
                    {"text": "had",  "is_correct": False},
                    {"text": "rag",  "is_correct": False},
                    {"text": "jog",  "is_correct": False},
                ],
                [
                    {"text": "fit",  "is_correct": True},
                    {"text": "cup",  "is_correct": True},
                    {"text": "cook", "is_correct": True},
                    {"text": "rid",  "is_correct": False},
                    {"text": "rob",  "is_correct": False},
                    {"text": "code", "is_correct": False},
                ],
                [
                    {"text": "pack", "is_correct": True},
                    {"text": "pit",  "is_correct": True},
                    {"text": "pick", "is_correct": True},
                    {"text": "pad",  "is_correct": False},
                    {"text": "bid",  "is_correct": False},
                    {"text": "pig",  "is_correct": False},
                ],
                [
                    {"text": "cat",  "is_correct": True},
                    {"text": "hat",  "is_correct": True},
                    {"text": "kick", "is_correct": True},
                    {"text": "mad",  "is_correct": False},
                    {"text": "rib",  "is_correct": False},
                    {"text": "log",  "is_correct": False},
                ],
            ]
        },

    "R#7 — /t/ → [ʔ] before alveolar nasal (same word)":
        {
            "desc": "In many accents, /t/ is replaced by a glottal stop before an alveolar nasal within the same word.",
            "sets": [
                [
                    {"text": "button",  "is_correct": True},
                    {"text": "kitten",  "is_correct": True},
                    {"text": "mountain","is_correct": True},
                    {"text": "captain", "is_correct": True},
                    {"text": "batman",  "is_correct": False},  # /t/ before /m/
                    {"text": "atlas",   "is_correct": False},
                ],
                [
                    {"text": "beaten",  "is_correct": True},
                    {"text": "written", "is_correct": True},
                    {"text": "curtain", "is_correct": True},
                    {"text": "mutton",  "is_correct": True},
                    {"text": "biting",  "is_correct": False},
                    {"text": "metal",   "is_correct": False},
                ],
                [
                    {"text": "rotten",  "is_correct": True},
                    {"text": "cotton",  "is_correct": True},
                    {"text": "eaten",   "is_correct": True},
                    {"text": "forgotten","is_correct": True},
                    {"text": "pattern", "is_correct": False},
                    {"text": "Latin",   "is_correct": False},
                ],
                [
                    {"text": "mountain","is_correct": True},
                    {"text": "curtain", "is_correct": True},
                    {"text": "Britain", "is_correct": True},
                    {"text": "written", "is_correct": True},
                    {"text": "detail",  "is_correct": False},
                    {"text": "attain",  "is_correct": False},
                ],
                [
                    {"text": "button",  "is_correct": True},
                    {"text": "kitten",  "is_correct": True},
                    {"text": "beaten",  "is_correct": True},
                    {"text": "mitten",  "is_correct": True},
                    {"text": "batman",  "is_correct": False},
                    {"text": "metal",   "is_correct": False},
                ],
            ]
        },

    "R#8 — Alveolars → dentals before dental consonants":
        {
            "desc": "Alveolar consonants become dental before dental consonants (place assimilation).",
            "sets": [
                [
                    {"text": "eighth", "is_correct": True},
                    {"text": "tenth",  "is_correct": True},
                    {"text": "wealth", "is_correct": True},
                    {"text": "at this","is_correct": True},
                    {"text": "nice thing","is_correct": True},
                    {"text": "eat soup","is_correct": False},
                ],
                [
                    {"text": "width",    "is_correct": True},
                    {"text": "at that",  "is_correct": True},
                    {"text": "said that","is_correct": True},
                    {"text": "with them","is_correct": True},
                    {"text": "add this", "is_correct": True},
                    {"text": "add on",   "is_correct": False},
                ],
                [
                    {"text": "tenth place","is_correct": True},
                    {"text": "eighth note","is_correct": True},
                    {"text": "at three",   "is_correct": True},
                    {"text": "bad thing",  "is_correct": True},
                    {"text": "red thread", "is_correct": True},
                    {"text": "eat there",  "is_correct": True},
                ],
                [
                    {"text": "at this",   "is_correct": True},
                    {"text": "at those",  "is_correct": True},
                    {"text": "said thanks","is_correct": True},
                    {"text": "meet them", "is_correct": True},
                    {"text": "get this",  "is_correct": True},
                    {"text": "eat apples","is_correct": False},
                ],
                [
                    {"text": "tenth",  "is_correct": True},
                    {"text": "wealth", "is_correct": True},
                    {"text": "width",  "is_correct": True},
                    {"text": "bath towel","is_correct": True},
                    {"text": "with those","is_correct": True},
                    {"text": "red apple",  "is_correct": False},
                ],
            ]
        },

    "R#9 — Velars more front before front vowels":
        {
            "desc": "Velar stops become more front before more front vowels (non-distinctive quality change).",
            "sets": [
                [
                    {"text": "key",   "is_correct": True},
                    {"text": "keep",  "is_correct": True},
                    {"text": "kid",   "is_correct": True},
                    {"text": "cool",  "is_correct": False},
                    {"text": "caught","is_correct": False},
                    {"text": "caw",   "is_correct": False},
                ],
                [
                    {"text": "cap",   "is_correct": True},
                    {"text": "kit",   "is_correct": True},
                    {"text": "kitchen","is_correct": True},
                    {"text": "cough", "is_correct": False},
                    {"text": "cord",  "is_correct": False},
                    {"text": "coo",   "is_correct": False},
                ],
                [
                    {"text": "keg",   "is_correct": True},
                    {"text": "cane",  "is_correct": True},
                    {"text": "candy", "is_correct": True},
                    {"text": "coal",  "is_correct": False},
                    {"text": "cone",  "is_correct": False},
                    {"text": "cool",  "is_correct": False},
                ],
                [
                    {"text": "kiss",  "is_correct": True},
                    {"text": "kidney","is_correct": True},
                    {"text": "cabin", "is_correct": True},
                    {"text": "coffee","is_correct": False},
                    {"text": "cob",   "is_correct": False},
                    {"text": "cog",   "is_correct": False},
                ],
                [
                    {"text": "caper", "is_correct": True},
                    {"text": "keeper","is_correct": True},
                    {"text": "kiddo", "is_correct": True},
                    {"text": "cocoa", "is_correct": False},
                    {"text": "caulk", "is_correct": False},
                    {"text": "coarse","is_correct": False},
                ],
            ]
        },

    "R#10 — Tap from alveolar stop or /n/ + stop between vowels (2nd unstressed)":
        {
            "desc": "Alveolar stops and alveolar nasal + stop sequences become a voiced tap between vowels when the second vowel is unstressed.",
            "sets": [
                [
                    {"text": "painter", "is_correct": True},
                    {"text": "splinter","is_correct": True},
                    {"text": "winter",  "is_correct": True},
                    {"text": "pantry",  "is_correct": False},
                    {"text": "enter",   "is_correct": True},
                    {"text": "antenna", "is_correct": False},
                ],
                [
                    {"text": "center",  "is_correct": True},
                    {"text": "dental",  "is_correct": True},
                    {"text": "planetary","is_correct": False},
                    {"text": "monetary","is_correct": False},
                    {"text": "continental","is_correct": True},
                    {"text": "intern",  "is_correct": False},
                ],
                [
                    {"text": "wintering","is_correct": True},
                    {"text": "painterly","is_correct": True},
                    {"text": "splintering","is_correct": True},
                    {"text": "pantryman","is_correct": False},
                    {"text": "entering","is_correct": True},
                    {"text": "intense", "is_correct": False},
                ],
                [
                    {"text": "Santa Ana","is_correct": True},
                    {"text": "center of", "is_correct": True},
                    {"text": "winter is", "is_correct": True},
                    {"text": "pantry of", "is_correct": False},
                    {"text": "intend it", "is_correct": False},
                    {"text": "dinner is", "is_correct": False},
                ],
                [
                    {"text": "painter", "is_correct": True},
                    {"text": "winter",  "is_correct": True},
                    {"text": "enter",   "is_correct": True},
                    {"text": "country", "is_correct": False},
                    {"text": "interest","is_correct": False},
                    {"text": "panther", "is_correct": False},
                ],
            ]
        },

    "R#11 — Alveolar stop deletion/reduction between two consonants":
        {
            "desc": "Alveolar stops are reduced or omitted when between two consonants.",
            "sets": [
                [
                    {"text": "most people", "is_correct": True},
                    {"text": "best game",   "is_correct": True},
                    {"text": "west bank",   "is_correct": True},
                    {"text": "best actor",  "is_correct": False},
                    {"text": "lost it",     "is_correct": False},
                    {"text": "post office", "is_correct": False},
                ],
                [
                    {"text": "first prize", "is_correct": True},
                    {"text": "last man",    "is_correct": True},
                    {"text": "guest book",  "is_correct": True},
                    {"text": "best album",  "is_correct": False},  # /t/ + vowel
                    {"text": "past event",  "is_correct": False},
                    {"text": "post area",   "is_correct": False},
                ],
                [
                    {"text": "cold cuts",   "is_correct": True},
                    {"text": "wild card",   "is_correct": True},
                    {"text": "old boy",     "is_correct": True},
                    {"text": "old apple",   "is_correct": False},
                    {"text": "lost item",   "is_correct": False},
                    {"text": "most orange","is_correct": False},
                ],
                [
                    {"text": "next train",  "is_correct": True},
                    {"text": "last straw",  "is_correct": True},
                    {"text": "first time",  "is_correct": True},
                    {"text": "best idea",   "is_correct": False},
                    {"text": "past era",    "is_correct": False},
                    {"text": "lost art",    "is_correct": False},
                ],
                [
                    {"text": "frost bite",  "is_correct": True},
                    {"text": "guest speaker","is_correct": True},
                    {"text": "act plan",    "is_correct": True},
                    {"text": "post office", "is_correct": False},
                    {"text": "lost apple",  "is_correct": False},
                    {"text": "best artist", "is_correct": False},
                ],
            ]
        },

    "R#12 — Epenthetic voiceless stop after nasal + before voiceless fricative":
        {
            "desc": "A homorganic voiceless stop may occur after a nasal before a voiceless fricative when followed by an unstressed vowel in the same word.",
            "sets": [
                [
                    {"text": "something", "is_correct": True},  # [mpθ] for many
                    {"text": "youngster", "is_correct": True},  # [ŋk]
                    {"text": "prince",    "is_correct": True},  # [nts]
                    {"text": "sunfish",   "is_correct": False},
                    {"text": "answer",    "is_correct": False},
                    {"text": "sandstorm", "is_correct": False},
                ],
                [
                    {"text": "hamster",  "is_correct": True},   # [mpst]
                    {"text": "minstrel", "is_correct": True},   # often [mpstr-] like cluster
                    {"text": "prints",   "is_correct": True},   # homorganic stop visible in spelling
                    {"text": "pencil",   "is_correct": False},
                    {"text": "sunset",   "is_correct": False},
                    {"text": "insight",  "is_correct": False},
                ],
                [
                    {"text": "princely", "is_correct": True},
                    {"text": "youngster","is_correct": True},
                    {"text": "something","is_correct": True},
                    {"text": "sense",    "is_correct": False},
                    {"text": "insist",   "is_correct": False},
                    {"text": "unsaid",   "is_correct": False},
                ],
                [
                    {"text": "prince",   "is_correct": True},
                    {"text": "hamster",  "is_correct": True},
                    {"text": "youngster","is_correct": True},
                    {"text": "monsoon",  "is_correct": False},
                    {"text": "censor",   "is_correct": False},
                    {"text": "sunscreen","is_correct": False},
                ],
                [
                    {"text": "something","is_correct": True},
                    {"text": "princely", "is_correct": True},
                    {"text": "youngsters","is_correct": True},
                    {"text": "insult",   "is_correct": False},
                    {"text": "censoring","is_correct": False},
                    {"text": "sunfish",  "is_correct": False},
                ],
            ]
        },

    "R#13 — Shortening before identical consonant (no deletion)":
        {
            "desc": "A consonant is shortened when it appears before an identical consonant; there is no deletion.",
            "sets": [
                [
                    {"text": "big game",   "is_correct": True},
                    {"text": "white teeth","is_correct": True},
                    {"text": "bookkeeper","is_correct": True},
                    {"text": "big cat",    "is_correct": False},
                    {"text": "white sun",  "is_correct": False},
                    {"text": "back door",  "is_correct": False},
                ],
                [
                    {"text": "hip pocket", "is_correct": True},
                    {"text": "back cover", "is_correct": True},
                    {"text": "black coat", "is_correct": True},
                    {"text": "black car",  "is_correct": False},
                    {"text": "big cup",    "is_correct": False},
                    {"text": "hot coffee", "is_correct": False},
                ],
                [
                    {"text": "red dress",  "is_correct": True},
                    {"text": "bad debt",   "is_correct": True},
                    {"text": "good day",   "is_correct": True},
                    {"text": "red door",   "is_correct": False},
                    {"text": "bad dog",    "is_correct": False},
                    {"text": "good deal",  "is_correct": False},
                ],
                [
                    {"text": "short time", "is_correct": True},
                    {"text": "great team", "is_correct": True},
                    {"text": "nice soup",  "is_correct": False},
                    {"text": "sweet tea",  "is_correct": False},
                    {"text": "late train", "is_correct": False},
                    {"text": "hot tea",    "is_correct": False},
                ],
                [
                    {"text": "quick call", "is_correct": True},
                    {"text": "big game",   "is_correct": True},
                    {"text": "white teeth","is_correct": True},
                    {"text": "quick car",  "is_correct": False},
                    {"text": "big gate",   "is_correct": False},
                    {"text": "white table","is_correct": False},
                ],
            ]
        },

    "R#14 — Partial devoicing of word-final or pre-voiceless obstruents":
        {
            "desc": "Voiced obstruents are voiced through only a small part of their articulation at utterance end or before a voiceless sound (partial devoicing).",
            "sets": [
                [
                    {"text": "prove",        "is_correct": True},
                    {"text": "add two",      "is_correct": True},
                    {"text": "leave town",   "is_correct": True},
                    {"text": "prove it",     "is_correct": False},
                    {"text": "add a number", "is_correct": False},
                    {"text": "move over",    "is_correct": False},
                ],
                [
                    {"text": "smooth",       "is_correct": True},
                    {"text": "choose",       "is_correct": True},
                    {"text": "rogue",        "is_correct": True},
                    {"text": "prove it",     "is_correct": False},
                    {"text": "leave it",     "is_correct": False},
                    {"text": "add it",       "is_correct": False},
                ],
                [
                    {"text": "try to improve","is_correct": True},
                    {"text": "add two",       "is_correct": True},
                    {"text": "love Kate",     "is_correct": True},
                    {"text": "prove it",      "is_correct": False},
                    {"text": "love Anna",     "is_correct": False},
                    {"text": "save it",       "is_correct": False},
                ],
                [
                    {"text": "move past", "is_correct": True},
                    {"text": "leave Pete","is_correct": True},
                    {"text": "save Paul", "is_correct": True},
                    {"text": "move in",   "is_correct": False},
                    {"text": "leave early","is_correct": False},
                    {"text": "save it",   "is_correct": False},
                ],
                [
                    {"text": "prove",      "is_correct": True},
                    {"text": "smooth",     "is_correct": True},
                    {"text": "choose",     "is_correct": True},
                    {"text": "prove it",   "is_correct": False},
                    {"text": "smooth it",  "is_correct": False},
                    {"text": "choose it",  "is_correct": False},
                ],
            ]
        },
}

# -----------------------
# Helpers for state & UI
# -----------------------
def init_state():
    if "rule_select" not in st.session_state:
        st.session_state.rule_select = list(RULES.keys())[0]
    if "set_idx" not in st.session_state:
        st.session_state.set_idx = {k: 0 for k in RULES.keys()}
    if "nonce" not in st.session_state:
        st.session_state.nonce = 0

def next_set(rule_key: str):
    st.session_state.set_idx[rule_key] = (st.session_state.set_idx[rule_key] + 1) % len(RULES[rule_key]["sets"])
    st.session_state.nonce += 1  # force new checkbox keys

def reset_set(rule_key: str):
    st.session_state.set_idx[rule_key] = 0
    st.session_state.nonce += 1

def evaluate_selection(items, selected_flags):
    correct_flags = [it["is_correct"] for it in items]
    perfect = all(s == c for s, c in zip(selected_flags, correct_flags))
    must_select = [it["text"] for i, it in enumerate(items) if correct_flags[i] and not selected_flags[i]]
    should_uncheck = [it["text"] for i, it in enumerate(items) if not correct_flags[i] and selected_flags[i]]
    return perfect, must_select, should_uncheck


# -----------------------
# App UI
# -----------------------
init_state()

st.markdown("### Select a rule")
rule_key = st.selectbox("Rule", list(RULES.keys()), index=list(RULES.keys()).index(st.session_state.rule_select))
if rule_key != st.session_state.rule_select:
    st.session_state.rule_select = rule_key
    reset_set(rule_key)

rule = RULES[rule_key]
set_idx = st.session_state.set_idx[rule_key]
items = rule["sets"][set_idx]

st.markdown(f"**Description:** {rule['desc']}")
st.caption(f"Set {set_idx + 1} of {len(rule['sets'])}")

st.divider()
st.markdown("**Select all items that exemplify the rule:**")

# Render checkboxes (stable unique keys using nonce)
selected = []
for i, it in enumerate(items):
    key = f"chk_{rule_key}_{set_idx}_{i}_{st.session_state.nonce}"
    selected.append(st.checkbox(it["text"], key=key))

st.divider()
colA, colB = st.columns([1,1])

with colA:
    if st.button("Submit"):
        perfect, must_select, should_uncheck = evaluate_selection(items, selected)
        if perfect:
            st.success("🎉 Well done!")
        else:
            st.error("Not quite. Review the feedback below.")
            if must_select:
                st.write("**You missed these correct items:**")
                st.write(", ".join(must_select))
            if should_uncheck:
                st.write("**These should not be selected:**")
                st.write(", ".join(should_uncheck))

with colB:
    if st.button("Show me another set of words"):
        next_set(rule_key)     # updates session_state
        # no rerun call needed


st.caption("Tip: Use the dropdown to switch to another rule. Each rule has 5 different sets.")
