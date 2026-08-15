import { Search, MoreVertical, Plus } from 'lucide-react';
import { api } from '../api';
import { useEffect, useState } from 'react';
import type { Farm } from '../api';

export default function Farmers() {
  const [farms, setFarms] = useState<Farm[]>([]);

  useEffect(() => {
    api.getFarms().then(res => setFarms(res.data));
  }, []);

  return (
    <div className="flex-1 flex flex-col min-w-0">
            <div className="p-8 max-w-[1440px] mx-auto w-full flex flex-col gap-6">
        <div className="flex justify-between items-end">
          <div>
            <h2 className="text-3xl font-bold text-on-background">Farmers Directory</h2>
            <p className="text-base text-on-surface-variant mt-1">Manage registered farmers and their policies.</p>
          </div>
          <button className="bg-primary text-on-primary px-4 py-2 rounded-lg text-sm hover:bg-surface-tint transition-colors shadow-sm flex items-center gap-2">
            <Plus size={18} />
            Add New Farmer
          </button>
        </div>

        <div className="bg-surface-container-lowest border border-outline-variant rounded-xl p-6 shadow-sm flex flex-col md:flex-row gap-6 items-end">
          <div className="flex-1 w-full">
            <label className="block text-sm font-medium text-on-surface-variant mb-2">Search</label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-outline" size={20} />
              <input className="w-full pl-10 pr-4 py-2 bg-surface rounded-lg border border-outline-variant focus:border-primary-container focus:ring-1 focus:ring-primary-container transition-colors text-sm" placeholder="Search by name, ID, or location..." type="text" />
            </div>
          </div>
          <div className="w-full md:w-48">
            <label className="block text-sm font-medium text-on-surface-variant mb-2">Region</label>
            <select className="w-full px-4 py-2 bg-surface rounded-lg border border-outline-variant focus:border-primary-container focus:ring-1 focus:ring-primary-container transition-colors text-sm">
              <option>All Regions</option>
              <option>Midwest</option>
              <option>Southwest</option>
              <option>Northwest</option>
            </select>
          </div>
          <div className="w-full md:w-48">
            <label className="block text-sm font-medium text-on-surface-variant mb-2">Crop Type</label>
            <select className="w-full px-4 py-2 bg-surface rounded-lg border border-outline-variant focus:border-primary-container focus:ring-1 focus:ring-primary-container transition-colors text-sm">
              <option>All Crops</option>
              <option>Corn</option>
              <option>Wheat</option>
              <option>Soybeans</option>
            </select>
          </div>
        </div>

        <div className="bg-surface-container-lowest border border-outline-variant rounded-xl shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-surface border-b border-outline-variant">
                  <th className="px-6 py-3 text-xs font-medium text-on-surface-variant uppercase tracking-wider sticky top-0">Farm ID</th>
                  <th className="px-6 py-3 text-xs font-medium text-on-surface-variant uppercase tracking-wider sticky top-0">Name</th>
                  <th className="px-6 py-3 text-xs font-medium text-on-surface-variant uppercase tracking-wider sticky top-0">Crop</th>
                  <th className="px-6 py-3 text-xs font-medium text-on-surface-variant uppercase tracking-wider sticky top-0">Area (m²)</th>
                  <th className="px-6 py-3 text-xs font-medium text-on-surface-variant uppercase tracking-wider sticky top-0">Status</th>
                  <th className="px-6 py-3 text-xs font-medium text-on-surface-variant uppercase tracking-wider sticky top-0 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="text-sm text-on-surface">
                {farms.map((farm) => (
                  <tr key={farm.id} className="border-b border-outline-variant/30 hover:bg-surface-variant/50 transition-colors">
                    <td className="px-6 py-4">{farm.id}</td>
                    <td className="px-6 py-4 font-semibold">{farm.name}</td>
                    <td className="px-6 py-4">{farm.crop || 'N/A'}</td>
                    <td className="px-6 py-4">{farm.area_m2.toLocaleString()}</td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                        farm.status === 'VERIFIED' ? 'bg-primary/10 text-primary' : 
                        farm.status === 'PENDING' ? 'bg-secondary-container/10 text-secondary-container' : 
                        'bg-error/10 text-error'
                      }`}>
                        {farm.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <button className="text-tertiary hover:text-tertiary-container transition-colors">
                        <MoreVertical size={20} />
                      </button>
                    </td>
                  </tr>
                ))}
                {farms.length === 0 && (
                  <tr>
                    <td colSpan={6} className="px-6 py-8 text-center text-on-surface-variant">
                      No farms loaded. (Check Demo Mode)
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
          <div className="bg-surface border-t border-outline-variant px-6 py-3 flex items-center justify-between">
            <span className="text-xs text-on-surface-variant">Showing {farms.length} entries</span>
            <div className="flex gap-2">
              <button className="px-3 py-1 rounded border border-outline-variant text-on-surface-variant hover:bg-surface-container-high transition-colors text-xs disabled:opacity-50" disabled>Prev</button>
              <button className="px-3 py-1 rounded border border-primary-container bg-primary-container text-on-primary text-xs">1</button>
              <button className="px-3 py-1 rounded border border-outline-variant text-on-surface-variant hover:bg-surface-container-high transition-colors text-xs">2</button>
              <button className="px-3 py-1 rounded border border-outline-variant text-on-surface-variant hover:bg-surface-container-high transition-colors text-xs">Next</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
