/**
 * Admin route for creating a new movie.
 */
import { createFileRoute } from "@tanstack/react-router"

import { CreateMovieForm } from "@/components/Movies/CreateMovieForm"
import { useAdmin } from "@/hooks/useAdmin"

/**
 * Configure the admin-only create movie route.
 */
export const Route = createFileRoute("/_layout/movies/create")({
  component: CreateMoviePage,
  head: () => ({
    meta: [
      {
        title: "Create Movie - Movie Review Platform",
      },
    ],
  }),
})

/**
 * Display the movie creation form only to administrators.
 */
function CreateMoviePage() {
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
      <CreateMovieForm />
    </div>
  )
}