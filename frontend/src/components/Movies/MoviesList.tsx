/**
 * Movie list component and query configuration for retrieving movies.
 */
import { MoviesService } from "@/client"
import { useQuery} from "@tanstack/react-query"
import { MovieCard } from "./MovieCard"

/**
 * Configure the query used to retrieve the first page of movies.
 */
function getMoviesQueryOptions() {
  return {
    queryFn: async () =>
      (await MoviesService.getMovies({ query: { page: 1, page_size: 50 }})).data,
    queryKey: ["movies"]
  }
}

/**
 * Fetch and display movies returned by the backend.
 */
export function MoviesList() {
  const { data, isLoading, isError } = useQuery(getMoviesQueryOptions())

  if (isLoading) {
    return <p>Loading...</p>
  }

  if (isError) return <div className="text-muted-foreground"> Unable to load movies.</div>

  return (
    <div>
      <h2 className="mb-4 text-2xl font-bold tracking-tight">Movies</h2>
      {!data || data.movies.length === 0 ? (
        <p className="text-muted-foreground">No movies available.</p>
      ) : (
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {data?.movies.map((movie) => (
            <MovieCard key={movie.id} movie={movie} />
          ))}
        </div>
      )}
    </div>
  )
}
