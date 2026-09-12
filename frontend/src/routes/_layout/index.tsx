/**
 * Main authenticated page containing the welcome section,
 * movie search controls and movie list.
 */
import useAuth from "@/hooks/useAuth"
import { createFileRoute } from "@tanstack/react-router"
import { MoviesList } from "@/components/Movies/MoviesList"
import { useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { FilteredMoviesList } from "@/components/Movies/FilteredMoviesList"
import { GenresService } from "@/client"

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
 * Display the authenticated user's dashboard with movie search
 * and available movies.
 */
function Dashboard() {
  const { user: currentUser } = useAuth()
  const [searchType, setSearchType] = useState<"title" | "genre" | "actor" | "director">("title")
  const [searchValue, setSearchValue] = useState("")

  const { data: genresData, isLoading: genresLoading } = useQuery({
    queryKey: ["genres"],
    queryFn: async () => {
      const response = await GenresService.getGenres()
      return response.data
    },
    enabled: searchType === "genre"
  })

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

      <div className="flex flex-col gap-4 sm:flex-row sm:items-end">
        <div className="space-y-1">
          <label
            htmlFor="search_type"
            className="block text-sm font-medium"
          >
            Search by
          </label>

          <select
            id="search_type"
            value={searchType}
            onChange={(event) => { setSearchType(event.target.value as "title" | "genre" | "actor" | "director");setSearchValue("")}}
            className="w-40 rounded-md border border-input bg-background px-3 py-2 text-sm outline-none transition-colors focus:border-primary"
          >
            <option value="title">Title</option>
            <option value="genre">Genre</option>
            <option value="actor">Actor</option>
            <option value="director">Director</option>
          </select>
        </div>

        <div className="space-y-1">
          <label
            htmlFor="search_value"
            className="block text-sm font-medium"
          >
            Search value
          </label>

          {searchType === "genre" ? (
            <select
              id="search_value"
              value={searchValue}
              onChange={(event) => setSearchValue(event.target.value)}
              className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm outline-none transition-colors focus:border-primary sm:w-72"
            >
              <option value="">Select genre...</option>

              {genresLoading ? (
                <option disabled>Loading genres...</option>
              ) : (
                genresData?.genres.map((genre) => (
                  <option key={genre.id} value={genre.name}>{genre.name}</option>
                ))
              )}
            </select>
            ) : (
            <input
              id="search_value"
              type="text"
              value={searchValue}
              onChange={(event) => setSearchValue(event.target.value)}
              placeholder="Type to search..."
              className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm outline-none transition-colors focus:border-primary sm:w-72"
            />
          )}
        </div>
      </div>

      {searchValue.trim() !== "" ?(
        <FilteredMoviesList
          searchType={searchType}
          searchValue={searchValue.trim()}
        />
      ) : (
        <MoviesList />
      )}
    </div>
  )
}
