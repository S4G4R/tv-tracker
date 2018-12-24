import tmdbsimple as tmdb

def search_movie(title):

    search = tmdb.Search()

    response = search.movie(query=title)

    return search.results

def search_tv(title):

    search = tmdb.Search()

    response = search.tv(query=title)

    return search.results

def search_by_id(id, type):

    if type == 'tv':
        result = tmdb.TV(id)
    else :
        result = tmdb.Movies(id)

    return result
