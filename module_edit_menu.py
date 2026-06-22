#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# get the edit button logic done - have done name edit but should bring up the new edit page with list items

import streamlit as st
import json
#from helper import *
from dictionary_scratchpad import *

st.markdown(
    """
    <style>
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        overflow-x: auto; /* Adds a scrollbar if content is too wide */
    }
    [data-testid="stHorizontalBlock"] > div {
        min-width: 0 !important; /* Prevents columns from expanding and cracking layout */
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

if "module_to_edit" not in st.session_state:
    st.session_state.module_to_edit = ""


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

st.title(f"Edit {module_key}")

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


    add_new_module_item = st.text_input(label=" ", placeholder="add new module item here", on_change=add_new_item_func, key="add_new_module_item_text")

module_edit_list_sorter(module_key)

# module_new_item_button =  st.button("➕", key="module_new_item_button")

# if module_new_item_button:
#         st.session_state.module_item_add_button_input = True

# if st.session_state.module_item_add_button_input:
#     with st.form(key="new_module_item_input"):
#         user_input = st.text_input("Add an item:")
#         form_button_container = st.container(horizontal=True) 
#         with form_button_container:
#             submit_button = st.form_submit_button(label="Add", type="primary")
#             cancel_button = st.form_submit_button(label="Cancel")

#         if submit_button:
#             if user_input:
#                 # test to see if it already exists in any sub_dicts
#                 if user_input not in module_contents:
#                     # add it and reset input key
#                     module_contents.append(user_input)
#                     st.session_state["json_data"]["modules"][module_key] = module_contents
#                     st.session_state.module_item_add_button_input = False
#                     st.rerun()
#                 else:
#                     # don't add it
#                     st.warning("Item already exists")
#             else:
#                 st.warning("Please enter some text before submitting.")
#         if cancel_button:
#             st.session_state.module_item_add_button_input = False
#             st.rerun()

module_edit_list_draw(module_key)

if st.button("Return"):
    st.switch_page("module_summary_menu.py")