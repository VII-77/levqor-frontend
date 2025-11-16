"use client";
import Link from "next/link";
import { useState } from "react";
import Logo from "./Logo";

export default function PublicNav() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 bg-slate-950/80 backdrop-blur-md border-b border-slate-800/60">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center gap-8">
          <Logo />
          
          {/* Desktop Navigation */}
          <div className="hidden lg:flex gap-6">
            {/* Product Dropdown */}
            <div className="group relative">
              <button className="text-sm text-slate-300 hover:text-white transition flex items-center gap-1">
                Product
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div className="absolute left-0 mt-2 w-56 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all bg-slate-900 border border-slate-800 rounded-lg shadow-xl py-2">
                <Link href="/how-it-works" className="block px-4 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white">How It Works</Link>
                <Link href="/integrations" className="block px-4 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white">Integrations</Link>
                <Link href="/tour" className="block px-4 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white">Product Tour</Link>
                <Link href="/screenshots" className="block px-4 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white">Screenshots</Link>
              </div>
            </div>

            {/* Solutions Dropdown */}
            <div className="group relative">
              <button className="text-sm text-slate-300 hover:text-white transition flex items-center gap-1">
                Solutions
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div className="absolute left-0 mt-2 w-56 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all bg-slate-900 border border-slate-800 rounded-lg shadow-xl py-2">
                <Link href="/solutions/ecommerce" className="block px-4 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white">For eCommerce</Link>
                <Link href="/solutions/agencies" className="block px-4 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white">For Agencies</Link>
                <Link href="/solutions/coaches" className="block px-4 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white">For Coaches</Link>
                <Link href="/solutions/creators" className="block px-4 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white">For Creators</Link>
                <Link href="/solutions/smb" className="block px-4 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white">For Small Business</Link>
              </div>
            </div>

            {/* Resources Dropdown */}
            <div className="group relative">
              <button className="text-sm text-slate-300 hover:text-white transition flex items-center gap-1">
                Resources
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div className="absolute left-0 mt-2 w-56 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all bg-slate-900 border border-slate-800 rounded-lg shadow-xl py-2">
                <Link href="/blog" className="block px-4 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white">Blog</Link>
                <Link href="/case-studies" className="block px-4 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white">Case Studies</Link>
                <Link href="/faq" className="block px-4 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white">FAQ</Link>
                <Link href="/changelog" className="block px-4 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white">Changelog</Link>
                <Link href="/roadmap" className="block px-4 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white">Roadmap</Link>
                <Link href="/support" className="block px-4 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white">Support Center</Link>
              </div>
            </div>

            {/* Company Dropdown */}
            <div className="group relative">
              <button className="text-sm text-slate-300 hover:text-white transition flex items-center gap-1">
                Company
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div className="absolute left-0 mt-2 w-56 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all bg-slate-900 border border-slate-800 rounded-lg shadow-xl py-2">
                <Link href="/about" className="block px-4 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white">About Us</Link>
                <Link href="/story" className="block px-4 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white">Our Story</Link>
                <Link href="/team" className="block px-4 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white">Team</Link>
                <Link href="/security" className="block px-4 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white">Security & Compliance</Link>
                <Link href="/contact" className="block px-4 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white">Contact</Link>
              </div>
            </div>

            <Link href="/pricing" className="text-sm text-slate-300 hover:text-white transition">Pricing</Link>
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="lg:hidden text-slate-300 hover:text-white"
            aria-label="Toggle menu"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={mobileMenuOpen ? "M6 18L18 6M6 6l12 12" : "M4 6h16M4 12h16M4 18h16"} />
            </svg>
          </button>
        </div>

        <div className="flex items-center gap-4">
          <Link href="/signin" className="hidden sm:block text-sm text-slate-300 hover:text-white transition">
            Sign in
          </Link>
          <Link href="/pricing" className="px-5 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition text-sm">
            Get Started
          </Link>
        </div>
      </nav>

      {/* Mobile menu */}
      {mobileMenuOpen && (
        <div className="lg:hidden bg-slate-900 border-t border-slate-800">
          <div className="px-4 py-4 space-y-3">
            <div>
              <div className="font-semibold text-white mb-2">Product</div>
              <Link href="/how-it-works" className="block py-2 text-sm text-slate-300">How It Works</Link>
              <Link href="/integrations" className="block py-2 text-sm text-slate-300">Integrations</Link>
              <Link href="/tour" className="block py-2 text-sm text-slate-300">Product Tour</Link>
              <Link href="/screenshots" className="block py-2 text-sm text-slate-300">Screenshots</Link>
            </div>
            <div>
              <div className="font-semibold text-white mb-2">Solutions</div>
              <Link href="/solutions/ecommerce" className="block py-2 text-sm text-slate-300">For eCommerce</Link>
              <Link href="/solutions/agencies" className="block py-2 text-sm text-slate-300">For Agencies</Link>
              <Link href="/solutions/coaches" className="block py-2 text-sm text-slate-300">For Coaches</Link>
              <Link href="/solutions/creators" className="block py-2 text-sm text-slate-300">For Creators</Link>
              <Link href="/solutions/smb" className="block py-2 text-sm text-slate-300">For Small Business</Link>
            </div>
            <div>
              <div className="font-semibold text-white mb-2">Resources</div>
              <Link href="/blog" className="block py-2 text-sm text-slate-300">Blog</Link>
              <Link href="/case-studies" className="block py-2 text-sm text-slate-300">Case Studies</Link>
              <Link href="/faq" className="block py-2 text-sm text-slate-300">FAQ</Link>
              <Link href="/changelog" className="block py-2 text-sm text-slate-300">Changelog</Link>
              <Link href="/roadmap" className="block py-2 text-sm text-slate-300">Roadmap</Link>
              <Link href="/support" className="block py-2 text-sm text-slate-300">Support</Link>
            </div>
            <div>
              <div className="font-semibold text-white mb-2">Company</div>
              <Link href="/about" className="block py-2 text-sm text-slate-300">About Us</Link>
              <Link href="/story" className="block py-2 text-sm text-slate-300">Our Story</Link>
              <Link href="/team" className="block py-2 text-sm text-slate-300">Team</Link>
              <Link href="/security" className="block py-2 text-sm text-slate-300">Security</Link>
              <Link href="/contact" className="block py-2 text-sm text-slate-300">Contact</Link>
            </div>
            <Link href="/pricing" className="block py-2 text-sm font-semibold text-white">Pricing</Link>
          </div>
        </div>
      )}
    </header>
  );
}
