/**
 * Review card for displaying and managing a single movie review.
 */
import type { ReviewPublic } from "@/client"
import useAuth from "@/hooks/useAuth"
import { UpdateReviewForm } from "@/components/Reviews/UpdateReviewForm"
import { useState } from "react"
import { DeleteReviewButton } from "@/components/Reviews/DeleteReviewButton"

/**
 * Display a review and provide edit and delete actions to its owner.
 */
export function ReviewCard( { review } : { review: ReviewPublic}) {
    const reviewDate = review.updated_at || review.created_at

    const { user: currentUser } = useAuth()
    const [isEditing, setIsEditing] = useState(false)

    const isOwner = currentUser?.id === review.user_id

    if (isEditing) {
      return (
        <UpdateReviewForm
          movieId={review.movie_id}
          review={review}
          onCancel={() => setIsEditing(false)}
        />
      )
    }

    return (
    <article className="rounded-lg border bg-card p-4">
      <div className="flex flex-col gap-3">

        {isOwner && (
          <div className="flex items-center justify-between">
            <button
              type="button"
              onClick={() => setIsEditing(true)}
              className="text-sm text-muted-foreground transition-colors hover:text-foreground"
            >
              Edit
            </button>

            <DeleteReviewButton reviewId={review.id} movieId={review.movie_id} />
          </div>
        )}

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
