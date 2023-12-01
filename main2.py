import streamlit as st

# initialise a boolean attr in session state

if "button" not in st.session_state:
    st.session_state.button = False

# write a function for toggle functionality


def toggle():
    if st.session_state.button:
        st.session_state.button = False
    else:
        st.session_state.button = True


# create the button
st.button("Button", on_click=toggle)

with st.expander('expander', expanded=st.session_state.button):
    st.write('Hello!')
