# Vim / Neovim

![img](vim.png)

**NeoVim** (and by extension **Vim**) is the editor I currently use 
both on stage, for development, writing my PhD thesis and also to write the docs. 
Its target audience is mostly developers, old Unix gurus and command-line users.
**Vim** is a modal text editor with multiple modes for editing and jumping around 
in the source code. It can be extended using plugins and tweaked to your liking. 
Quite powerful, but it requires some learning to be proficient. The process for
working with **Sardine** from **Neovim** is pretty straightforward:

1. install the [slime](https://github.com/jpalardy/vim-slime) plugin.
   -   note that the technique to do so might vary depending on your configuration. I am using [Lua](https://github.com/nanotee/nvim-lua-guide) to write my configuration. In the past, I had previously used [Plug](https://github.com/junegunn/vim-plug) for years without encountering any issue!
2. split your workspace in two vertical (`:vs`) or horizontal (`:sp`) panes.
3. open up a `:terminal` in one of them and run `fishery`.
4. work in the other one and use `C-c C-c` (`Control+C` twice) to send code from one side to the other.
   -   **slime** will probably ask you which job to target, just press enter!

There are other plugins out there doing the exact same thing (probably better):
[Iron](https://github.com/hkupty/iron.nvim),
[ToggleTerm](https://github.com/akinsho/toggleterm.nvim).
