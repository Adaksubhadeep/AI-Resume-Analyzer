import streamlit as st

def render_custom_css():
    st.markdown(
        """
        <style>
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 13px;
            font-weight: 600;
            margin: 3px;
        }
        .badge-matched {
            background-color: #DEF7EC;
            color: #03543F;
            border: 1px solid #84E1BC;
        }
        .badge-missing {
            background-color: #FDE8E8;
            color: #9B1C1C;
            border: 1px solid #F8B4B4;
        }
        .badge-partial {
            background-color: #FEF08A;
            color: #713F12;
            border: 1px solid #FDE047;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def display_badges(items, badge_type):
    if not items:
        st.write("None identified.")
        return
    html = "".join([f'<span class="badge badge-{badge_type}">{item}</span>' for item in items])
    st.markdown(html, unsafe_allow_html=True)