import tmdbsimple as tmdb

def search_movie(title):

    search = tmdb.Search()

    response = search.movie(query=title)

    return search.results

def search_tv(title):

    search = tmdb.Search()

    response = search.tv(query=title)

    return search.results
