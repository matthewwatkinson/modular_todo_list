#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import streamlit as st

pg = st.navigation([st.Page("current_list.py"), st.Page("module_summary_menu.py"), st.Page("module_edit_menu.py")])
pg.run()