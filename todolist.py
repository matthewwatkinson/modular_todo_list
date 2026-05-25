#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### need to make data persistent between sessions

### need to make a list addable to a list

### need to make the starting interface

### add options to mark whole list done/undone

### change list display into numbered list and make that number the toggle selector/remove selector

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
    
def start_menu(message="Welcome to the modular list maker. Please select from the menu below"):
    print(f"""{message}
          
1) Create a new list
2) View an existing list
3) Delete an existing list
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
    
def list_modifier_menu(target_list):
    print(target_list)
    print("""
What would you like to do with your list?

1) Add item
2) Remove item
3) Toggle item
4) Return to main menu
""")
    modifier_valid_menu_selections = ["1", "2", "3", "4"]
    modifier_menu_selection = input("Please input the number of your choice: ")
    if modifier_menu_selection not in modifier_valid_menu_selections:
        print("This is not a valid choice")
        list_modifier_menu(target_list)
    elif modifier_menu_selection == "4":
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


