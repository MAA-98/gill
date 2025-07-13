import os

def init_gill_dir(debug_bool: bool):
    dir_name = ".gill"
    cwd = os.getcwd()
    gill_path = os.path.join(cwd, dir_name)

    if os.path.exists(gill_path):
        if os.path.isdir(gill_path):
            print(f"Directory '{dir_name}' already exists at {gill_path}")
        else:
            print(f"A file named '{dir_name}' exists at {gill_path}")
            return
    else:
        try:
            os.makedirs(gill_path)
            if debug_bool:
                print(f"Directory '{dir_name}' created at {gill_path}")
        except OSError as e:
            print(f"Error creating directory '{dir_name}': {e}")
            return

    sysprompt_path = os.path.join(gill_path, "sysprompt")
    try:
        # This opens (creates if doesn't exist) and immediately closes the file.
        with open(sysprompt_path, "w") as f:
            f.write("")  # or put some initial content here if you want
        if debug_bool:
            print(f"File 'sysprompt' created at {sysprompt_path}")
    except OSError as e:
        print(f"Error creating file 'sysprompt': {e}")