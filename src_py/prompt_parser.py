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

import sys
from enum import Enum
from typing import Optional
import re
from typing import Tuple, Union

def parse_line_range(s: str) -> Union[Tuple[int], Tuple[int, int]]:
    """
    Parses a string that can represent:

    - a single integer "12"
    - two integers separated by one of these delimiters: "-", ",", "--", ".", ".."
    
    Returns:
        (int,) or (int, int)
        
    Raises:
        ValueError if the string doesn't conform.
    """
    s = s.strip()
    # Pattern to match two numbers separated by delimiters: - , -- . ..
    # We'll consider any of these delimiters, only one of them should exist between two numbers.
    # To be flexible, we consider the longest delimiter first (--, ..), then single (-, .)
    delimiters = ["--", "-", ",", "..", "."]

    # Try single number first
    if re.fullmatch(r"\d+", s):
        return (int(s),)

    # Try to split by delimiters, trying longest first to avoid splitting "12--13" as "12", "-13"
    for delim in delimiters:
        parts = s.split(delim)
        if len(parts) == 2:
            left, right = parts[0].strip(), parts[1].strip()
            if left.isdigit() and right.isdigit():
                return (int(left), int(right))

    raise ValueError(f"String '{s}' is not a recognized integer or integer range with delimiters.")

class InputKind(Enum):
    Message = "message"
    File = "file"
    Line = "line"

def insert_file():
    return None

def parse_prompt_args(args) -> str:
    """
    Parse argv manually to support interleaved -m/--message and -f/--file flags,
    preserving their order in the input.
    """
    flag: Optional[InputKind] = None
    filename: Optional[str] = None
    i = 0

    # ```len(prompt) == 2``` indicates a file has been declared at the point between 
    # the two strings, but not yet inserted. Leaving possibility to insert lines at 
    # the end or the whole file in between the two strings:
    prompt: Union[Tuple[str], Tuple[str, str]] = ("",)

    # def insert_on_newline(prompt: str, new_msg: str)-> str:
    #     if prompt == "":
    #         prompt = new_msg
    #     else:
    #         prompt = prompt + "\n\n" + new_msg
    #     return prompt

    while i < len(args):
        arg = args[i]

        # First checks flags, so you can cancel flags ```gill -f -m "msg"``` == ```gill -m "msg"```
        if arg in ("-m", "--message"):
            flag = InputKind.Message
        elif arg in ("-f", "--file"):
            flag = InputKind.File
        elif arg in ("-l", "--line"):
            flag = InputKind.Line

        # Argument is not a flag, so execute if you have a flag on
        elif flag == InputKind.Message:
            if len(prompt) == 1:
                prompt = (prompt[0] + "\n" + arg + "\n", ) # Can stack messages: ```-m "Msg number 1" "Msg number 2"```
            else:
                prompt = (prompt[0], prompt[1] + "\n" + arg + "\n")
        elif flag == InputKind.File:
            # Can stack filenames: ```-f file0 file1```

            # If file is already inserted then can just go to next, otherwise insert it
            if filename:

                if len(prompt) == 2: # indicates a file was declared but not yet inserted
                    try:
                        with open(filename, "r") as f:
                            content = f.read()
                            prompt = (prompt[0] + f"\n```{filename}\n{content}\n```\n" + prompt[1], "") # empty string to indicate new filename not yet inserted
                    except OSError as e:
                        print(f"Failed reading file {filename}: {e}", file=sys.stderr)
                        raise sys.exit(1)
                else: # old filename inserted already
                    prompt = (prompt[0], "") # empty string to indicate new filename not yet inserted
            else: # no stored filename so just indicate the new file is not yet inserted
                prompt = (prompt[0], "")

            filename = arg # Update filename

        elif flag == InputKind.Line:

            # Can stack lines: ```-f file0 -l 2-14 25 30-45``` so do not clear flag
            # Not stopped from inserting lines in weird combinations!

            if not filename:
                print("No filename given for lines.")
                raise sys.exit(1)
            else:
                # Parse the requested lines, e.g. "12", "12-15", "12,15"
                try:
                    lines_spec = parse_line_range(arg)
                    # Determine which lines to keep
                    if len(lines_spec) == 1:
                        start = lines_spec[0]
                        end = start
                    else:
                        start, end = lines_spec
                except ValueError as e:
                    print(f"Invalid line range '{arg}': {e}", file=sys.stderr)
                    sys.exit(1)
    
                # Open whole file as array of lines
                try:
                    with open(filename, "r") as f:
                        all_lines = f.readlines()
                except OSError as e:
                    print(f"Failed reading file {arg}: {e}", file=sys.stderr)
                    raise sys.exit(1)
                
                # Clip to valid line numbers within file
                start = max(start, 1)
                end = min(end, len(all_lines))
                if start > end:
                    print(f"Invalid line range: start ({start}) > end ({end})", file=sys.stderr)
                    sys.exit(1)

                selected_lines = all_lines[start-1 : end]  # 0-based slicing

                # Join selected lines into a string
                selected_content = ''.join(selected_lines).rstrip('\n')  # strip trailing newlines to control output

                # Create code block with filename header and fenced code block
                if len(lines_spec) == 1:
                    code_block = f"\n```{filename}, line {start}\n{selected_content}\n```\n"
                else:
                    code_block = f"\n```{filename}, lines {start}-{end}\n{selected_content}\n```\n"
                
                # Insert, creating 1-tuple to indicate file was inserted
                if len(prompt) == 1: # indicates lines already inserted
                    prompt = (prompt[0] + code_block, )
                else: # indicates file contents not yet inserted
                    prompt = (prompt[0] + prompt[1] + code_block, )

        else:                                                   # Comes when no message or filename flags have been made
            raise ValueError(f"Unexpected argument {args[i]}")
        i += 1

    # Take care of possible dangling file at the end
    if filename and len(prompt) == 2:  # indicates a file was declared but not yet inserted
        try:
            with open(filename, "r") as f:
                content = f.read()
                prompt = (prompt[0] + f"\n```{filename}\n{content}\n```\n" + prompt[1], )
        except OSError as e:
            print(f"Failed reading file {filename}: {e}", file=sys.stderr)
            raise sys.exit(1)

    # strip new lines on both sides
    return prompt[0].strip('\n') # tuple should be length 1 anyway, TODO: casting and type checks