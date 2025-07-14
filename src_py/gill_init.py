# Copyright 2025 Marek Antoni Kurczynski (also known as Mark Alexander Anthony)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

def gill_init(debug_bool: bool, args: list[str]):
    dir_name = ".gill"
    cwd = os.getcwd()
    gill_path = os.path.join(cwd, dir_name)

    if os.path.exists(gill_path):
        if os.path.isdir(gill_path):
            raise IsADirectoryError(f"Directory already exists at {gill_path}. Delete or move it and try again.")
        else:
            raise FileExistsError(f"A file named '{dir_name}' exists at {cwd}. Delete or move it and try again.")
    else:
        try:
            os.makedirs(gill_path)
            if debug_bool:
                print(f"Directory '{dir_name}' created at {gill_path}")
        except OSError as e:
            raise OSError(f"Error creating directory '{dir_name}': {e}")

    sysprompt_path = os.path.join(gill_path, "sysprompt")
    try:
        # This opens (creates if doesn't exist) and immediately closes the file.
        with open(sysprompt_path, "w") as f:
            f.write("")  # or put some initial content here if you want
        if debug_bool:
            print(f"File 'sysprompt' created at {sysprompt_path}")
    except OSError as e:
        raise OSError(f"Error creating file 'sysprompt': {e}")