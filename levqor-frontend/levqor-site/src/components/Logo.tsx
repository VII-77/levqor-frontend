import Link from "next/link";

export default function Logo({ className = "" }: { className?: string }) {
  return (
    <Link href="/" className={`flex items-center gap-2 ${className}`}>
      <div className="flex items-center justify-center w-8 h-8 bg-gradient-to-br from-blue-500 to-violet-600 rounded-lg">
        <span className="text-white font-bold text-lg">L</span>
      </div>
      <span className="text-xl font-bold text-white">Levqor</span>
    </Link>
  );
}
