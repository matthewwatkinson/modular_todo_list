#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import json
#from helper import *
from dictionary_scratchpad import *

hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.markdown(
    """
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
    """, 
    unsafe_allow_html=True
)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

json_dictionary = data_load()

#but only use json if we don't have a session state
if "json_data" not in st.session_state:
    st.session_state["json_data"] = json_dictionary
    # special case that this is first time to ever use app and there is no current list
    if not current_and_populated():
        # add a basic list
        st.session_state["json_data"]["existing_lists"]["New list"] = {"tier_0_list": list_builder("New list", ["New item 1"], 0)}
        st.session_state["json_data"]["current_list"] = "New list"
    else:
    # need to initialise the true/false state for each item in just the current list, if we have a current_list with items
        current_key = st.session_state["json_data"]["current_list"]
        for sub_dict in st.session_state["json_data"]["existing_lists"][current_key]:
            for key, value in st.session_state["json_data"]["existing_lists"][current_key][sub_dict]["content_list"].items():
                ref_key = widget_key_maker("cb", current_key, key)
                st.session_state[ref_key] = value

else:
    # otherwise we need to save the latest state to json
    data_save()

current_key = st.session_state["json_data"]["current_list"]

page_header()
            
st.write(f"#### Save '{current_key}' unique list as new module")

#text input for module name
proposed_module_name = st.text_input(label=" ", label_visibility="collapsed", placeholder="input new module name", key="list_to_mod_text")

# checkboxes, pre-checked, for each item

target_dict_keys = st.session_state["json_data"]["existing_lists"][current_key]["tier_0_list"]["content_list"].keys()

with st.container():
    final_item_list = [item for item in target_dict_keys if st.checkbox(item, value=True)] 

# draw the buttons

with st.container(border=False, horizontal=True, key="settings_submit_container"):
    saved = st.button("Save and return", type="primary")
    canceled = st.button("Cancel")

# save and return checks the list name for dupes, shows any warnings, saves the list, back to current
if saved:
    if proposed_module_name:
        if proposed_module_name.casefold() not in (module_name.casefold() for module_name in st.session_state["json_data"]["modules"]):
            #add it
            st.session_state["json_data"]["modules"][proposed_module_name] = final_item_list
            st.switch_page("current_list.py")
        else:
            st.warning("A module with this name already exists")
    else:
        st.warning("Please enter a valid name")
# cancel just takes you back to current list without doing anything
if canceled:
    st.switch_page("current_list.py")