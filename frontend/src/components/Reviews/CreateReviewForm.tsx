/**
 * Form for creating a review for a movie.
 */
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useForm } from "react-hook-form"
import { ReviewsService, type ReviewCreate } from "@/client"
import { AxiosError } from "axios"

/**
 * Create a review for the selected movie.
 */
export function CreateReviewForm({ movieId, onCreated } : { movieId: string, onCreated: () => void}) {
    const queryClient = useQueryClient()

    const form = useForm<ReviewCreate>({
        defaultValues: {
            rating: 1,
            comment: "",
        },
    })

    const mutation = useMutation({
        mutationFn: (data: ReviewCreate) =>
            ReviewsService.createReview({
                path: { movie_id: movieId },
                body: {
                    rating: data.rating,
                    comment: data.comment,
                }
            }),

        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: ["reviews", movieId],
            })

            form.reset()
            onCreated()
        },
    })

    function onSubmit(data: ReviewCreate) {
        mutation.mutate(data)
    }

    const errorMessage =
        mutation.error instanceof AxiosError
        ? (mutation.error.response?.data as { detail?: string } | undefined)?.detail
        : undefined

    return (
        <form
            onSubmit={form.handleSubmit(onSubmit)}
            className="flex w-full max-w-2xl flex-col gap-4 rounded-lg border bg-card p-5"
        >
            <div>
            <h2 className="text-xl font-semibold">Write a review</h2>
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

            <button
            type="submit"
            disabled={mutation.isPending}
            className="inline-flex w-fit rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90 disabled:cursor-not-allowed disabled:opacity-50"
            >
            {mutation.isPending ? "Submitting..." : "Submit review"}
            </button>

            {mutation.isError && (
            <p className="text-sm text-destructive">
                {errorMessage ?? "Unable to submit review. Please try again."}
            </p>
            )}
        </form>
    )
}