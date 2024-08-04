import streamlit as st
from collections import deque

if not hasattr(st, "cv_count"):
    st.cv_count = deque([0])

def increment_cv_count():
    st.cv_count[0] += 1

def get_cv_count():
    return st.cv_count[0]