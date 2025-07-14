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

from openai import OpenAI
from openai.types.responses import ResponseStreamEvent
from openai.types.chat import ChatCompletionChunk

from typing import Iterator
import os
import re

client = OpenAI()

# See general docs at: https://platform.openai.com/docs/guides/
# For streaming CC: https://platform.openai.com/docs/api-reference/chat-streaming

def ask_openai(prompt: str) -> Iterator[ChatCompletionChunk]:
    cwd = os.getcwd()
    dir_name = ".gill"
    gill_path = os.path.join(cwd, dir_name)
    sysprompt_path = os.path.join(gill_path, "sysprompt")

    if os.path.isfile(sysprompt_path):
        with open(sysprompt_path, "r", encoding="utf-8") as f:
            sysprompt_content = f.read()
            # Remove trailing newlines, spaces, or carriage returns for request
            prompt = prompt.rstrip('\n\r ')
            # Remove unwanted control chars except \n and tabs if you want:
            prompt = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F]', '', prompt)
    else:
        sysprompt_content = ""

    return client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "developer", "content": sysprompt_content},
            {"role": "user", "content": prompt}
        ],
        stream=True,
    )