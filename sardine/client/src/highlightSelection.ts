import { Decoration, DecorationSet } from "@codemirror/view"
import { StateField, StateEffect, ChangeDesc } from "@codemirror/state"
import { EditorView } from "@codemirror/view"
import { invertedEffects } from "@codemirror/commands"
import { Extension } from "@codemirror/state"


function mapRange(range: {from: number, to: number}, change: ChangeDesc) {
    let from = change.mapPos(range.from), to = change.mapPos(range.to)
    return from < to ? {from, to} : undefined
}
  
const addHighlight = StateEffect.define<{from: number, to: number}>({
    map: mapRange
})

const removeHighlight = StateEffect.define<{from: number, to: number}>({
    map: mapRange
})
  
const highlight = Decoration.mark({
    attributes: {style: `background-color: #ffad42`}
})
  
const highlightedRanges = StateField.define({
    create() {
        return Decoration.none
    },
    update(ranges, tr) {
        ranges = ranges.map(tr.changes)
        for (let e of tr.effects) {
            if (e.is(addHighlight))
                ranges = addRange(ranges, e.value)
            else if (e.is(removeHighlight))
                ranges = cutRange(ranges, e.value)
        }
        return ranges
    },
    provide: field => EditorView.decorations.from(field)
})
  
function cutRange(ranges: DecorationSet, r: {from: number, to: number}) {
    let leftover: any[] = []
    ranges.between(r.from, r.to, (from, to, deco) => {
        if (from < r.from) leftover.push(deco.range(from, r.from))
        if (to > r.to) leftover.push(deco.range(r.to, to))
    })
    return ranges.update({
        filterFrom: r.from,
        filterTo: r.to,
        filter: () => false,
        add: leftover
    })
}
  
function addRange(ranges: DecorationSet, r: {from: number, to: number}) {
    ranges.between(r.from, r.to, (from, to) => {
        if (from < r.from) r = {from, to: r.to}
        if (to > r.to) r = {from: r.from, to}
    })
    return ranges.update({
        filterFrom: r.from,
        filterTo: r.to,
        filter: () => false,
        add: [highlight.range(r.from, r.to)]
    })
}
  
  
const invertHighlight = invertedEffects.of(tr => {
    let found = []
    for (let e of tr.effects) {
        if (e.is(addHighlight)) found.push(removeHighlight.of(e.value))
        else if (e.is(removeHighlight)) found.push(addHighlight.of(e.value))
    }
    let ranges = tr.startState.field(highlightedRanges)
    tr.changes.iterChangedRanges((chFrom, chTo) => {
        ranges.between(chFrom, chTo, (rFrom, rTo) => {
        if (rFrom >= chFrom || rTo <= chTo) {
            let from = Math.max(chFrom, rFrom), to = Math.min(chTo, rTo)
            if (from < to) found.push(addHighlight.of({from, to}))
        }
    })
    })
    return found
})
  
export function highlightSelection(view: EditorView) {
    view.dispatch({
        effects: view.state.selection.ranges.filter(r => !r.empty)
            .map(r => addHighlight.of(r))
    })
    return true
}
  
export function unhighlightSelection(view: EditorView) {
    let highlighted = view.state.field(highlightedRanges)
    let effects: any[] = []
    for (let sel of view.state.selection.ranges) {
        highlighted.between(sel.from, sel.to, (rFrom, rTo) => {
        let from = Math.max(sel.from, rFrom), to = Math.min(sel.to, rTo)
        if (from < to) effects.push(removeHighlight.of({from, to}))
    })
    }
    view.dispatch({effects})
    return true
}
  
export function rangeHighlighting(): Extension {
    return [
      highlightedRanges,
      invertHighlight,
    ]
}