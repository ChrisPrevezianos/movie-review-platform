/**
 * Button for reactivating a user account.
 */
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { UsersService } from "@/client"
import { AxiosError } from "axios"

/**
 * Reactivate the selected user account.
 */
export function ReactivateUserButton({ userId } : { userId: string}) {

    const queryClient = useQueryClient()

    const mutation = useMutation({
        mutationFn: () => UsersService.reactivateUser({
            path: { user_id: userId },
        }),

        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: ["users"]
            })
        },
    })

    function handleReactivate() {
        if (window.confirm("Are you sure you want to reactivate this user?")) {
            mutation.mutate()
        }
    }

    const errorDetail = mutation.error instanceof AxiosError
    ? (mutation.error.response?.data as { detail?: unknown } | undefined)?.detail
    : undefined

    const errorMessage = typeof errorDetail === "string" ? errorDetail : undefined

    return (
        <div className="flex flex-col items-end gap-1">
            <button
                type="button"
                onClick={handleReactivate}
                disabled={mutation.isPending}
                className="text-sm text-muted-foreground transition-colors hover:text-primary disabled:cursor-not-allowed disabled:opacity-50"
            >
                {mutation.isPending ? "Reactivating..." : "Reactivate"}
            </button>

            {mutation.isError && (
                <p className="text-xs text-destructive">
                    {errorMessage ?? "Unable to reactivate user. Please try again."}
                </p>
            )}
        </div>
    )
}
