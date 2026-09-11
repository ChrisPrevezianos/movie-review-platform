/**
 * Admin form for updating a user's account details and permissions.
 */
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useForm } from "react-hook-form"
import { AxiosError } from "axios"
import { UsersService, type UserPrivateData, type UserUpdate } from "@/client"

/**
 * Allow an administrator to update a user's account.
 */
export function UpdateUserForm({ user, onCancel } : { user: UserPrivateData, onCancel: () => void }) {

    const queryClient = useQueryClient()

    const form = useForm<UserUpdate>({
        defaultValues: {
            username: user.username,
            email: user.email,
            password: "",
            is_active: user.is_active,
            is_superuser: user.is_superuser
        },
    })

    const mutation = useMutation({
        mutationFn: (data: UserUpdate) =>
            UsersService.updateUser({
                path: { user_id: user.id},
                body: data
            }),

        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: ["users"]
            })

            queryClient.invalidateQueries({
                queryKey: ["is-admin"]
            })
            onCancel()
        },
    })

    /**
    * Submit only the user fields that have changed.
    */
    function onSubmit(data: UserUpdate) {
        const updateData: UserUpdate = {}

        if (data.username !== user.username) {
            updateData.username = data.username
        }

        if (data.email !== user.email) {
            updateData.email = data.email
        }

        if (data.password) {
            updateData.password = data.password
        }

        if (data.is_active !== user.is_active) {
            updateData.is_active = data.is_active
        }

        if (data.is_superuser !== user.is_superuser) {
            updateData.is_superuser = data.is_superuser
        }

        mutation.mutate(updateData)
    }

    const errorDetail =
        mutation.error instanceof AxiosError
        ? (mutation.error.response?.data as { detail?: unknown } | undefined)?.detail
        : undefined

    const errorMessage = typeof errorDetail === "string" ? errorDetail : undefined

    return (
        <form
            onSubmit={form.handleSubmit(onSubmit)}
            className="max-w-xl space-y-5"
        >
            <div>
                <h2 className="text-xl font-semibold">Update User</h2>
                <p className="mt-1 text-sm text-muted-foreground">
                    Update account information and permissions.
                </p>
            </div>

            <div className="space-y-2">
                <label htmlFor="username" className="text-sm font-medium">Username</label>
                <input
                    id="username"
                    type="text"
                    className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm outline-none transition-colors focus:border-primary"
                    {...form.register("username", {
                        required: "Username is required.",
                    })}
                />
                {form.formState.errors.username && (
                    <p className="text-sm text-destructive">
                        {form.formState.errors.username.message}
                    </p>
                )}
            </div>

            <div className="space-y-2">
                <label htmlFor="email" className="text-sm font-medium">Email</label>
                <input
                    id="email"
                    type="email"
                    className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm outline-none transition-colors focus:border-primary"
                    {...form.register("email", {
                        required: "Email is required.",
                    })}
                />
                {form.formState.errors.email && (
                    <p className="text-sm text-destructive">
                        {form.formState.errors.email.message}
                    </p>
                )}
            </div>

            <div className="space-y-2">
                <label htmlFor="password" className="text-sm font-medium">Password</label>
                <input
                    id="password"
                    type="password"
                    className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm outline-none transition-colors focus:border-primary"
                    {...form.register("password")}
                />
                    <p className="text-xs text-muted-foreground">
                        Leave blank to keep the current password.
                    </p>
            </div>

            <div className="flex items-center gap-3">
                <label htmlFor="is_active" className="text-sm font-medium">Active account</label>
                <input
                    id="is_active"
                    type="checkbox"
                    className="h-4 w-4 accent-primary"
                    {...form.register("is_active")}
                />
            </div>

            <div className="flex items-center gap-3">
                <label htmlFor="is_superuser" className="text-sm font-medium">Superuser</label>
                <input
                    id="is_superuser"
                    type ="checkbox"
                    className="h-4 w-4 accent-primary"
                    {...form.register("is_superuser")}
                />
            </div>

            <div className="flex items-center gap-3 pt-2">
                <button
                    type="submit"
                    disabled={mutation.isPending}
                    className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
                >
                    {mutation.isPending ? "Updating..." : "Update User"}
                </button>

                <button
                    type="button"
                    onClick={onCancel}
                    className="rounded-md border border-border px-4 py-2 text-sm font-medium text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
                >
                    Cancel
                </button>
            </div>
            {mutation.isError && (
                <p className="text-sm text-destructive">
                    {errorMessage ?? "Unable to update user. Please try again."}
                </p>
            )}
        </form>
    )
}
