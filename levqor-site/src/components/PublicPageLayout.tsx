import PublicNav from "./PublicNav";
import Footer from "./Footer";

export default function PublicPageLayout({ 
  children 
}: { 
  children: React.ReactNode 
}) {
  return (
    <div className="min-h-screen bg-slate-950">
      <PublicNav />
      <main className="min-h-[60vh]">
        {children}
      </main>
      <Footer />
    </div>
  );
}
