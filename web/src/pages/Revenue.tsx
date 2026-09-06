import { useState } from 'react';
import { 
  TrendingUp, 
  DollarSign, 
  ShieldCheck, 
  Building2, 
  Users, 
  LandPlot, 
  Percent, 
  CheckCircle2, 
  Award,
  Sliders
} from 'lucide-react';

export default function Revenue() {
  // Interactive Forecaster State
  const [enrolledFarmers, setEnrolledFarmers] = useState<number>(750000); // 7.5 Lakh farmers
  const [avgFarmHectares, setAvgFarmHectares] = useState<number>(1.4); // National avg ~1.3-1.5 ha
  const [premiumPerHa, setPremiumPerHa] = useState<number>(5800); // PMFBY actuarial avg ₹5,800/ha
  const [commissionRate, setCommissionRate] = useState<number>(1.75); // 1.75% tech fee
  const [claimRate, setClaimRate] = useState<number>(12); // ~12% crop loss event frequency
  const [activeTab, setActiveTab] = useState<'overview' | 'monetization' | 'projections' | 'calculator'>('overview');

  // Derived Calculations
  const totalHectares = enrolledFarmers * avgFarmHectares;
  const grossPremiumPool = totalHectares * premiumPerHa; // In INR
  const platformTechCommission = grossPremiumPool * (commissionRate / 100);
  const totalClaims = Math.round(enrolledFarmers * (claimRate / 100));
  const claimVerificationFees = totalClaims * 180; // ₹180 per AI assessment
  const spatialAntiFraudFees = totalHectares * 35; // ₹35/ha for PostGIS boundary fraud de-duplication
  const totalAnnualRevenue = platformTechCommission + claimVerificationFees + spatialAntiFraudFees;
  
  // Insurer Savings (Assuming 32% fraud detection on 12% claims, avg claim size ₹28,000)
  const preventedFraudulentClaims = Math.round(totalClaims * 0.32);
  const insurerFraudSavings = preventedFraudulentClaims * 28000;
  const netInsurerROI = ((insurerFraudSavings - totalAnnualRevenue) / totalAnnualRevenue) * 100;

  const formatINR = (val: number) => {
    if (val >= 10000000) {
      return `₹${(val / 10000000).toFixed(2)} Cr`;
    } else if (val >= 100000) {
      return `₹${(val / 100000).toFixed(2)} Lakh`;
    }
    return `₹${val.toLocaleString('en-IN')}`;
  };

  return (
    <div className="flex-1 p-8 max-w-[1440px] mx-auto w-full">
      {/* Header */}
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-end gap-4 mb-8">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="px-3 py-1 bg-primary/10 text-primary rounded-full text-xs font-bold uppercase tracking-wider flex items-center gap-1.5">
              <Award size={13} /> PMFBY InsurTech Unit Economics
            </span>
            <span className="px-3 py-1 bg-tertiary-container/30 text-tertiary rounded-full text-xs font-semibold">
              Live Projections & Financial Viability
            </span>
          </div>
          <h2 className="text-3xl font-bold text-on-background">Revenue Model & Viability</h2>
          <p className="text-base text-on-surface-variant mt-1">
            How AgriShield monetizes through PMFBY insurer underwriting tech fees, AI claim verification, and anti-fraud land audit.
          </p>
        </div>

        {/* Tab Switcher */}
        <div className="flex bg-surface-container-high p-1 rounded-xl border border-outline-variant">
          {(['overview', 'monetization', 'projections', 'calculator'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all capitalize ${
                activeTab === tab 
                  ? 'bg-surface text-primary shadow-sm' 
                  : 'text-on-surface-variant hover:text-on-surface'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>

      {/* Top Level Metric Highlights */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
        <div className="bg-surface-container-lowest border border-outline-variant p-6 rounded-2xl shadow-sm hover:border-primary/40 transition-colors">
          <div className="flex justify-between items-start mb-3">
            <span className="text-xs font-bold text-on-surface-variant uppercase tracking-wider">PMFBY National Pool</span>
            <div className="w-9 h-9 rounded-lg bg-primary-container/20 text-primary flex items-center justify-center">
              <DollarSign size={20} />
            </div>
          </div>
          <h3 className="text-2xl font-bold text-on-surface mb-1">₹31,500 Cr</h3>
          <p className="text-xs text-on-surface-variant flex items-center gap-1">
            <span className="text-primary font-bold">~5.52 Cr</span> annual farmer enrollments
          </p>
        </div>

        <div className="bg-surface-container-lowest border border-outline-variant p-6 rounded-2xl shadow-sm hover:border-primary/40 transition-colors">
          <div className="flex justify-between items-start mb-3">
            <span className="text-xs font-bold text-on-surface-variant uppercase tracking-wider">Tech Platform Fee</span>
            <div className="w-9 h-9 rounded-lg bg-secondary-container/20 text-secondary flex items-center justify-center">
              <Percent size={20} />
            </div>
          </div>
          <h3 className="text-2xl font-bold text-on-surface mb-1">1.5% – 2.0%</h3>
          <p className="text-xs text-on-surface-variant">
            Of Gross Written Premium from insurers
          </p>
        </div>

        <div className="bg-surface-container-lowest border border-outline-variant p-6 rounded-2xl shadow-sm hover:border-primary/40 transition-colors">
          <div className="flex justify-between items-start mb-3">
            <span className="text-xs font-bold text-on-surface-variant uppercase tracking-wider">Insurer Loss Reduction</span>
            <div className="w-9 h-9 rounded-lg bg-tertiary-container/30 text-tertiary flex items-center justify-center">
              <ShieldCheck size={20} />
            </div>
          </div>
          <h3 className="text-2xl font-bold text-tertiary mb-1">32% Fraud Cut</h3>
          <p className="text-xs text-on-surface-variant">
            Via PostGIS overlap check & on-chain audit
          </p>
        </div>

        <div className="bg-surface-container-lowest border border-outline-variant p-6 rounded-2xl shadow-sm hover:border-primary/40 transition-colors">
          <div className="flex justify-between items-start mb-3">
            <span className="text-xs font-bold text-on-surface-variant uppercase tracking-wider">Year-3 Projected Run Rate</span>
            <div className="w-9 h-9 rounded-lg bg-primary/10 text-primary flex items-center justify-center">
              <TrendingUp size={20} />
            </div>
          </div>
          <h3 className="text-2xl font-bold text-primary mb-1">₹247.5 Cr</h3>
          <p className="text-xs text-on-surface-variant flex items-center gap-1">
            <span className="text-primary font-bold">81%</span> gross operating margin
          </p>
        </div>
      </div>

      {/* TAB 1: OVERVIEW & MACRO OPPORTUNITY */}
      {activeTab === 'overview' && (
        <div className="space-y-8">
          {/* Market Context Hero */}
          <div className="bg-gradient-to-br from-primary/10 via-surface to-secondary-container/10 border border-primary/20 rounded-3xl p-8 relative overflow-hidden shadow-sm">
            <div className="max-w-3xl relative z-10">
              <h3 className="text-2xl font-bold text-on-surface mb-3">
                The ₹31,500 Crore Pradhan Mantri Fasal Bima Yojana (PMFBY) Opportunity
              </h3>
              <p className="text-base text-on-surface-variant leading-relaxed mb-6">
                PMFBY is India’s flagship crop insurance scheme protecting over 55 million registered farmers across 52.8 million hectares. 
                Under PMFBY rules, farmers pay an ultra-subsidized flat premium of only <strong>1.5% for Rabi crops</strong>, <strong>2.0% for Kharif crops</strong>, and <strong>5.0% for commercial crops</strong>, with the Central & State Governments funding the remaining 85–90% actuarial premium.
              </p>
              
              <div className="grid sm:grid-cols-3 gap-4">
                <div className="bg-surface/90 backdrop-blur p-4 rounded-xl border border-outline-variant">
                  <div className="text-xs text-on-surface-variant font-medium">Annual Farmer Base</div>
                  <div className="text-xl font-bold text-on-surface mt-1">55.2 Million+</div>
                  <div className="text-[11px] text-primary mt-1 font-medium">Largest scheme globally</div>
                </div>
                <div className="bg-surface/90 backdrop-blur p-4 rounded-xl border border-outline-variant">
                  <div className="text-xs text-on-surface-variant font-medium">Gross Annual Claims</div>
                  <div className="text-xl font-bold text-on-surface mt-1">₹18,200 Cr</div>
                  <div className="text-[11px] text-on-surface-variant mt-1 font-medium">Avg settlement: 45 days</div>
                </div>
                <div className="bg-surface/90 backdrop-blur p-4 rounded-xl border border-outline-variant">
                  <div className="text-xs text-on-surface-variant font-medium">Loss Ratio Burden</div>
                  <div className="text-xl font-bold text-error mt-1">82% – 94%</div>
                  <div className="text-[11px] text-on-surface-variant mt-1 font-medium">Eroded by claim leakage</div>
                </div>
              </div>
            </div>
          </div>

          {/* Core Value Proposition to Insurers & Govt */}
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-surface-container-lowest border border-outline-variant p-6 rounded-2xl shadow-sm">
              <div className="w-12 h-12 rounded-xl bg-primary/10 text-primary flex items-center justify-center mb-4">
                <Building2 size={24} />
              </div>
              <h4 className="text-lg font-bold text-on-surface mb-2">Empanelled Insurers (B2B)</h4>
              <p className="text-sm text-on-surface-variant leading-relaxed mb-4">
                Insurance providers (AIC, HDFC ERGO, SBI General, Bajaj Allianz) license AgriShield to automate risk scoring, eliminate manual surveyor visits, and prevent fraudulent claims.
              </p>
              <ul className="text-xs space-y-2 text-on-surface-variant font-medium">
                <li className="flex items-center gap-2">
                  <CheckCircle2 size={14} className="text-primary flex-shrink-0" />
                  <span>32% fraud prevention via boundary collision check</span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 size={14} className="text-primary flex-shrink-0" />
                  <span>Settlement turnaround cut from 45 days to 72 hours</span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 size={14} className="text-primary flex-shrink-0" />
                  <span>Saves ₹1,320 per claim in manual surveyor costs</span>
                </li>
              </ul>
            </div>

            <div className="bg-surface-container-lowest border border-outline-variant p-6 rounded-2xl shadow-sm">
              <div className="w-12 h-12 rounded-xl bg-secondary-container/30 text-secondary flex items-center justify-center mb-4">
                <LandPlot size={24} />
              </div>
              <h4 className="text-lg font-bold text-on-surface mb-2">State Agri Depts & Banks</h4>
              <p className="text-sm text-on-surface-variant leading-relaxed mb-4">
                State nodal agencies and Kisan Credit Card (KCC) lending banks integrate AgriShield’s PostGIS land boundary registry to verify physical parcel ownership and prevent duplicate subsidies.
              </p>
              <ul className="text-xs space-y-2 text-on-surface-variant font-medium">
                <li className="flex items-center gap-2">
                  <CheckCircle2 size={14} className="text-primary flex-shrink-0" />
                  <span>Polygon spatial intersection restricts ghost parcels</span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 size={14} className="text-primary flex-shrink-0" />
                  <span>Tamper-proof Polygon Amoy blockchain proof</span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 size={14} className="text-primary flex-shrink-0" />
                  <span>Automated PMFBY portal subsidy reconciliations</span>
                </li>
              </ul>
            </div>

            <div className="bg-surface-container-lowest border border-outline-variant p-6 rounded-2xl shadow-sm">
              <div className="w-12 h-12 rounded-xl bg-tertiary-container/30 text-tertiary flex items-center justify-center mb-4">
                <Users size={24} />
              </div>
              <h4 className="text-lg font-bold text-on-surface mb-2">Farmers (100% Free Core)</h4>
              <p className="text-sm text-on-surface-variant leading-relaxed mb-4">
                Zero friction for smallholder farmers. Free registration, instant PMFBY quotes, satellite NDVI crop health telemetry, and transparent digital claims tracking directly to bank accounts.
              </p>
              <ul className="text-xs space-y-2 text-on-surface-variant font-medium">
                <li className="flex items-center gap-2">
                  <CheckCircle2 size={14} className="text-primary flex-shrink-0" />
                  <span>No upfront fees or deductions for the farmer</span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 size={14} className="text-primary flex-shrink-0" />
                  <span>Live 4-step claim audit with photographic proof</span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 size={14} className="text-primary flex-shrink-0" />
                  <span>Direct DBT bank account claim disbursement</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: MONETIZATION PILLARS */}
      {activeTab === 'monetization' && (
        <div className="space-y-8">
          <div className="grid md:grid-cols-2 gap-6">
            {/* Pillar 1 */}
            <div className="bg-surface-container-lowest border border-outline-variant p-6 rounded-2xl shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <span className="px-3 py-1 bg-primary/10 text-primary font-bold text-xs rounded-full">
                  Pillar 1 • Core Engine
                </span>
                <span className="text-sm font-bold text-primary">1.50% – 2.00%</span>
              </div>
              <h4 className="text-xl font-bold text-on-surface mb-2">PMFBY Underwriting & Distribution Fee</h4>
              <p className="text-sm text-on-surface-variant leading-relaxed mb-4">
                Charged directly to empanelled general insurance companies for every policy underwritten through AgriShield's automated pipeline. Includes satellite land verification, dynamic actuarial risk scoring, and PMFBY portal sync.
              </p>
              <div className="bg-surface p-4 rounded-xl border border-outline-variant space-y-2 text-xs">
                <div className="flex justify-between">
                  <span className="text-on-surface-variant">Standard Actuarial Premium:</span>
                  <span className="font-bold">₹5,800 per Hectare</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-on-surface-variant">AgriShield 1.75% Tech Fee:</span>
                  <span className="font-bold text-primary">₹101.50 per Hectare</span>
                </div>
                <div className="flex justify-between border-t border-outline-variant pt-2">
                  <span className="text-on-surface-variant">Per 100,000 Enrolled Ha:</span>
                  <span className="font-bold text-on-surface">₹1.015 Crore Pure Tech Fee</span>
                </div>
              </div>
            </div>

            {/* Pillar 2 */}
            <div className="bg-surface-container-lowest border border-outline-variant p-6 rounded-2xl shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <span className="px-3 py-1 bg-secondary-container/30 text-secondary font-bold text-xs rounded-full">
                  Pillar 2 • Claim Velocity
                </span>
                <span className="text-sm font-bold text-secondary">₹180 / Assessment</span>
              </div>
              <h4 className="text-xl font-bold text-on-surface mb-2">AI Damage Assessment & Verification</h4>
              <p className="text-sm text-on-surface-variant leading-relaxed mb-4">
                Insurers pay a flat processing fee per claim for automated damage scoring using Sentinel-2 NDVI spectral difference + EfficientNet-B0 vision models. Eliminates 70% of physical surveyor dispatch costs (which currently cost ₹1,500+ per visit).
              </p>
              <div className="bg-surface p-4 rounded-xl border border-outline-variant space-y-2 text-xs">
                <div className="flex justify-between">
                  <span className="text-on-surface-variant">Traditional Manual Surveyor:</span>
                  <span className="font-bold text-error">₹1,500 – ₹2,200 / survey</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-on-surface-variant">AgriShield AI Verification:</span>
                  <span className="font-bold text-primary">₹180 / assessment</span>
                </div>
                <div className="flex justify-between border-t border-outline-variant pt-2">
                  <span className="text-on-surface-variant">Net Insurer Cost Reduction:</span>
                  <span className="font-bold text-primary">88% Processing Savings</span>
                </div>
              </div>
            </div>

            {/* Pillar 3 */}
            <div className="bg-surface-container-lowest border border-outline-variant p-6 rounded-2xl shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <span className="px-3 py-1 bg-tertiary-container/30 text-tertiary font-bold text-xs rounded-full">
                  Pillar 3 • Anti-Fraud Security
                </span>
                <span className="text-sm font-bold text-tertiary">₹35 / Hectare / Year</span>
              </div>
              <h4 className="text-xl font-bold text-on-surface mb-2">Geospatial Boundary & Identity Audit</h4>
              <p className="text-sm text-on-surface-variant leading-relaxed mb-4">
                Annual enterprise API subscription for state agriculture departments and lending banks. Employs PostGIS polygon intersection checks to stop cross-farmer boundary collisions, duplicate claims on identical plots, and ghost claims.
              </p>
              <div className="bg-surface p-4 rounded-xl border border-outline-variant space-y-2 text-xs">
                <div className="flex justify-between">
                  <span className="text-on-surface-variant">Spatial De-duplication:</span>
                  <span className="font-bold">PostGIS SRID 4326 Intersect Check</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-on-surface-variant">Cryptographic State Proof:</span>
                  <span className="font-bold text-on-surface">Polygon Amoy SHA-256 On-chain</span>
                </div>
                <div className="flex justify-between border-t border-outline-variant pt-2">
                  <span className="text-on-surface-variant">Average Fraud Leakage Saved:</span>
                  <span className="font-bold text-primary">₹8,960 per prevented bogus claim</span>
                </div>
              </div>
            </div>

            {/* Pillar 4 */}
            <div className="bg-surface-container-lowest border border-outline-variant p-6 rounded-2xl shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <span className="px-3 py-1 bg-surface-variant text-on-surface-variant font-bold text-xs rounded-full">
                  Pillar 4 • Agronomic Data B2B
                </span>
                <span className="text-sm font-bold text-on-surface">B2B SaaS</span>
              </div>
              <h4 className="text-xl font-bold text-on-surface mb-2">Enterprise Climate & Risk Feeds</h4>
              <p className="text-sm text-on-surface-variant leading-relaxed mb-4">
                Aggregated, anonymized soil nutrition maps (N-P-K-pH via Soil Health Card OCR), hyper-local drought indices, and yield forecasting feeds sold to agri-input companies (seed, fertilizer) and rural credit institutions.
              </p>
              <div className="bg-surface p-4 rounded-xl border border-outline-variant space-y-2 text-xs">
                <div className="flex justify-between">
                  <span className="text-on-surface-variant">Yield Prediction Accuracy:</span>
                  <span className="font-bold text-primary">89.4% (XGBoost + Weather)</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-on-surface-variant">Soil OCR Extraction:</span>
                  <span className="font-bold text-on-surface">91.8% Character Precision</span>
                </div>
                <div className="flex justify-between border-t border-outline-variant pt-2">
                  <span className="text-on-surface-variant">Institutional API Pricing:</span>
                  <span className="font-bold text-on-surface">₹2.5 Lakh – ₹10 Lakh / year</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: 3-YEAR FINANCIAL PROJECTIONS */}
      {activeTab === 'projections' && (
        <div className="space-y-8">
          <div className="bg-surface-container-lowest border border-outline-variant rounded-2xl p-6 shadow-sm overflow-x-auto">
            <div className="flex justify-between items-center mb-6">
              <div>
                <h3 className="text-xl font-bold text-on-surface">3-Year Growth & Revenue Projections</h3>
                <p className="text-sm text-on-surface-variant">Phased rollout across PMFBY clusters in Madhya Pradesh, Maharashtra, and Uttar Pradesh.</p>
              </div>
              <span className="px-3 py-1 bg-primary/10 text-primary font-bold text-xs rounded-full">
                Targeting 21% National PMFBY Share by Year 3
              </span>
            </div>

            <table className="w-full text-left border-collapse min-w-[700px]">
              <thead>
                <tr className="border-b border-outline-variant text-xs text-on-surface-variant uppercase tracking-wider font-semibold">
                  <th className="pb-4">Metric / Timeline</th>
                  <th className="pb-4">Year 1 (Pilot - 3 States)</th>
                  <th className="pb-4">Year 2 (Scale - 8 States)</th>
                  <th className="pb-4 text-primary">Year 3 (Pan-India - 18 States)</th>
                </tr>
              </thead>
              <tbody className="text-sm divide-y divide-outline-variant/60 font-medium">
                <tr>
                  <td className="py-4 text-on-surface font-semibold flex items-center gap-2">
                    <Users size={16} className="text-primary" /> Active Enrolled Farmers
                  </td>
                  <td className="py-4">950,000</td>
                  <td className="py-4">3,800,000</td>
                  <td className="py-4 text-primary font-bold">11,500,000 (~21% PMFBY)</td>
                </tr>
                <tr>
                  <td className="py-4 text-on-surface font-semibold flex items-center gap-2">
                    <LandPlot size={16} className="text-primary" /> Underwritten Land Area
                  </td>
                  <td className="py-4">1.2 Million Ha</td>
                  <td className="py-4">4.8 Million Ha</td>
                  <td className="py-4 text-primary font-bold">14.5 Million Ha</td>
                </tr>
                <tr>
                  <td className="py-4 text-on-surface font-semibold flex items-center gap-2">
                    <DollarSign size={16} className="text-primary" /> Gross Facilitated Premium
                  </td>
                  <td className="py-4">₹720 Cr</td>
                  <td className="py-4">₹2,880 Cr</td>
                  <td className="py-4 text-primary font-bold">₹8,700 Cr</td>
                </tr>
                <tr className="bg-surface/50">
                  <td className="py-4 text-on-surface font-bold pl-2">
                    1. PMFBY Tech Commission (1.75%)
                  </td>
                  <td className="py-4 font-semibold text-on-surface">₹12.60 Cr</td>
                  <td className="py-4 font-semibold text-on-surface">₹50.40 Cr</td>
                  <td className="py-4 font-bold text-primary">₹152.25 Cr</td>
                </tr>
                <tr className="bg-surface/50">
                  <td className="py-4 text-on-surface font-bold pl-2">
                    2. AI Claim Verification Fees (₹180)
                  </td>
                  <td className="py-4 font-semibold text-on-surface">₹3.60 Cr</td>
                  <td className="py-4 font-semibold text-on-surface">₹14.40 Cr</td>
                  <td className="py-4 font-bold text-primary">₹43.50 Cr</td>
                </tr>
                <tr className="bg-surface/50">
                  <td className="py-4 text-on-surface font-bold pl-2">
                    3. Geospatial & Anti-Fraud API Fees
                  </td>
                  <td className="py-4 font-semibold text-on-surface">₹4.25 Cr</td>
                  <td className="py-4 font-semibold text-on-surface">₹17.10 Cr</td>
                  <td className="py-4 font-bold text-primary">₹51.75 Cr</td>
                </tr>
                <tr className="border-t-2 border-primary/40 bg-primary/5">
                  <td className="py-4 text-on-surface font-bold text-base pl-2">
                    Total Platform Net Revenue
                  </td>
                  <td className="py-4 font-bold text-base text-on-surface">₹20.45 Cr ($2.46M)</td>
                  <td className="py-4 font-bold text-base text-on-surface">₹81.90 Cr ($9.85M)</td>
                  <td className="py-4 font-bold text-lg text-primary">₹247.50 Cr ($29.75M)</td>
                </tr>
                <tr>
                  <td className="py-4 text-on-surface-variant pl-2">
                    Operating Margin (Cloud, Satellite, Polygon Gas)
                  </td>
                  <td className="py-4 text-on-surface-variant font-semibold">68%</td>
                  <td className="py-4 text-on-surface-variant font-semibold">74%</td>
                  <td className="py-4 text-primary font-bold">81%</td>
                </tr>
              </tbody>
            </table>
          </div>

          {/* Insurer Loss Ratio Impact */}
          <div className="bg-surface-container-lowest border border-outline-variant p-6 rounded-2xl shadow-sm">
            <h4 className="text-lg font-bold text-on-surface mb-3 flex items-center gap-2">
              <ShieldCheck className="text-primary" size={20} />
              Empanelled Insurer Fraud Savings & Loss Ratio Reduction
            </h4>
            <div className="grid md:grid-cols-3 gap-4 text-center">
              <div className="p-4 bg-surface rounded-xl border border-outline-variant">
                <p className="text-xs text-on-surface-variant mb-1">Bogus/Duplicate Claims Prevented (Y3)</p>
                <p className="text-2xl font-bold text-primary">441,600 Claims</p>
                <p className="text-xs text-on-surface-variant mt-1">Spatial PostGIS collision checks</p>
              </div>
              <div className="p-4 bg-surface rounded-xl border border-outline-variant">
                <p className="text-xs text-on-surface-variant mb-1">Direct Fraud Payouts Saved for Insurers</p>
                <p className="text-2xl font-bold text-tertiary">₹1,236 Crore</p>
                <p className="text-xs text-on-surface-variant mt-1">Net loss leakage eliminated</p>
              </div>
              <div className="p-4 bg-surface rounded-xl border border-outline-variant">
                <p className="text-xs text-on-surface-variant mb-1">Insurer Net Combined Ratio</p>
                <p className="text-2xl font-bold text-on-surface">88.4% → 81.2%</p>
                <p className="text-xs text-primary mt-1 font-bold">7.2% Margin Improvement</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 4: INTERACTIVE REVENUE CALCULATOR */}
      {activeTab === 'calculator' && (
        <div className="space-y-8">
          <div className="grid lg:grid-cols-12 gap-8">
            {/* Controls */}
            <div className="lg:col-span-7 bg-surface-container-lowest border border-outline-variant p-6 rounded-2xl shadow-sm space-y-6">
              <div>
                <h3 className="text-xl font-bold text-on-surface mb-1 flex items-center gap-2">
                  <Sliders size={20} className="text-primary" />
                  Live Unit Economics & Revenue Simulator
                </h3>
                <p className="text-sm text-on-surface-variant">
                  Adjust enrollment targets and fee structures to see real-time commission forecasts and insurer savings.
                </p>
              </div>

              {/* Slider 1: Farmers Enrolled */}
              <div>
                <div className="flex justify-between items-center mb-2">
                  <label className="text-sm font-semibold text-on-surface">
                    Registered Farmers: <span className="text-primary font-bold">{(enrolledFarmers / 100000).toFixed(1)} Lakh ({enrolledFarmers.toLocaleString()})</span>
                  </label>
                  <span className="text-xs text-on-surface-variant">PMFBY National: 5.5 Cr</span>
                </div>
                <input
                  type="range"
                  min={50000}
                  max={3000000}
                  step={50000}
                  value={enrolledFarmers}
                  onChange={(e) => setEnrolledFarmers(Number(e.target.value))}
                  className="w-full h-2 bg-surface-container-high rounded-lg appearance-none cursor-pointer accent-primary"
                />
                <div className="flex justify-between text-[11px] text-on-surface-variant mt-1">
                  <span>50k (District Pilot)</span>
                  <span>10 Lakh (State Scale)</span>
                  <span>30 Lakh (Multi-State)</span>
                </div>
              </div>

              {/* Slider 2: Average Farm Size */}
              <div>
                <div className="flex justify-between items-center mb-2">
                  <label className="text-sm font-semibold text-on-surface">
                    Average Farm Size: <span className="text-primary font-bold">{avgFarmHectares.toFixed(1)} Hectares</span>
                  </label>
                  <span className="text-xs text-on-surface-variant">National Avg: ~1.4 Ha</span>
                </div>
                <input
                  type="range"
                  min={0.5}
                  max={4.0}
                  step={0.1}
                  value={avgFarmHectares}
                  onChange={(e) => setAvgFarmHectares(Number(e.target.value))}
                  className="w-full h-2 bg-surface-container-high rounded-lg appearance-none cursor-pointer accent-primary"
                />
              </div>

              {/* Slider 3: PMFBY Premium per Ha */}
              <div>
                <div className="flex justify-between items-center mb-2">
                  <label className="text-sm font-semibold text-on-surface">
                    Avg Gross Premium: <span className="text-primary font-bold">₹{premiumPerHa.toLocaleString()}/Ha</span>
                  </label>
                  <span className="text-xs text-on-surface-variant">Actuarial Benchmark</span>
                </div>
                <input
                  type="range"
                  min={3500}
                  max={9000}
                  step={100}
                  value={premiumPerHa}
                  onChange={(e) => setPremiumPerHa(Number(e.target.value))}
                  className="w-full h-2 bg-surface-container-high rounded-lg appearance-none cursor-pointer accent-primary"
                />
              </div>

              {/* Slider 4: AgriShield Tech Commission Rate */}
              <div>
                <div className="flex justify-between items-center mb-2">
                  <label className="text-sm font-semibold text-on-surface">
                    AgriShield Tech Fee: <span className="text-primary font-bold">{commissionRate.toFixed(2)}%</span>
                  </label>
                  <span className="text-xs text-on-surface-variant">Industry norm: 1.5% - 2.5%</span>
                </div>
                <input
                  type="range"
                  min={1.0}
                  max={3.0}
                  step={0.05}
                  value={commissionRate}
                  onChange={(e) => setCommissionRate(Number(e.target.value))}
                  className="w-full h-2 bg-surface-container-high rounded-lg appearance-none cursor-pointer accent-primary"
                />
              </div>

              {/* Slider 5: Seasonal Claim Frequency */}
              <div>
                <div className="flex justify-between items-center mb-2">
                  <label className="text-sm font-semibold text-on-surface">
                    Seasonal Loss Claim Rate: <span className="text-secondary font-bold">{claimRate}% of farms</span>
                  </label>
                  <span className="text-xs text-on-surface-variant">Drought/Hail frequency</span>
                </div>
                <input
                  type="range"
                  min={5}
                  max={30}
                  step={1}
                  value={claimRate}
                  onChange={(e) => setClaimRate(Number(e.target.value))}
                  className="w-full h-2 bg-surface-container-high rounded-lg appearance-none cursor-pointer accent-secondary"
                />
              </div>
            </div>

            {/* Results Output */}
            <div className="lg:col-span-5 flex flex-col gap-6">
              <div className="bg-gradient-to-br from-primary/15 via-surface-container-lowest to-surface-container-lowest border border-primary/30 p-6 rounded-2xl shadow-sm flex-1 flex flex-col justify-between">
                <div>
                  <span className="text-xs font-bold text-primary uppercase tracking-wider">Simulated Annual Outcome</span>
                  <h4 className="text-3xl font-extrabold text-on-surface mt-2 mb-1">
                    {formatINR(totalAnnualRevenue)}
                  </h4>
                  <p className="text-xs text-on-surface-variant mb-6">
                    Total Estimated Annual Platform Revenue (INR)
                  </p>

                  <div className="space-y-3 text-sm">
                    <div className="flex justify-between items-center p-3 bg-surface rounded-xl border border-outline-variant">
                      <span className="text-on-surface-variant">Gross Premium Pool:</span>
                      <span className="font-bold text-on-surface">{formatINR(grossPremiumPool)}</span>
                    </div>

                    <div className="flex justify-between items-center p-3 bg-surface rounded-xl border border-outline-variant">
                      <span className="text-on-surface-variant">1. Tech Fee ({commissionRate}%):</span>
                      <span className="font-bold text-primary">{formatINR(platformTechCommission)}</span>
                    </div>

                    <div className="flex justify-between items-center p-3 bg-surface rounded-xl border border-outline-variant">
                      <span className="text-on-surface-variant">2. AI Claim Verification (₹180/ea):</span>
                      <span className="font-bold text-secondary">{formatINR(claimVerificationFees)}</span>
                    </div>

                    <div className="flex justify-between items-center p-3 bg-surface rounded-xl border border-outline-variant">
                      <span className="text-on-surface-variant">3. Spatial Land De-dup (₹35/ha):</span>
                      <span className="font-bold text-tertiary">{formatINR(spatialAntiFraudFees)}</span>
                    </div>
                  </div>
                </div>

                <div className="mt-6 pt-6 border-t border-outline-variant">
                  <div className="bg-primary/5 p-4 rounded-xl border border-primary/20">
                    <div className="flex items-center gap-2 mb-1">
                      <ShieldCheck size={18} className="text-primary" />
                      <span className="text-xs font-bold text-primary uppercase">Insurer Anti-Fraud Value</span>
                    </div>
                    <div className="flex justify-between items-end mt-2">
                      <div>
                        <div className="text-lg font-bold text-on-surface">{formatINR(insurerFraudSavings)}</div>
                        <div className="text-[11px] text-on-surface-variant">Fraud loss eliminated for insurers</div>
                      </div>
                      <span className="text-xs font-bold text-primary bg-primary/10 px-2 py-1 rounded">
                        +{netInsurerROI.toFixed(0)}% ROI
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
