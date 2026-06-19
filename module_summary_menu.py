#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# get the edit button logic done - have done name edit but should bring up the new edit page with list items

import streamlit as st
import json
from dictionary_scratchpad import *

smaller_button_css = """
<style>
button[data-testid="stBaseButton-secondary"] {
    min-height: 0.25rem;
    padding-top: 0rem;
    padding-bottom: 0rem;
}
</style>
"""

st.markdown(smaller_button_css, unsafe_allow_html=True)

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

#if "module_edit_button_input" not in st.session_state:
#   st.session_state.module_edit_button_input = False

if "new_module_page_jump" not in st.session_state:
    st.session_state.new_module_page_jump = False

if st.session_state.new_module_page_jump:
    st.session_state.new_module_page_jump = False
    st.switch_page("module_edit_menu.py")



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
    
#        with st.container(border=True, horizontal=True):
        col1, col2, col3, col4 =st.columns([3, 2, 1, 1])

        with col1:
            st.write(f"{key}")

        with col2:
            st.write(f"({len(st.session_state["json_data"]["modules"][key])} items)")

        with col3:
            if st.button(
                #label="✏️",
                label="e",
                key=f"{key}_edit_button",
            ):
                # record the module to be edited
                st.session_state.module_to_edit = key
                # switch to edit page
                st.switch_page("module_edit_menu.py")

        with col4:
            st.button(
                #label="🗑️",
                label="d",
                key=f"{key}_delete_button",
                on_click=delete_confirm
            )

module_list_sorter()
st.title("Modules")

with st.container():
    def add_new_module_func():
        new_name = st.session_state.add_new_module_text
        #logic for empty string, dupe item etc
        if new_name:
            # test to see if it already exists in any sub_dicts
            if new_name.casefold() not in (module_name.casefold() for module_name in st.session_state["json_data"]["modules"]):
                # add it as an empty list and reset input key
                st.session_state["json_data"]["modules"][new_name] = []
                st.session_state.module_to_edit = new_name

                st.session_state.add_new_module_text = ""
                # set the page jumper
                st.session_state.new_module_page_jump = True

            else:
                # don't add it
                st.warning("List with this name already exists")

    add_new_module = st.text_input(label=" ", placeholder="add new module here", on_change=add_new_module_func, key="add_new_module_text")

module_list_draw()

