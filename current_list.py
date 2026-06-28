#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# get rid of padding for top elements in turn
# need to be able to delete modules

# take all edit functions (edit title, add/remove module, save unique list as module to pop out accessed by single pencil button)
# put new unique list item input inside expander if possible

# need to be able to rename lists

# clean up old functions, current_list etc etc

# would like a green tick or whatever in expander header if all items checked
# if we are always calling tier 0 list tier_0_list then master_sub_sort is maybe redundant?

# tier_0_list hardcoding in edit section needs to be fixed (master_sub_list... can help)


import streamlit as st
import json
#from helper import *
from dictionary_scratchpad import *

smaller_button_css = """
<style>
button[data-testid="stBaseButton-secondary"] {
    min-height: 0.5rem;
    padding-top: 0rem;
    padding-bottom: 0rem;
}
</style>
"""

#st.markdown(smaller_button_css, unsafe_allow_html=True)

hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

padding_css = """
<style>
[data-testid="stExpander"] details {
    padding: 0px !important;
}
[data-testid="stExpander"] div[data-testid="stVerticalBlock"] {
    gap: 0.1rem !important;  /* Adjust the gap between elements inside the expander */
    padding-top: 0px !important;
    padding-bottom: 0px !important;
}
</style>
"""

st.markdown(padding_css, unsafe_allow_html=True)

container_padding_css = """
<style>
[data-testid="stContainer"] details {
    padding: 50px !important;
}
</style>
"""

st.markdown(container_padding_css, unsafe_allow_html=True)


st.markdown(
    """
    <style>
    /* Reset the inner structural gap of the expander block */
    [data-testid="stExpander"] [data-testid="stVerticalBlock"] {
        gap: 1.0rem !important;
    }

    /* Precision margin adjustments specifically for checkboxes inside the expander columns */
    [data-testid="stExpander"] [data-testid="column"] [data-testid="stCheckbox"] {
        margin-top: -11px !important;    /* Pulls elements closer together vertically */
        margin-bottom: -11px !important; 
        padding-top: 0px !important;     /* Protects text descenders from clipping */
        padding-bottom: 0px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    [data-testid="stMain"] .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

#CSS just for the text input container in the unique list
st.markdown(
    """
    <style>
    /* Target the block wrapper containing your unique key class */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.st-key-unique_list_text_input_container) {
        padding-bottom: 1.0rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
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

menu_format = """
.st-key-top_menu_container {
    background-color: rgba(100, 100, 200, 0.3);
}
"""
st.html(f"<style>{menu_format}</style>")

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

current_list_sorter()

def current_list_modules_draw(module_key_list: dict):
    current_key = st.session_state["json_data"]["current_list"]
    for sublist in module_key_list:
        unique_expander_key = widget_key_maker("expander", sublist, "")
        expanded = st.session_state["json_data"]["existing_lists"][current_key][sublist]["expanded"]
        with st.expander(
            sublist,
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

with st.container(border=True, width="stretch", horizontal=True, key="top_menu_container"):
    col1, col2 = st.columns(2)
    with col1:
        navigate_to_lists_button = st.button("lists", type="primary", width="stretch", key="current_list_to_lists_menu_button")
    with col2:
        navigate_to_modules_button = st.button("modules", type="secondary", width="stretch", key="current_list_to_modules_button")
        if navigate_to_modules_button:
            st.switch_page("module_summary_menu.py")
        if navigate_to_lists_button:
            st.switch_page("list_summary_menu.py")



control_button_container = st.container(horizontal=True, border=True)
with control_button_container:
    col1, col2, col3 =st.columns([3,1,1], gap="xxsmall")

    # add list title
    with col1:
        st.write(f"##### {current_key}")
    with col2:
        mark_all_done_button = st.button("all", key="mark_all_done_button", width="stretch")
    with col3:
        clear_all_button = st.button("none", key="clear_all_button", width="stretch")

    if mark_all_done_button:
        st.session_state.mark_all_done = True
    if clear_all_button:
        st.session_state.clear_all = True


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

with st.container(width="stretch", border=True, height=60, gap=None):
    # def add_new_item_func():
    #     new_name = st.session_state.add_new_item_text
    #     #logic for empty string, dupe item etc
    #     if new_name:
    #         # test to see if it already exists in any sub_dicts
    #         current_key = st.session_state["json_data"]["current_list"]
    #         if not item_crosschecker(new_name, 0, st.session_state["json_data"]["existing_lists"][current_key]):
    #             # add it
    #             st.session_state["json_data"]["existing_lists"][current_key]["tier_0_list"]["content_list"][new_name] = False
    #             st.session_state.add_new_item_text = ""
    #         else:
    #             # don't add it
    #             st.warning("Item with this name already exists")

    col1, col2 = st.columns([2,1], vertical_alignment="bottom")
    # with col1:
    #     add_new_item = st.text_input(label=" ", placeholder="add new list item here", on_change=add_new_item_func, key="add_new_item_text")

    with col2:
        if st.button("add module", width="stretch"):
            # get the list for selection box
            module_select_list = []
            for module in st.session_state["json_data"]["modules"]:
                module_select_list.append(module)
            # select box
            st.session_state.add_module_input = st.selectbox("hidden", options=module_select_list, index=None, placeholder="Select module to add", label_visibility="collapsed", key="module_add_key", on_change=module_to_list)


master_sub_list_sort_launch()