import json
import random
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# pages/ 폴더 방식이면 페이지마다 둘 수 있습니다.
# st.navigation 방식이면 이 줄은 지우고 메인 파일에서만 설정하세요.
st.set_page_config(page_title="99 Phonology Term Practice", page_icon="📚", layout="wide")

ASSETS = Path(__file__).resolve().parent.parent / "assets"
PLAYER_PATH = ASSETS / "tce_terms_player.html"   # 플래시카드·퀴즈 화면 (99개 용어 내장)
TERMS_PATH = ASSETS / "tce_terms.json"           # 용어 번호와 이름 목록
RANGES = [(1, 20), (21, 40), (41, 60), (61, 80), (81, 99)]


def embed(html: str, height: int) -> None:
    """최신 Streamlit(st.iframe 있음)은 내용 높이에 맞춰 자동 조절, 이전 버전은 components.html 사용."""
    if hasattr(st, "iframe"):
        st.iframe(html, height="content")
    else:
        components.html(html, height=height, scrolling=True)


@st.cache_data
def load_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


TERMS = json.loads(load_text(str(TERMS_PATH)))

# ---- 선택 상태: 범위를 바꿔도 유지되도록 별도 집합에 저장 ----
ss = st.session_state
ss.setdefault("term_sel", set(range(1, 21)))  # 처음에는 1–20번 선택
ss.setdefault("term_ver", 0)                  # 전체 선택/해제 시 체크박스를 새로 그리기 위한 번호
ss.setdefault("term_seed", 0)


def toggle(n: int, widget_key: str) -> None:
    if ss[widget_key]:
        ss.term_sel.add(n)
    else:
        ss.term_sel.discard(n)


def set_many(nums, value: bool) -> None:
    if value:
        ss.term_sel.update(nums)
    else:
        ss.term_sel.difference_update(nums)
    ss.term_ver += 1


def reshuffle() -> None:
    ss.term_seed += 1


st.title("Phonology Key Terminology")
tab1, tab2, tab3 = st.tabs(["🐾 Select terms", "🐾 Flashcards", "🐾 Quiz"])

with tab1:
    idx = st.selectbox(
        "Term set",
        range(len(RANGES)),
        format_func=lambda i: f"Terms {RANGES[i][0]}–{RANGES[i][1]}",
    )
    lo, hi = RANGES[idx]
    in_range = [t for t in TERMS if lo <= t["n"] <= hi]
    nums = [t["n"] for t in in_range]

    b1, b2, b3, _ = st.columns([1, 1, 1.3, 3])
    b1.button("Select all", on_click=set_many, args=(nums, True), use_container_width=True)
    b2.button("Clear", on_click=set_many, args=(nums, False), use_container_width=True)
    b3.button("Clear all sets", on_click=set_many, args=([t["n"] for t in TERMS], False),
              use_container_width=True)

    cols = st.columns(3)
    for i, t in enumerate(in_range):
        k = f"term_cb_{t['n']}_{ss.term_ver}"
        cols[i % 3].checkbox(f"{t['n']}. {t['label']}", value=t["n"] in ss.term_sel,
                             key=k, on_change=toggle, args=(t["n"], k))

    st.divider()
    s1, s2 = st.columns([1, 3])
    shuffle = s1.toggle("Shuffle order", key="term_shuffle")
    if shuffle:
        s2.button("Reshuffle", on_click=reshuffle)
    st.caption(f"{len(ss.term_sel)} term(s) selected across all sets. "
               "Open the Flashcards or Quiz tab to practise them.")

# ---- 선택한 용어로 덱 만들기 ----
order = sorted(ss.term_sel)
if ss.get("term_shuffle"):
    random.Random(ss.term_seed).shuffle(order)


def player(mode: str, height: int) -> None:
    html = load_text(str(PLAYER_PATH)).replace(
        '/*__CONFIG__*/{"mode": "flash", "order": []}',
        json.dumps({"mode": mode, "order": order}),
    )
    embed(html, height)


with tab2:
    player("flash", 720)

with tab3:
    player("quiz", 820)
