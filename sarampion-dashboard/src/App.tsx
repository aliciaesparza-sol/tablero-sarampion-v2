import { useState, useEffect } from "react";

const LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Secretar%C3%ADa_de_Salud_%28Mexico%29_logo.svg/320px-Secretar%C3%ADa_de_Salud_%28Mexico%29_logo.svg.png";

const GIGANTE_LOGO = `data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 240'><defs><linearGradient id='g1' x1='0%25' y1='0%25' x2='100%25' y2='100%25'><stop offset='0%25' style='stop-color:%23f7971e'/><stop offset='50%25' style='stop-color:%23e84393'/><stop offset='100%25' style='stop-color:%234facfe'/></linearGradient></defs><polygon points='100,10 60,100 80,100 55,190 100,140 145,190 120,100 140,100' fill='url(%23g1)'/><text x='100' y='210' text-anchor='middle' font-size='18' font-weight='bold' fill='%23555' font-family='Arial'>CONSTRUYE</text><text x='100' y='230' text-anchor='middle' font-size='22' font-weight='900' fill='%23333' font-family='Arial'>GIGANTE</text></svg>`;

interface Municipio {
  MUNICIPIO: string;
  DOSIS_12M: number;
  DOSIS_18M: number;
  DOSIS_6A: number;
  DOSIS_10_49: number;
  TOTAL: number;
  META_TOTAL: number;
  COB_12M: number;
  COB_18M: number;
  COB_6A: number;
  COB_ADULT: number;
  COBERTURA: number;
  SEMAFORO: string;
}

interface DashData {
  corte: string;
  semana: number;
  municipios: Municipio[];
}

const TABS = [
  { key: "resumen", label: "📊 Resumen Total" },
  { key: "12m",     label: "👶 12 Meses" },
  { key: "18m",     label: "🧒 18 Meses" },
  { key: "6a",      label: "📚 6 Años" },
  { key: "adultos", label: "🧑 Adultos 10-49" },
];

function semColor(cob: number) {
  if (cob >= 95) return { bg: "#d4edda", text: "#155724", label: "✅ META" };
  if (cob >= 80) return { bg: "#c3e6cb", text: "#155724", label: "🟢 AVANZADO" };
  if (cob >= 50) return { bg: "#fff3cd", text: "#856404", label: "🟡 EN PROCESO" };
  if (cob >= 25) return { bg: "#ffe5cc", text: "#7d3c00", label: "🟠 REZAGO" };
  return { bg: "#f8d7da", text: "#721c24", label: "🔴 CRÍTICO" };
}

