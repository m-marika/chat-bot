import asyncio
import wikipedia

wikipedia.set_lang('ru')

async def search_wiki(query):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, wikipedia.search, query)

async def wiki_page(page_name):
    loop = asyncio.get_running_loop()
    page = await loop.run_in_executor(None, wikipedia.page, page_name)
    return page.title, page.summary, page.url
