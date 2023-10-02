import os
import re
import xml.etree.ElementTree as ET


def highest_numbers_in_subfolders(parent_directory):
    results = {}

    # Directly iterate over subfolders in the parent directory
    for subfolder in os.listdir(parent_directory):
        subfolder_path = os.path.join(parent_directory, subfolder)

        # Only consider directories (skip files)
        if os.path.isdir(subfolder_path):
            highest_number = -1

            # Check files inside the subfolder
            for filename in os.listdir(subfolder_path):
                if filename.endswith(".png"):
                    number_part = "".join(
                        [char for char in filename if char.isdigit()]
                    )  # Extract numbers

                    if number_part:  # if there is any number in the filename
                        num = int(number_part)
                        if 1 <= num <= 999999 and num > highest_number:
                            highest_number = num

            # If any valid number is found in the subfolder, add it to results
            if highest_number != -1:
                results[subfolder] = highest_number

    return results


def update_record(record, max_numbers):
    from_attr = record.get("from")
    if from_attr and "/" in from_attr:
        first_folder, second_folder = from_attr.split("/")

        # print(f"Debug: Trying to match '{second_folder}'")  # Debug line

        # Use regular expressions to separate the string and numeric parts
        match = re.match(r"([a-zA-Z\s]+)(\d+)$", second_folder)

        if match:
            second_folder, number = match.groups()
        else:
            print(
                f"Skipping this record as it doesn't match the expected pattern: {second_folder}"
            )
            return

        # Determine if the string values match or not
        string_values_match = first_folder.lower() == second_folder.lower()

        # Get the max number for the folder
        max_number = max_numbers.get(second_folder, None)

        # Initialize the new number as the original number
        new_number = number

        # If the max number exists and is less than the original number, update the new number
        try:
            num_as_int = int(number)
            if max_number is not None and num_as_int > max_number:
                new_number = str(min(num_as_int, max_number))
        except ValueError:
            print(f"Could not convert '{number}' to integer. Skipping this record.")
            return

        # Update the record if either the string values don't match or the number has changed
        if not string_values_match or new_number != number:
            new_from = f"{second_folder}/{second_folder}{new_number}"
            record.set("from", new_from)
            print(
                f"Record updated: Previous value '{from_attr}', New value '{new_from}'"
            )


def update_xml_file(file_path, max_numbers):
    tree = ET.parse(file_path)
    root = tree.getroot()

    list_element = root.find(".//list[@id='maps']")
    if list_element is not None:
        for record in list_element.findall("record"):
            update_record(record, max_numbers)

    # Save the updated XML back to the file
    tree.write(file_path)


if __name__ == "__main__":
    parent_folder_path = input("Enter the parent directory path: ")
    result_dict = highest_numbers_in_subfolders(parent_folder_path)
    for subfolder, highest_num in result_dict.items():
        print(f"{subfolder}: {highest_num}")
    file_path = input("Enter the path to the XML file: ")
    update_xml_file(file_path, result_dict)
    print(f"XML file at {file_path} has been updated.")
