#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# get the edit button logic done - have done name edit but should bring up the new edit page with list items

import streamlit as st
import json
#from helper import *
from dictionary_scratchpad import *

if "module_item_edit_button_input" not in st.session_state:
    st.session_state.module_item_edit_button_input = False

if "module_item_add_button_input" not in st.session_state:
    st.session_state.module_item_add_button_input = False

module_key = st.session_state.module_to_edit
module_contents = st.session_state["json_data"]["modules"][module_key]

if st.session_state.module_item_edit_button_input:
    # retrieve item to be edited
    item_name = st.session_state["module_item_to_be_edited"]
    with st.form(key="module_edit_item_name_input"):
        user_input = st.text_input(f"Edit '{item_name}':")
        edit_form_button_container = st.container(horizontal=True) 
        with edit_form_button_container:
            submit_button = st.form_submit_button(label="Confirm", type="primary")
            cancel_button = st.form_submit_button(label="Cancel")

        if submit_button:
            if user_input:
                # test to see if it already exists in the module
                if user_input not in module_contents:
                    # replace it, and delete the now unneeded key
                    old_value_index = module_contents.index(item_name)
                    module_contents.pop(old_value_index)
                    module_contents.append(user_input)
                    # deal with edit button keys
                    del st.session_state[f"{item_name}_edit_button"]
                    # and replace into session state
                    st.session_state["json_data"]["modules"][module_key] = module_contents
                    st.session_state.module_item_edit_button_input = False
                    st.rerun()  # Instantly refreshes to show updated state
                else:
                    # don't add it
                    st.warning("This item name already in use")
            else:
                st.warning("Blank items are not permitted")
        if cancel_button:
            st.session_state.module_item_edit_button_input = False
            st.rerun()  # Instantly refreshes to show updated state


module_edit_list_sorter(module_key)

st.title(f"Edit {module_key}")

module_new_item_button =  st.button("➕", key="module_new_item_button")

if module_new_item_button:
        st.session_state.module_item_add_button_input = True

if st.session_state.module_item_add_button_input:
    with st.form(key="new_module_item_input"):
        user_input = st.text_input("Add an item:")
        form_button_container = st.container(horizontal=True) 
        with form_button_container:
            submit_button = st.form_submit_button(label="Add", type="primary")
            cancel_button = st.form_submit_button(label="Cancel")

        if submit_button:
            if user_input:
                # test to see if it already exists in any sub_dicts
                if user_input not in module_contents:
                    # add it and reset input key
                    module_contents.append(user_input)
                    st.session_state["json_data"]["modules"][module_key] = module_contents
                    st.session_state.module_item_add_button_input = False
                    st.rerun()
                else:
                    # don't add it
                    st.warning("Item already exists")
            else:
                st.warning("Please enter some text before submitting.")
        if cancel_button:
            st.session_state.module_item_add_button_input = False
            st.rerun()

module_edit_list_draw(module_key)

if st.button("Return"):
    st.switch_page("module_summary_menu.py")