/**
 * Main application sidebar for authenticated users.
 */
import { Home, Plus, Users } from "lucide-react"
import { SidebarAppearance } from "@/components/Common/Appearance"
import { Logo } from "@/components/Common/Logo"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
} from "@/components/ui/sidebar"
import useAuth from "@/hooks/useAuth"
import { type Item, Main } from "./Main"
import { User } from "./User"
import { useAdmin } from "@/hooks/useAdmin"

const baseItems: Item[] = [
  { icon: Home, title: "Dashboard", path: "/" },
]

/**
 * Display application navigation, appearance settings, and user information.
 */
export function AppSidebar() {
  const { user: currentUser } = useAuth()
  const { isAdmin } = useAdmin()

  const items = isAdmin
    ? [
        ...baseItems,
        { icon: Plus, title: "Create Movie", path: "/movies/create" },
        { icon: Users, title: "Manage Users", path: "/users"}
      ]
    : baseItems

  return (
    <Sidebar collapsible="icon">
      <SidebarHeader className="px-4 py-6 group-data-[collapsible=icon]:px-0 group-data-[collapsible=icon]:items-center">
        <Logo variant="responsive" />
      </SidebarHeader>
      <SidebarContent>
        <Main items={items} />
      </SidebarContent>
      <SidebarFooter>
        <SidebarAppearance />
        <User user={currentUser} />
      </SidebarFooter>
    </Sidebar>
  )
}

export default AppSidebar
