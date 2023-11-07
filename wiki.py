import wikipedia

  # TODO: add select language!
wikipedia.set_lang('ru')

def search_wiki(query):
  return wikipedia.search(query)


def wiki_page(page_name):
  page = wikipedia.page(page_name)
  return page.title, page.summary, page.url
