#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import streamlit as st

pg = st.navigation(
    [
    st.Page("list_summary_menu.py"),
    st.Page("current_list.py"),
    st.Page("module_summary_menu.py"),
    st.Page("module_edit_menu.py"),
    st.Page("module_from_unique_list.py")
    ],
    position="hidden"
    )
pg.run()