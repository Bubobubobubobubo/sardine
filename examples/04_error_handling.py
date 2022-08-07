# This is a perfectly valid function

async def blabla(delay=1):
    print("blabla")
    cs(blabla, delay=1)

cs(blabla, delay=1)

# This is not anymore. Note that the old function will continue to play.
# You now have time to correct and amend your function before reeval.

async def blabla(delay=1):
    pint("blabla")
    cs(blabla, delay=1)
