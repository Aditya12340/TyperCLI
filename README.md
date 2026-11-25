# typetest-cli
 
A tiny Monkeytype clone for your terminal made by Claude
## What it does
 
Shows you a line of words. You type them. Correct characters turn green, mistakes turn red. When you finish, it prints your WPM and accuracy.
 
## How it works
 
- **Word list**: `words.txt` holds ~1000 common English words, one giant space-separated blob. On startup the script reads it and splits it into a list.
- **Prompt generation**: `gen_words(n=25)` picks `n` random words from that list and joins them into one string — that's your typing prompt.
- **Rendering**: Uses Python's built-in `curses` library to draw text directly to the terminal. Each character in the prompt gets colored based on whether you've typed it yet, and if so, whether it matches:
  - white = not typed yet
  - green = correct
  - red = wrong
- **Input loop**: Reads one keystroke at a time (`get_wch()`), updates the "typed" buffer, redraws the screen, and checks for backspace / Esc.
- **Scoring**: Once you've typed the full prompt, WPM is calculated as `(characters typed / 5) / (minutes elapsed)` — the standard "5 chars = 1 word" convention — and accuracy is `(correct chars / total typed) * 100`.
 
## Setup
 
Requires Python 3 (preinstalled on macOS/Linux; on Windows use WSL, since `curses` isn't native there).
 
```bash
git clone https://github.com/Aditya12340/typetest-cli.git
cd typetest-cli
python3 typetest.py
```
 
Make sure `typetest.py` and `words.txt` stay in the same folder — the script loads the word list relative to its own location.
 
## Customizing the word list
 
`words.txt` is just plain text, space- or newline-separated. Add, remove, or swap in your own words and save — no code changes needed.
 
## Controls
 
- Start typing to begin the timer
- Backspace to fix mistakes
- `Esc` to quit early
## License
 
MIT — do whatever you want with it.
 
