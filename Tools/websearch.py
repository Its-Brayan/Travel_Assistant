from duckduckgo_search import DDGS

def search_web(text: str,max_results:int = 5):

    with DDGS() as ddgs:
        results = list(ddgs.text(text, max_results))
        for item in results:
            print("Title",item.get('title'))
            print("URL",item.get('href'))
            print("Snippet", item.get('body'))

    
    return results
