import { FileSearch, Filter } from 'lucide-react';
import { api } from '../api';
import { useEffect, useState } from 'react';
import type { Claim } from '../api';

export default function Claims() {
  const [claims, setClaims] = useState<Claim[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getClaims()
      .then(res => setClaims(res.data))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="flex-1 flex flex-col min-w-0">
            <div className="p-8 max-w-[1440px] mx-auto w-full flex flex-col gap-6">
        <div className="flex justify-between items-end">
          <div>
            <h2 className="text-3xl font-bold text-on-background">Claims Dashboard</h2>
            <p className="text-base text-on-surface-variant mt-1">Review and manage AI-assessed insurance claims.</p>
          </div>
          <button className="bg-surface-container-highest text-on-surface border border-outline-variant px-4 py-2 rounded-lg text-sm hover:bg-surface-variant transition-colors shadow-sm flex items-center gap-2">
            <Filter size={18} />
            Filter
          </button>
        </div>

        <div className="bg-surface-container-lowest border border-outline-variant rounded-xl shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-surface border-b border-outline-variant">
                  <th className="px-6 py-3 text-xs font-medium text-on-surface-variant uppercase tracking-wider">Claim ID</th>
                  <th className="px-6 py-3 text-xs font-medium text-on-surface-variant uppercase tracking-wider">Event</th>
                  <th className="px-6 py-3 text-xs font-medium text-on-surface-variant uppercase tracking-wider">Date</th>
                  <th className="px-6 py-3 text-xs font-medium text-on-surface-variant uppercase tracking-wider">Damage Pct</th>
                  <th className="px-6 py-3 text-xs font-medium text-on-surface-variant uppercase tracking-wider">AI Confidence</th>
                  <th className="px-6 py-3 text-xs font-medium text-on-surface-variant uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-xs font-medium text-on-surface-variant uppercase tracking-wider text-right">Action</th>
                </tr>
              </thead>
              <tbody className="text-sm text-on-surface">
                {loading ? (
                  <tr><td colSpan={7} className="px-6 py-8 text-center text-on-surface-variant">Loading claims...</td></tr>
                ) : claims.length === 0 ? (
                  <tr><td colSpan={7} className="px-6 py-8 text-center text-on-surface-variant">No claims found.</td></tr>
                ) : (
                  claims.map(claim => (
                    <tr key={claim.id} className="border-b border-outline-variant/30 hover:bg-surface-variant/50 transition-colors">
                      <td className="px-6 py-4 font-mono text-xs">{claim.id}</td>
                      <td className="px-6 py-4 font-semibold capitalize">{claim.event_type}</td>
                      <td className="px-6 py-4">{claim.incident_date}</td>
                      <td className="px-6 py-4">{claim.damage_pct ? `${claim.damage_pct}%` : 'N/A'}</td>
                      <td className="px-6 py-4">
                        {claim.ai_confidence ? (
                          <div className="flex flex-col gap-1">
                            <span>{(claim.ai_confidence * 100).toFixed(0)}%</span>
                            <span className="text-[10px] text-tertiary font-bold bg-tertiary-container/30 px-1 py-0.5 rounded w-fit">Demo / AI-assisted</span>
                          </div>
                        ) : 'Pending'}
                      </td>
                      <td className="px-6 py-4">
                        <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                          claim.status === 'APPROVED' ? 'bg-primary/10 text-primary' : 
                          claim.status === 'REJECTED' ? 'bg-error/10 text-error' : 
                          claim.status === 'AI_ASSESSED' ? 'bg-tertiary/10 text-tertiary' :
                          'bg-secondary-container/10 text-secondary-container'
                        }`}>
                          {claim.status.replace('_', ' ')}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-right">
                        <button className="text-primary hover:text-primary-container font-semibold transition-colors flex items-center justify-end gap-1 ml-auto">
                          Review <FileSearch size={16} />
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
