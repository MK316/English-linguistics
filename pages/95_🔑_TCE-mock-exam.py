from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# pages/ 폴더 방식이면 페이지마다 둘 수 있습니다.
# st.navigation 방식이면 이 줄은 지우고 메인 파일에서만 설정하세요.
st.set_page_config(page_title="TCE mock exam", page_icon="📝", layout="wide")

# 앱 루트/assets/  (이 파일은 앱 루트/pages/ 안에 있음)
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
PHONOTACTICS_HTML = ASSETS_DIR / "tce_phonotactics.html"
STRESS_INTONATION_HTML = ASSETS_DIR / "tce-stress-mock-exam.html"


@st.cache_data
def load_html(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def show_exam(path: Path) -> None:
    if not path.exists():
        st.error(f"File not found: assets/{path.name}")
        return
    # 피드백을 열면 내용이 길어지므로 높이를 넉넉히 주고 내부 스크롤을 켭니다.
    components.html(load_html(str(path)), height=1700, scrolling=True)


st.title("TCE mock exam")

tab1, tab2, tab3 = st.tabs(["phonotactics", "Stress & intonation", "TBA"])

with tab1:
    show_exam(PHONOTACTICS_HTML)

with tab2:
    show_exam(STRESS_INTONATION_HTML)

with tab3:
    st.info("Coming soon.")
