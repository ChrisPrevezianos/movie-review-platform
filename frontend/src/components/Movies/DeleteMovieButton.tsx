/**
 * Button for deleting a movie.
 */
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useNavigate } from "@tanstack/react-router"
import { AxiosError } from "axios"

import { MoviesService } from "@/client"

/**
 * Delete the selected movie after confirmation.
 */
export function DeleteMovieButton({ movieId }: { movieId: string }) {
  const queryClient = useQueryClient()
  const navigate = useNavigate()

  const mutation = useMutation({
    mutationFn: () =>
      MoviesService.deleteMovie({
        path: {
          movie_id: movieId,
        },
      }),

    onSuccess: async () => {
      await queryClient.invalidateQueries({
        queryKey: ["movies"],
      })

      navigate({ to: "/" })
    },
  })

  function handleDelete() {
    if (window.confirm("Are you sure you want to delete this movie?")) {
      mutation.mutate()
    }
  }

  const errorDetail =
    mutation.error instanceof AxiosError
      ? (mutation.error.response?.data as { detail?: unknown } | undefined)
          ?.detail
      : undefined

  const errorMessage =
    typeof errorDetail === "string" ? errorDetail : undefined

  return (
    <div className="flex flex-col items-end gap-1">
      <button
        type="button"
        onClick={handleDelete}
        disabled={mutation.isPending}
        className="text-sm text-muted-foreground transition-colors hover:text-destructive disabled:cursor-not-allowed disabled:opacity-50"
      >
        {mutation.isPending ? "Deleting..." : "Delete"}
      </button>

      {mutation.isError && (
        <p className="text-xs text-destructive">
          {errorMessage ?? "Unable to delete movie. Please try again."}
        </p>
      )}
    </div>
  )
}