export function kedDownHandler(event) {
    // Ctrl + Enter
    if(event.key === 'Enter' && event.shiftKey) {
      event.preventDefault();
      executeCode(getSelectedLines()+"\n\n");
    }
  }

export function getSelection() {
    const { from, to } = codeMirror.current?.view?.state?.selection.main
    return codeMirror.current?.view?.state?.doc.sliceString(from, to)
  }

export function getSelectedLines() {
    // Get the current state of the editor
    const state = codeMirror.current?.view?.state;

    // Get the current selection
    const { from, to } = state?.selection.main

    // Get the line the cursor is currently on
    const fromLine = state?.doc.lineAt(from)
    const toLine = state?.doc.lineAt(to)

    return state?.doc.sliceString(fromLine.from, toLine.to)
  }

  export default { kedDownHandler, getSelection, getSelectedLines}