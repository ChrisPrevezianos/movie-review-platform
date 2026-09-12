/**
 * Movie details page for displaying complete information about a movie.
 */
import { useQuery } from "@tanstack/react-query"
import { Link, createFileRoute } from "@tanstack/react-router"
import { MoviesService } from "@/client"
import { ReviewsList } from "@/components/Reviews/ReviewsList"
import { CreateReviewForm } from "@/components/Reviews/CreateReviewForm"
import { useState } from "react"
import { useAdmin } from "@/hooks/useAdmin"
import { DeleteMovieButton } from "@/components/Movies/DeleteMovieButton"
import { MovieRating } from "@/components/Movies/MovieRating"

export const Route = createFileRoute("/_layout/movies/$movieId")({
    component: MovieDetails,
})

/**
 * Display the selected movie with its metadata, cast, directors, and trailer.
 */
function MovieDetails() {
    const { movieId } = Route.useParams()

    const [showReviewForm, setShowReviewForm] = useState(false)
    const { isAdmin } = useAdmin()

    const { data: movie, isLoading } = useQuery({
        queryKey: ["movie", movieId],
        queryFn: async () => {
            const response = await MoviesService.getMovie({
                path: { movie_id: movieId},
            })
            return response.data
        }
    })

    if (isLoading) return <p className="text-muted-foreground">Loading...</p>

    if (!movie) return <p className="text-muted-foreground">Movie not found.</p>

    return (
    <div className="flex flex-col gap-8">
      <div className="flex items-center justify-between">
        <Link
          to="/"
          className="w-fit text-sm text-muted-foreground hover:text-foreground"
        >
          ← Back to movies
        </Link>

        {isAdmin && (
          <div className="flex items-center gap-4">
            <Link
              to="/movies/$movieId/edit"
              params={{ movieId: movie.id }}
              className="text-sm text-muted-foreground transition-colors hover:text-foreground"
            >
              Edit
            </Link>
            <DeleteMovieButton movieId={movie.id} />
          </div>
        )}
      </div>

      <div className="grid gap-8 md:grid-cols-[300px_1fr]">
        <div>
          <img
            src={movie.poster_url}
            alt={movie.title}
            className="w-full rounded-lg border object-cover"
          />
        </div>

        <div className="flex flex-col gap-6">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">
              {movie.title}
            </h1>

            <div className="mt-2">
              <MovieRating movieId={movie.id} />
            </div>

            <div className="mt-3 flex flex-wrap gap-3 text-sm text-muted-foreground">
              <span>{movie.release_year}</span>
              <span>•</span>
              <span>{movie.duration} min</span>
              <span>•</span>
              <span>{movie.age_rating}</span>
            </div>
          </div>

          <div>
            <h2 className="mb-2 text-lg font-semibold">Synopsis</h2>
            <p className="leading-7 text-muted-foreground">
              {movie.synopsis}
            </p>
          </div>

          <div>
            <h2 className="mb-2 text-lg font-semibold">Genres</h2>

            <div className="flex flex-wrap gap-2">
              {movie.genres.map((genre) => (
                <Link
                  key={genre.id}
                  to="/genres/$genreId"
                  params={{ genreId: genre.id }}
                  className="rounded-full bg-muted px-3 py-1 text-sm text-muted-foreground transition-colors hover:text-primary"
                >
                  {genre.name}
                </Link>
              ))}
            </div>
          </div>

          <div>
            <h2 className="mb-2 text-lg font-semibold">Director</h2>

            <p className="text-muted-foreground">
              {movie.directors
                .map(
                  (director, index) => (
                    <span>
                      {index > 0 && ", "}
                      <Link
                        key={director.id}
                        to="/directors/$directorId"
                        params={{ directorId: director.id }}
                        className="text-muted-foreground transition-colors hover:text-primary"
                      >
                        {director.first_name} {director.last_name}
                      </Link>
                    </span>
                ))}
            </p>
          </div>

          <div>
            <h2 className="mb-2 text-lg font-semibold">Cast</h2>

            <div className="flex flex-wrap gap-2">
              {movie.actors.map((actor) => (
                <Link
                  key={actor.id}
                  to="/actors/$actorId"
                  params={{ actorId: actor.id }}
                  className="rounded-md border border-border px-3 py-1.5 text-sm transition-colors hover:border-primary hover:text-primary"
                >
                  {actor.first_name} {actor.last_name}
                </Link>
              ))}
            </div>
          </div>

          <a
            href={movie.trailer_url}
            target="_blank"
            rel="noreferrer"
            className="inline-flex w-fit rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90"
          >
            Watch trailer
          </a>

          <div className="w-full max-w-2xl">
            <div className="mb-1 flex justify-end">
              <button
                type="button"
                onClick={() => setShowReviewForm((current) => !current)}
                className="text-sm text-muted-foreground transition-colors hover:text-foreground"
              >
                {showReviewForm ? "Cancel" : "+ Review"}
              </button>
            </div>
            <ReviewsList movieId={movie.id} />

            {showReviewForm && (
              <div className="mt-4">
                <CreateReviewForm movieId={movie.id} onCreated={() => setShowReviewForm(false)} />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
