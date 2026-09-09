/**
 * Button for deleting the current user's review.
 */
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { ReviewsService } from "@/client"

/**
 * Delete button for removing the current user's review.
 */
export function DeleteReviewButton({ reviewId, movieId } : { reviewId: string, movieId: string}) {
    const queryClient = useQueryClient()

    const mutation = useMutation({
        mutationFn: () =>
            ReviewsService.deleteReview({
                path: { review_id: reviewId },
            }),

        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: ["reviews", movieId],
            })
        },
    })

    /**
    * Confirm and delete the selected review.
    */
    function handleDelete() {
        if (window.confirm("Are you sure you want to delete this review?")) {
           mutation.mutate()
        }
    }

    return (
        <div className="flex flex-col items-end gap-1">
            <button
                type="button"
                onClick={handleDelete}
                disabled={mutation.isPending}
                className="text-sm text-muted-foreground transition-colors hover:text-foreground disabled:cursor-not-allowed disabled:opacity-50"
            >
                {mutation.isPending ? "Deleting..." : "Delete"}
            </button>

            {mutation.isError && (
                <p className="text-sm text-destructive">
                    Unable to delete review. Please try again.
                </p>
            )}
        </div>
    )
}
