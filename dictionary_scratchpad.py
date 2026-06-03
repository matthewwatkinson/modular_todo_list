#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def list_builder(name: str, content_list=[], tier=0):
    list_container = {}
    list_container["list_name"] = name
    list_container["list_tier"] = tier
    list_container["content_list"] = {}
    for item in content_list:
        list_container["content_list"][item] = False

    return list_container

def item_crosschecker(new_item: str, new_item_tier: int, check_dict: dict):
    # check against a dict that represents the [current_shown_list] of the master dict (dict of list_builder_dicts)
    # flag if action needs to be taken outside of function (action: don't include new_item in the list being added)
    cancel_insert = False
    for sub_dict in check_dict:
        # will this list mod work when multiple sub_dicts?
        for key in list(check_dict[sub_dict]["content_list"].keys()):
            if key == new_item:
                # compare tiers
                check_tier = check_dict[sub_dict]["list_tier"]
                if new_item_tier < check_tier:
                    # new_item is in the senior dict, so delete from check_dict
                    del check_dict[sub_dict]["content_list"][key]
                else:
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


# test_list = ["red", "yellow", "green", "purple", "black"]
# another_test_list = ["1", "x", "gg"]
# check_list = ["shoe", "sock", "red", "gg", "black"]

# test_dict = list_builder("test", test_list, 1)
# another_test_dict = list_builder("another_test", another_test_list, 1)
# check_dict = list_builder("check", check_list, 1)
# #print(check_dict)
# test_summary_dict = {}
# test_summary_dict[test_dict["list_name"]] = test_dict
# test_summary_dict[another_test_dict["list_name"]] = another_test_dict
# #print(test_summary_dict)

# # check when no dupes
#first_check = item_crosschecker("hair", 1, test_summary_dict)
#print(first_check)

# check when dupe, and new item is in junior list
#second_check = item_crosschecker("green", 1, test_summary_dict)
#print(second_check)

# check when dupe, and new item is senior
#third_check = item_crosschecker("green", 0, test_summary_dict)
#print(third_check)
#print(test_summary_dict)

#big_check = list_crosschecker(check_dict, test_summary_dict)
#print(big_check)
#print(test_summary_dict)