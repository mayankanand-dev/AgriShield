import { FileText, ShieldAlert, Users, Activity, Download, TrendingUp, TrendingDown, Map as MapIcon } from 'lucide-react';
import { api } from '../api';
import { useState, useEffect } from 'react';

export default function Dashboard() {
  const [stats, setStats] = useState({ policies: 0, claims: 0, farmers: 0, riskScore: 0 });

  useEffect(() => {
    async function fetchStats() {
      try {
        const [policiesRes, claimsRes, farmsRes] = await Promise.all([
          api.getPolicies(),
          api.getClaims(),
          api.getFarms()
        ]);
        
        // Count unique farmers based on unique user_ids in farms
        const uniqueFarmers = new Set(farmsRes.data.map(f => f.user_id)).size;
        
        setStats({
          policies: policiesRes.data.length,
          claims: claimsRes.data.length,
          farmers: uniqueFarmers,
          riskScore: 42.5 // Hardcoded for now as there's no aggregate risk score endpoint
        });
      } catch (err) {
        console.error("Failed to fetch dashboard stats", err);
      }
    }
    fetchStats();
  }, []);

  return (
    <div className="flex-1 flex flex-col min-w-0">
            <div className="p-8 max-w-[1440px] mx-auto w-full flex flex-col gap-8">
        <div className="flex justify-between items-end mb-2">
          <div>
            <h2 className="text-3xl font-bold text-on-background">Overview</h2>
            <p className="text-base text-on-surface-variant mt-1">Real-time agricultural portfolio metrics.</p>
          </div>
          <button className="bg-primary text-on-primary px-4 py-2 rounded-lg text-sm hover:bg-surface-tint transition-colors shadow-sm flex items-center gap-2">
            <Download size={18} />
            Export Report
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard title="Active Policies" value={stats.policies.toLocaleString()} trend="+5.2%" isPositive={true} icon={FileText} colorClass="text-primary bg-primary-container/10" trendColor="text-[#1B7A3D] bg-[#1B7A3D]/10" />
          <StatCard title="Pending Claims" value={stats.claims.toLocaleString()} trend="+1.2%" isPositive={true} icon={ShieldAlert} colorClass="text-secondary bg-secondary-container/10" trendColor="text-[#F5821F] bg-[#F5821F]/10" />
          <StatCard title="Total Farmers" value={stats.farmers.toLocaleString()} trend="+8.4%" isPositive={true} icon={Users} colorClass="text-tertiary bg-tertiary-container/10" trendColor="text-[#1B7A3D] bg-[#1B7A3D]/10" />
          <StatCard title="Avg. Risk Score" value={stats.riskScore.toString()} trend="-0.5%" isPositive={false} icon={Activity} colorClass="text-error bg-error-container/10" trendColor="text-[#ba1a1a] bg-[#ba1a1a]/10" />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[500px]">
          <div className="lg:col-span-2 bg-surface-container-lowest border border-surface-variant rounded-xl flex flex-col overflow-hidden shadow-sm relative">
            <div className="p-6 border-b border-surface-variant flex justify-between items-center bg-white z-10">
              <h3 className="text-lg font-bold text-on-background">Geographic Risk Distribution</h3>
            </div>
            <div className="flex-1 bg-surface-variant flex items-center justify-center">
              <MapIcon className="w-16 h-16 text-on-surface-variant opacity-50" />
              <span className="ml-2 text-on-surface-variant font-medium">Map Component Placeholder</span>
            </div>
          </div>
          <div className="bg-surface-container-lowest border border-surface-variant rounded-xl flex flex-col overflow-hidden shadow-sm">
             <div className="p-6 border-b border-surface-variant bg-white z-10">
              <h3 className="text-lg font-bold text-on-background">Recent Activity</h3>
            </div>
            <div className="flex-1 p-6 overflow-y-auto">
               <p className="text-on-surface-variant text-sm">Demo / AI-assisted feed...</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, trend, isPositive, icon: Icon, colorClass, trendColor }: any) {
  return (
    <div className="bg-surface-container-lowest border border-surface-variant rounded-xl p-6 shadow-sm hover:-translate-y-1 transition-transform duration-200">
      <div className="flex justify-between items-start mb-4">
        <div className={`p-2 rounded-lg ${colorClass}`}>
          <Icon size={24} />
        </div>
        <div className={`flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${trendColor}`}>
          {isPositive ? <TrendingUp size={14} /> : <TrendingDown size={14} />}
          {trend}
        </div>
      </div>
      <p className="text-sm text-on-surface-variant mb-1">{title}</p>
      <h3 className="text-3xl font-bold text-on-background">{value}</h3>
    </div>
  );
}
