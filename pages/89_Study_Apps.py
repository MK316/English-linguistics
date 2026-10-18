import csv
import io
import json
import urllib.request
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# pages/ 폴더 방식이면 페이지마다 둘 수 있습니다.
# st.navigation 방식이면 이 줄은 지우고 메인 파일에서만 설정하세요.
st.set_page_config(page_title="Voca Practice", page_icon="🧩", layout="wide")

ASSETS = Path(__file__).resolve().parent.parent / "assets"
HTML_PATH = ASSETS / "voca_practice.html"
LOCAL_CSV = ASSETS / "md33.csv"   # 있으면 이 파일을 우선 사용
DRIVE_ID = "135Vhhudwg0Jv8Rixvam37n1Qss43NJd6"
DRIVE_URL = f"https://drive.google.com/uc?export=download&id={DRIVE_ID}"
COLUMNS = ["Initial", "SID", "Word", "POS", "WME", "WMK", "WIC", "WICK", "SEM-REL"]


def embed(html: str, height: int) -> None:
    """최신 Streamlit(st.iframe 있음)은 내용 높이에 맞춰 자동 조절, 이전 버전은 components.html 사용."""
    if hasattr(st, "iframe"):
        st.iframe(html, height="content")
    else:
        components.html(html, height=height, scrolling=True)


def parse_csv(text: str) -> list[dict]:
    reader = csv.DictReader(io.StringIO(text.lstrip("﻿")))
    reader.fieldnames = [(f or "").strip() for f in reader.fieldnames or []]
    missing = [c for c in COLUMNS if c not in reader.fieldnames]
    if missing:
        raise ValueError(f"CSV is missing column(s): {', '.join(missing)}")
    rows = []
    for r in reader:
        row = {c: (r.get(c) or "").strip() for c in COLUMNS}
        if row["Word"]:
            rows.append(row)
    return rows


@st.cache_data
def load_local(path: str, mtime: float) -> list[dict]:
    return parse_csv(Path(path).read_text(encoding="utf-8-sig"))


@st.cache_data(ttl=3600)
def load_drive() -> list[dict]:
    req = urllib.request.Request(DRIVE_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        text = resp.read().decode("utf-8-sig")
    if text.lstrip().startswith("<"):
        raise ValueError("Google Drive returned a web page instead of the CSV. "
                         "Share the file as 'Anyone with the link'.")
    return parse_csv(text)


@st.cache_data
def load_html(path: str, mtime: float) -> str:
    return Path(path).read_text(encoding="utf-8")


try:
    if LOCAL_CSV.exists():
        rows = load_local(str(LOCAL_CSV), LOCAL_CSV.stat().st_mtime)
    else:
        rows = load_drive()
except Exception as e:
    st.error(f"Could not load the MD-33 data: {e}")
    st.stop()

html = load_html(str(HTML_PATH), HTML_PATH.stat().st_mtime).replace(
    "/*__DATA__*/[]", json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")
)
embed(html, 900)
