import type { Extension } from "@codemirror/state"
import { keybindingsMessage } from "./help/keybindingsHelp";
import { generalTutorials } from "./help/generalHelp";
import { RunnerService } from "./RunnerService";
import { EditorState, Compartment } from "@codemirror/state"
import { vim } from "@replit/codemirror-vim";
import { EditorView } from "codemirror";
import { python } from "@codemirror/lang-python";
import { editorSetup } from "./EditorSetup";
import { ViewUpdate } from "@codemirror/view";
import { type Settings, AppSettings } from "./AppSettings";
import { 
  highlightSelection, 
  unhighlightSelection, 
  rangeHighlighting 
} from "./highlightSelection";
import './style.css';

interface SavedFiles { [key: string]: string }

class Editor {

  // Settings storage
  settings: AppSettings = new AppSettings()
  buffers: SavedFiles

  // CodeMirror related attributes
  userPlugins: Extension[]  = []

  // Communication with REPL
  runnerService: any
  // logs: string[]

  // Is Sardine Playing?
  playing: boolean = true

  // Is the footer window open?
  footer_open: boolean = false

  play_button: HTMLButtonElement = document.getElementById('play-pause') as HTMLButtonElement
  save_button: HTMLButtonElement = document.getElementById('save-buffer') as HTMLButtonElement
  open_info: HTMLButtonElement = document.getElementById('open-info') as HTMLButtonElement
  share_buffer: HTMLButtonElement = document.getElementById('share-buffer') as HTMLButtonElement
  clear_button: HTMLButtonElement = document.getElementById('clear-buffers') as HTMLButtonElement
  file_selector: HTMLSelectElement = document.getElementById('file-selector') as HTMLSelectElement

  // Footer
  footer_content: HTMLDivElement = document.getElementById('footer-content') as HTMLDivElement
  settings_content: HTMLDivElement = document.getElementById('settings-content') as HTMLDivElement
  // logs_button: HTMLButtonElement = document.getElementById('logs-button') as HTMLButtonElement
  docs_button: HTMLButtonElement = document.getElementById('docs-button') as HTMLButtonElement
  settings_button: HTMLButtonElement = document.getElementById('settings-button') as HTMLButtonElement

  // Checkboxes
  vim_mode_checkbox: HTMLInputElement = document.getElementById('vim-mode-checkbox') as HTMLInputElement
  font_selector: HTMLSelectElement = document.getElementById('font-selector') as HTMLSelectElement

  view: EditorView
  selectedBuffer: string = "Default"
  editorExtensions: Extension[];
  state: EditorState;

