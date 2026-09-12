/**
 * Top-rated movies section.
 */
import { useQuery } from "@tanstack/react-query"
import { useState } from "react"
import { MoviesService } from "@/client"
import { MovieCard } from "@/components/Movies/MovieCard"

/**
 * Load and display the highest-rated movies with a configurable limit.
 */
export function TopRatedMovies() {
    const [limit, setLimit] = useState(5)

    const { data, isLoading, isError } = useQuery({
        queryKey: ["top-rated-movies", limit],
        queryFn: async () => {
            const response = await MoviesService.getTopRatedMovies({
                query: { limit }
            })
            return response.data
        }
    })

    if (isLoading) return <p className="text-sm text-muted-foreground">Loading top rated movies...</p>

    if (isError) return <p className="text-sm text-destructive">Unable to load top rated movies.</p>

    if (!data || data.count === 0) return <p className="text-sm text-muted-foreground">No top rated movies available.</p>

    return (
        <div className="space-y-5">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <h2 className="text-2xl font-semibold">Top Rated Movies</h2>
            
                <select
                    value={limit}
                    onChange={(event) => setLimit(Number(event.target.value))}
                    className="w-fit rounded-md border border-input bg-background px-3 py-2 text-sm outline-none transition-colors focus:border-primary"
                >
                    <option value={5}>Top 5</option>
                    <option value={10}>Top 10</option>
                    <option value={20}>Top 20</option>
                    <option value={50}>Top 50</option>
                </select>
            </div>

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
