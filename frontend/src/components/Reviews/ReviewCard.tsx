/**
 * Review card for displaying a single movie review.
 */
import type { ReviewPublic } from "@/client"

/**
 * Display the rating, comment, and date of a review.
 */
export function ReviewCard( { review } : { review: ReviewPublic}) {
    const reviewDate = review.updated_at || review.created_at

    return (
    <article className="rounded-lg border bg-card p-4">
      <div className="flex flex-col gap-3">
        <div className="flex items-center justify-between">
          <span className="font-semibold">
            Rating: {review.rating}/10
          </span>

          <span className="text-sm text-muted-foreground">
            {new Date(reviewDate).toLocaleDateString()}
          </span>
        </div>

        {review.comment && (
          <p className="leading-6 text-muted-foreground">
            {review.comment}
          </p>
        )}
      </div>
    </article>
  )
}
