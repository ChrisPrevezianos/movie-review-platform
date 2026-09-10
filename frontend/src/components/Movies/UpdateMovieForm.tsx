/**
 * Form for updating a movie with its genres, actors, and directors.
 */
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useQuery } from "@tanstack/react-query"
import { useFieldArray, useForm } from "react-hook-form"
import { AxiosError } from "axios"
import {
    GenresService,
    MoviesService,
    type MovieUpdate,
    type MoviePublic
} from "@/client"
import { useNavigate } from "@tanstack/react-router"

/**
 * Update a movie and its related domain data.
 */
export function UpdateMovieForm({ movie }: { movie: MoviePublic }) {
    const navigate = useNavigate()

    const queryClient = useQueryClient()

    const form = useForm<MovieUpdate>({
        defaultValues: {
            title: movie.title,
            synopsis: movie.synopsis,
            release_year: movie.release_year,
            duration: movie.duration,
            age_rating: movie.age_rating,
            poster_url: movie.poster_url,
            trailer_url: movie.trailer_url,
            genre_ids: movie.genres.map((genre) => genre.id),
            actors: movie.actors.map((actor) => ({
                first_name: actor.first_name,
                last_name: actor.last_name,
                birth_date: null,
            })),
            directors: movie.directors.map((director) => ({
                first_name: director.first_name,
                last_name: director.last_name,
                birth_date: null,
            })),
        },
})

    const {
        fields: actorFields,
        append: appendActor,
        remove: removeActor,
    } = useFieldArray({
        control: form.control,
        name: "actors",
    })

    const {
        fields: directorFields,
        append: appendDirector,
        remove: removeDirector,
    } = useFieldArray({
        control: form.control,
        name: "directors",
    })

    const mutation = useMutation({
        mutationFn: (data: MovieUpdate) =>
            MoviesService.updateMovie({
                path: {
                    movie_id: movie.id,
                },
                body: data,
            }),

        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: ["movies"],
            })

            queryClient.invalidateQueries({
                queryKey: ["movie", movie.id],
            })

            navigate({
                to: "/movies/$movieId",
                params: {
                    movieId: movie.id,
                },
            })
        },
    })

    /**
    * Submit the update movie data.
    */
    function onSubmit(data: MovieUpdate) {
        const updateData: MovieUpdate = {}

        if (data.title !== movie.title) {
            updateData.title = data.title
        }

        if (data.synopsis !== movie.synopsis) {
            updateData.synopsis = data.synopsis
        }

        if (data.release_year !== movie.release_year) {
            updateData.release_year = data.release_year
        }

        if (data.duration !== movie.duration) {
            updateData.duration = data.duration
        }

        if (data.age_rating !== movie.age_rating) {
            updateData.age_rating = data.age_rating
        }

        if (data.poster_url !== movie.poster_url) {
            updateData.poster_url = data.poster_url
        }

        if (data.trailer_url !== movie.trailer_url) {
            updateData.trailer_url = data.trailer_url
        }

        const currentGenreIds = movie.genres.map((genre) => genre.id).sort()
        const updatedGenreIds = [...(data.genre_ids ?? [])].sort()

        if (JSON.stringify(updatedGenreIds) !== JSON.stringify(currentGenreIds)) {
            updateData.genre_ids = updatedGenreIds
        }

        const currentActors = movie.actors
            .map((actor) => `${actor.first_name.toLowerCase()}|${actor.last_name.toLowerCase()}`)
            .sort()

        const updatedActors = (data.actors ?? [])
            .map((actor) => `${actor.first_name.toLowerCase()}|${actor.last_name.toLowerCase()}`)
            .sort()

        if (JSON.stringify(updatedActors) !== JSON.stringify(currentActors)) {
            updateData.actors = data.actors
        }

        const currentDirectors = movie.directors
            .map((directors) => `${directors.first_name.toLowerCase()}|${directors.last_name.toLowerCase()}`)
            .sort()

        const updatedDirectors = (data.directors ?? [])
            .map((directors) => `${directors.first_name.toLowerCase()}|${directors.last_name.toLowerCase()}`)
            .sort()

        if (JSON.stringify(updatedDirectors) !== JSON.stringify(currentDirectors)) {
            updateData.directors = data.directors
        }

        mutation.mutate(updateData)
    }

    const errorDetail =
        mutation.error instanceof AxiosError
        ? (mutation.error.response?.data as { detail?: unknown } | undefined)?.detail
        : undefined

    const errorMessage = typeof errorDetail === "string" ? errorDetail : undefined

    const { data: genres = [], isLoading: isGenresLoading, isError: isGenresError } = useQuery({
        queryKey: ["genres"],
        queryFn: async () => {
            const response = await GenresService.getGenres()
            return response.data.genres
        },
    })

    return (
        <form
            onSubmit={form.handleSubmit(onSubmit)}
            className="flex w-full max-w-3xl flex-col gap-6 rounded-lg border bg-card p-6"
        >
            <div className="flex flex-col gap-2">
                <h2 className="text-xl font-semibold">Update movie</h2>
            </div>

            <div className="flex flex-col gap-2">
                <label htmlFor="title" className="text-sm font-medium">Title</label>

                <input
                    id="title"
                    type="text"
                    className="rounded-md border bg-background px-3 py-2"
                    {... form.register("title", {
                        required: "Title is required.",
                    })}
                />
            </div>

            <div className="flex flex-col gap-2">
                <label htmlFor="synopsis" className="text-sm font-medium">Synopsis</label>

                <textarea
                    id="synopsis"
                    rows={5}
                    className="resize-y rounded-md border bg-background px-3 py-2"
                    {... form.register("synopsis", {
                        required: "Synopsis is required.",
                    })}
                />
            </div>

            <div className="flex flex-col gap-2">
                <label htmlFor="release_year" className="text-sm font-medium">release_year</label>
                <input
                    id="release_year"
                    type="number"
                    className="rounded-md border bg-background px-3 py-2"
                    {... form.register("release_year", {
                        required: "Release year is required.",
                    valueAsNumber: true,
                    min: {
                        value: 1888,
                        message: "Release year is invalid.",
                    }
                })}
                />
            </div>

            <div className="flex flex-col gap-2">
                <label htmlFor="duration" className="text-sm font-medium">duration</label>
                <input
                    id="duration"
                    type="number"
                    className="rounded-md border bg-background px-3 py-2"
                    {... form.register("duration", {
                        required: "Duration is required.",
                    valueAsNumber: true,
                    min: {
                        value: 1,
                        message: "Duration must be greater than 0.",
                    }
                })}
                />
            </div>

            <div className="flex flex-col gap-2">
                <label htmlFor="age_rating" className="text-sm font-medium">age_rating</label>
                <select
                    id="age_rating"
                    className="rounded-md border bg-background px-3 py-2"
                    {... form.register("age_rating", {
                        required: "Age rating is required.",
                    })}
                >
                    <option value="G">G</option>
                    <option value="PG">PG</option>
                    <option value="PG-13">PG-13</option>
                    <option value="R">R</option>
                    <option value="NC-17">NC-17</option>
                </select>
            </div>

            <div className="flex flex-col gap-2">
                <label htmlFor="poster_url" className="text-sm font-medium">poster_url</label>
                <input
                    id="poster_url"
                    type="url"
                    className="rounded-md border bg-background px-3 py-2"
                    {... form.register("poster_url", {
                        required: "Poster URL is required.",
                    })}
                />
            </div>

            <div className="flex flex-col gap-2">
                <label htmlFor="trailer_url" className="text-sm font-medium">trailer_url</label>
                <input
                    id="trailer_url"
                    type="url"
                    className="rounded-md border bg-background px-3 py-2"
                    {... form.register("trailer_url", {
                        required: "Trailer URL is required.",
                    })}
                />
            </div>

            <div className="flex flex-col gap-2">
                <h3 className="font-medium">Genres</h3>

                <div className="flex flex-wrap gap-3">
                    {isGenresLoading && (
                        <p className="text-sm text-muted-foreground">Loading genres...</p>
                    )}

                    {isGenresError && (
                        <p className="text-sm text-destructive">Unable to load genres.</p>
                    )}

                    {genres.map((genre) => (
                        <label key={genre.id} className="flex items-center gap-2 text-sm">
                            <input
                                type="checkbox"
                                value={genre.id}
                                className="rounded-md border bg-background px-3 py-2"
                                {...form.register("genre_ids", {required: "Please select at least one genre."})}
                            />
                            {genre.name}
                        </label>
                    ))}
                    {form.formState.errors.genre_ids && (
                        <p className="text-sm text-destructive">
                            Please select at least one genre.
                        </p>
                    )}
                </div>
            </div>

            <div className="flex flex-col gap-3">
                <h3 className="font-medium">Actors</h3>

                {actorFields.map((field, index) => (
                    <div key={field.id} className="grid gap-2 md:grid-cols-[1fr_1fr_1fr_auto]">
                        <input
                            placeholder="First Name"
                            className="rounded-md border bg-background px-3 py-2"
                            {...form.register(`actors.${index}.first_name`, {
                                required: "First name is required.",
                            })}
                        />

                        <input
                            placeholder="Last Name"
                            className="rounded-md border bg-background px-3 py-2"
                            {...form.register(`actors.${index}.last_name`, {
                                required: "Last name is required.",
                            })}
                        />

                        <input
                            type="date"
                            className="rounded-md border bg-background px-3 py-2"
                            {...form.register(`actors.${index}.birth_date`, {setValueAs: (value) => value === "" ? null : value})}
                        />

                        <button
                            type="button" onClick={() => removeActor(index)}
                            className="text-sm text-muted-foreground transition-colors hover:text-destructive"
                        >
                            Remove
                        </button>
                    </div>
                ))}

                <button
                    type="button"
                    onClick={() =>
                        appendActor({
                            first_name: "",
                            last_name: "",
                            birth_date: null,
                        })
                    }
                    className="w-fit text-sm text-muted-foreground transition-colors hover:text-foreground"
                >
                    Add Actor
                </button>
            </div>

            <div className="flex flex-col gap-3">
                <h3 className="font-medium">Directors</h3>

                {directorFields.map((field, index) => (
                    <div key={field.id} className="grid gap-2 md:grid-cols-[1fr_1fr_1fr_auto]">
                        <input
                            placeholder="First Name"
                            className="rounded-md border bg-background px-3 py-2"
                            {...form.register(`directors.${index}.first_name`, {
                                required: "First name is required.",
                            })}
                        />

                        <input
                            placeholder="Last Name"
                            className="rounded-md border bg-background px-3 py-2"
                            {...form.register(`directors.${index}.last_name`, {
                                required: "Last name is required.",
                            })}
                        />

                        <input
                            type="date"
                            className="rounded-md border bg-background px-3 py-2"
                            {...form.register(`directors.${index}.birth_date`, {setValueAs: (value) => value === "" ? null : value})}
                        />

                        <button
                            type="button" onClick={() => removeDirector(index)}
                            className="text-sm text-muted-foreground transition-colors hover:text-destructive"
                        >
                            Remove
                        </button>
                    </div>
                ))}

                <button
                    type="button"
                    onClick={() =>
                        appendDirector({
                            first_name: "",
                            last_name: "",
                            birth_date: null,
                        })
                    }
                    className="w-fit text-sm text-muted-foreground transition-colors hover:text-foreground"
                >
                    Add Director
                </button>
            </div>

            {Object.keys(form.formState.errors).length > 0 && (
                <p className="text-sm text-destructive">
                    Please complete all required fields correctly.
                </p>
            )}

            <button
                type="submit"
                disabled={mutation.isPending}
                className="w-fit rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90 disabled:cursor-not-allowed disabled:opacity-50"
            >
                {mutation.isPending ? "Updating..." : "Update movie"}
            </button>
            {mutation.isError && (
                <p className="text-sm text-destructive">
                    {errorMessage ?? "Unable to update movie. Please try again."}
                </p>
            )}
        </form>
    )
}