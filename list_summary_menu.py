#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# get the edit button logic done - have done name edit but should bring up the new edit page with list items

import streamlit as st
import json
#from helper import *
from dictionary_scratchpad import *

data_save()

# no update/deletion of "current_list" key, want to preserve across sessions

if "new_list_page_jump" not in st.session_state:
    st.session_state.new_list_page_jump = False

if st.session_state.new_list_page_jump:
    st.session_state.new_list_page_jump = False
    st.switch_page("current_list.py")

st.title("My Lists")

with st.container():
    def add_new_list_func():
        new_name = st.session_state.add_new_list_text
        #logic for empty string, dupe item etc
        if new_name:
            # test to see if it already exists in any sub_dicts
            if new_name.casefold() not in (list_name.casefold() for list_name in st.session_state["json_data"]["existing_lists"]):
                # add it as an empty dict, make it the current_list, and reset input key
                st.session_state["json_data"]["existing_lists"][new_name]= {}
                st.session_state["json_data"]["existing_lists"][new_name]["tier_0_list"] = list_builder(new_name, [], 0)
                st.session_state["json_data"]["current_list"] = new_name
                st.session_state.add_new_list_text = ""
                # set the page jumper
                st.session_state.new_list_page_jump = True

            else:
                # don't add it
                st.warning("List with this name already exists")
#        else:
#               st.warning("Please enter some text before submitting.")

    add_new_list = st.text_input(label=" ", placeholder="add new list here", on_change=add_new_list_func, key="add_new_list_text")


def lists_list_sorter_alph():
    # this sorts alphabetically. But may prefer just to move most recently changed to top for recency sort
    lists_list_to_sort = st.session_state["json_data"]["existing_lists"]
    sorted_dict = dict(sorted(lists_list_to_sort.items(), key=lambda item: item[0].lower()))
    st.session_state["json_data"]["existing_lists"] = sorted_dict

def lists_list_draw():
    for key in st.session_state["json_data"]["existing_lists"]:

        @st.dialog(title="Are you sure you want to delete this list?", dismissible=False)
        def delete_confirm(name=key):
            col1, col2 = st.columns(2)
            with col1:
                if st.button("OK", type="primary", use_container_width=True):
                    delete_update(name)
                    st.rerun()
            with col2:
                if st.button("Cancel", use_container_width=True):
                    st.rerun()

        def delete_update(name=key):
            
            del st.session_state["json_data"]["existing_lists"][name]
            del st.session_state[f"{name}_list_delete_button"]
    
        col1, col2, col3 =st.columns([10, 1, 1])

        with col1:
            st.write(f"{key}")

        with col2:
             if st.button(
                label="✏️",
                key=f"{key}_list_edit_button",
            ):
                # make the selected list the current list
                st.session_state["json_data"]["current_list"] = key
                # switch to edit page
                st.switch_page("current_list.py")

        with col3:
            st.button(
                label="🗑️",
                key=f"{key}_list_delete_button",
                on_click=delete_confirm
            )


lists_list_draw()