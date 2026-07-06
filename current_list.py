#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# get rid of padding for top elements in turn

# add a background for the st.form
# tighten up the spacing for the st.form elements using padding, margin, unique keys per container

# clean up old functions, current_list etc etc

# would like a green tick or whatever in expander header if all items checked


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
    try:
        current_key = st.session_state["json_data"]["current_list"]
        current_exists = st.session_state["json_data"]["existing_lists"][current_key]
    except KeyError:
        st.switch_page("list_summary_menu.py")
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

current_key = st.session_state["json_data"]["current_list"]

if "edit_button_input" not in st.session_state:
    st.session_state.edit_button_input = False

if "add_button_input" not in st.session_state:
    st.session_state.add_button_input = False

if "mark_all_done" not in st.session_state:
    st.session_state.mark_all_done = False

if "clear_all" not in st.session_state:
    st.session_state.clear_all = False

if "module_add_key" not in st.session_state:
    st.session_state.module_add_key = False

if "list_settings_toggle" not in st.session_state:
    st.session_state.list_settings_toggle = False

if "namechange_toggle" not in st.session_state:
    st.session_state.namechange_toggle = False

current_list_to_top()
current_list_sorter()

def current_list_modules_draw(module_key_list: dict):
    current_key = st.session_state["json_data"]["current_list"]
    for sublist in module_key_list:
        unique_expander_key = widget_key_maker("expander", sublist, "")
        expanded = st.session_state["json_data"]["existing_lists"][current_key][sublist]["expanded"]
        with st.expander(
            expander_title(st.session_state["json_data"]["existing_lists"][current_key][sublist], sublist),
            expanded=expanded,
            key=unique_expander_key,
            on_change=update_state,
            args=("expanded", unique_expander_key, st.session_state["json_data"]["existing_lists"][current_key][sublist])
        ):
            target_dict = st.session_state["json_data"]["existing_lists"][current_key][sublist]["content_list"]
            for item in target_dict:
                cb_val = st.session_state["json_data"]["existing_lists"][current_key][sublist]["content_list"][item]
                unique_key = widget_key_maker("cb", current_key, item)
                st.session_state[unique_key] = cb_val
                st.checkbox(
                label=item,
                key=unique_key,
                on_change=update_state, args=(item, unique_key, target_dict)
                )

def current_list_draw(current_list_master):
    current_key = st.session_state["json_data"]["current_list"]
    target_dict = st.session_state["json_data"]["existing_lists"][current_key][current_list_master]["content_list"]
    unique_expander_key = widget_key_maker("expander", current_key, current_list_master)
    expanded = st.session_state["json_data"]["existing_lists"][current_key][current_list_master]["expanded"]

    def add_new_item_func():
        new_name = st.session_state.add_new_item_text
        #logic for empty string, dupe item etc
        if new_name:
            # test to see if it already exists in any sub_dicts
            current_key = st.session_state["json_data"]["current_list"]
            if not item_crosschecker(new_name, 0, st.session_state["json_data"]["existing_lists"][current_key]):
                # add it
                st.session_state["json_data"]["existing_lists"][current_key]["tier_0_list"]["content_list"][new_name] = False
                st.session_state.add_new_item_text = ""
            else:
                # don't add it
                st.warning("Item with this name already exists")

    with st.expander(
        "Unique items",
        expanded=expanded,
        key=unique_expander_key,
        on_change=update_state,
        args=("expanded", unique_expander_key, st.session_state["json_data"]["existing_lists"][current_key][current_list_master])
    ):
        with st.container(height=50, border=False):
            st.text_input(label=" ", placeholder="add new list item here", on_change=add_new_item_func, key="add_new_item_text", label_visibility="collapsed")

        for item in target_dict.keys():
            #def update_state(name, key):
            #    st.session_state["json_data"]["existing_lists"][current_key][current_list_master]["content_list"][name] = st.session_state[key]

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
                
                del st.session_state["json_data"]["existing_lists"][current_key][current_list_master]["content_list"][name]
                del_key = widget_key_maker("delete", current_key, name)
                del st.session_state[del_key]
            
            def edit_confirm(name=item):
                # trigger session_state, set the item key
                st.session_state.edit_button_input = True
                st.session_state["item_to_be_edited"] = name
            
            col1, col2, col3 =st.columns([6, 1, 1])
            with col1:
                cb_val = st.session_state["json_data"]["existing_lists"][current_key][current_list_master]["content_list"][item]
                unique_key = widget_key_maker("cb", current_key, item)
                st.session_state[unique_key] = cb_val
                st.checkbox(
                    label=item,
                    key=unique_key,
                    on_change=update_state, args=(item, unique_key, target_dict)
                )
            with col2:
                unique_edit_key = widget_key_maker("edit", current_key, item)
                st.button(
                    label="",
                    icon=":material/edit:",
                    key=unique_edit_key,
                    on_click=edit_confirm
                )

            with col3:
                unique_del_key = widget_key_maker("delete", current_key, item)
                st.button(
                    label="",
                    icon=":material/delete:",
                    key=unique_del_key,
                    on_click=delete_confirm
                )

