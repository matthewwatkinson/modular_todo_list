#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# next up: update json format so we have dictionaries with the name, the actual list dictionary
# also: practice expander logic using last_list
# works currently with "current list" as a special case. Need to figure out how to generalize.
# All lists will need the same format, same ordering logic, same key updates.
# Perhaps the difference between "modules" and "base" is a boolean dictionary property?
# first step is a dictionary design that can contain all the information that might be needed

# when adding lists, will need to check if items already exist in any other existing list, else key errors will arise

"""
dictionary design. every dictionary needs a nested dictionary dict_actual_list of item: T/F pairs.
It also needs a list_name key and value
It also needs a list_tier: 0/1 pair
All these dictionaries need to exist in a top dictionary that holds exclusively lists and sublists for this particular task list
And all task list master dictionaries exist in the json_dictionary[lists] tier.
json_dictionary[current_shown_list] should contain key for last list used
then we can just load the last list used by referencing with that key

will also need to think about how to build a new list from scratch.
"""

import streamlit as st
import json
#from helper import *
from dictionary_scratchpad import *

baseline_json_dict = {
  "current_list": "",
  "existing_lists": {},
  "modules": {}
}

last_list = {"red": False, "yellow": False, "green": True, "purple": False, "black": False}

def data_load():
    # import json
    try:
        with open("list_storage.json", "r") as file:
            json_dictionary = json.load(file)
    except json.decoder.JSONDecodeError:
        # Triggered if the file is completely empty or has invalid syntax
        json_dictionary = baseline_json_dict.copy()
    except FileNotFoundError:
        # Triggered if the file does not exist at all
        json_dictionary = baseline_json_dict.copy()
    return json_dictionary

def data_save():
    with open("list_storage.json", "w") as file:
        json_dictionary = st.session_state["json_data"]
        json.dump(json_dictionary, file, indent=2)

def current_and_populated():
    current_and_populated_exists = False
    if st.session_state["json_data"]["current_list"]:
        current_key = st.session_state["json_data"]["current_list"]
        if st.session_state["json_data"]["existing_lists"][current_key]:
            current_and_populated_exists = True
    return current_and_populated_exists

def current_list_sorter():
    current_key = st.session_state["json_data"]["current_list"]
    for sub_dict in st.session_state["json_data"]["existing_lists"][current_key]:
        list_to_sort = st.session_state["json_data"]["existing_lists"][current_key][sub_dict]["content_list"]
        # make sorted dict at "content_list" level
        sorted_dict = dict(sorted(list_to_sort.items(), key=lambda item: (-item[1], item[0])))
        # reinsert into session state
        st.session_state["json_data"]["existing_lists"][current_key][sub_dict]["content_list"] = sorted_dict


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
                st.session_state[f"cb_{key}"] = value
else:
    # otherwise we need to save the latest state to json
    data_save()

if "add_button_input" not in st.session_state:
    st.session_state.add_button_input = False

if "mark_all_done" not in st.session_state:
    st.session_state.mark_all_done = False

if "clear_all" not in st.session_state:
    st.session_state.clear_all = False

current_list_sorter()

def current_list_draw():
    current_key = st.session_state["json_data"]["current_list"]
    for sub_dict in st.session_state["json_data"]["existing_lists"][current_key]:
        target_dict = st.session_state["json_data"]["existing_lists"][current_key][sub_dict]["content_list"]
        for item in target_dict.keys():
            def update_state(name=item):
                st.session_state["json_data"]["existing_lists"][current_key][sub_dict]["content_list"][name] = st.session_state[f"cb_{name}"]

            @st.dialog(title="Delete this item?", dismissible=False)
            def delete_confirm(name=item):
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("OK", type="primary", use_container_width=True):
                        delete_update(name)
                        st.rerun()
                with col2:
                    if st.button("Cancel", use_container_width=True):
                        st.rerun()

            def delete_update(name=item):
                
                del st.session_state["json_data"]["existing_lists"][current_key][sub_dict]["content_list"][name]
                del st.session_state[f"{item}_delete_button"]
            
            col1, col2 =st.columns([1, 1])
            with col1:
                st.checkbox(
                    label=item,
                    #value = state (had originally, seems superfluous)
                    key=f"cb_{item}",
                    on_change=update_state
                )
            with col2:
                st.button(
                    label=f"🗑️",
                    key=f"{item}_delete_button",
                    on_click=delete_confirm
                )
                

control_button_container = st.container(horizontal=True)
with control_button_container:
    new_item_button =  st.button("➕", key="new_item_button")
    mark_all_done_button = st.button("mark all done", key="mark_all_done_button")
    clear_all_button = st.button("clear all", key="clear_all_button")
    if new_item_button:
        st.session_state.add_button_input = True
    if mark_all_done_button:
        st.session_state.mark_all_done = True
    if clear_all_button:
        st.session_state.clear_all = True

if st.session_state.mark_all_done:
    current_key = st.session_state["json_data"]["current_list"]
    for sub_dict in st.session_state["json_data"]["existing_lists"][current_key]:
        target_dict = st.session_state["json_data"]["existing_lists"][current_key][sub_dict]["content_list"]
        for key in target_dict.keys():
            st.session_state["json_data"]["existing_lists"][current_key][sub_dict]["content_list"][key] = True
            st.session_state[f"cb_{key}"] = True
    st.session_state.mark_all_done = False
    st.rerun()

if st.session_state.clear_all:
    current_key = st.session_state["json_data"]["current_list"]
    for sub_dict in st.session_state["json_data"]["existing_lists"][current_key]:
        target_dict = st.session_state["json_data"]["existing_lists"][current_key][sub_dict]["content_list"]
        for key in target_dict.keys():
            st.session_state["json_data"]["existing_lists"][current_key][sub_dict]["content_list"][key] = False
            st.session_state[f"cb_{key}"] = False
    st.session_state.clear_all = False
    st.rerun()


if st.session_state.add_button_input:
    with st.form(key="new_item_input"):
        user_input = st.text_input("Add an item:")
        form_button_container = st.container(horizontal=True) 
        with form_button_container:
            submit_button = st.form_submit_button(label="Add", type="primary")
            cancel_button = st.form_submit_button(label="Cancel")

        if submit_button:
            if user_input:
                # test to see if it already exists in any sub_dicts
                current_key = st.session_state["json_data"]["current_list"]
                if not item_crosschecker(user_input, 0, st.session_state["json_data"]["existing_lists"][current_key]):
                    # add it
                    st.session_state["json_data"]["existing_lists"][current_key]["tier_0_list"]["content_list"][user_input] = False
                    st.session_state.add_button_input = False
                    st.rerun()  # Instantly refreshes to show updated state
                else:
                    # don't add it
                    st.warning("Item already exists")
            else:
                st.warning("Please enter some text before submitting.")
        if cancel_button:
            st.session_state.add_button_input = False
            st.rerun()  # Instantly refreshes to show updated state

   
current_list_draw()
