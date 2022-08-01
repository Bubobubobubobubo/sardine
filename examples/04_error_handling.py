# This is a perfectly valid function

async def blabla():
    print("blabla")
    cs(blabla())

cs(blabla())

# This is not anymore
async def blabla():
    pint("blabla")
    cs(blabla())
