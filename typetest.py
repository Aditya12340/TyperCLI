#!/usr/bin/env python3
"""Minimal CLI typing test — Monkeytype-style. Stdlib only."""
import curses
import os
import random
import time

WORDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "words.txt")

with open(WORDS_FILE) as f:
    WORDS = f.read().split()


def gen_words(n=25):
    return [random.choice(WORDS) for _ in range(n)]


def run(stdscr):
    curses.curs_set(1)
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_WHITE, -1)

    words = gen_words()
    target = " ".join(words)
    typed = ""
    start = None
    errors = 0

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        stdscr.addstr(0, 0, "monkeytype-cli  |  esc to quit  |  start typing to begin")

        row, col = 2, 0
        for i, ch in enumerate(target):
            if col >= w - 1:
                row += 1
                col = 0
            if i < len(typed):
                attr = curses.color_pair(1) if typed[i] == ch else curses.color_pair(2)
            else:
                attr = curses.color_pair(3)
            try:
                stdscr.addstr(row, col, ch, attr)
            except curses.error:
                pass
            col += 1

        if start:
            elapsed = max(time.time() - start, 0.01)
            wpm = (len(typed) / 5) / (elapsed / 60)
            acc = 100 * max(len(typed) - errors, 0) / max(len(typed), 1)
            stdscr.addstr(row + 2, 0, f"WPM: {wpm:5.1f}   ACC: {acc:5.1f}%   time: {elapsed:4.1f}s")

        stdscr.refresh()

        if len(typed) >= len(target):
            break

        try:
            key = stdscr.get_wch()
        except curses.error:
            continue

        if key == chr(27):  # ESC
            return None

        if start is None:
            start = time.time()

        if key in ("\b", "\x7f", curses.KEY_BACKSPACE):
            if typed:
                if typed[-1] != target[len(typed) - 1]:
                    errors = max(errors - 1, 0)
                typed = typed[:-1]
            continue

        if isinstance(key, str) and len(key) == 1 and key.isprintable():
            if len(typed) < len(target):
                if key != target[len(typed)]:
                    errors += 1
                typed += key

    elapsed = time.time() - start
    wpm = (len(typed) / 5) / (elapsed / 60)
    acc = 100 * max(len(typed) - errors, 0) / max(len(typed), 1)
    return wpm, acc, elapsed


def main():
    result = curses.wrapper(run)
    if result:
        wpm, acc, elapsed = result
        print(f"\nDone! WPM: {wpm:.1f}  Accuracy: {acc:.1f}%  Time: {elapsed:.1f}s")
    else:
        print("\nQuit early.")


if __name__ == "__main__":
    main()
