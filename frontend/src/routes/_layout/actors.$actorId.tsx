/**
 * Actor detail page with related movies.
 */
import { Link, createFileRoute } from "@tanstack/react-router"
import { useQuery } from "@tanstack/react-query"
import { ActorsService, MoviesService } from "@/client"
import { MovieCard } from "@/components/Movies/MovieCard"

/**
 * Configure the actor details route.
 */
export const Route = createFileRoute("/_layout/actors/$actorId")({
    component: ActorDetails,
})

/**
 * Load an actor and display their related movies.
 */
function ActorDetails() {
    const { actorId } = Route.useParams()

    const { data, isLoading, isError } = useQuery({
        queryKey: ["actor", actorId],
        queryFn: async () => {
            const response = await ActorsService.getActor({
                path: { actor_id: actorId }
            })
            return response.data
        }
    })

    const actorName = data
        ? `${data.first_name} ${data.last_name}`
        : ""

    const { data: moviesData, isLoading: isLoadingMovies, isError: isErrorMovies } = useQuery({
        queryKey: ["actorMovies", actorId],
        queryFn: async () => {
            const response = await MoviesService.getMoviesByActor({
                query: {
                    actor: actorName,
                    page: 1,
                    page_size: 50
                }
            })
            return response.data
        },
        enabled: !!data
    })

    if (isLoading) return <p className="text-sm text-muted-foreground">Loading actor...</p>

    if (isError) return <p className="text-sm text-destructive">Error loading actor.</p>

    if (!data) return <p className="text-sm text-muted-foreground">Actor not found.</p>

    if (isLoadingMovies) return <p className="text-sm text-muted-foreground">Loading movies...</p>

    if (isErrorMovies) return <p className="text-sm text-destructive">Error loading movies.</p>

    return (
        <div className="space-y-8 py-6">
            <div>
                <Link
                    to="/"
                    className="w-fit text-sm text-muted-foreground transition-colors hover:text-foreground"
                >
                    ← Back to movies
                </Link>
            </div>

            <div>
                <h1
                    className="text-3xl font-bold tracking-tight"
                >
                    {actorName}
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