function TablaGrupo({ municipios, dosisKey, cobKey, meta, label }: {
  municipios: Municipio[];
  dosisKey: keyof Municipio;
  cobKey: keyof Municipio;
  meta: number;
  label: string;
}) {
  const sorted = [...municipios].sort((a, b) => (a[cobKey] as number) - (b[cobKey] as number));
  const totalDosis = municipios.reduce((s, m) => s + (m[dosisKey] as number), 0);
  const totalMeta = municipios.reduce((s, m) => s + Math.round(m.META_TOTAL * meta), 0);
  const cobTotal = totalMeta > 0 ? (totalDosis / totalMeta * 100) : 0;
  const sc = semColor(cobTotal);

  return (
    <div>
      <div style={{ background: "#f8f9fa", border: "1px solid #dee2e6", borderRadius: 8, padding: "12px 16px", marginBottom: 16, display: "flex", gap: 32, flexWrap: "wrap" }}>
        <div><span style={{ color: "#6c757d", fontSize: 13 }}>Meta sectorial</span><br /><strong style={{ fontSize: 18 }}>{totalMeta.toLocaleString()}</strong></div>
        <div><span style={{ color: "#6c757d", fontSize: 13 }}>Dosis aplicadas</span><br /><strong style={{ fontSize: 18 }}>{totalDosis.toLocaleString()}</strong></div>
        <div><span style={{ color: "#6c757d", fontSize: 13 }}>Cobertura estatal</span><br /><strong style={{ fontSize: 18, color: cobTotal >= 80 ? "#28a745" : cobTotal >= 50 ? "#856404" : "#dc3545" }}>{cobTotal.toFixed(1)}%</strong></div>
      </div>
      <div style={{ overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
          <thead>
            <tr style={{ background: "#343a40", color: "white" }}>
              <th style={{ padding: "10px 14px", textAlign: "left", position: "sticky", left: 0, background: "#343a40" }}>Municipio</th>
              <th style={{ padding: "10px 14px", textAlign: "right" }}>Meta</th>
              <th style={{ padding: "10px 14px", textAlign: "right" }}>Dosis</th>
              <th style={{ padding: "10px 14px", textAlign: "right" }}>Pendientes</th>
              <th style={{ padding: "10px 14px", textAlign: "center" }}>Cobertura %</th>
              <th style={{ padding: "10px 14px", textAlign: "center" }}>Semáforo</th>
            </tr>
          </thead>
          <tbody>
            {sorted.map((m, i) => {
              const dosis = m[dosisKey] as number;
              const cob = m[cobKey] as number;
              const metaMun = Math.round(m.META_TOTAL * meta);
              const pend = Math.max(0, metaMun - dosis);
              const sc = semColor(cob);
              return (
                <tr key={m.MUNICIPIO} style={{ background: i % 2 === 0 ? "#ffffff" : "#f8f9fa", borderBottom: "1px solid #dee2e6" }}>
                  <td style={{ padding: "9px 14px", fontWeight: 500, position: "sticky", left: 0, background: i % 2 === 0 ? "#ffffff" : "#f8f9fa" }}>{m.MUNICIPIO}</td>
                  <td style={{ padding: "9px 14px", textAlign: "right" }}>{metaMun.toLocaleString()}</td>
                  <td style={{ padding: "9px 14px", textAlign: "right" }}>{Math.round(dosis).toLocaleString()}</td>
                  <td style={{ padding: "9px 14px", textAlign: "right", color: pend > 0 ? "#dc3545" : "#28a745" }}>{pend.toLocaleString()}</td>
                  <td style={{ padding: "9px 14px", textAlign: "center", fontWeight: 700 }}>{cob.toFixed(1)}%</td>
                  <td style={{ padding: "9px 14px", textAlign: "center" }}>
                    <span style={{ background: sc.bg, color: sc.text, padding: "3px 10px", borderRadius: 12, fontSize: 12, fontWeight: 600, whiteSpace: "nowrap" }}>{sc.label}</span>
                  </td>
                </tr>
              );
            })}
          </tbody>
          <tfoot>
            <tr style={{ background: "#343a40", color: "white", fontWeight: 700 }}>
              <td style={{ padding: "10px 14px" }}>TOTAL DURANGO</td>
              <td style={{ padding: "10px 14px", textAlign: "right" }}>{totalMeta.toLocaleString()}</td>
              <td style={{ padding: "10px 14px", textAlign: "right" }}>{totalDosis.toLocaleString()}</td>
              <td style={{ padding: "10px 14px", textAlign: "right" }}>{Math.max(0, totalMeta - totalDosis).toLocaleString()}</td>
              <td style={{ padding: "10px 14px", textAlign: "center" }}>{cobTotal.toFixed(1)}%</td>
              <td style={{ padding: "10px 14px", textAlign: "center" }}>
                <span style={{ background: sc.bg, color: sc.text, padding: "3px 10px", borderRadius: 12, fontSize: 12, fontWeight: 600 }}>{sc.label}</span>
              </td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>
  );
}

function ResumenTab({ municipios }: { municipios: Municipio[] }) {
  const sorted = [...municipios].sort((a, b) => a.COBERTURA - b.COBERTURA);
  const totalDosis = municipios.reduce((s, m) => s + m.TOTAL, 0);
  const totalMeta = municipios.reduce((s, m) => s + m.META_TOTAL, 0);
  const cobTotal = totalMeta > 0 ? (totalDosis / totalMeta * 100) : 0;
  const sc = semColor(cobTotal);

  return (
    <div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))", gap: 12, marginBottom: 20 }}>
        {[
          { label: "Universo Total", val: totalMeta.toLocaleString(), color: "#0d6efd" },
          { label: "Total Dosis", val: totalDosis.toLocaleString(), color: "#28a745" },
          { label: "Pendientes", val: Math.max(0, totalMeta - totalDosis).toLocaleString(), color: "#dc3545" },
          { label: "Cobertura", val: cobTotal.toFixed(1) + "%", color: cobTotal >= 80 ? "#28a745" : cobTotal >= 50 ? "#856404" : "#dc3545" },
        ].map(k => (
          <div key={k.label} style={{ background: "#f8f9fa", border: "1px solid #dee2e6", borderRadius: 8, padding: "14px 16px", borderTop: `4px solid ${k.color}` }}>
            <div style={{ color: "#6c757d", fontSize: 12, marginBottom: 4 }}>{k.label}</div>
            <div style={{ fontSize: 22, fontWeight: 700, color: k.color }}>{k.val}</div>
          </div>
        ))}
      </div>
      <div style={{ overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
          <thead>
            <tr style={{ background: "#343a40", color: "white" }}>
              {["Municipio","Meta","12M","18M","6A","Adultos","Total","Cobertura","Semáforo"].map(h => (
                <th key={h} style={{ padding: "10px 12px", textAlign: h === "Municipio" ? "left" : "center", whiteSpace: "nowrap" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sorted.map((m, i) => {
              const sc = semColor(m.COBERTURA);
              return (
                <tr key={m.MUNICIPIO} style={{ background: i % 2 === 0 ? "#ffffff" : "#f8f9fa", borderBottom: "1px solid #dee2e6" }}>
                  <td style={{ padding: "8px 12px", fontWeight: 500 }}>{m.MUNICIPIO}</td>
                  <td style={{ padding: "8px 12px", textAlign: "right" }}>{Math.round(m.META_TOTAL).toLocaleString()}</td>
                  <td style={{ padding: "8px 12px", textAlign: "right" }}>{Math.round(m.DOSIS_12M).toLocaleString()}</td>
                  <td style={{ padding: "8px 12px", textAlign: "right" }}>{Math.round(m.DOSIS_18M).toLocaleString()}</td>
                  <td style={{ padding: "8px 12px", textAlign: "right" }}>{Math.round(m.DOSIS_6A).toLocaleString()}</td>
                  <td style={{ padding: "8px 12px", textAlign: "right" }}>{Math.round(m.DOSIS_10_49).toLocaleString()}</td>
                  <td style={{ padding: "8px 12px", textAlign: "right", fontWeight: 700 }}>{Math.round(m.TOTAL).toLocaleString()}</td>
                  <td style={{ padding: "8px 12px", textAlign: "center", fontWeight: 700 }}>{m.COBERTURA.toFixed(1)}%</td>
                  <td style={{ padding: "8px 12px", textAlign: "center" }}>
                    <span style={{ background: sc.bg, color: sc.text, padding: "3px 10px", borderRadius: 12, fontSize: 11, fontWeight: 600, whiteSpace: "nowrap" }}>{sc.label}</span>
                  </td>
                </tr>
              );
            })}
          </tbody>
          <tfoot>
            <tr style={{ background: "#343a40", color: "white", fontWeight: 700 }}>
              <td style={{ padding: "10px 12px" }}>TOTAL DURANGO</td>
              <td style={{ padding: "10px 12px", textAlign: "right" }}>{Math.round(totalMeta).toLocaleString()}</td>
              <td colSpan={4} style={{ padding: "10px 12px" }}></td>
              <td style={{ padding: "10px 12px", textAlign: "right" }}>{Math.round(totalDosis).toLocaleString()}</td>
              <td style={{ padding: "10px 12px", textAlign: "center" }}>{cobTotal.toFixed(1)}%</td>
              <td style={{ padding: "10px 12px", textAlign: "center" }}>
                <span style={{ background: sc.bg, color: sc.text, padding: "3px 10px", borderRadius: 12, fontSize: 11, fontWeight: 600 }}>{sc.label}</span>
              </td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>
  );
}

const App = () => {
  const [data, setData] = useState<DashData | null>(null);
  const [tab, setTab] = useState("resumen");

  useEffect(() => {
    fetch("/data.json").then(r => r.json()).then(setData).catch(console.error);
  }, []);

  if (!data) return <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: "100vh", fontSize: 18, color: "#6c757d" }}>Cargando datos...</div>;

  return (
    <div style={{ minHeight: "100vh", background: "#ffffff", fontFamily: "Arial, sans-serif" }}>
      {/* Header */}
      <div style={{ background: "#ffffff", borderBottom: "3px solid #28a745", padding: "16px 24px", display: "flex", alignItems: "center", gap: 20, boxShadow: "0 2px 8px rgba(0,0,0,0.08)" }}>
        <img src={GIGANTE_LOGO} alt="Logo" style={{ height: 64, width: "auto" }} />
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 11, color: "#6c757d", textTransform: "uppercase", letterSpacing: 1 }}>Servicios de Salud de Durango</div>
          <h1 style={{ margin: "2px 0", fontSize: 22, fontWeight: 700, color: "#212529" }}>🦠 Cobertura Sarampión SRP/SR · Durango</h1>
          <div style={{ fontSize: 13, color: "#6c757d" }}>Universo CONAPO 2026 · Corte: {data.corte} · Semana {data.semana}</div>
        </div>
        <div style={{ textAlign: "right" }}>
          <div style={{ fontSize: 11, color: "#6c757d" }}>Actualizado</div>
          <div style={{ fontSize: 13, fontWeight: 600, color: "#28a745" }}>{data.corte}</div>
        </div>
      </div>

      {/* Leyenda semáforo */}
      <div style={{ background: "#f8f9fa", borderBottom: "1px solid #dee2e6", padding: "8px 24px", display: "flex", gap: 12, flexWrap: "wrap", alignItems: "center" }}>
        <span style={{ fontSize: 12, color: "#6c757d", marginRight: 4 }}>Semáforo:</span>
        {[
          { bg: "#d4edda", text: "#155724", label: "✅ ≥95% META" },
          { bg: "#c3e6cb", text: "#155724", label: "🟢 80-94% AVANZADO" },
          { bg: "#fff3cd", text: "#856404", label: "🟡 50-79% EN PROCESO" },
          { bg: "#ffe5cc", text: "#7d3c00", label: "🟠 25-49% REZAGO" },
          { bg: "#f8d7da", text: "#721c24", label: "🔴 <25% CRÍTICO" },
        ].map(s => (
          <span key={s.label} style={{ background: s.bg, color: s.text, padding: "3px 10px", borderRadius: 12, fontSize: 11, fontWeight: 600 }}>{s.label}</span>
        ))}
      </div>

      {/* Tabs */}
      <div style={{ borderBottom: "2px solid #dee2e6", padding: "0 24px", background: "#fff", display: "flex", gap: 4 }}>
        {TABS.map(t => (
          <button key={t.key} onClick={() => setTab(t.key)}
            style={{ padding: "12px 18px", border: "none", background: "none", cursor: "pointer", fontSize: 13, fontWeight: tab === t.key ? 700 : 400, color: tab === t.key ? "#28a745" : "#6c757d", borderBottom: tab === t.key ? "3px solid #28a745" : "3px solid transparent", marginBottom: -2 }}>
            {t.label}
          </button>
        ))}
      </div>

      {/* Contenido */}
      <div style={{ padding: "20px 24px" }}>
        {tab === "resumen"  && <ResumenTab municipios={data.municipios} />}
        {tab === "12m"      && <TablaGrupo municipios={data.municipios} dosisKey="DOSIS_12M"   cobKey="COB_12M"   meta={1.0} label="12 Meses" />}
        {tab === "18m"      && <TablaGrupo municipios={data.municipios} dosisKey="DOSIS_18M"   cobKey="COB_18M"   meta={1.0} label="18 Meses" />}
        {tab === "6a"       && <TablaGrupo municipios={data.municipios} dosisKey="DOSIS_6A"    cobKey="COB_6A"    meta={0.5} label="6 Años" />}
        {tab === "adultos"  && <TablaGrupo municipios={data.municipios} dosisKey="DOSIS_10_49" cobKey="COB_ADULT" meta={0.5} label="Adultos 10-49" />}
      </div>

      <div style={{ textAlign: "center", padding: "16px", fontSize: 11, color: "#adb5bd", borderTop: "1px solid #dee2e6" }}>
        * Datos nominales CeNSIA · Actualización automática diaria · Durango Servicios de Salud
      </div>
    </div>
  );
};

export default App;
