import SidebarLayoutAdvanced from '@/components/layout/SidebarLayoutAdvanced'

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <SidebarLayoutAdvanced>
      {children}
    </SidebarLayoutAdvanced>
  )
}