  constructor(runnerService: RunnerService) {
    // Loading the files from the localStorage
    this.buffers = {
      "Default": "// This is Sardine Web",
      ...generalTutorials
    }

    if (localStorage.getItem("sardine_buffers") !== null) {
      console.log('Loading files from localStorage')
      this.buffers = JSON.parse(localStorage.getItem("sardine_buffers")!)
      this.buffers = {
        ...this.buffers, 
        ...generalTutorials
      };
    } else {
      console.log('Creating empty files')
      localStorage.setItem("sardine_buffers", JSON.stringify(this.settings))
    }

    // The Runner Service is our connexion to the REPL
    this.runnerService = runnerService;
    // this.logs = [];

    // setInterval(() => {
    //   runnerService.watchLogs((log) => {
    //     this.logs = [...this.logs, log];
    //   });
    // }, 1000)


    this.editorExtensions = [
      rangeHighlighting(),
      editorSetup, python(),
      EditorView.updateListener.of((v:ViewUpdate) => {
        if (v.docChanged) {
          this.buffers[this.selectedBuffer] = v.state.doc.toString()
        }
      }),
      ...this.userPlugins
    ]

    let dynamicPlugins = new Compartment;
    this.state = EditorState.create({
      extensions: [
        ...this.editorExtensions,
        dynamicPlugins.of(this.userPlugins)
      ],
      doc: this.buffers[this.selectedBuffer],
    })


    // Building a CodeMirror editor!
    this.view = new EditorView({
      parent: document.getElementById('editor') as HTMLElement,
      state: this.state
    });

    document.addEventListener('keydown', (event: KeyboardEvent) => {
		  // Cancel 'tab' from being used as a navigation key
		  if (event.key === 'Tab') {
		  	event.preventDefault();
		  }

      // If the user presses Ctrl + Shift + V, switch to Vim mode!
      if ((event.key === 'v' || event.key === 'V') && event.ctrlKey && event.shiftKey) {
        this.settings.vimMode = !this.settings.vimMode
        event.preventDefault();
        this.vim_mode_checkbox.checked = !this.settings.vimMode;
        this.userPlugins = this.settings.vimMode ? [] : [vim()]
        this.view.dispatch({
          effects: dynamicPlugins.reconfigure(this.userPlugins)
        })
      }

		  if ((event.key === 'Enter' || event.key === 'Return') && event.ctrlKey) {
        event.preventDefault();
		  	const code = this.getCodeBlock();
		  	runnerService.executeCode(code + '\n\n');
        localStorage.setItem("sardine_buffers", JSON.stringify(this.buffers))
		  }

		  // Shift + Enter or Ctrl + E (Rémi Georges mode)
		  if ((event.key === 'Enter' && event.shiftKey) || (event.key === 'e' && event.ctrlKey)) {
		  	event.preventDefault(); // Prevents the addition of a new line
		  	const code = this.getSelectedLines();
		  	runnerService.executeCode(code + '\n\n');
        localStorage.setItem("sardine_buffers", JSON.stringify(this.buffers))
		  }
    })

    // Change the file-selector content to match the selected buffer
    this.file_selector.value = this.selectedBuffer
    this.file_selector.addEventListener('keyup', (event: KeyboardEvent) => {
      if (event.key === 'Enter') {
        localStorage.setItem("sardine_buffers", JSON.stringify(this.buffers))
        this.switchBuffer(this.file_selector.value)
        this.view.dispatch({
          changes: {
            from: 0, 
            to: this.view.state.doc.length,
            insert: this.buffers[this.selectedBuffer]
          },
        });
      }
    });

    this.play_button.addEventListener('click', () => {
      runnerService.executeCode(this.playing? 
        "bowl.dispatch('resume')" : "bowl.dispatch('pause')"
      )
    })

    this.save_button.addEventListener('click', () => {
		  const blob = new Blob([this.buffers[this.selectedBuffer]], 
        { type: 'text/plain' }
      );
		  const a = document.createElement('a');
		  a.href = URL.createObjectURL(blob);
		  a.download = 'sardine.py';
		  a.style.display = 'none';
		  document.body.appendChild(a);
		  a.click();
		  document.body.removeChild(a);
    })

    this.share_buffer.addEventListener('click', () => {
      // Encode the current buffer in base64, make the link shareable
      let encoded_buffer = btoa(this.buffers[this.selectedBuffer]);
      // TODO: implement a way to share the buffer
    })

    // this.logs_button.addEventListener('click', () => {
    //   this.footer_open = !this.footer_open
    //   if (this.footer_open) {
    //     // Create a pre/code element to display the logs
    //     let logs = document.createElement('pre'); logs.id = 'logs'
    //     let code = logs.appendChild(document.createElement('code'))
    //     code.className = 'text-xs';
    //     code.innerHTML = this.logs == undefined? "Sardine hasn't started" : this.logs.join('\n')

    //     // Make this footer_content display the logs
    //     this.footer_content.appendChild(logs)
    //   } else {
    //     this.footer_content.removeChild(document.getElementById('logs') as HTMLElement)
    //   }
    // })

    this.docs_button.addEventListener('click', () => {
      window.open('https://sardine.raphaelforment.fr')
    })
    this.open_info.addEventListener('click', () => {
      window.open('https://sardine.raphaelforment.fr')
    })
    this.clear_button.addEventListener('click', () => {
      // Ask for user confirmation in a popup
      let confirmation = confirm("Are you sure you want to clear all your files? This action cannot be undone. You will lose all your text files. Create a copy of your files before proceeding.")
      if (confirmation) {
          // Restore buffers to default
          this.buffers = {
            "Default": "// This is Sardine Web",
            ...generalTutorials
          };
          this.switchBuffer('Default');
          this.view.dispatch({
            changes: {
              from: 0,
              to: this.view.state.doc.length,
              insert: this.buffers[this.selectedBuffer]
            },
          });
      }
    })

    this.settings_button.addEventListener('click', () => {
      let settings = document.getElementById('settings-content') as HTMLElement
      this.footer_open = !this.footer_open
      if (this.footer_open) {
        settings.classList.remove('hidden')
      } else {
        settings.classList.add('hidden')
      }
    })

    this.vim_mode_checkbox.checked = this.settings.vimMode;
    this.vim_mode_checkbox.addEventListener('change', () => {
      let value = this.vim_mode_checkbox.checked
      if (value) {
        this.settings.vimMode = true; this.userPlugins = [vim()]
        this.view.dispatch({
          effects: dynamicPlugins.reconfigure(this.userPlugins)
        })
      } else {
        this.settings.vimMode = false; this.userPlugins = []
        this.view.dispatch({
          effects: dynamicPlugins.reconfigure(this.userPlugins)
        })
      }
    });

    this.font_selector.addEventListener('input', () => {
      this.settings.font = this.font_selector.value
      // Update font on body element
      document.body.style.fontFamily = this.settings.font
      let editor = document.getElementById('editor') as HTMLElement
      let scroller = editor.getElementsByClassName('cm-scroller')[0] as HTMLElement
      scroller.style.fontFamily = this.settings.font
    })


    // Replace the content of the Default buffer with the help text
    this.view.dispatch({
      changes: {
        from: 0,
        to: this.view.state.doc.length,
        insert: keybindingsMessage
      }
    })
  };




