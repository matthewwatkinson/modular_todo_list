#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# get the edit button logic done - have done name edit but should bring up the new edit page with list items

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


if "module_item_edit_button_input" not in st.session_state:
    st.session_state.module_item_edit_button_input = False

if "module_item_add_button_input" not in st.session_state:
    st.session_state.module_item_add_button_input = False

module_key = st.session_state["json_data"]["module_to_edit"]
module_contents = st.session_state["json_data"]["modules"][module_key]

page_header()
            
st.write(f"#### Edit {module_key}")

if st.session_state.module_item_edit_button_input:
    # retrieve item to be edited
    item_name = st.session_state["json_data"]["module_item_to_be_edited"]
    with st.form(key="module_edit_item_name_input"):
        user_input = st.text_input(f"Edit '{item_name}':", label_visibility="collapsed", value=item_name)
        edit_form_button_container = st.container(horizontal=True) 
        with edit_form_button_container:
            submit_button = st.form_submit_button(label="Confirm edit", type="primary")
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

with st.container():
    def add_new_item_func():
        new_name = st.session_state.add_new_module_item_text
        #logic for empty string, dupe item etc
        if new_name:
            # test to see if it already exists in any sub_dicts
            if new_name.casefold() not in (module_item.casefold() for module_item in module_contents):
                # add it
                module_contents.append(new_name)
                st.session_state["json_data"]["modules"][module_key] = module_contents
                st.session_state.add_new_module_item_text = ""

            else:
                # don't add it
                st.warning("Item with this name already exists")


    add_new_module_item = st.text_input(label=" ", label_visibility="collapsed", placeholder="add new module item here", on_change=add_new_item_func, key="add_new_module_item_text")

module_edit_list_sorter(module_key)

module_edit_list_draw(module_key)

if st.button("Return"):
    st.switch_page("module_summary_menu.py")