#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# next up: update json format so we have dictionaries with the name, the actual list dictionary
# also: practice expander logic using last_list

import streamlit as st
import json

last_list = {"red": False, "yellow": False, "green": True, "purple": False, "black": False}

# import json
try:
    with open("list_storage.json", "r") as file:
        json_dictionary = json.load(file)
except json.decoder.JSONDecodeError:
    # Triggered if the file is completely empty or has invalid syntax
    json_dictionary = {}
except FileNotFoundError:
    # Triggered if the file does not exist at all
    json_dictionary = {}
if "current" not in json_dictionary:
    json_dictionary["current"] = {}

#but only use json if we don't have a session state
if "current_list" not in st.session_state:
    st.session_state["current_list"] = json_dictionary["current"]
    # need to initialise the true/false state for each item
    for item in st.session_state["current_list"]:
        st.session_state[f"cb_{item}"] = st.session_state["current_list"][item]
else:
    # otherwise we need to save the latest state to json
    with open("list_storage.json", "w") as file:
        json_dictionary["current"] = st.session_state["current_list"]
        json.dump(json_dictionary, file, indent=2)

if "add_button_input" not in st.session_state:
    st.session_state.add_button_input = False

if "mark_all_done" not in st.session_state:
    st.session_state.mark_all_done = False

if "clear_all" not in st.session_state:
    st.session_state.clear_all = False


current_list = st.session_state["current_list"]
# sort by checked/unchecked and then name
ordered_list = dict(sorted(current_list.items(), key=lambda item: (-item[1], item[0])))
# reinsert into session state
st.session_state["current_list"] = ordered_list

def list_draw(target_dict_key: str):
        target_dict = st.session_state[target_dict_key]
        for item, state in target_dict.items():
            def update_state(name=item):
                st.session_state[target_dict_key][name] = st.session_state[f"cb_{name}"]

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
                
                del st.session_state[target_dict_key][name]
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
    for item in st.session_state.current_list:
        st.session_state["current_list"][item] = True
        st.session_state[f"cb_{item}"] = True
    st.session_state.mark_all_done = False
    st.rerun()

if st.session_state.clear_all:
    for item in st.session_state.current_list:
        st.session_state["current_list"][item] = False
        st.session_state[f"cb_{item}"] = False
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
                if user_input in current_list:
                    st.warning("Item already exists")
                else:
                    st.session_state.current_list[user_input] = False
                    st.session_state.add_button_input = False
                    st.rerun()  # Instantly refreshes to show updated state
            else:
                st.warning("Please enter some text before submitting.")
        if cancel_button:
            st.session_state.add_button_input = False
            st.rerun()  # Instantly refreshes to show updated state

   
list_draw("current_list")