  switchBuffer(bufferName: string): void {
    localStorage.setItem("sardine_buffers", JSON.stringify(this.buffers))
    this.buffers[bufferName] = this.buffers[bufferName] || ""
    this.selectedBuffer = bufferName
    this.file_selector.value = bufferName
    this.view.dispatch({
      changes: {
        from: 0,

      }
    })
  }

  getCodeBlock(): string {
    // Capture the position of the cursor
    let cursor = this.view.state.selection.main.head
		const state = this.view.state;
		const { head } = state.selection.main;
		const currentLine = state.doc.lineAt(head);
		let startLine = currentLine;
		while (startLine.number > 1 && !/^\s*$/.test(state.doc.line(startLine.number - 1).text)) {
			startLine = state.doc.line(startLine.number - 1);
		}
		let endLine = currentLine;
		while (
      endLine.number < state.doc.lines && !/^\s*$/.test(state.doc.line(endLine.number + 1).text)) { 
        endLine = state.doc.line(endLine.number + 1);
      }

      this.view.dispatch({selection: {anchor: 0 + startLine.from, head: endLine.to}});
      highlightSelection(this.view);

		  setTimeout(() => {
        unhighlightSelection(this.view)
        this.view.dispatch({selection: {anchor: cursor, head: cursor}});
       }, 200);

       let result_string = state.doc.sliceString(startLine.from, endLine.to);
       result_string = result_string.split('\n').map((line, index, lines) => {
         if (index === lines.length - 1 || /^\s/.test(lines[index + 1])) {
           return line;
         } else {
           return line + ';\\';
         }
       }).join('\n');
       return result_string
  }

  getSelectedLines = (): string => {
    const state = this.view.state;
    const { from, to } = state.selection.main;
    const fromLine = state.doc.lineAt(from);
    const toLine = state.doc.lineAt(to);
    this.view.dispatch({selection: {anchor: 0 + fromLine.from, head: toLine.to}});
    // Release the selection and get the cursor back to its original position

  	// Blink the text!
    highlightSelection(this.view);

		setTimeout(() => {
      unhighlightSelection(this.view)
      this.view.dispatch({selection: {anchor: from, head: from}});
		}, 200);
 		return state.doc.sliceString(fromLine.from, toLine.to);   
  }

}

const runnerService = new RunnerService(8000);
const editor = new Editor(runnerService);

// Save files when the user leaves the page
window.onbeforeunload = function() {
  console.log('Saving files to localStorage')
  localStorage.setItem("sardine_buffers", JSON.stringify(editor.buffers))
  localStorage.setItem("sardine_settings", JSON.stringify(editor.settings.data as Settings))
}