export const default_buffer = `# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Welcome to the embedded Sardine Code Editor! Press Shift+Enter while selecting text 
# to eval your code. You can select the editing mode through the menubar. Have fun!

# You can play on any tab. They will be saved automatically :) (except scratch : *)
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

@swim
def baba(p=0.5, i=0):
	"""I am the default swimming function. Please evaluate me!"""
	D('bd, hh, sn, hh', speed='1,1,0.5', i=i)
	again(baba, p=0.5, i=i+1)

// Remember about surfboards :)
Pa >> d('bd, cp')
`;
