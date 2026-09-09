/**
 * Form for updating an existing movie review.
 */
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useForm } from "react-hook-form"
import {
  ReviewsService,
  type ReviewPublic,
  type ReviewUpdate,
} from "@/client"

/**
 * Update the rating and comment of the current user's review.
 */
export function UpdateReviewForm({ movieId, review, onCancel } : { movieId: string, review: ReviewPublic, onCancel: () => void}) {
    const queryClient = useQueryClient()

    const form = useForm<ReviewUpdate>({
        defaultValues: {
            rating: review.rating,
            comment: review.comment ?? "",
        },
    })

    const mutation = useMutation({
        mutationFn: (data: ReviewUpdate) =>
            ReviewsService.updateReview({
                path: {
                    review_id: review.id,
                },
                body: {
                    rating: data.rating,
                    comment: data.comment,
                }
            }),

        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: ["reviews", movieId],
            })
            onCancel()
        },
    })

    /**
    * Submit the updated review data.
    */
    function onSubmit(data: ReviewUpdate) {
        mutation.mutate(data)
    }

    return (
        <form
            onSubmit={form.handleSubmit(onSubmit)}
            className="flex w-full max-w-2xl flex-col gap-4 rounded-lg border bg-card p-5"
        >
            <div>
            <h2 className="text-xl font-semibold">Edit review</h2>
            <p className="mt-1 text-sm text-muted-foreground">
                Rate this movie from 1 to 10 and optionally leave a comment.
            </p>
            </div>

            <div className="flex flex-col gap-2">
            <label htmlFor="rating" className="text-sm font-medium">
                Rating
            </label>

            <input
                id="rating"
                type="number"
                min={1}
                max={10}
                className="w-24 rounded-md border bg-background px-3 py-2"
                {...form.register("rating", {
                required: "Rating is required.",
                min: {
                    value: 1,
                    message: "Rating must be at least 1.",
                },
                max: {
                    value: 10,
                    message: "Rating cannot be greater than 10.",
                },
                valueAsNumber: true,
                })}
            />

            {form.formState.errors.rating && (
                <p className="text-sm text-destructive">
                {form.formState.errors.rating.message}
                </p>
            )}
            </div>

            <div className="flex flex-col gap-2">
            <label htmlFor="comment" className="text-sm font-medium">
                Comment
                <span className="ml-1 text-muted-foreground">(optional)</span>
            </label>

            <textarea
                id="comment"
                rows={4}
                className="resize-y rounded-md border bg-background px-3 py-2"
                placeholder="What did you think about the movie?"
                {...form.register("comment")}
            />
            </div>

            <div className="flex items-center justify-between">
                <button
                    type="submit"
                    disabled={mutation.isPending}
                    className="inline-flex w-fit rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90 disabled:cursor-not-allowed disabled:opacity-50"
                >

                    {mutation.isPending ? "Saving..." : "Save changes"}
                </button>

                <button
                    type="button"
                    onClick={onCancel}
                    className="text-sm text-muted-foreground transition-colors hover:text-foreground"
                >
                    Cancel
                </button>
            </div>

            {mutation.isError && (
            <p className="text-sm text-destructive">
                Unable to update review. Please try again.
            </p>
            )}
        </form>
    )
}
