# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.


from search_engine_parser import GoogleSearch
from userge import userge, Message


@userge.on_cmd("google", about="""\
__do a Google search__

**Available Flags:**

    `-p` : __page of results to return (default to 1)__
    `-l` : __limit the number of returned results (defaults to 5)(max 10)__
    
**Usage:**

    `.google [flags] [query | reply to msg]`
    
**Example:**

    `.google -p4 -l10 github-userge`""")
async def gsearch(message: Message):
    await message.edit("Processing ...")

    query = message.filtered_input_str
    flags = message.flags
    page = int(flags.get('-p', 1))
    limit = int(flags.get('-l', 5))

    if message.reply_to_message:
        query = message.reply_to_message.text

    if not query:
        await message.err(text="Give a query or reply to a message to google!")
        return

    try:
        g_search = GoogleSearch()
        gresults = g_search.search(query, page)

    except Exception as e:
        await message.err(text=e)
        return

    output = ""

    for i in range(limit):
        try:
            title = gresults["titles"][i]
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            output += f"[{title}]({link})\n"
            output += f"`{desc}`\n\n"

        except IndexError:
            break

    output = f"**Google Search:**\n`{query}`\n\n**Results:**\n{output}"

    await message.edit_or_send_as_file(text=output, caption=query, disable_web_page_preview=True)
