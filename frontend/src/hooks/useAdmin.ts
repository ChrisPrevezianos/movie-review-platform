/**
 * Authorization hook for checking whether the current user is an administrator.
 */
import { useQuery } from "@tanstack/react-query"
import { AxiosError } from "axios"
import { UsersService } from "@/client"
import useAuth from "./useAuth"

/**
 * Check whether the authenticated user can access admin-only resources.
 */
export const useAdmin = () => {
    const { user } = useAuth()

    const {
        data: isAdmin = false,
        isLoading: isAdminLoading,
    } = useQuery<boolean>({
        queryKey: ["is-admin", user?.id],

        queryFn: async () => {
            try {
                await UsersService.getUsersPrivateDada({
                    query: {
                        page: 1,
                        page_size: 1,
                    }
                })
                return true
            } catch (error) {
                if (error instanceof AxiosError && error.response?.status === 403) {
                    return false
                }
                throw error
            }
        },

        enabled: !!user,
        retry: false,
        staleTime: Infinity,
    })

    return {
        isAdmin,
        isAdminLoading
    }
}
