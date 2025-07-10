# gill

**gill** is a command-line utility for building prompts to send to an LLM (currently only OpenAI API). It allows you to quickly construct prompts by interleaving textual messages and code excerpts from files, precisely selecting lines and controlling their order in the final prompt. This makes it ideal for convenient everyday use of a developer.

---

## Features

- **Flexible Prompt Building:** Compose prompts from messages (`-m`), whole files (`-f`), or precise line ranges within files (`-l`).
- **Order Preserved:** The order of `-m`, `-f`, and `-l` flags and their arguments is preserved, letting you craft exactly the prompt you want, in the order you want.
- **Stacked Arguments:** Pass multiple files or lines in a row for conciseness.
- **Line Extraction:** Reference line(s) or ranges from the most recent file argument so you can excerpt code and send only what’s needed.
- **Fenced Code Blocks:** Files and line selections are output as Markdown code blocks with filepath and line context.
- **Test mode:** Learn what prompts your commands make wihtout sending to the API with a beginning `--test` flag.

---

## Installation



---

## Usage

```bash
gill [-m|--message <text> ...] [-f|--file <filename> ...] [-l|--line <range> ...] ...
```

- Use `-l` only after a file flag; it applies to the most recent file.
- **Order is preserved**, and each flag can take multiple arguments.

## Test Usage

```bash
gill --test [-m|--message <text> ...] [-f|--file <filename> ...] [-l|--line <range> ...] ...
```

- Prepend with '--test' command to print the prompt created, rather than sending to API.

### Examples

#### Simple prompt with a message

```bash
gill -m "What's the capital of Australia?"
```

#### Insert a whole file

```bash
gill -m "Explain this script line-by-line: " -f myscript.py
```

#### Insert just a range of lines from a file

```bash
gill -m "What does this function do?" -f ./src/main.cpp -l 120-145
```

#### Build a multi-part prompt

```bash
gill -m "Compare these two:" -f file1.py -l 2-10 -f file2.py -l 3-8
```

#### Mixing multiple messages and files

```bash
gill -m "A bug is happening in these segments." -f bug.py -l 14-23 45,46 -m "Here's the log:" -f error.log -l 2
```

#### Test mode (print prompt only, don’t send)

```bash
gill --test -m "Explain this function." -f my.py -l 22-40
```

---

## Line Range Syntax

Line ranges for `-l` flags can be specified flexibly:

- Single line: `-l 8`
- Range: `-l 12-15`
- Comma: `-l 20,24`
- Double hyphen or double dot: `-l 50--60` or `-l 50..60`
- Multiple `-l` flags/args can stack for multiple excerpts from one file.

---

## Output Format

Relevant file or line excerpts are embedded as Markdown fenced code blocks with filenames and line info for clarity:

<pre>
<code>
```file.py, lines 23-30
(def foo...
# code here
)
```
</code>
</pre>

Messages are inserted as plain text sections, separated by blank lines.

---

## Under the Hood

- Prompts are built in command-line order.
- Files and lines are read as-needed, and errors are surfaced clearly.
- API calls are handled through your `llm_api.ask_openai()` implementation (not included here).

---

## Exit Codes & Error Handling

- Exits with code 1 and a message on invalid arguments, missing files, or API errors.

---

## Development

- Requires Python 3.7+.
- Needs a local `llm_api.py` with an `ask_openai(prompt: str)->str` function.
- PRs and issues welcome!

---

## License

MIT License (include actual text as desired).

---

## Example Workflow

```bash
gill -m "Please explain the bug in these lines." -f foo.py -l 33-86 -m "This, too:" -f bar.py -l 15-20 --test
```
Output:
```markdown
Please explain the bug in these lines.

```foo.py, lines 33-86
# foo.py lines 33-86...
```

This, too:

```bar.py, lines 15-20
# bar.py lines...
```
```

---

## Contributing

Feedback, feature requests, and bug reports are welcomed! Open an issue or PR.

---

**Questions?**  
Feel free to open an issue!

---

*Craft powerful LLM prompts, right from your shell.*