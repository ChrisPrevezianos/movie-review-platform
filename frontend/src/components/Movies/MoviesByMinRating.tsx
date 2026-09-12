/**
 * Movies filtered by minimum average rating.
 */
import { useQuery } from "@tanstack/react-query"
import { MoviesService } from "@/client"
import { MovieCard } from "@/components/Movies/MovieCard"

/**
 * Load and display movies whose average rating meets the selected minimum.
 */
export function MoviesByMinRating({ minRating }: { minRating: number }) {

    const { data, isLoading, isError } = useQuery({
        queryKey: ["movies-by-min-rating", minRating],
        queryFn: async () => {
            const response = await MoviesService.getMoviesByMinRating({
                query: { 
                    min_rating: minRating,
                    page: 1, 
                    page_size: 50 }   
            })
            return response.data
        }
    })

    if (isLoading) return <p className="text-sm text-muted-foreground">Loading movies...</p>

    if (isError) return <p className="text-sm text-destructive">Unable to load movies.</p>

    if (!data || data.count === 0) return <p className="text-sm text-muted-foreground">No movies found for this minimum rating.</p>

    return (
        <div className="space-y-5">
            <h2 className="text-2xl font-semibold">Movies By Minimum Rating</h2>

            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                {data.movies.map((movie) => (
                    <MovieCard 
                        key={movie.id} 
                        movie={movie} 
                        averageRating={movie.average_rating}
                    />
                ))}
            </div>
        </div>
    )
}