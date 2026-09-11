/**
 * Admin route for managing user accounts.
 */
import { createFileRoute } from "@tanstack/react-router"
import { UsersList } from "@/components/Users/UsersList"
import { useAdmin } from "@/hooks/useAdmin"

/**
 * Configure the admin-only user management route.
 */
export const Route = createFileRoute("/_layout/users")({
    component: UsersPage,
    head: () => ({
        meta: [
            {
                title: "Manage Users - Movie Review Platform"
            }
        ]
    })
})

/**
 * Display user management tools to administrators.
 */
function UsersPage() {
    const { isAdmin, isAdminLoading } = useAdmin()

    if (isAdminLoading) {
        return (
            <p className="text-sm text-muted-foreground">
                Checking permissions...
            </p>
        )
    }

    if (!isAdmin) {
        return (
            <p className="text-sm text-destructive">
                You do not have permission to access this page.
            </p>
        )
    }

    return (
        <div className="py-6">
            <UsersList />
        </div>
    )
}