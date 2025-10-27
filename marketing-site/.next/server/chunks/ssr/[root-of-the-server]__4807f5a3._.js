module.exports=[93695,(a,b,c)=>{b.exports=a.x("next/dist/shared/lib/no-fallback-error.external.js",()=>require("next/dist/shared/lib/no-fallback-error.external.js"))},70864,a=>{a.n(a.i(33290))},2894,a=>{a.n(a.i(66188))},13718,a=>{a.n(a.i(85523))},18198,a=>{a.n(a.i(45518))},62212,a=>{a.n(a.i(66114))},71688,a=>{a.n(a.i(20178))},1529,a=>{"use strict";var b=a.i(7997);function c(){return(0,b.jsxs)("div",{style:{maxWidth:"1200px",margin:"2rem auto",padding:"2rem"},children:[(0,b.jsx)("h1",{children:"EchoPilotAI API Documentation"}),(0,b.jsx)("p",{children:"RESTful API reference for EchoPilotAI automation platform."}),(0,b.jsxs)("div",{style:{marginTop:"3rem"},children:[(0,b.jsx)("h2",{children:"Health & Status"}),(0,b.jsxs)("div",{style:{backgroundColor:"#f5f5f5",padding:"1rem",borderRadius:"4px",marginTop:"1rem"},children:[(0,b.jsxs)("code",{children:[(0,b.jsx)("strong",{children:"GET"})," /health"]}),(0,b.jsx)("p",{children:"Check system health status"}),(0,b.jsx)("pre",{style:{backgroundColor:"#fff",padding:"1rem",borderRadius:"4px",overflow:"auto"},children:`{
  "status": "healthy",
  "timestamp": 1234567890
}`})]})]}),(0,b.jsxs)("div",{style:{marginTop:"2rem"},children:[(0,b.jsx)("h2",{children:"Feedback"}),(0,b.jsxs)("div",{style:{backgroundColor:"#f5f5f5",padding:"1rem",borderRadius:"4px",marginTop:"1rem"},children:[(0,b.jsxs)("code",{children:[(0,b.jsx)("strong",{children:"POST"})," /api/feedback"]}),(0,b.jsx)("p",{children:"Submit user feedback"}),(0,b.jsx)("pre",{style:{backgroundColor:"#fff",padding:"1rem",borderRadius:"4px",overflow:"auto"},children:`Request:
{
  "email": "user@example.com",
  "message": "Great product!",
  "page": "https://echopilotai.com/pricing"
}

Response:
{
  "ok": true,
  "message": "Feedback received"
}`})]})]}),(0,b.jsxs)("div",{style:{marginTop:"2rem"},children:[(0,b.jsx)("h2",{children:"Incident Management"}),(0,b.jsxs)("div",{style:{backgroundColor:"#f5f5f5",padding:"1rem",borderRadius:"4px",marginTop:"1rem"},children:[(0,b.jsxs)("code",{children:[(0,b.jsx)("strong",{children:"POST"})," /api/incident/report"]}),(0,b.jsx)("p",{children:"Trigger incident report (requires authentication)"}),(0,b.jsx)("pre",{style:{backgroundColor:"#fff",padding:"1rem",borderRadius:"4px",overflow:"auto"},children:`Headers:
Authorization: Bearer <ADMIN_BEARER>

Response:
{
  "ok": true,
  "message": "Incident report generated"
}`})]})]}),(0,b.jsxs)("div",{style:{marginTop:"2rem"},children:[(0,b.jsx)("h2",{children:"Multi-Tenant"}),(0,b.jsxs)("div",{style:{backgroundColor:"#f5f5f5",padding:"1rem",borderRadius:"4px",marginTop:"1rem"},children:[(0,b.jsxs)("code",{children:[(0,b.jsx)("strong",{children:"GET"})," /api/tenant/ping"]}),(0,b.jsx)("p",{children:"Get current tenant information"}),(0,b.jsx)("pre",{style:{backgroundColor:"#fff",padding:"1rem",borderRadius:"4px",overflow:"auto"},children:`Headers:
X-Tenant: acme

Response:
{
  "tenant": "acme",
  "ok": true
}`})]})]}),(0,b.jsxs)("div",{style:{marginTop:"2rem"},children:[(0,b.jsx)("h2",{children:"Billing Analytics"}),(0,b.jsxs)("div",{style:{backgroundColor:"#f5f5f5",padding:"1rem",borderRadius:"4px",marginTop:"1rem"},children:[(0,b.jsxs)("code",{children:[(0,b.jsx)("strong",{children:"GET"})," /api/billing/summary"]}),(0,b.jsx)("p",{children:"Get billing analytics summary"}),(0,b.jsx)("pre",{style:{backgroundColor:"#fff",padding:"1rem",borderRadius:"4px",overflow:"auto"},children:`Response:
{
  "mrr": 12500.00,
  "arpa": 125.00,
  "churn": 2.5,
  "customers": 100
}`})]})]}),(0,b.jsxs)("div",{style:{marginTop:"2rem"},children:[(0,b.jsx)("h2",{children:"Usage Metering"}),(0,b.jsxs)("div",{style:{backgroundColor:"#f5f5f5",padding:"1rem",borderRadius:"4px",marginTop:"1rem"},children:[(0,b.jsxs)("code",{children:[(0,b.jsx)("strong",{children:"POST"})," /api/meter/usage"]}),(0,b.jsx)("p",{children:"Record usage for metered billing"}),(0,b.jsx)("pre",{style:{backgroundColor:"#fff",padding:"1rem",borderRadius:"4px",overflow:"auto"},children:`Request:
{
  "meter": "api_calls",
  "quantity": 100,
  "user": "user123",
  "tenant": "acme"
}

Response:
{
  "ok": true
}`})]})]}),(0,b.jsxs)("div",{style:{marginTop:"2rem"},children:[(0,b.jsx)("h2",{children:"AI Cost Management"}),(0,b.jsxs)("div",{style:{backgroundColor:"#f5f5f5",padding:"1rem",borderRadius:"4px",marginTop:"1rem"},children:[(0,b.jsxs)("code",{children:[(0,b.jsx)("strong",{children:"GET"})," /api/ai/cost-cap"]}),(0,b.jsx)("p",{children:"View AI cost budget and remaining allocation"}),(0,b.jsx)("pre",{style:{backgroundColor:"#fff",padding:"1rem",borderRadius:"4px",overflow:"auto"},children:`Response:
{
  "daily_cap_usd": 2.00,
  "spent_today_usd": 0.45,
  "remaining_usd": 1.55,
  "ok": true
}`})]})]}),(0,b.jsxs)("div",{style:{marginTop:"2rem"},children:[(0,b.jsx)("h2",{children:"Autopilot"}),(0,b.jsxs)("div",{style:{backgroundColor:"#f5f5f5",padding:"1rem",borderRadius:"4px",marginTop:"1rem"},children:[(0,b.jsxs)("code",{children:[(0,b.jsx)("strong",{children:"POST"})," /api/autopilot/toggle"]}),(0,b.jsx)("p",{children:"Enable or disable autopilot mode"}),(0,b.jsx)("pre",{style:{backgroundColor:"#fff",padding:"1rem",borderRadius:"4px",overflow:"auto"},children:`Request:
{
  "enabled": true
}

Response:
{
  "enabled": true,
  "ok": true
}`})]}),(0,b.jsxs)("div",{style:{backgroundColor:"#f5f5f5",padding:"1rem",borderRadius:"4px",marginTop:"1rem"},children:[(0,b.jsxs)("code",{children:[(0,b.jsx)("strong",{children:"GET"})," /api/autopilot/status"]}),(0,b.jsx)("p",{children:"Get autopilot status"}),(0,b.jsx)("pre",{style:{backgroundColor:"#fff",padding:"1rem",borderRadius:"4px",overflow:"auto"},children:`Response:
{
  "enabled": false
}`})]})]}),(0,b.jsxs)("div",{style:{marginTop:"3rem",padding:"1rem",backgroundColor:"#e3f2fd",borderRadius:"4px"},children:[(0,b.jsx)("h3",{children:"Support"}),(0,b.jsxs)("p",{children:["For API support, contact ",(0,b.jsx)("a",{href:"mailto:vii7cc@gmail.com",children:"vii7cc@gmail.com"})]})]})]})}a.s(["default",()=>c])}];

//# sourceMappingURL=%5Broot-of-the-server%5D__4807f5a3._.js.map