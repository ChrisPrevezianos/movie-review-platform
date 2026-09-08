/**
 * Main authenticated page containing the welcome section and movie list.
 */
import useAuth from "@/hooks/useAuth"
import { createFileRoute } from "@tanstack/react-router"
import { MoviesList } from "@/components/Movies/MoviesList"

/**
 * Configure the main authenticated dashboard route.
 */
export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
  head: () => ({
    meta: [
      {
        title: "Dashboard -  Movie Review Platform",
      },
    ],
  }),
})

/**
 * Display the authenticated user's dashboard and available movies.
 */
function Dashboard() {
  const { user: currentUser } = useAuth()

  if (!currentUser) {
    return null
  }

  return (
    <div className="flex flex-col gap-8">
      <div>
        <h1 className="text-2xl truncate max-w-sm">
          Hi, {currentUser?.username || currentUser?.email} 👋
        </h1>
        <p className="text-muted-foreground">
          Welcome back, nice to see you again!!!
        </p>
      </div>
      <MoviesList />
    </div>
  )
}
