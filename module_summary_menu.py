#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# get the edit button logic done - have done name edit but should bring up the new edit page with list items

import streamlit as st
import json
from dictionary_scratchpad import *

#if "module_edit_button_input" not in st.session_state:
#   st.session_state.module_edit_button_input = False

if "new_module_button_input" not in st.session_state:
    st.session_state.new_module_button_input = False

def module_list_sorter():
    module_list_to_sort = st.session_state["json_data"]["modules"]
    sorted_dict = dict(sorted(module_list_to_sort.items(), key=lambda item: item[0].lower()))
    st.session_state["json_data"]["modules"] = sorted_dict

def module_list_draw():
    for key in st.session_state["json_data"]["modules"]:

        @st.dialog(title="Are you sure you want to delete this module?", dismissible=False)
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
            
            del st.session_state["json_data"]["modules"][name]
            del st.session_state[f"{name}_delete_button"]
    
        col1, col2, col3, col4 =st.columns([8, 2, 1, 1])

        with col1:
            st.write(f"{key}")

        with col2:
            st.write(f"({len(st.session_state["json_data"]["modules"][key])} items)")

        with col3:
             if st.button(
                label="✏️",
                key=f"{key}_edit_button",
            ):
                # record the module to be edited
                st.session_state.module_to_edit = key
                # switch to edit page
                st.switch_page("module_edit_menu.py")

        with col4:
            st.button(
                label="🗑️",
                key=f"{key}_delete_button",
                on_click=delete_confirm
            )

module_list_sorter()
st.title("Modules")
new_module_button =  st.button("➕", key="new_module_button")  

if new_module_button:
    # trigger popup with new module name input. check if it exists, then switch page
    st.session_state.new_module_button_input = True

if st.session_state.new_module_button_input:
    with st.form(key="new_module_input"):
        user_input = st.text_input("Add a new module:")
        form_button_container = st.container(horizontal=True) 
        with form_button_container:
            submit_button = st.form_submit_button(label="Add", type="primary")
            cancel_button = st.form_submit_button(label="Cancel")

        if submit_button:
            if user_input:
                # test to see if a module with this name exists
                if user_input not in st.session_state["json_data"]["modules"]:
                    # add it as an empty list and reset input key
                    st.session_state["json_data"]["modules"][user_input] = []
                    st.session_state.new_module_button_input = False
                    # jump to edit page
                    st.session_state.module_to_edit = user_input
                    st.switch_page("module_edit_menu.py")

                else:
                    # don't add it
                    st.warning("Module with this name already exists")
            else:
                st.warning("Please enter some text before submitting.")
        if cancel_button:
            st.session_state.new_module_button_input = False
            st.rerun()

module_list_draw()

