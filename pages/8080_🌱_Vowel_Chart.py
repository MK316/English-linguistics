import streamlit as st

st.set_page_config(page_title="Clean IPA Vowel Chart")

st.title("🌱 Clean IPA Vowel Chart")

html_table = """
<style>
table {
    border-collapse: collapse;
    margin-top: 1rem;
    width: 600px;
}
td, th {
    border: none;
    padding: 0.8em;
    text-align: center;
    vertical-align: middle;
    font-size: 1.3em;
}
thead th {
    background-color: transparent;
    font-weight: bold;
}
.orange {
    color: orange;
    font-weight: bold;
}
.rowlabel {
    font-weight: bold;
    text-align: center;
    vertical-align: middle;
}
</style>

<table>
    <thead>
        <tr>
            <th></th>
            <th>Front</th>
            <th>Central</th>
            <th>Back</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="rowlabel">high</td>
            <td>i<br>ɪ</td>
            <td></td>
            <td>u<br>ʊ</td>
        </tr>
        <tr>
            <td class="rowlabel">mid</td>
            <td><span class="orange">e</span><br>ɛ</td>
            <td>ə</td>
            <td><span class="orange">o</span><br>ɔ</td>
        </tr>
        <tr>
            <td class="rowlabel">low</td>
            <td>æ</td>
            <td><span class="orange">a</span></td>
            <td>ɑ</td>
        </tr>
    </tbody>
</table>
"""

st.markdown(html_table, unsafe_allow_html=True)
