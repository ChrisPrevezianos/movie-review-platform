/**
 * Review list for displaying reviews associated with a movie.
 */
import { useQuery } from "@tanstack/react-query"
import { ReviewsService } from "@/client"
import { ReviewCard } from "./ReviewCard"

/**
 * Build the query configuration for a movie's reviews.
 */
function getReviewsQueryOptions(movieId: string) {
    return {
        queryFn: async () =>
        (await ReviewsService.getReviewsByMovie(
            { path : { movie_id: movieId },
            query: { page: 1, page_size: 50 },
        })).data,
        queryKey: ["reviews", movieId],
    }
}

/**
 * Display reviews for the selected movie.
 */
export function ReviewsList({ movieId } : { movieId: string}) {
    const { data, isLoading, isError } = useQuery(getReviewsQueryOptions(movieId))

    if (isLoading) return <div className="text-muted-foreground">Loading...</div>

    if (isError) return <div className="text-muted-foreground"> Unable to load reviews.</div>

    return (
    <section className="flex w-full max-w-2xl flex-col gap-4">
      <div className="flex items-baseline gap-3">
        <h2 className="text-2xl font-bold tracking-tight">Reviews</h2>

        {data && (
          <span className="text-sm text-muted-foreground">
            {data.count} {data.count === 1 ? "review" : "reviews"}
          </span>
        )}
      </div>

      {!data || data.reviews.length === 0 ? (
        <p className="text-muted-foreground">
          No reviews yet. Be the first to review this movie.
        </p>
      ) : (
        <div className="flex flex-col gap-4">
          {data.reviews.map((review) => (
            <ReviewCard key={review.id} review={review} />
          ))}
        </div>
      )}
    </section>
  )
}
