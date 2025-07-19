import streamlit as st

st.set_page_config(page_title="Final IPA Vowel Chart")

st.title("🌱 Final IPA Vowel Chart")

html_table = """
<style>
table {
    border-collapse: collapse;
    margin-top: 1rem;
    width: 600px;
}
td {
    border: none;
    padding: 0.8em;
    text-align: center;
    vertical-align: middle;
    font-size: 1.3em;
}
th {
    border: none;
    padding: 0.8em;
    font-size: 1.3em;
    font-weight: bold;
}
.orange {
    color: orange;
    font-weight: bold;
}
.rowlabel {
    text-align: center;
    vertical-align: middle;
    font-weight: bold;
}
/* Bottom-align only specific cells */
.bottomcell {
    vertical-align: bottom;
    height: 4em;
}
</style>

<table>
    <thead>
        <tr>
            <th style="text-align:center; vertical-align:middle;"></th>
            <th style="text-align:center; vertical-align:middle;">Front</th>
            <th style="text-align:center; vertical-align:middle;">(Central)</th>
            <th style="text-align:center; vertical-align:middle;">Back</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="rowlabel">High</td>
            <td>i<br>ɪ</td>
            <td></td>
            <td>u<br>ʊ</td>
        </tr>
        <tr>
            <td class="rowlabel">(Mid)</td>
            <td><span class="orange">e</span><br>ɛ</td>
            <td>ə<br>ʌ (ɜ)</td>
            <td><span class="orange">o</span><br>ɔ</td>
        </tr>
        <tr>
            <td class="rowlabel">Low</td>
            <td>æ</td>
            <td class="bottomcell"><span class="orange">a</span></td>
            <td class="bottomcell">ɑ / ɒ</td>
        </tr>
    </tbody>
</table>
"""

st.markdown(html_table, unsafe_allow_html=True)

st.markdown("""
#### 🚩 Notes: 

Vowel inventories vary significantly depending on English dialects.

1. /e/ and /o/ are considered either monophthongs or parts of diphthongs depending on the dialect — e.g., /eɪ/, /oʊ/.

2. /ɒ/ is a rounded version of /ɑ/.

3. /ɜ/ is a contextual variant — for example, it appears in r-colored vowels or after r-deletion in some dialects.
""")