def master_sub_list_sort_launch():
    current_key = st.session_state["json_data"]["current_list"]
    master_list = []
    sub_lists = []
    for sub_dict in st.session_state["json_data"]["existing_lists"][current_key]:
        if st.session_state["json_data"]["existing_lists"][current_key][sub_dict]["list_tier"] == 0:
            master_list.append(sub_dict)
        else:
            sub_lists.append(sub_dict)
    for single_list in master_list:
        current_list_draw(single_list)
    current_list_modules_draw(sub_lists)

def module_to_list():
    current_key = st.session_state["json_data"]["current_list"]
    # use selectbox key to identify module
    module_to_list_key = st.session_state.module_add_key
    # have we already imported this module?
    if module_to_list_key in st.session_state["json_data"]["existing_lists"][current_key]:
        st.warning("You have already added this module")
    else:
        # get a list of items and check whether already in list
        filtered_list = []
        unfiltered_list = st.session_state["json_data"]["modules"][module_to_list_key]
        check_subject = st.session_state["json_data"]["existing_lists"][current_key]
        for item in unfiltered_list:
            if not item_crosschecker(item, 1, check_subject):
                filtered_list.append(item)
        # pass this module through list_builder()
        module_as_dict = list_builder(module_to_list_key, filtered_list, 1)
        module_as_dict["expanded"] = True
        # add the new dict into the current list's dictionary structure
        st.session_state["json_data"]["existing_lists"][current_key][module_to_list_key] = module_as_dict
        st.rerun()

page_header()

control_button_container = st.container(horizontal=False, border=True)
with control_button_container:
    col1, col2, col3, col4, col5 =st.columns([5,1,1,1,1,], gap="xsmall")

    #add list title
    with col1:
        if st.button(f"{current_key}", icon=":material/edit:", icon_position="left", type="tertiary", key="list_namechange_button"):
            #toggle the text input
            if st.session_state.namechange_toggle:
                st.session_state.namechange_toggle = False
            else:
                st.session_state.namechange_toggle = True
    with col2:
        mark_all_done_button = st.button("", icon=":material/check_circle_unread:", key="mark_all_done_button", help="mark all done")
    with col3:
        clear_all_button = st.button("", icon=":material/app_badging:", key="clear_all_button", help="clear all")
    with col4:
        if st.button("", icon=":material/library_add:", help="save unique list to new module"):
            st.switch_page("module_from_unique_list.py")
    with col5:
        settings_button = st.button("", icon=":material/settings:", key="edit_settings_button")
        if settings_button:
            #toggle the settings form
            if st.session_state.list_settings_toggle:
                st.session_state.list_settings_toggle = False
            else:
                st.session_state.list_settings_toggle = True
 
    if mark_all_done_button:
        st.session_state.mark_all_done = True
    if clear_all_button:
        st.session_state.clear_all = True

if st.session_state.namechange_toggle:
    new_list_name = st.text_input("change list name?", label_visibility="collapsed", placeholder="enter new list name here")
    if new_list_name:
        if new_list_name.casefold() not in (list_name.casefold() for list_name in st.session_state["json_data"]["existing_lists"]):
            #change it
            list_renamer(current_key, new_list_name)
            st.session_state.namechange_toggle = False
            st.rerun()
        else:
            st.warning("A list with this name already exists")

