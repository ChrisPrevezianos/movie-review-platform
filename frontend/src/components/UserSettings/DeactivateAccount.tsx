/**
 * Account settings component for deactivating the current user's account.
 */
import { useMutation } from "@tanstack/react-query";
import { AxiosError } from "axios";
import useAuth from "../../hooks/useAuth";
import { UsersService } from "@/client"

/**
 * Allow the authenticated user to deactivate their own account.
 */
export default function DeactivateAccount() {
    const { logout } = useAuth();

    const mutation = useMutation({
        mutationFn: () => UsersService.deactivateUserMe(),
        onSuccess: () => {
            logout();
        },
    })

    /**
     * Confirm and request account deactivation.
     */
    function handleDeactivate() {
        const confirmed = window.confirm(
            "Are you sure you want to deactivate your account"
        )

        if (confirmed) {
            mutation.mutate();
        }
    }

    const errorDetail = mutation.error instanceof AxiosError
        ? (mutation.error.response?.data as { detail?: unknown } | undefined)
          ?.detail
        : undefined

    const errorMessage =
        typeof errorDetail === "string" ? errorDetail : undefined

    return (
        <div className="max-w-xl space-y-4">
            <div>
                <h2 className="text-lg font-semibold">Deactivate Account</h2>

                <p className="mt-1 text-sm text-muted-foreground">
                    Deactivating your account will prevent you from signing in until an
                    administrator reactivates it.
                </p>
            </div>

            <button
                type="button"
                onClick={handleDeactivate}
                disabled={mutation.isPending}
                className="text-sm font-medium text-destructive transition-colors hover:underline disabled:cursor-not-allowed disabled:opacity-50"
            >
                {mutation.isPending ? "Deactivating..." : "Deactivate Account"}
            </button>

            {mutation.isError && (
            <p className="text-sm text-destructive">
                {errorMessage ??
                "Unable to deactivate your account. Please try again."}
            </p>
            )}
        </div>
    )
}
