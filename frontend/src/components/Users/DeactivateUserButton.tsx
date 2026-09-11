/**
 * Button for deactivating a user account.
 */
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { UsersService } from "@/client"
import { AxiosError } from "axios"

/**
 * Deactivate the selected user after confirmation.
 */
export function DeactivateUserButton({ userId } : { userId: string}) {

    const queryClient = useQueryClient()

    const mutation = useMutation({
        mutationFn: () => UsersService.deactivateUser({
            path: { user_id: userId },
        }),

        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: ["users"]
            })
        },
    })

    function handleDeactivate() {
        if (window.confirm("Are you sure you want to deactivate this user?")) {
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
                onClick={handleDeactivate}
                disabled={mutation.isPending}
                className="text-sm text-muted-foreground transition-colors hover:text-destructive disabled:cursor-not-allowed disabled:opacity-50"
            >
                {mutation.isPending ? "Deactivating..." : "Deactivate"}
            </button>

            {mutation.isError && (
                <p className="text-xs text-destructive">
                    {errorMessage ?? "Unable to deactivate user. Please try again."}
                </p>
            )}
        </div>
    )
}