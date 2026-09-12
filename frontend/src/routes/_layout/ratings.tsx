/**
 * Ratings page for exploring movies based on user ratings.
 */
import { createFileRoute } from "@tanstack/react-router"
import { useState } from "react"
import { MoviesByMinRating } from "@/components/Movies/MoviesByMinRating"
import { TopRatedMovies } from "@/components/Movies/TopRatedMovies"

export const Route = createFileRoute("/_layout/ratings")({
  component: Ratings,
})

/**
 * Display the selected rating view and allow filtering movies
 * by a user-defined minimum average rating.
 */
function Ratings() {
  const [ratingView, setRatingView] = useState<"top" | "minimum">("top")
  const [minRating, setMinRating] = useState("1")

  const numericMinRating = Number(minRating.replace(",", "."))
  const isValidMinRating =
    Number.isFinite(numericMinRating) &&
    numericMinRating >= 1 && 
    numericMinRating <= 10

  return (
        <div className="space-y-8">
        <div>
            <h1 className="text-3xl font-bold">Ratings</h1>

            <p className="mt-1 text-sm text-muted-foreground">
                Explore movies based on user ratings.
            </p>
        </div>
        
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end">
            <div  className="space-y-1">
                <label
                    htmlFor="rating_view"
                    className="block text-sm font-medium"
                >
                    View
                </label>

                <select
                    id="rating_view"
                    value={ratingView}
                    onChange={(event) => setRatingView(event.target.value as "top" | "minimum")
                    }
                    className="rounded-md border border-input bg-background px-3 py-2 text-sm outline-none transition-colors focus:border-primary"
                >
                    <option value="top">Top Rated</option>
                    <option value="minimum">Minimum Rating</option>
                </select>
            </div>

            {ratingView === "minimum" && (
                <div className="space-y-1">
                    <label
                        htmlFor="min_rating"
                        className="block text-sm font-medium"
                    >
                        Minimum rating
                    </label>

                    <input
                        id="min_rating"
                        type="text"
                        inputMode="decimal"
                        value={minRating}
                        onChange={(event) => setMinRating(event.target.value)}
                        className="w-28 rounded-md border border-input bg-background px-3 py-2 text-sm outline-none transition-colors focus:border-primary"
                        />
                    </div>
                )}
            </div>

            {ratingView === "top" && <TopRatedMovies />}
            
            {ratingView === "minimum" && isValidMinRating && (
                <MoviesByMinRating minRating={numericMinRating} />
            )}

            {ratingView === "minimum" && !isValidMinRating && (
                <p className="text-sm text-destructive">
                   Enter a rating between 1 and 10.
                </p>
            )}
        </div>
    )
}
