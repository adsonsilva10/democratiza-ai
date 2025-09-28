import CleanSidebarLayout from '@/components/layout/CleanSidebarLayoutSimple'

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return <CleanSidebarLayout>{children}</CleanSidebarLayout>
}