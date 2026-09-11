/**
 * Administrator user list.
 */
import { useQuery } from "@tanstack/react-query"
import { UsersService } from "@/client"
import { UserCard } from "@/components/Users/UserCard"

function getUsersQueryOptions() {
    return {
        queryFn: async () => (await UsersService.getUsersPrivateDada({ query: { page: 1, page_size: 50 }})).data,
        queryKey: ["users"]
    }
}

/**
 * Load and display user accounts for administration.
 */
export function UsersList() {
    const { data, isLoading, isError } = useQuery(getUsersQueryOptions())

    if (isLoading) {
        return <p className="text-sm text-muted-foreground">Loading users...</p>
    }

    if (isError) return <p className="text-sm text-destructive">Unable to load users.</p>

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-xl font-semibold">Users</h2>
                <p className="mt-1 text-sm text-muted-foreground">
                    Manage user accounts, permissions, and account status.
                </p>
            </div>

            {!data || data.count === 0 ? (
                <p className="text-sm text-muted-foreground">No users available.</p>
            ) : (
                <div className="grid gap-4">
                    {data.users.map((user) => (
                        <UserCard key={user.id} user={user} />
                    ))}
                </div>
            )}

        </div>
    )
}