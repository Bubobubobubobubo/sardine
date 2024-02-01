# Vim / Neovim

![img](vim.png)


**NeoVim** (and by extension **Vim**) is the editor I currently use both on stage, for development, writing my PhD thesis and also to write the docs. Its target audience is mostly developers, old Unix gurus and command-line users. **Vim** is a modal text editor with multiple modes for editing and jumping around in the source code. It can be extended using plugins and tweaked to your liking. Quite powerful, but it requires some learning to be proficient. 

## Using vim-slime

The process for working with **Sardine** from **Neovim** is pretty straightforward:

1. install the [slime](https://github.com/jpalardy/vim-slime) plugin.
   -   note that the technique to do so might vary depending on your configuration. I am using [Lua](https://github.com/nanotee/nvim-lua-guide) to write my configuration. In the past, I had previously used [Plug](https://github.com/junegunn/vim-plug) for years without encountering any issue!
2. split your workspace in two vertical (`:vs`) or horizontal (`:sp`) panes.
3. open up a `:terminal` in one of them and run `sardine`.
4. work in the other one and use `C-c C-c` (`Control+C` twice) to send code from one side to the other.
   -   **slime** will probably ask you which job to target, just press enter!

## Usin iron.nvim

[iron.nvim](https://github.com/Vigemus/iron.nvim) is a modern plugin for handling REPLs from Neovim. It took me some time to configure but it works well too.
1) install by following the instructions on the repository.
2) copy/paste all the necessary configuration files and customize it to your liking.
3) take note of the details below.

For sending code blocks, you will have to customize your REPL a little more. Note that I am using Lua, the modern Neovim replacement to VimScript. Please look at the following amendments to the base configuration:
```lua
local iron = require("iron.core")
iron.setup({

  repl_open_cmd = "vertical botright 50 split", -- better split
  config = {
    -- Whether a repl should be discarded or not
    scratch_repl = false,
    close_window_on_exit = true,
    -- Your repl definitions come here
    repl_definition = {
      sh = {
        -- Can be a table or a function that
        -- returns a table (see below)
        command = { "zsh" },
        python = {
          command = { "sardine" },
      },
        format = require("iron.fts.common").bracketed_paste, -- super important (!!!)
      },
    },
    -- How the repl window will be displayed
    -- See below for more information
    repl_open_cmd = require("iron.view").split.vertical.botright(50),
  },
  -- ... etc ... your typical config
})
```

This will allow you to send the following events to the Sardine REPL:
- **sending a single line:** `<space>sl` with your cursor on the line you want to send.
- **sending a code block**: `<space>sc` with a selected block of text for multi-line.
