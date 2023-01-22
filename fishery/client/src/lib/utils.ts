/**
 * This function is used to capture user code and to transmit
 * it to the Flask Server running along the Fishery instance.
 * 
 * @param event Key Event received by the handler
 */
export function kedDownHandler(event) {
    if(event.key === 'Enter' && event.shiftKey) {
      event.preventDefault();
      executeCode(getSelectedLines()+"\n\n");
    }
  }

/**
 * 
 * This function grabs the current selection from the CodeMirror editor
 * and transmits the data to the Flask server running inside Fishery.
 * 
 * @returns Current selection of user code sent for evaluation
 */
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