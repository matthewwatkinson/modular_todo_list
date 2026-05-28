#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import jsonpickle

### add the module delete function

### add list rename to list modifier menu

### need to make a list addable to a list

### change list display into numbered list and make that number the toggle selector/remove selector

### is a manual save option required for module edit? can we just save when program ends? write simple end() function to make sure the save doesn't get skipped

### should modules have descriptions?

class ListItem:
    # each list item belongs to an owner_list, has a name and a done/not_done state

    def __init__(self, item_name, state="not_done", owner_list="unknown"):
        self.item_name = item_name
        self.state = state
        self.owner_list = owner_list

    def __str__(self):
        # print all the info we know about this item
        return f"task: {self.item_name} belongs to {self.owner_list} and is {self.state}"
    
    def __eq__(self, other):
        return self.item_name == other

    def status_change(self):
        # toggles between done and not done
        if self.state == "not_done":
            self.state = "done"
        else:
            self.state = "not_done"

    def name_change(self, new_name: str):
        # edit the item name
        self.item_name = new_name

class ListModule:

    def __init__(self, list_name):
        # create a new to-do list
        self.list_name = list_name
        self.item_list = []

    def add_item(self, new_item_name: str):
        # add a new item, put in list if does not already exists and is valid input
        if not new_item_name:
            print("\nPlease provide a valid task name in order to add to list")
            return
        if new_item_name in self.item_list:
            print(f"\nThe to-do item '{new_item_name}' already exists.")
        else:
            self.item_list.append(ListItem(new_item_name, "not_done", self.list_name))
            print(f"\n{new_item_name} added successfully.")

    def remove_item(self, existing_item: str):
        # remove an item, if it exists and is valid input, and list not empty
        if not self.item_list:
            print("\nThere are no items in this list")
            list_modifier_menu(self)
        if not existing_item:
            print("\nPlease provide a valid task name in order to remove from list")
            return
        if existing_item in self.item_list:
            self.item_list.remove(existing_item)
            print(f"\n{existing_item} removed successfully.")
        else:
            print(f"\nThe to-do item '{existing_item}' does not exist.")

    def item_toggle(self, target):
        #toggle an item, if it exists
        if target not in self.item_list:
            print(f"{target} is not an item in this list")
        else:
            target_index = self.item_list.index(target)
            self.item_list[target_index].status_change()

    def all_done(self, message):
        for item in self.item_list:
            item.state = "done"
        if message == 1:
            print(f"All items in {self.list_name} set to 'done'")
    
    def all_undone(self, message):
        for item in self.item_list:
            item.state = "not_done"
        if message == 1:
            print(f"All items in {self.list_name} set to 'not_done'")

    def __str__(self):
        print_string = "\n"
        if not self.item_list:
            return "\nYour list does not have any items yet"
        for item in self.item_list:
            done = "x"
            if item.state == "done":
                done = "o"
            print_string += f" {done} | {item.item_name} belongs to {item.owner_list} and is {item.state}\n"
        return print_string
    
    def display_as_line(self):
        list_length = len(self.item_list)
        name_length = len(self.list_name)
        spaces = " " * (20 - name_length)
        #print 20 total name and spaces
        print(f"{self.list_name}{spaces}contains {list_length} items")

    def display_as_module(self):
        print(f"\nThe module {self.list_name} contains the following items:\n")
        for i in self.item_list:
            print(i.item_name)
    
    def save_as_module(self):
        # add the currently displayed list to the module dictionary after setting all items to "undone"
        # unless already exists or empty
        if self.list_name in module_dictionary:
            overwrite_choice = input("\nA module with this name already exists. Would you like to overwrite the existing module y/n? ")
            if overwrite_choice == "n":
                print("You can rename the list and save as a new module\n")
                list_modifier_menu(self)
        else:
            if not self:
                print("Can not save empty list as module")
                list_modifier_menu(self)
            self.all_undone(0)
            module_dictionary[self.list_name] = self
            #save to json
            json_compatible_module_dict = jsonpickle.encode(module_dictionary)
            with open("module_list_storage.json", "w") as f:
                json.dump(json_compatible_module_dict, f, indent=2, )
            print(f"Added to modules as {self.list_name}")
            list_modifier_menu(self)

    def module_delete(self):
            are_you_sure = input(f"\nAre you sure you wish to permanently delete '{self.list_name}'?  y/n: ")
            if are_you_sure == "y":
                del module_dictionary[self.list_name]
                print(f"\n'{self.list_name}' successfully deleted")
                #save to json
                json_compatible_module_dict = jsonpickle.encode(module_dictionary)
                with open("module_list_storage.json", "w") as f:
                    json.dump(json_compatible_module_dict, f, indent=2, )
                module_display_menu()
            else:
                module_display_menu()


    
