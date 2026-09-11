/**
 * Director detail page with related movies.
 */
import { createFileRoute } from "@tanstack/react-router"
import { useQuery } from "@tanstack/react-query"
import { DirectorsService, MoviesService } from "@/client"
import { MovieCard } from "@/components/Movies/MovieCard"

/**
 * Configure the director details route.
 */
export const Route = createFileRoute("/_layout/directors/$directorId")({
    component: DirectorDetails,
})

/**
 * Load a director and display their related movies.
 */
export function DirectorDetails() {
    const { directorId } = Route.useParams()

    const { data, isLoading, isError } = useQuery({
        queryKey: ["director", directorId],
        queryFn: async () => {
            const response = await DirectorsService.getDirector({
                path: { director_id: directorId }
            })
            return response.data
        }
    })

    const directorName = data
        ? `${data.first_name} ${data.last_name}`
        : ""

    const { data: moviesData, isLoading: isLoadingMovies, isError: isErrorMovies } = useQuery({
        queryKey: ["directorMovies", directorId],
        queryFn: async () => {
            const response = await MoviesService.getMoviesByDirector({
                query: {
                    director: directorName,
                    page: 1,
                    page_size: 50
                }
            })
            return response.data
        },
        enabled: !!data
    })

    if (isLoading) return <p className="text-sm text-muted-foreground">Loading director...</p>

    if (isError) return <p className="text-sm text-destructive">Error loading director.</p>

    if (!data) return <p className="text-sm text-muted-foreground">Director not found.</p>

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
                    {directorName}
                </h1>

                {data.birth_date && (
                    <p className="mt-2 text-sm text-muted-foreground">
                        Born: {new Date(data.birth_date).toLocaleDateString("en-GB")}
                    </p>
                )}
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
