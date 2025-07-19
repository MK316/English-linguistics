import streamlit as st

st.set_page_config(page_title="Static IPA Vowel Chart")

st.title("💐 Static IPA Vowel Chart")

# HTML table for static vowel chart
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
            <td>e<br>ɛ</td>
            <td>ə</td>
            <td>o<br>ɔ</td>
        </tr>
        <tr>
            <th>low</th>
            <td>æ</td>
            <td>a</td>
            <td>ɑ</td>
        </tr>
    </tbody>
</table>
"""

st.markdown(html_table, unsafe_allow_html=True)
