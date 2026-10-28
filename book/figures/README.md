# Figures

Each figure is two files: `<id>.svg` (the drawing) and `<id>.yaml` (its words, one block per language). A chapter shows it with `::: figure <id>`. The build puts the words in, and the theme gives the colours, so one drawing serves every language and every theme.

## Rules (the build stops when one is broken)

- **No colour, no style.** No `#hex`, `rgb()`, colour names, `style=` or `<style>`. Use only the classes below.
- **No words in the SVG.** Every `<text>` has `data-t="<key>"`, and the key is in the YAML for every language. The text inside the SVG is a placeholder.
- **A caption** for every language (`caption:` in the YAML).

## Size

- `viewBox` 600 wide. That is about the width of the text column on a desktop and is still readable on a phone.
- Leave room: a Chinese line is shorter than an English one, a German one would be longer. Keep labels to a few words.
- One idea per figure. If it needs a long sentence, the sentence goes in the text, not the figure.

## Classes

The style is "lit and dimmed": one accent colour marks what matters; everything else is dimmed. Do not use a class for decoration.

| Class | Use it for |
| --- | --- |
| `box` | A thing (an agent, a file, a step) |
| `box-lit` | The thing the figure is about |
| `box-plain` | Something outside, optional or refused (dashed) |
| `label` | Normal text |
| `label-lit` | Text on or about the lit thing |
| `label-muted` | Small notes, axis names, values |
| `label-big` | One big number or word, at most one per figure |
| `line`, `line-lit` | Connections |
| `head`, `head-lit` | Arrow heads (a small `<path>` triangle; no markers) |
| `bar`, `bar-lit` | Bars in a comparison |

## Steps

A figure that shows a process can be stepped through. Give an element `data-step="n"`: it appears at step n. Elements with no `data-step` show from the start. The YAML then needs `step-1` … `step-N` for every language: one short sentence per step, shown under the figure.

The reader moves with Back and Next. Without JavaScript the whole figure shows, with all the steps as a list, so it still reads.

Use steps for a process, not for decoration. A comparison or a map stays one picture.

## Numbers

A number in a figure comes from a source the chapter names (a test guide, a report, a doc in the harness). Write "about" when it is from one run.
