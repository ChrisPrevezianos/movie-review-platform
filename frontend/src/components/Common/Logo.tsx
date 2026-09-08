/**
 * Application logo used across authentication pages and the main sidebar.
 */
import { Link } from "@tanstack/react-router"
import { Film } from "lucide-react"

interface LogoProps {
  variant?: "full" | "icon" | "responsive"
  className?: string
  asLink?: boolean
}

/**
 * Display the Movie Review Platform branding in full, icon, or responsive form.
 */
export function Logo({
  variant = "full",
  className,
  asLink = true,
}: LogoProps) {

  const content =
    variant === "responsive" ? (
      <>
        <div
          className={`flex items-center gap-2 group-data-[collapsible=icon]:hidden ${className ?? ""}`}
        >
          <Film className="size-6" />
          <span className="text-lg font-semibold">Movie Review Platform</span>
        </div>

        <Film
          className={`size-5 hidden group-data-[collapsible=icon]:block ${className ?? ""}`}
        />
      </>
    ) : variant === "icon" ? (
      <Film className={`size-5 ${className ?? ""}`} />
    ) : (
      <div className={`flex items-center gap-3 ${className ?? ""}`}>
        <Film className="size-10" />
        <span className="text-3xl font-semibold">Movie Review Platform</span>
      </div>
    )

  if (!asLink) {
    return content
  }

  return <Link to="/">{content}</Link>
}
