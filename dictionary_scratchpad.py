#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import streamlit as st


baseline_json_dict = {
  "current_list": "",
  "existing_lists": {},
  "modules": {}
}

def page_header():
    with st.container(border=False, width="stretch", horizontal=True, key="top_menu_container", gap=None):
        col1, col2 = st.columns(2)
        with col1:
            navigate_to_lists_button = st.button("lists", type="primary", width="stretch", key="current_list_to_lists_menu_button")
        with col2:
            navigate_to_modules_button = st.button("modules", type="secondary", width="stretch", key="current_list_to_modules_button")
            if navigate_to_modules_button:
                st.switch_page("module_summary_menu.py")
            if navigate_to_lists_button:
                st.switch_page("list_summary_menu.py")

def current_list_to_top():
    # reorders existing lists dictionary to bring current to top, thereby ordering by last used
    lists_folder = st.session_state["json_data"]["existing_lists"]
    current_list = st.session_state["json_data"]["current_list"]
    # extract the current list and reinsert at head
    lists_folder = {current_list: lists_folder.pop(current_list), **lists_folder}
    # reinsert into session state
    st.session_state["json_data"]["existing_lists"] = lists_folder

def list_builder(name: str, content_list=[], tier=0):
    list_container = {}
    list_container["list_name"] = name
    list_container["list_tier"] = tier
    list_container["content_list"] = {}
    for item in content_list:
        list_container["content_list"][item] = False

    return list_container

def widget_key_maker(type: str, master_list_name: str, item_name: str):
    # create widget key in standardm form. types are "cb", "delete", "edit"
    return f"{type}_{master_list_name}_{item_name}"

def update_state(item_name, item_key, target_list_dict):
    target_list_dict[item_name] = st.session_state[item_key]

def list_renamer(existing_name, new_name):
    # make sure not empty input
    if new_name:
        #change it
        copied_dict = st.session_state["json_data"]["existing_lists"][existing_name]
        st.session_state["json_data"]["existing_lists"][new_name] = copied_dict
        del st.session_state["json_data"]["existing_lists"][existing_name]
        st.session_state["json_data"]["current_list"] = new_name

def item_crosschecker(new_item: str, new_item_tier: int, check_dict: dict):
    # check against a dict that represents the [current_shown_list] of the master dict (dict of list_builder_dicts)
    # returns True if item already exists
    cancel_insert = False
    for sub_dict in check_dict:
        for key in list(check_dict[sub_dict]["content_list"].keys()):
            if key.lower() == new_item.lower():
                # compare tiers
                #check_tier = check_dict[sub_dict]["list_tier"]
                #if new_item_tier < check_tier:
                    # new_item is in the senior dict, so delete from check_dict
                #    del check_dict[sub_dict]["content_list"][key]
                #else:
                cancel_insert = True
    return cancel_insert

def list_crosschecker(new: dict, existing: dict):
    # for any list_builder_dict, check if items are shared with existing dict of list_builder_dicts.
    # return a list of items that may be added (i.e. not duplicates)
    # delete from junior list or new list if tiers equal
    
    # make list of non-dupes
    accepted_list = []

    # get the tier
    list_tier = new["list_tier"]
    # get the keys
    for item in list(new["content_list"].keys()):
        print(item)
        cancel_insert_check = item_crosschecker(item, list_tier, existing)
        if not cancel_insert_check:
            accepted_list.append(item)
    return accepted_list

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

def module_edit_list_sorter(key):
    unsorted_list = st.session_state["json_data"]["modules"][key]
    sorted_list = sorted(unsorted_list)
    st.session_state["json_data"]["modules"][key] = sorted_list

def module_edit_list_draw(key):
    for item in st.session_state["json_data"]["modules"][key]:

        @st.dialog(title="Are you sure you want to delete this item?", dismissible=False)
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
            delete_index = st.session_state["json_data"]["modules"][key].index(name)
            del st.session_state["json_data"]["modules"][key][delete_index]
            del st.session_state[f"{name}_delete_button"]

        def edit_confirm(name=item):
            # trigger session_state, set the item key
            st.session_state.module_item_edit_button_input = True
            st.session_state["json_data"]["module_item_to_be_edited"] = name

        col1, col2, col3 =st.columns([6, 1, 1])

        with col1:
            st.write(f"{item}")

        with col2:
             st.button(
                label="",
                icon=":material/edit:",
                key=f"{item}_edit_button",
                on_click=edit_confirm
            )

        with col3:
            st.button(
                label="",
                icon=":material/delete:",
                key=f"{item}_delete_button",
                on_click=delete_confirm
            )

def expander_title(target_dict, base_string):
    # is everything true?
    all_true = True
    for key in target_dict["content_list"]:
        if target_dict["content_list"][key] == False:
            all_true = False
    if all_true:
        return f"{base_string} &nbsp; &nbsp; &nbsp; 🟢"
    else:
        return base_string
            
