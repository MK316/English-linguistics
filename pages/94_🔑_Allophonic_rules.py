import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# pages/ 폴더 방식이면 페이지마다 둘 수 있습니다.
# st.navigation 방식이면 이 줄은 지우고 메인 파일에서만 설정하세요.
st.set_page_config(page_title="Allophonic Rules", page_icon="🔤", layout="centered")

ASSETS = Path(__file__).resolve().parent.parent / "assets"
HTML_PATH = ASSETS / "allophonic_rules.html"            # 화면
CSV_PATH = ASSETS / "allophonic_rules_dataset.csv"      # 데이터 (이 파일만 고치면 앱에 반영됨)


def embed(html: str, height: int) -> None:
    """최신 Streamlit(st.iframe 있음)은 내용 높이에 맞춰 자동 조절, 이전 버전은 components.html 사용."""
    if hasattr(st, "iframe"):
        st.iframe(html, height="content")
    else:
        components.html(html, height=height, scrolling=True)


@st.cache_data
def load_text(path: str, mtime: float) -> str:
    # mtime을 인자로 넣어 두면 파일을 고칠 때마다 캐시가 자동으로 새로 고쳐집니다.
    return Path(path).read_text(encoding="utf-8-sig")


html = load_text(str(HTML_PATH), HTML_PATH.stat().st_mtime)
csv_text = load_text(str(CSV_PATH), CSV_PATH.stat().st_mtime)
html = html.replace('/*__CSV__*/""', json.dumps(csv_text, ensure_ascii=False))

embed(html, 900)
