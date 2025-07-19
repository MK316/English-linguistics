import streamlit as st

st.set_page_config(page_title="Static IPA Vowel Chart")

st.title("🌳 Static IPA Vowel Chart")

# Define custom CSS for orange
html_table = """
<style>
table {
    border-collapse: collapse;
    margin-top: 1rem;
}
td, th {
    border: 1px solid #999;
    padding: 0.5em 0.8em;
    text-align: center;
    font-size: 1.3em;
}
thead th {
    background-color: #f2f2f2;
}
.orange {
    color: orange;
    font-weight: bold;
}
</style>

<table>
    <thead>
        <tr>
            <th></th>
            <th>front</th>
            <th>central</th>
            <th>back</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th>high</th>
            <td>i<br>ɪ</td>
            <td>ɨ</td>
            <td>u<br>ʊ</td>
        </tr>
        <tr>
            <th>mid</th>
            <td><span class="orange">e</span><br>ɛ</td>
            <td>ə</td>
            <td><span class="orange">o</span><br>ɔ</td>
        </tr>
        <tr>
            <th>low</th>
            <td>æ</td>
            <td><span class="orange">a</span></td>
            <td>ɑ</td>
        </tr>
    </tbody>
</table>
"""

st.markdown(html_table, unsafe_allow_html=True)
