/**
 * Admin route for updating an existing movie.
 */
import { createFileRoute } from "@tanstack/react-router"
import { useQuery } from "@tanstack/react-query"
import { MoviesService } from "@/client"
import { useAdmin } from "@/hooks/useAdmin"
import { UpdateMovieForm } from "@/components/Movies/UpdateMovieForm"

/**
 * Configure the admin-only movie update route.
 */
export const Route = createFileRoute("/_layout/movies/$movieId_/edit")({
  component: UpdateMoviePage,
  head: () => ({
    meta: [
      {
        title: "Update Movie - Movie Review Platform",
      },
    ],
  }),
})

/**
 * Load the selected movie and display its update form to administrators.
 */
function UpdateMoviePage() {
    const { movieId } = Route.useParams()

    const { isAdmin, isAdminLoading } = useAdmin()

    const { data: movie, isLoading, isError } = useQuery({
        queryKey: ["movie", movieId],
        queryFn: async () => {
            const response = await MoviesService.getMovie({
                path: { movie_id: movieId },
            })
            return response.data
        },
        enabled: isAdmin,
    })

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

    if (isLoading) {
        return <p className="text-muted-foreground">Loading...</p>
    }

    if (isError) {
        return (
            <p className="text-sm text-destructive">
                Unable to load movie.
            </p>
        )
    }

    if (!movie) {
        return <p className="text-muted-foreground">Movie not found.</p>
    }

    return (
        <div className="py-6">
          <UpdateMovieForm movie={movie} />
        </div>
      )
}