import tmdbsimple as tmdb

def search_movie(title):
    """
    Connects to API to search for a specific movie by title.
    """
    search = tmdb.Search()

    response = search.movie(query=title)

    return search.results

def search_tv(title):
    """
    Connects to API to search for a specific tv show by title.
    """
    search = tmdb.Search()

    response = search.tv(query=title)

    return search.results

def search_by_id(id, type):
    """
    Connects to API to search for a specific movie or show by id.
    """
    if type == 'tv':
        result = tmdb.TV(id)
    else :
        result = tmdb.Movies(id)

    return result.info()
