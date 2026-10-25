from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# pages/ 폴더 방식이면 페이지마다 둘 수 있습니다.
# st.navigation 방식이면 이 줄은 지우고 메인 파일에서만 설정하세요.
st.set_page_config(page_title="TCE mock exam", page_icon="📝", layout="wide")

# 앱 루트/assets/tce_phonotactics.html  (이 파일은 앱 루트/pages/ 안에 있음)
HTML_PATH = Path(__file__).resolve().parent.parent / "assets" / "tce_phonotactics.html"


@st.cache_data
def load_html(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


st.title("TCE mock exam")

tab1, tab2, tab3 = st.tabs(["phonotactics", "Stress", "Intonation"])

with tab1:
    # 피드백을 열면 내용이 길어지므로 높이를 넉넉히 주고 내부 스크롤을 켭니다.
    components.html(load_html(str(HTML_PATH)), height=1700, scrolling=True)

with tab2:
    st.info("Coming soon.")

with tab3:
    st.info("Coming soon.")
