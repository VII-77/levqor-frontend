module.exports=[93695,(a,b,c)=>{b.exports=a.x("next/dist/shared/lib/no-fallback-error.external.js",()=>require("next/dist/shared/lib/no-fallback-error.external.js"))},70864,a=>{a.n(a.i(33290))},2894,a=>{a.n(a.i(66188))},13718,a=>{a.n(a.i(85523))},18198,a=>{a.n(a.i(45518))},62212,a=>{a.n(a.i(66114))},71688,a=>{a.n(a.i(20178))},99981,a=>{"use strict";var b=a.i(7997);function c(){return(0,b.jsxs)("div",{className:"prose max-w-none",children:[(0,b.jsx)("h1",{children:"Workflow Engine API"}),(0,b.jsx)("p",{children:"The Workflow Engine provides live automation monitoring and control through a RESTful API."}),(0,b.jsx)("h2",{children:"Endpoints"}),(0,b.jsx)("h3",{children:"GET /api/workflows"}),(0,b.jsx)("p",{children:"List all workflows with current stats."}),(0,b.jsx)("h4",{children:"Response Fields"}),(0,b.jsxs)("ul",{children:[(0,b.jsxs)("li",{children:[(0,b.jsx)("code",{children:"id"})," (string) - Unique workflow identifier"]}),(0,b.jsxs)("li",{children:[(0,b.jsx)("code",{children:"name"})," (string) - Human-readable workflow name"]}),(0,b.jsxs)("li",{children:[(0,b.jsx)("code",{children:"enabled"})," (boolean) - Whether workflow is enabled"]}),(0,b.jsxs)("li",{children:[(0,b.jsx)("code",{children:"last_run"})," (number) - Unix timestamp of last execution"]}),(0,b.jsxs)("li",{children:[(0,b.jsx)("code",{children:"status"})," (string) - One of: ok, degraded, fail"]}),(0,b.jsxs)("li",{children:[(0,b.jsx)("code",{children:"avg_latency_ms"})," (number) - Average execution time in milliseconds"]}),(0,b.jsxs)("li",{children:[(0,b.jsx)("code",{children:"success_7d"})," (number) - Successful runs in last 7 days"]}),(0,b.jsxs)("li",{children:[(0,b.jsx)("code",{children:"fail_7d"})," (number) - Failed runs in last 7 days"]})]}),(0,b.jsx)("h4",{children:"Example Response"}),(0,b.jsx)("pre",{className:"bg-gray-50 p-4 rounded text-sm overflow-x-auto",children:`[
  {
    "id": "self_heal",
    "name": "Self-Heal Cycle",
    "enabled": true,
    "last_run": 1729900000,
    "status": "ok",
    "avg_latency_ms": 245.5,
    "success_7d": 168,
    "fail_7d": 0
  },
  {
    "id": "health_monitor",
    "name": "Health Monitor",
    "enabled": true,
    "last_run": 1729899700,
    "status": "ok",
    "avg_latency_ms": 120.3,
    "success_7d": 504,
    "fail_7d": 2
  }
]`}),(0,b.jsx)("h3",{children:"GET /api/workflows/<id>/runs"}),(0,b.jsx)("p",{children:"Get the last 50 execution runs for a specific workflow."}),(0,b.jsx)("h4",{children:"Parameters"}),(0,b.jsx)("ul",{children:(0,b.jsxs)("li",{children:[(0,b.jsx)("code",{children:"id"})," (path) - Workflow ID"]})}),(0,b.jsx)("h4",{children:"Response Fields"}),(0,b.jsxs)("ul",{children:[(0,b.jsxs)("li",{children:[(0,b.jsx)("code",{children:"ts"})," (number) - Unix timestamp of run"]}),(0,b.jsxs)("li",{children:[(0,b.jsx)("code",{children:"duration_ms"})," (number) - Execution time in milliseconds"]}),(0,b.jsxs)("li",{children:[(0,b.jsx)("code",{children:"status"})," (string) - Run status: ok or fail"]}),(0,b.jsxs)("li",{children:[(0,b.jsx)("code",{children:"note"})," (string) - Additional context or error message"]})]}),(0,b.jsx)("h4",{children:"Example Response"}),(0,b.jsx)("pre",{className:"bg-gray-50 p-4 rounded text-sm overflow-x-auto",children:`[
  {
    "ts": 1729900000,
    "duration_ms": 250,
    "status": "ok",
    "note": "Self-heal cycle #42"
  },
  {
    "ts": 1729896400,
    "duration_ms": 220,
    "status": "ok",
    "note": "Self-heal cycle #41"
  }
]`}),(0,b.jsx)("h3",{children:"POST /api/workflows/<id>/toggle"}),(0,b.jsx)("p",{children:"Enable or disable a workflow. Toggles the current state."}),(0,b.jsx)("h4",{children:"Parameters"}),(0,b.jsx)("ul",{children:(0,b.jsxs)("li",{children:[(0,b.jsx)("code",{children:"id"})," (path) - Workflow ID"]})}),(0,b.jsx)("h4",{children:"Response Fields"}),(0,b.jsxs)("ul",{children:[(0,b.jsxs)("li",{children:[(0,b.jsx)("code",{children:"ok"})," (boolean) - Whether operation succeeded"]}),(0,b.jsxs)("li",{children:[(0,b.jsx)("code",{children:"workflow_id"})," (string) - ID of toggled workflow"]}),(0,b.jsxs)("li",{children:[(0,b.jsx)("code",{children:"enabled"})," (boolean) - New enabled state"]})]}),(0,b.jsx)("h4",{children:"Example Response"}),(0,b.jsx)("pre",{className:"bg-gray-50 p-4 rounded text-sm overflow-x-auto",children:`{
  "ok": true,
  "workflow_id": "self_heal",
  "enabled": false
}`}),(0,b.jsx)("h2",{children:"Rate Limits"}),(0,b.jsxs)("p",{children:["All workflow API endpoints are rate-limited to ",(0,b.jsx)("strong",{children:"5 requests per second per IP address"}),". Exceeding this limit returns HTTP 429 with error message."]}),(0,b.jsx)("h2",{children:"Error Responses"}),(0,b.jsx)("h3",{children:"404 Not Found"}),(0,b.jsx)("pre",{className:"bg-gray-50 p-4 rounded text-sm overflow-x-auto",children:`{
  "ok": false,
  "error": "Workflow not found"
}`}),(0,b.jsx)("h3",{children:"429 Rate Limit Exceeded"}),(0,b.jsx)("pre",{className:"bg-gray-50 p-4 rounded text-sm overflow-x-auto",children:`{
  "ok": false,
  "error": "Rate limit exceeded"
}`}),(0,b.jsx)("h3",{children:"500 Internal Server Error"}),(0,b.jsx)("pre",{className:"bg-gray-50 p-4 rounded text-sm overflow-x-auto",children:`{
  "ok": false,
  "error": "Error message here"
}`}),(0,b.jsx)("h2",{children:"Data Sources"}),(0,b.jsx)("p",{children:"Workflow data is aggregated from multiple log files:"}),(0,b.jsxs)("ul",{children:[(0,b.jsxs)("li",{children:[(0,b.jsx)("code",{children:"logs/self_heal.ndjson"})," - Self-healing cycle execution logs"]}),(0,b.jsxs)("li",{children:[(0,b.jsx)("code",{children:"logs/auto_rollback.ndjson"})," - Automatic rollback logs"]}),(0,b.jsxs)("li",{children:[(0,b.jsx)("code",{children:"exports/uptime_*.json"})," - Health monitoring uptime data"]})]}),(0,b.jsx)("p",{children:"If log files are missing or empty, the API returns mock data to keep endpoints stable."}),(0,b.jsx)("h2",{children:"Live Dashboard"}),(0,b.jsxs)("p",{children:["Visit ",(0,b.jsx)("a",{href:"/dashboard",className:"text-blue-600 hover:underline",children:"/dashboard"})," to see the live workflow engine in action with auto-refreshing data every 10 seconds."]})]})}a.s(["default",()=>c])}];

//# sourceMappingURL=%5Broot-of-the-server%5D__bff57e03._.js.map