import {keymap, highlightSpecialChars, drawSelection, highlightActiveLine, dropCursor,
    rectangularSelection, crosshairCursor,
    lineNumbers, highlightActiveLineGutter} from "@codemirror/view"
import { EditorState } from "@codemirror/state"
import {
    syntaxHighlighting, 
    indentOnInput, 
    bracketMatching,
    indentUnit,
    foldGutter, foldKeymap} from "@codemirror/language"
import {defaultKeymap, history, historyKeymap} from "@codemirror/commands"
import {searchKeymap, highlightSelectionMatches} from "@codemirror/search"
import {autocompletion, completionKeymap, closeBrackets, closeBracketsKeymap} from "@codemirror/autocomplete"
import {lintKeymap} from "@codemirror/lint"
import { SardineTheme } from "./SardineTheme"
import { python } from "@codemirror/lang-python";


// Still haven't imported my own theme
export const SardineBasicSetup = (() => [
    SardineTheme,
    python(),
    lineNumbers(),
    indentUnit.of("    "),
    highlightActiveLineGutter(),
    highlightSpecialChars(),
    drawSelection(),
    indentOnInput(),
    // syntaxHighlighting(defaultHighlightStyle, {
    //     fallback: true
    // }),
    rectangularSelection(),
    crosshairCursor(),
    highlightActiveLine(),
    highlightSelectionMatches(),
    keymap.of([
    ...closeBracketsKeymap,
    ...defaultKeymap,
    ...searchKeymap,
    ...historyKeymap,
    ...foldKeymap,
    ...completionKeymap,
    ...lintKeymap
    ])
    ]
)()
