import { useState } from "react";
import { ShieldCheck, Upload, Zap, Copy, Download, Activity } from "lucide-react";

const API = "";

const pill = (v) =>
  v === "OUT_OF_SCOPE"
    ? "bg-red-100 text-red-700 border-red-200"
    : v === "GREY_AREA"
      ? "bg-amber-100 text-amber-700 border-amber-200"
      : "bg-emerald-100 text-emerald-700 border-emerald-200";

export default function App() {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showTele, setShowTele] = useState(false);
  const [copied, setCopied] = useState(false);
  const [projectName, setProjectName] = useState("BrightKart Website");
  const [clientName, setClientName] = useState("BrightKart Retail");
  const [rate, setRate] = useState(60);
  const [sowFile, setSowFile] = useState(null);
  const [csvFile, setCsvFile] = useState(null);

  async function runDemo() {
    setLoading(true);
    setError("");
    try {
      const r = await fetch(`${API}/api/demo/audit`);
      if (!r.ok) throw new Error(`demo failed: ${r.status}`);
      setReport(await r.json());
    } catch (e) {
      setError("Backend offline — run: uvicorn backend.main:app --port 8000");
    } finally {
      setLoading(false);
    }
  }

  async function runUpload(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      if (!sowFile || !csvFile) throw new Error("Attach both SOW and CSV first.");
      const p = await fetch(`${API}/api/projects`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ project_name: projectName, client_name: clientName, contracted_hourly_rate: String(rate) }),
      });
      if (!p.ok) throw new Error("project create failed");
      const { project_id } = await p.json();
      const sowFd = new FormData();
      sowFd.append("file", sowFile);
      const s = await fetch(`${API}/api/projects/${project_id}/sow`, { method: "POST", body: sowFd });
      if (!s.ok) throw new Error("SOW upload failed — PDF or Markdown only");
      const csvFd = new FormData();
      csvFd.append("file", csvFile);
      const a = await fetch(`${API}/api/projects/${project_id}/audit`, { method: "POST", body: csvFd });
      if (!a.ok) {
        const t = await a.text();
        throw new Error(t.includes("SOW") ? t : "Audit failed — check CSV headers");
      }
      setReport(await a.json());
    } catch (err) {
      setError(err.message || "Upload failed");
    } finally {
      setLoading(false);
    }
  }

  function copyEmail() {
    if (!report) return;
    const email = report.change_order_markdown.split("---")[1] || report.change_order_markdown;
    navigator.clipboard.writeText(email.trim());
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  }

  function downloadMD() {
    if (!report) return;
    const blob = new Blob([report.change_order_markdown], { type: "text/markdown" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "scopeshield-change-order.md";
    a.click();
  }


  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b bg-white">
        <div className="mx-auto flex max-w-6xl items-center gap-3 px-6 py-4">
          <ShieldCheck className="h-7 w-7 text-emerald-600" />
          <div>
            <h1 className="text-xl font-bold">ScopeShield</h1>
            <p className="text-xs text-slate-500">NDA-safe scope-creep auditor · scopeshield.tech</p>
          </div>
          <button
            onClick={runDemo}
            disabled={loading}
            className="ml-auto flex items-center gap-2 rounded-lg bg-emerald-600 px-4 py-2 text-sm font-semibold text-white hover:bg-emerald-700 disabled:opacity-50"
          >
            <Zap className="h-4 w-4" /> {loading ? "Auditing…" : "Run Real Agency Audit"}
          </button>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-8">
        {!report && (
          <form onSubmit={runUpload} className="rounded-xl border bg-white p-6">
            <h2 className="flex items-center gap-2 text-lg font-semibold"><Upload className="h-5 w-5" /> Audit your week</h2>
            <div className="mt-4 grid grid-cols-3 gap-3">
              <label className="text-xs font-semibold">Project<input value={projectName} onChange={(e) => setProjectName(e.target.value)} className="mt-1 w-full rounded-lg border px-3 py-2 text-sm" /></label>
              <label className="text-xs font-semibold">Client<input value={clientName} onChange={(e) => setClientName(e.target.value)} className="mt-1 w-full rounded-lg border px-3 py-2 text-sm" /></label>
              <label className="text-xs font-semibold">Rate $/hr<input type="number" value={rate} onChange={(e) => setRate(e.target.value)} className="mt-1 w-full rounded-lg border px-3 py-2 text-sm" /></label>
            </div>
            <div className="mt-3 grid grid-cols-2 gap-3">
              <label className="rounded-lg border border-dashed p-4 text-xs font-semibold">SOW PDF / Markdown<input type="file" accept=".pdf,.md" onChange={(e) => setSowFile(e.target.files[0])} className="mt-2 block text-xs font-normal" /></label>
              <label className="rounded-lg border border-dashed p-4 text-xs font-semibold">Work-log CSV<input type="file" accept=".csv" onChange={(e) => setCsvFile(e.target.files[0])} className="mt-2 block text-xs font-normal" /></label>
            </div>
            <div className="mt-4 flex items-center gap-3">
              <button disabled={loading} className="rounded-lg bg-slate-900 px-4 py-2 text-sm font-semibold text-white disabled:opacity-50">{loading ? "Auditing…" : "Audit My Week →"}</button>
              <span className="text-xs text-slate-500">or hit <b>Run Real Agency Audit</b> above for the 1-click judge demo</span>
            </div>
          </form>
        )}
        {error && <p className="rounded-lg bg-red-50 p-4 text-sm text-red-700">{error}</p>}

        {report && (
          <>
            <div className="grid grid-cols-3 gap-4">
              {[
                ["Hours logged", report.total_hours_logged],
                ["Out-of-scope hrs", report.out_of_scope_hours],
                ["Recoverable $", `$${report.total_recoverable_revenue_usd.toLocaleString()}`],
              ].map(([k, v]) => (
                <div key={k} className="rounded-xl border bg-white p-4">
                  <p className="text-xs uppercase tracking-wide text-slate-500">{k}</p>
                  <p className="mt-1 text-2xl font-bold">{v}</p>
                </div>
              ))}
            </div>

            <div className="mt-6 overflow-hidden rounded-xl border bg-white">
              <table className="w-full text-left text-sm">
                <thead className="bg-slate-100 text-xs uppercase text-slate-500">
                  <tr><th className="px-4 py-2">Ticket</th><th className="px-4 py-2">Verdict</th><th className="px-4 py-2">Leak</th><th className="px-4 py-2">Clause</th><th className="px-4 py-2 text-right">Recover $</th></tr>
                </thead>
                <tbody>
                  {report.items.map((it) => (
                    <tr key={it.ticket_id} className="border-t">
                      <td className="px-4 py-2"><b>{it.ticket_id}</b> <span className="text-slate-500">{it.task_title}</span></td>
                      <td className="px-4 py-2"><span className={`rounded-full border px-2 py-0.5 text-xs font-semibold ${pill(it.verdict)}`}>{it.verdict}</span></td>
                      <td className="px-4 py-2">{it.tabpfn_leakage_probability}</td>
                      <td className="px-4 py-2 text-xs text-slate-600" title={it.contractual_reasoning}>{it.violated_or_matched_clause}</td>
                      <td className="px-4 py-2 text-right font-semibold">{it.recoverable_amount_usd ? `$${it.recoverable_amount_usd}` : "—"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="mt-6 rounded-xl border bg-white p-5">
              <div className="flex items-center gap-2">
                <h3 className="font-semibold">Client-ready change order</h3>
                <button onClick={copyEmail} className="ml-auto flex items-center gap-1 rounded-lg border px-3 py-1.5 text-xs font-semibold hover:bg-slate-50">
                  <Copy className="h-3.5 w-3.5" /> {copied ? "Copied!" : "Copy Email"}
                </button>
                <button onClick={downloadMD} className="flex items-center gap-1 rounded-lg border px-3 py-1.5 text-xs font-semibold hover:bg-slate-50">
                  <Download className="h-3.5 w-3.5" /> Download
                </button>
              </div>
              <pre className="mt-3 max-h-72 overflow-auto whitespace-pre-wrap rounded-lg bg-slate-950 p-4 text-xs text-slate-100">{report.change_order_markdown}</pre>
            </div>

            <button onClick={() => setShowTele(!showTele)} className="mt-4 flex items-center gap-2 text-xs font-semibold text-slate-500 hover:text-slate-800">
              <Activity className="h-3.5 w-3.5" /> {showTele ? "Hide" : "Show"} Agent Telemetry
            </button>
            {showTele && (
              <pre className="mt-2 overflow-auto rounded-lg border bg-white p-4 text-xs">{JSON.stringify(report.telemetry, null, 2)}</pre>
            )}
          </>
        )}
      </main>
    </div>
  );
}
