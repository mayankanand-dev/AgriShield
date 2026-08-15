# Stitch prompts — AgriShield

Paste one block at a time into Stitch (stitch.withgoogle.com). Generate the
app first, then the website, so the website can visually match it.

---

## 1. Flutter Farmer App prompt

```
Design a mobile app called "AgriShield" — an AI-powered crop insurance and
farm monitoring app for Indian farmers, built for the PMFBY government
insurance scheme.

Brand: friendly, trustworthy, agricultural. Primary color deep green (#1B7A3D),
secondary accent warm orange (#F5821F), neutral off-white background, clean
sans-serif type. Icon language: rounded, simple line icons (leaf, satellite,
shield, rupee, camera). Should feel approachable to a farmer with basic
smartphone literacy, not a corporate fintech app — large tap targets, minimal
text per screen, strong icon+color coding, supports Hindi/regional-language
labels.

Generate these screens:
1. Onboarding / language picker — pick from Hindi, English, Marathi, etc.
2. Login screen — phone number + OTP, large single-column form.
3. Farmer dashboard (home) — list of farm cards, each showing crop name,
   a colored risk badge (green/yellow/red), a small weather icon + temp,
   and an insurance status pill (Insured / Not Insured / Claim Pending).
   Floating action button to add a new farm.
4. Add Farm screen — full-screen map with GPS "walk the boundary" polygon
   drawing tool, a running area readout (hectares) at the bottom, Save button.
5. Farm detail screen — tabs for Overview / Weather / Soil / Insurance.
   Overview tab shows a satellite thumbnail, crop health status card with a
   confidence percentage, and quick-action buttons: "Scan Crop Photo",
   "Upload Soil Report", "Get Insurance Quote".
6. Crop photo scan screen — camera viewfinder with a leaf-outline guide
   overlay, capture button, and a results card below showing
   Healthy/Diseased status, severity, and confidence %.
7. Soil report screen — upload button (camera/PDF), then a results card
   showing N/P/K/pH values as small gauges, and if no report exists, a
   "Using Soil Health Card data" fallback banner with a recommended crop.
8. Insurance quote & purchase screen — premium amount in large type, a
   breakdown (base rate, risk adjustment), crop/area summary, "Buy Policy"
   button.
9. File a claim screen — incident type picker (hailstorm/drought/flood/pest
   icons), date picker, multi-photo evidence upload grid, submit button.
10. Claim status timeline screen — vertical stepper: Submitted → AI Assessed
    → Under Review → Approved, with a small "Verified on blockchain" badge
    and hash snippet once confirmed.
11. Notifications / alerts screen — list of weather/disease/irrigation alerts
    with colored severity icons.

Style: soft rounded cards with subtle shadows, bottom navigation bar with 4
icons (Home, Farms, Insurance, Alerts), status bar area respected, mobile
portrait 375x812 frame.
```

---

## 2. React Admin/Insurer Website prompt

```
Design a responsive web dashboard called "AgriShield Admin" for insurance
company staff and government reviewers to manage crop insurance policies and
claims. Desktop-first (1440px), also usable on tablet.

Brand: match a companion mobile app — deep green (#1B7A3D) primary, warm
orange (#F5821F) accent, off-white background, clean sans-serif, rounded
cards, subtle shadows. Professional but not sterile — this is agriculture +
government + insurance, so keep it trustworthy and data-forward rather than
flashy.

Layout: left sidebar navigation (Dashboard, Farmers, Farms Map, Policies,
Claims, Verification, Reports), top bar with search + admin profile.

Generate these pages:
1. Dashboard — KPI cards across the top (Active Policies, Pending Claims,
   Total Farmers, Avg. Risk Score), a map widget showing farm pins colored by
   risk level, and a recent-activity feed list below.
2. Farms map view — full-width interactive map with clustered farm markers,
   a filter panel (state, crop, risk level, insurance status), and a side
   panel that shows farm details when a pin is selected (polygon outline,
   crop, satellite thumbnail, health status).
3. Claims dashboard — data table with columns: Claim ID, Farmer, Crop, Event
   Type, Damage %, AI Confidence, Status (colored pill), Date. Filter chips
   at top for status. Clicking a row opens a claim detail panel.
4. Claim review detail — split view: left side shows uploaded evidence
   photos in a gallery + AI damage-assessment overlay (bounding boxes on the
   image) with confidence score; right side shows claim metadata, an
   Approve/Reject action bar, and a comment box for the reviewer.
5. Policy detail page — policy timeline (Quoted → Purchased → Active),
   premium breakdown table, linked farm summary card, and a "Blockchain
   Verification" panel showing SHA-256 hash, Polygon Amoy tx hash, and a
   green "Verified" / amber "Pending" / red "Mismatch" status badge.
6. Reports page — simple bar and line charts (claims per month, average
   payout by crop, risk score distribution) in card containers.

Style: clean data tables with zebra striping, colored status pills (green
Approved, amber Pending, red Rejected), card-based KPI tiles with a small
trend arrow, consistent 8px spacing grid, light mode only.
```
