/**
 * Genre detail page with related movies.
 */
import { createFileRoute } from "@tanstack/react-router"
import { useQuery } from "@tanstack/react-query"
import { GenresService, MoviesService } from "@/client"
import { MovieCard } from "@/components/Movies/MovieCard"

/**
 * Configure the genre details route.
 */
export const Route = createFileRoute("/_layout/genres/$genreId")({
    component: GenreDetails,
})

/**
 * Load a genre and display its related movies.
 */
function GenreDetails() {
    const { genreId } = Route.useParams()

    const { data, isLoading, isError } = useQuery({
        queryKey: ["genre", genreId],
        queryFn: async () => {
            const response = await GenresService.getGenre({
                path: { genre_id: genreId }
            })
            return response.data
        }
    })

    const genreName = data?.name ?? ""

    const { data: moviesData, isLoading: isLoadingMovies, isError: isErrorMovies } = useQuery({
        queryKey: ["genreMovies", genreId],
        queryFn: async () => {
            const response = await MoviesService.getMoviesByGenre({
                query: {
                    genre: genreName,
                    page: 1,
                    page_size: 50
                }
            })
            return response.data
        },
        enabled: !!data
    })

    if (isLoading) return <p className="text-sm text-muted-foreground">Loading genre...</p>

    if (isError) return <p className="text-sm text-destructive">Error loading genre.</p>

    if (!data) return <p className="text-sm text-muted-foreground">Genre not found.</p>

    if (isLoadingMovies) return <p className="text-sm text-muted-foreground">Loading movies...</p>

    if (isErrorMovies) return <p className="text-sm text-destructive">Error loading movies.</p>

    return (
        <div className="space-y-8 py-6">
            <div>
                <button
                    type="button"
                    onClick={() => window.history.back()}
                    className="w-fit text-sm text-muted-foreground transition-colors hover:text-foreground"
                >
                    ← Back
                </button>
            </div>

            <div>
                <h1
                    className="text-3xl font-bold tracking-tight"
                >
                    {genreName}
                </h1>
            </div>

            <div className="space-y-4">
                <h2 className="text-2xl font-semibold">Movies</h2>

                {!moviesData || moviesData.count === 0 ? (
                    <p className="text-sm text-muted-foreground">
                        No movies found.
                    </p>
                ) : (
                    <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                        {moviesData.movies.map((movie) => (
                            <MovieCard key={movie.id} movie={movie} />
                        ))}
                    </div>
                )}
            </div>
        </div>
    )
}
