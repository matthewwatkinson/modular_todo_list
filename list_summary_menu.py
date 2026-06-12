#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# get the edit button logic done - have done name edit but should bring up the new edit page with list items

import streamlit as st
import json
#from helper import *
from dictionary_scratchpad import *

# no update/deletion of "current_list" key, want to preserve across sessions

if "new_list_button_input" not in st.session_state:
    st.session_state.new_list_button_input = False

st.title("My Lists")

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



new_list_button =  st.button("➕", key="new_list_button")  

if new_list_button:
    # trigger popup with new list name input. check if it exists, then switch page
    st.session_state.new_list_button_input = True

if st.session_state.new_list_button_input:
    with st.form(key="new_list_name_input"):
        user_input = st.text_input("Input name for new list")
        form_button_container = st.container(horizontal=True) 
        with form_button_container:
            submit_button = st.form_submit_button(label="Confirm", type="primary")
            cancel_button = st.form_submit_button(label="Cancel")

        if submit_button:
            if user_input:
                # test to see if a list with this name exists
                if user_input not in st.session_state["json_data"]["existing_lists"]:
                    # add it as an empty dict, make it the current_list, and reset input key
                    st.session_state["json_data"]["existing_lists"][user_input]= {}
                    st.session_state["json_data"]["existing_lists"][user_input]["tier_0_list"] = list_builder(user_input, [], 0)
                    st.session_state["json_data"]["current_list"] = user_input
                    st.session_state.new_list_button_input = False
                    # jump to edit page
                    st.switch_page("current_list.py")

                else:
                    # don't add it
                    st.warning("List with this name already exists")
            else:
                st.warning("Please enter some text before submitting.")
        if cancel_button:
            st.session_state.new_list_button_input = False
            st.rerun()



lists_list_draw()