if st.session_state.list_settings_toggle:
    #open up a menu containing the various minor functions
    with st.form(key="settings_form", border=True):
        with st.container(border=False, key="settings_add_module"):
            st.write("Add module list?")
            module_select_list = []
            #get the module lists, but only those not already added
            for module in st.session_state["json_data"]["modules"]:
                if module not in st.session_state["json_data"]["existing_lists"][current_key]:
                    module_select_list.append(module)
            # select box
            st.session_state.add_module_input = st.selectbox("hidden", options=module_select_list, index=None, placeholder="Select module to add", label_visibility="collapsed", key="module_add_key")

        #get the list of module lists
        sub_lists = []
        for sub_dict in st.session_state["json_data"]["existing_lists"][current_key]:
            if st.session_state["json_data"]["existing_lists"][current_key][sub_dict]["list_tier"] == 1:
                sub_lists.append(sub_dict)
        # offer delete option, as long as some modules have been added
        if sub_lists:
            with st.container(border=False, key="settings_delete_module"):
                st.write("Remove module lists?")
                delete_list = [mod_list for mod_list in sub_lists if st.checkbox(mod_list)] 

        with st.container(border=False, horizontal=True, key="settings_submit_container"):
            submitted = st.form_submit_button("Apply", type="primary")
            canceled = st.form_submit_button("Cancel")

        if submitted:
            #update everything
            if sub_lists:
                for mod_list in delete_list:
                    del st.session_state["json_data"]["existing_lists"][current_key][mod_list]
            #reset
            st.session_state.list_settings_toggle = False
            if st.session_state.module_add_key:
                module_to_list()
            st.rerun()
        if canceled:
            #reset
            st.session_state.list_settings_toggle = False
            st.rerun()       

if st.session_state.mark_all_done:
    current_key = st.session_state["json_data"]["current_list"]
    for sub_dict in st.session_state["json_data"]["existing_lists"][current_key]:
        target_dict = st.session_state["json_data"]["existing_lists"][current_key][sub_dict]["content_list"]
        for key in target_dict.keys():
            unique_key = widget_key_maker("cb", current_key, key)
            st.session_state["json_data"]["existing_lists"][current_key][sub_dict]["content_list"][key] = True
            st.session_state[unique_key] = True

    st.session_state.mark_all_done = False
    st.rerun()

if st.session_state.clear_all:
    current_key = st.session_state["json_data"]["current_list"]
    for sub_dict in st.session_state["json_data"]["existing_lists"][current_key]:
        target_dict = st.session_state["json_data"]["existing_lists"][current_key][sub_dict]["content_list"]
        for key in target_dict.keys():
            unique_key = widget_key_maker("cb", current_key, key)
            st.session_state["json_data"]["existing_lists"][current_key][sub_dict]["content_list"][key] = False
            st.session_state[unique_key] = False

    st.session_state.clear_all = False
    st.rerun()

if st.session_state.edit_button_input:
    # retrieve item to be edited
    item_name = st.session_state["item_to_be_edited"]
    with st.form(key="edit_item_name_input"):
        user_input = st.text_input(f"Edit '{item_name}':")
        edit_form_button_container = st.container(horizontal=True) 
        with edit_form_button_container:
            submit_button = st.form_submit_button(label="Confirm", type="primary")
            cancel_button = st.form_submit_button(label="Cancel")

        if submit_button:
            if user_input:
                # test to see if it already exists in any sub_dicts
                current_key = st.session_state["json_data"]["current_list"]
                if not item_crosschecker(user_input, 0, st.session_state["json_data"]["existing_lists"][current_key]):
                    # replace it, and delete the now unneeded key
                    # get the dictionary with items
                    content_dict = st.session_state["json_data"]["existing_lists"][current_key]["tier_0_list"]["content_list"]
                    # retrieve the old value to be passed
                    old_value = content_dict[item_name]
                    # deal with checkbox and edit button keys
                    unique_cb_key = widget_key_maker("cb", current_key, user_input)
                    unique_cb_key_for_deletion = widget_key_maker("cb", current_key, item_name)
                    unique_edit_key = widget_key_maker("edit", current_key, item_name)
                    st.session_state[unique_cb_key] = old_value
                    del st.session_state[unique_cb_key_for_deletion]
                    del st.session_state[unique_edit_key]
                    # now add the new key and value
                    content_dict[user_input] = old_value
                    # delete the old one
                    del content_dict[item_name]
                    # and replace into session state
                    st.session_state["json_data"]["existing_lists"][current_key]["tier_0_list"]["content_list"] = content_dict
                    st.session_state.edit_button_input = False
                    st.rerun()
                else:
                    # don't add it
                    st.warning("This item name already in use")
            else:
                st.warning("Blank items are not permitted")
        if cancel_button:
            st.session_state.edit_button_input = False
            st.rerun()

master_sub_list_sort_launch()