def start_menu(message="Welcome to the modular list maker. Please select from the menu below"):
    print(f"""{message}
          
1) Create a new list
2) View an existing list
3) View list modules
4) Exit program
""")
    valid_menu_selections = ["1", "2", "3", "4"]
    menu_selection = input("Please input the number of your choice: ")
    if menu_selection not in valid_menu_selections:
        start_menu("Please select a number from the menu")
    elif menu_selection == "4":
        # exit to terminal
        print("Thank you for using the program")
        return
    elif menu_selection == "1":
        #make and display a list
        list_name = input("What would you like to name your list? ")
        new_list = ListModule(list_name)
        print(f"New list {list_name} created")
        list_modifier_menu(new_list)
    elif menu_selection == "3":
        # launch module display
        module_display_menu()
    
def list_modifier_menu(target_list):
    print(target_list)
    print("""
What would you like to do with your list?

1) Add item
2) Remove item
3) Toggle item
4) Save as module
5) Return to main menu
""")
    modifier_valid_menu_selections = ["1", "2", "3", "4", "5"]
    modifier_menu_selection = input("Please input the number of your choice: ")
    if modifier_menu_selection not in modifier_valid_menu_selections:
        print("This is not a valid choice")
        list_modifier_menu(target_list)
    elif modifier_menu_selection == "5":
        # exit to main menu
        start_menu()
    elif modifier_menu_selection == "1":
        #add an item
        new_item_name = input("\nInput item to be added: ")
        target_list.add_item(new_item_name)
        list_modifier_menu(target_list)
    elif modifier_menu_selection == "2":
        # remove an item, unless there are none yet
        if not target_list.item_list:
            print("\nThe list is empty. Please add some items first.")
            list_modifier_menu(target_list)
        remove_item_name = input("\nInput item to be removed: ")
        target_list.remove_item(remove_item_name)
        list_modifier_menu(target_list)
    elif modifier_menu_selection == "3":
        if not target_list.item_list:
            print("\nThe list is empty. Please add some items first.")
            list_modifier_menu(target_list)
        toggle_target = input("\nWhich list item would you like to toggle? ")
        target_list.item_toggle(toggle_target)
        list_modifier_menu(target_list)
    elif modifier_menu_selection == "4":
        target_list.save_as_module()
        list_modifier_menu(target_list)

def module_display_menu():
    # first display all the modules
    print("\nThese are the currently saved modules\n")
    for l in module_dictionary:
        l_test = module_dictionary[l]
        l_test.display_as_line()

    print("""
What would you like to do?

1) Create new module
2) Delete existing module
3) Edit existing module
4) Return to main menu
""")
    module_display_valid_menu_selections = ["1", "2", "3", "4"]
    module_menu_selection = input("Please input the number of your choice: ")
    if module_menu_selection not in module_display_valid_menu_selections:
        print("\nThis is not a valid choice\n")
        module_display_menu()
    elif module_menu_selection == "4":
        start_menu()
    elif module_menu_selection == "2":
        # delete the module, if input correct, with confirmation
        delete_target = input("\nWhich module would you like to delete? ")
        if delete_target not in module_dictionary:
            print("\nThat module does not exist")
            module_display_menu()
        else:
            module_dictionary[delete_target].module_delete()
    elif module_menu_selection == "3":
        selected_module = input("\nWhich module would you like to edit? ")
        module_modifier_menu(module_dictionary[selected_module])

def module_modifier_menu(target_module):
    target_module.display_as_module()
    print("""
What would you like to do with your module?

1) Add item
2) Remove item
3) Save changes
4) Return to modules
""")
    module_modifier_valid_menu_selections = ["1", "2", "3", "4"]
    module_modifier_menu_selection = input("Please input the number of your choice: ")
    if module_modifier_menu_selection not in module_modifier_valid_menu_selections:
        print("This is not a valid choice")
        module_modifier_menu(target_module)
    elif module_modifier_menu_selection == "4":
        # exit to module menu
        module_display_menu()
    elif module_modifier_menu_selection == "1":
        #add an item
        new_item_name = input("\nInput item to be added: ")
        target_module.add_item(new_item_name)
        module_modifier_menu(target_module)
    elif module_modifier_menu_selection == "2":
        # remove an item, unless there are none yet
        # perhaps this should suggest deletion if only one item?
        if not target_module.item_list:
            print("\nThe module is empty. Please add some items first.")
            module_modifier_menu(target_module)
        remove_item_name = input("\nInput item to be removed: ")
        target_module.remove_item(remove_item_name)
        module_modifier_menu(target_module)
    elif module_modifier_menu_selection == "3":
        target_module.save_as_module()

module_dictionary = {}

with open("module_list_storage.json", "r") as f:
    module_dictionary_pickled = json.load(f)

module_dictionary = jsonpickle.decode(module_dictionary_pickled, classes=[ListModule, ListItem])

start_menu()

# test_list = ListModule("test_list")
# test_list.add_item("cooking")
# test_list.add_item("cleaning")
# test_list.add_item("cleaning")
# input_test = input("Input the task that you would like to add to the list: ")
# test_list.add_item(input_test)

# print(test_list)
# test_list.remove_item("polishing")
# test_list.remove_item("cleaning")

# print(test_list)


