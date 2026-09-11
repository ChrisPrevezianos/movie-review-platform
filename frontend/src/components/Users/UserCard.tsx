/**
 * Display administrator-only user account information and actions.
 */
import { useState } from "react"
import type { UserPrivateData } from "@/client"
import { UpdateUserForm } from "@/components/Users/UpdateUserForm"
import { DeactivateUserButton } from "@/components/Users/DeactivateUserButton"
import { ReactivateUserButton } from "@/components/Users/ReactivateUserButton"

/**
 * Display a user account with editing and status management actions.
 */
export function UserCard({ user } : { user: UserPrivateData}) {
    const [isEditing, setIsEditing] = useState(false)

    if (isEditing) {
        return (
            <div className="rounded-lg border border-border p-4">
                <UpdateUserForm
                    user={user}
                    onCancel={() => setIsEditing(false)}
                />
            </div>
        )
    }

    return (
        <div className="rounded-lg border border-border p-4">

            <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                <div className="min-w-0">
                    <h2 className="text-base font-semibold">
                        {user.username}
                    </h2>

                    <p className="mt-1 break-all text-sm text-muted-foreground">
                        {user.email}
                    </p>

                    <div className="mt-3 flex flex-wrap gap-2">
                        <span className="rounded-full bg-muted px-2.5 py-1 text-xs text-muted-foreground">
                            {user.is_active ? "Active" : "Inactive"}
                        </span>

                        <span className="rounded-full bg-muted px-2.5 py-1 text-xs text-muted-foreground">
                            {user.is_superuser ? "Superuser" : "User"}
                       </span>
                    </div>

                    <p className="mt-3 text-xs text-muted-foreground">
                        Created: {new Date(user.created_at).toLocaleDateString("en-GB")}
                    </p>
                </div>

                <div className="flex shrink-0 items-center gap-4">
                    <button
                        type="button"
                        onClick={() => setIsEditing(true)}
                        className="text-sm text-muted-foreground transition-colors hover:text-foreground"
                    >
                        Edit
                    </button>

                    {user.is_active ? (
                        <DeactivateUserButton userId={user.id} />
                        ) : (
                        <ReactivateUserButton userId={user.id} />
                    )}
                </div>
            </div>
        </div>
    )
}