/**
 * Reusable card component for displaying public movie information.
 */
import type { MoviePublic } from "@/client"
import { Link } from "@tanstack/react-router"

/**
 * Display a movie poster, title, release year, age rating, and genres.
 */
export function MovieCard( { movie } : { movie: MoviePublic}) {
    return (
        <div className="overflow-hidden rounded-lg border bg-card">
            <img src={movie.poster_url} alt={movie.title} className="aspect-[2/3] w-full object-cover" />
            <div className="flex flex-col gap-3 p-4">
                <h2 className="text-lg font-semibold">{movie.title}</h2>
                <div className="flex justify-between text-sm text-muted-foreground">
                    <span>{movie.release_year}</span>
                    <span>{movie.age_rating}</span>
                </div>
                <div className="flex flex-wrap gap-2">
                    {movie.genres.map((genre) => (
                    <span
                        key={genre.id}
                        className="rounded-full bg-muted px-2 py-1 text-xs text-muted-foreground"
                    >
                        {genre.name}
                    </span>
                    ))}
                </div>
                <Link
                    to="/movies/$movieId"
                    params={{ movieId: movie.id }}
                    className="mt-2 inline-flex w-fit rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90"
                >
                    View Details
                </Link>
            </div>
        </div>
    )
}
