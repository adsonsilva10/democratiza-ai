import CleanSidebarLayoutAdaptive from '@/components/layout/CleanSidebarLayoutAdaptive'

export default function PlataformaLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return <CleanSidebarLayoutAdaptive>{children}</CleanSidebarLayoutAdaptive>
}