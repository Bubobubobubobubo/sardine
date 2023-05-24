import {keymap, highlightSpecialChars, drawSelection, highlightActiveLine, dropCursor,
    rectangularSelection, crosshairCursor,
    lineNumbers, highlightActiveLineGutter} from "@codemirror/view"
import {
    syntaxHighlighting, 
    indentOnInput, 
    indentUnit,
    foldKeymap} from "@codemirror/language"
import {defaultKeymap, history, historyKeymap} from "@codemirror/commands"
import {highlightSelectionMatches} from "@codemirror/search"
import {closeBrackets} from "@codemirror/autocomplete"
import {lintKeymap} from "@codemirror/lint"
import { SardineTheme } from "./SardineTheme"
import { python } from "@codemirror/lang-python";

// This is a stripped down editor. It is more than enough for playing with small
// Python files!
export const SardineBasicSetup = (() => [
    SardineTheme,
    python(),
    lineNumbers(),
    history(),
    indentUnit.of("    "),
    highlightActiveLineGutter(),
    highlightSpecialChars(),
    drawSelection(),
    indentOnInput(),
    rectangularSelection(),
    crosshairCursor(),
    highlightActiveLine(),
    highlightSelectionMatches(),
    keymap.of([
    ...defaultKeymap,
    ...foldKeymap,
    ...historyKeymap,
    ...lintKeymap
    ])
    ]
)()
