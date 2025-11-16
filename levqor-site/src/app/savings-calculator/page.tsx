"use client";
import PublicPageLayout from "@/components/PublicPageLayout";
import { useState } from "react";
import Link from "next/link";

export default function SavingsCalculatorPage() {
  const [hoursPerWeek, setHoursPerWeek] = useState(10);
  const [hourlyValue, setHourlyValue] = useState(50);

  const weeklyWaste = hoursPerWeek * hourlyValue;
  const monthlyWaste = weeklyWaste * 4;
  const yearlyWaste = weeklyWaste * 52;

  return (
    <PublicPageLayout>
      <div className="max-w-4xl mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-200 mb-6">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            Savings Calculator
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            Calculate your automation ROI
          </h1>
          <p className="text-xl text-slate-400">
            See how much time and money you're wasting on manual tasks.
          </p>
        </div>

        <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-8 mb-12">
          <div className="space-y-8">
            {/* Hours Input */}
            <div>
              <label className="block text-white font-semibold mb-3">
                Hours per week spent on repetitive tasks
              </label>
              <input
                type="range"
                min="1"
                max="40"
                value={hoursPerWeek}
                onChange={(e) => setHoursPerWeek(Number(e.target.value))}
                className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer"
              />
              <div className="flex justify-between items-center mt-2">
                <span className="text-slate-400 text-sm">1 hour</span>
                <span className="text-emerald-400 font-bold text-2xl">{hoursPerWeek} hours</span>
                <span className="text-slate-400 text-sm">40 hours</span>
              </div>
            </div>

            {/* Hourly Value Input */}
            <div>
              <label className="block text-white font-semibold mb-3">
                What's your time worth per hour? (£)
              </label>
              <input
                type="range"
                min="20"
                max="200"
                step="10"
                value={hourlyValue}
                onChange={(e) => setHourlyValue(Number(e.target.value))}
                className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer"
              />
              <div className="flex justify-between items-center mt-2">
                <span className="text-slate-400 text-sm">£20/hr</span>
                <span className="text-emerald-400 font-bold text-2xl">£{hourlyValue}/hr</span>
                <span className="text-slate-400 text-sm">£200/hr</span>
              </div>
            </div>
          </div>
        </div>

        {/* Results */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <div className="bg-gradient-to-br from-red-500/10 to-orange-500/10 border border-red-500/30 rounded-xl p-6 text-center">
            <div className="text-4xl font-bold text-red-400 mb-2">£{weeklyWaste.toLocaleString()}</div>
            <div className="text-slate-300">Wasted per week</div>
          </div>
          <div className="bg-gradient-to-br from-orange-500/10 to-yellow-500/10 border border-orange-500/30 rounded-xl p-6 text-center">
            <div className="text-4xl font-bold text-orange-400 mb-2">£{monthlyWaste.toLocaleString()}</div>
            <div className="text-slate-300">Wasted per month</div>
          </div>
          <div className="bg-gradient-to-br from-yellow-500/10 to-red-500/10 border border-yellow-500/30 rounded-xl p-6 text-center">
            <div className="text-4xl font-bold text-yellow-400 mb-2">£{yearlyWaste.toLocaleString()}</div>
            <div className="text-slate-300">Wasted per year</div>
          </div>
        </div>

        {/* ROI Insight */}
        <div className="bg-emerald-500/5 border border-emerald-500/30 rounded-xl p-8 mb-12">
          <h3 className="text-2xl font-bold text-white mb-4">Your potential savings with Levqor:</h3>
          <p className="text-lg text-slate-300 mb-4">
            If Levqor saves you just <strong className="text-emerald-400">{hoursPerWeek} hours per week</strong>, you'd reclaim <strong className="text-emerald-400">£{monthlyWaste.toLocaleString()}/month</strong> worth of your time.
          </p>
          <p className="text-slate-400">
            Most Levqor clients report saving 20+ hours per week. At your hourly value, that's worth <strong className="text-white">£{(20 * hourlyValue * 4).toLocaleString()}/month</strong>.
          </p>
        </div>

        {/* CTA */}
        <div className="text-center bg-gradient-to-br from-emerald-500/10 to-blue-500/10 border border-emerald-500/30 rounded-2xl p-12">
          <h2 className="text-3xl font-bold mb-4 text-white">Stop wasting time on manual work</h2>
          <p className="text-lg text-slate-300 mb-8">
            Automate your busywork and reclaim your time with Levqor's DFY automation.
          </p>
          <Link 
            href="/pricing" 
            className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition-all shadow-lg"
          >
            View Pricing
          </Link>
        </div>
      </div>
    </PublicPageLayout>
  );
}
