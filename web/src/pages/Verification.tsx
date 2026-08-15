import { api } from '../api';
import type { PolicyVerification } from '../api';
import { useEffect, useState } from 'react';
import { ShieldCheck, Link2, Clock, CheckCircle, Database } from 'lucide-react';

export default function Verification() {
  const [verification, setVerification] = useState<PolicyVerification | null>(null);
  const [loading, setLoading] = useState(true);
  const [currentPolicyId, setCurrentPolicyId] = useState<string>('p1');

  useEffect(() => {
    api.getPolicies().then(policyRes => {
      const pId = policyRes.data && policyRes.data.length > 0 ? policyRes.data[0].id : 'p1';
      setCurrentPolicyId(pId);
      
      api.verifyPolicy(pId)
        .then(res => setVerification(res.data))
        .finally(() => setLoading(false));
    }).catch(() => setLoading(false));
  }, []);

  return (
    <div className="flex-1 p-8 max-w-[1000px] mx-auto w-full">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-on-background">Blockchain Verification</h2>
        <p className="text-base text-on-surface-variant mt-1">Immutable cryptographic audit trail for Policy #{currentPolicyId.substring(0, 8).toUpperCase()}</p>
      </div>

      {loading ? (
        <div className="p-12 text-center text-on-surface-variant">Querying blockchain...</div>
      ) : verification ? (
        <div className="bg-surface-container-lowest border border-outline-variant rounded-2xl p-8 shadow-sm">
          <div className="flex items-center gap-4 mb-8 pb-8 border-b border-outline-variant">
            <div className={`w-16 h-16 rounded-full flex items-center justify-center ${
              verification.status === 'VERIFIED' ? 'bg-primary/20 text-primary' : 'bg-error/20 text-error'
            }`}>
              <ShieldCheck size={32} />
            </div>
            <div>
              <h3 className="text-2xl font-bold flex items-center gap-2">
                {verification.status === 'VERIFIED' ? 'Cryptographically Verified' : 'Verification Pending'}
                {verification.status === 'VERIFIED' && <CheckCircle size={24} className="text-primary" />}
              </h3>
              <p className="text-on-surface-variant">The policy record matches the on-chain hash perfectly.</p>
            </div>
          </div>

          <div className="grid gap-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between p-4 bg-surface rounded-xl border border-outline-variant">
              <div className="flex items-center gap-3 mb-2 md:mb-0">
                <Database className="text-tertiary" size={24} />
                <span className="font-semibold text-on-surface">Network</span>
              </div>
              <span className="font-mono bg-tertiary-container/30 text-tertiary px-3 py-1 rounded-md text-sm">
                Polygon Amoy Testnet
              </span>
            </div>

            <div className="flex flex-col md:flex-row md:items-center justify-between p-4 bg-surface rounded-xl border border-outline-variant">
              <div className="flex items-center gap-3 mb-2 md:mb-0">
                <Link2 className="text-secondary" size={24} />
                <span className="font-semibold text-on-surface">Transaction Hash</span>
              </div>
              <span className="font-mono bg-surface-variant text-on-surface-variant px-3 py-1 rounded-md text-xs break-all">
                {verification.tx_hash || 'Not recorded yet'}
              </span>
            </div>

            <div className="flex flex-col md:flex-row md:items-center justify-between p-4 bg-surface rounded-xl border border-outline-variant">
              <div className="flex items-center gap-3 mb-2 md:mb-0">
                <Clock className="text-primary" size={24} />
                <span className="font-semibold text-on-surface">Canonical Hash</span>
              </div>
              <span className="text-on-surface-variant font-mono text-xs break-all">
                {verification.canonical_hash || 'Pending'}
              </span>
            </div>
          </div>
          
          <div className="mt-8 text-center">
            <button className="bg-surface-container-highest text-on-surface font-semibold px-6 py-3 rounded-full hover:bg-surface-variant transition-colors">
              View on Explorer
            </button>
          </div>
        </div>
      ) : (
        <div className="p-12 text-center text-on-surface-variant bg-surface-container-lowest rounded-2xl border border-outline-variant">
          Verification failed to load.
        </div>
      )}
    </div>
  );
}
