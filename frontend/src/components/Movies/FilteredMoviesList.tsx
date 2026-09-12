/**
 * Movie search results component.
 */
import { useQuery } from "@tanstack/react-query"
import { MoviesService } from "@/client"
import { MovieCard } from "@/components/Movies/MovieCard"

type SearchType = "title" | "genre" | "actor" | "director"

/**
 * Load and display movies based on the selected search type and value.
 */
export function FilteredMoviesList({ searchType, searchValue } : { searchType: SearchType, searchValue: string }) {

    const { data, isLoading, isError } = useQuery({
        queryKey: ["filtered-movies", searchType, searchValue],
        queryFn: async () => {
            switch (searchType) {
                case "title": {
                    const response = await MoviesService.getMoviesByTitle({
                        query: {
                            title: searchValue,
                            page: 1,
                            page_size: 50
                        }
                    })
                    return response.data
                }

                case "genre": {
                    const response = await MoviesService.getMoviesByGenre({
                        query: {
                            genre: searchValue,
                            page: 1,
                            page_size: 50
                        }
                    })
                    return response.data
                }

                case "actor": {
                    const response = await MoviesService.getMoviesByActor({
                        query: {
                            actor: searchValue,
                            page: 1,
                            page_size: 50
                        }
                    })
                    return response.data
                }

                case "director": {
                    const response = await MoviesService.getMoviesByDirector({
                        query: {
                            director: searchValue,
                            page: 1,
                            page_size: 50
                        }
                    })
                    return response.data
                }
            }
        }
    })

    if (isLoading) return <p className="text-sm text-muted-foreground">Loading movies...</p>


    if (isError) return <p className="text-sm text-destructive">Unable to load movies.</p>

    if (!data || data.count === 0) return <p className="text-sm text-muted-foreground"> No movies found.</p>

    return (
        <div className="space-y-5">
            <h2 className="text-2xl font-semibold">Search Results</h2>

            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                {data.movies.map((movie) => (
                    <MovieCard key={movie.id} movie={movie} />
                ))}
            </div>
        </div>
    )
}