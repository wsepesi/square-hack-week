import os
import shutil

def bubbler_upper(source_dir, destination_dir):
    file_names = []
    iterator = 0

    # Create the destination directory if it doesn't exist
    os.makedirs(destination_dir, exist_ok=True)

    # Traverse the source directory recursively
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.json'):
                # Get the full path of the JSON file
                source_path = os.path.join(root, file)
                thing = source_path.split('/')
                thing = thing[1:-1]
                thing = '_'.join(thing)
                if len(thing) > 0:
                    thing += "_"
                # Add the identifier tag to the file name
                file_name, extension = os.path.splitext(file)

                new_file_name = f"{thing}{file_name}{extension}"

                # Move the JSON file to the destination directory with the modified file name
                destination_path = os.path.join(destination_dir, new_file_name)
                shutil.move(source_path, destination_path)

                # Append the modified file name to the list
                iterator += 1
                file_names.append(new_file_name)

    return file_names

# # Example usage
# source_directory = 'slackmessages'
# destination_directory = 'slackmessages2'


# json_files = slack_bubbler_upper(source_directory, destination_directory)
# print("JSON files moved:")
# for file_name in json_files:
#     print(file_name)
