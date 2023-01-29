export const default_buffer = `# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Welcome to the embedded Sardine Code Editor! Press Shift+Enter while selecting text 
# to eval your code. You can select the editing mode through the menubar. Have fun!

# PRE WEB EDITOR RELEASE TASK LIST:
# - blinking on evaluation (!!)
# - fix the theme situation (!!)
# - make every button actually do something (!!)
# - make the logs resizable with a mouse handle (!!)
# - keybinding to switch tab and prevent losing focus
# - automatically create buffers folder when installing Sardine
# - shipping a tutorial along with the web editor

# You can play on any tab. They will be saved automatically :) (except scratch : *)
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=



@swim
def baba(p=0.5, i=0):
	"""I am the default swimming function. Please evaluate me!"""
	D('bd, hh, sn, hh', speed='1,1,0.5', i=i)
	again(baba, p=0.5, i=i+1)
`;