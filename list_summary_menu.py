#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# need to change the "exisiting lists" dictionary whenever current key changes - pop out and insert at head

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

if "new_list_page_jump" not in st.session_state:
    st.session_state.new_list_page_jump = False

if st.session_state.new_list_page_jump:
    st.session_state.new_list_page_jump = False
    st.switch_page("current_list.py")

page_header()
            
st.write("#### My Lists")

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
                st.session_state["json_data"]["existing_lists"][new_name]["tier_0_list"]["expanded"] = False
                st.session_state["json_data"]["current_list"] = new_name
                current_list_to_top()
                st.session_state.add_new_list_text = ""
                # set the page jumper
                st.session_state.new_list_page_jump = True

            else:
                # don't add it
                st.warning("List with this name already exists")

    add_new_list = st.text_input(label=" ", label_visibility="collapsed", placeholder="add new list here", on_change=add_new_list_func, key="add_new_list_text")


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
    
        col1, col2 =st.columns([7, 1], vertical_alignment="center")

        with col1:
            if st.button(
                label=f"{key}",
                type="tertiary",
                key=f"{key}_list_edit_button"
                ):
                # make the selected list the current list
                st.session_state["json_data"]["current_list"] = key
                current_list_to_top()
                # switch to edit page
                st.switch_page("current_list.py")

        with col2:
            st.button(
                label="",
                icon=":material/delete:",
                key=f"{key}_list_delete_button",
                on_click=delete_confirm
            )

lists_list_draw()