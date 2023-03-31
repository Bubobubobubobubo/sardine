# (Doom) Emacs

![doom](doom.png)

I am using **Doom Emacs** for many things in my life:
- writing this documentation
- writing manuscripts or papers
- playing some music with **Sardine**.

The venerable **Emacs** is of course able to manage **Sardine**!
Please use the `python.el` plugin. This mode will allow you to pipe easily your code 
from a text buffer to a running interpeter. The plugin is adding quality-of-life
features for working with **Python** in general but also makes working with a
**REPL** much easier and much more convenient. If you are new to the vast world
of **Emacs**, it is probably worthwhile to take a look at 
[Doom Emacs](https://github.com/doomemacs/doomemacs) 
or [Spacemacs](https://github.com/syl20bnr/spacemacs), both being equally great.
I will not dive into more details. If you are able to configure **Emacs**, you will be
able to configure your editor for **Sardine** :).

The following code is the one I use for running **Sardine** using **Doom Emacs**.
It is not great and I should probably make something cleaner or even create a
dedicated package for **Sardine** but life is short, and nobody is writing the docs
while I finetune my **Emacs** config.

```python
;; =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
;; SARDINE MODE
;; =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
;; Customize the python-mode to run Sardine code using the terminal.

(setq
 python-shell-interpreter "fishery"
 python-shell-interpreter-args "")

(defun sardine/start-sardine ()
  "Start a new interactive Sardine Session"
  (interactive)
  (run-python))

(defun sardine/eval-block ()
  "Evaluate a sardine code block"
  (interactive)
  (mark-paragraph)
  (if (and transient-mark-mode mark-active)
      (python-shell-send-region (point) (mark))
    (python-shell-send-region (point-at-bol) (point-at-eol)))
  (forward-paragraph))

(defun sardine/stop-code ()
  "Stop all the Sardine code currently running"
  (interactive)
  (python-shell-send-string "panic()"))

; Unmapping keys from the Python mode
(add-hook 'python-mode-hook
          (lambda() (local-unset-key (kbd "C-c C-c"))))
(add-hook 'python-mode-hook
          (lambda() (local-unset-key (kbd "C-c C-s"))))

; Remapping keys
(global-set-key (kbd "C-c C-c") #'sardine/eval-block)
(global-set-key (kbd "C-c C-s") #'sardine/stop-code)
```


