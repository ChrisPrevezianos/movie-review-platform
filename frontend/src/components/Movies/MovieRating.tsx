/**
 * Display the average rating for a movie.
 */
import { useQuery } from "@tanstack/react-query"
import { ReviewsService} from "@/client"

/**
 * Load movie reviews and calculate their average rating.
 */
export function MovieRating({ movieId } : { movieId : string }) {

    const { data, isLoading, isError } = useQuery({
        queryKey: ["reviews", movieId],
        queryFn: async () => {
            const response = await ReviewsService.getReviewsByMovie({
                path: { movie_id: movieId },
                query: { page: 1, page_size: 50}
            })
            return response.data
        }

    })

    if (isLoading) return <div className="text-sm text-muted-foreground">Loading...</div>

    if (isError) return <div className="text-sm text-destructive">Unable to load rating.</div>

    if (!data || data.count === 0) return <div className="text-sm text-muted-foreground">No ratings yet.</div>

    const totalRating = data.reviews.reduce((sum, review) => sum + review.rating, 0)

    const averageRating = (totalRating / data.reviews.length).toFixed(1)

    return (
        <div className="flex items-center gap-2">
            <span className="text-lg text-yellow-400">★</span>

            <span className="font-semibold">
                {averageRating}
            </span>

            <span className="text-sm text-muted-foreground">
                {data.count} {data.count === 1 ? "rating" : "ratings"}
            </span>
        </div>
    )
}