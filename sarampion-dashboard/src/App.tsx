import { useState, useEffect } from "react";

interface Municipio {
  MUNICIPIO: string; DOSIS_12M: number; DOSIS_18M: number;
  DOSIS_6A: number; DOSIS_10_49: number; TOTAL: number;
  META_TOTAL: number; COB_12M: number; COB_18M: number;
  COB_6A: number; COB_ADULT: number; COBERTURA: number; SEMAFORO: string;
}
interface DashData { corte: string; semana: number; municipios: Municipio[]; }

function sem(c: number) {
  if (c>=95) return {bg:"#d4edda",tx:"#155724",lb:"✅ META"};
  if (c>=80) return {bg:"#c3e6cb",tx:"#155724",lb:"🟢 AVANZADO"};
  if (c>=50) return {bg:"#fff3cd",tx:"#856404",lb:"🟡 EN PROCESO"};
  if (c>=25) return {bg:"#ffe5cc",tx:"#7d3c00",lb:"🟠 REZAGO"};
  return {bg:"#f8d7da",tx:"#721c24",lb:"🔴 CRITICO"};
}

const TABS = [
  {k:"res",l:"📊 Resumen Total"},{k:"12m",l:"👶 12 Meses"},
  {k:"18m",l:"🧒 18 Meses"},{k:"6a",l:"📚 6 Anos"},
  {k:"adu",l:"🧑 Adultos"},
];

interface TablaProps {
  muns: Municipio[];
  dk: keyof Municipio;
  ck: keyof Municipio;
  pct: number;
}

function Tabla({muns, dk, ck, pct}: TablaProps) {
  const s=[...muns].sort((a,b)=>(a[ck] as number)-(b[ck] as number));
  const td=muns.reduce((x,m)=>x+(m[dk] as number),0);
  const tm=muns.reduce((x,m)=>x+Math.round(m.META_TOTAL*pct),0);
  const ct=tm>0?td/tm*100:0;
  const sc=sem(ct);
  return(<div>
    <div style={{background:"#f8f9fa",border:"1px solid #dee2e6",borderRadius:8,padding:"12px 16px",marginBottom:16,display:"flex",gap:32}}>
      <div><small style={{color:"#6c757d"}}>Meta</small><br/><b style={{fontSize:18}}>{tm.toLocaleString()}</b></div>
      <div><small style={{color:"#6c757d"}}>Dosis</small><br/><b style={{fontSize:18}}>{Math.round(td).toLocaleString()}</b></div>
      <div><small style={{color:"#6c757d"}}>Cobertura</small><br/><b style={{fontSize:18,color:ct>=80?"#28a745":ct>=50?"#856404":"#dc3545"}}>{ct.toFixed(1)}%</b></div>
    </div>
    <div style={{overflowX:"auto"}}>
    <table style={{width:"100%",borderCollapse:"collapse",fontSize:14}}>
      <thead><tr style={{background:"#343a40",color:"white"}}>
        {["Municipio","Meta","Dosis","Pendientes","Cobertura %","Semaforo"].map(h=><th key={h} style={{padding:"10px 12px",textAlign:h==="Municipio"?"left":"center"}}>{h}</th>)}
      </tr></thead>
      <tbody>{s.map((m,i)=>{
        const d=m[dk] as number,c=m[ck] as number,mt=Math.round(m.META_TOTAL*pct),p=Math.max(0,mt-d),sc=sem(c);
        return(<tr key={m.MUNICIPIO} style={{background:i%2===0?"#fff":"#f8f9fa",borderBottom:"1px solid #dee2e6"}}>
          <td style={{padding:"8px 12px",fontWeight:500}}>{m.MUNICIPIO}</td>
          <td style={{padding:"8px 12px",textAlign:"right"}}>{mt.toLocaleString()}</td>
          <td style={{padding:"8px 12px",textAlign:"right"}}>{Math.round(d).toLocaleString()}</td>
          <td style={{padding:"8px 12px",textAlign:"right",color:p>0?"#dc3545":"#28a745"}}>{p.toLocaleString()}</td>
          <td style={{padding:"8px 12px",textAlign:"center",fontWeight:700}}>{c.toFixed(1)}%</td>
          <td style={{padding:"8px 12px",textAlign:"center"}}><span style={{background:sc.bg,color:sc.tx,padding:"3px 10px",borderRadius:12,fontSize:11,fontWeight:600}}>{sc.lb}</span></td>
        </tr>);
      })}</tbody>
      <tfoot><tr style={{background:"#343a40",color:"white",fontWeight:700}}>
        <td style={{padding:"10px 12px"}}>TOTAL DURANGO</td>
        <td style={{padding:"10px 12px",textAlign:"right"}}>{tm.toLocaleString()}</td>
        <td style={{padding:"10px 12px",textAlign:"right"}}>{Math.round(td).toLocaleString()}</td>
        <td style={{padding:"10px 12px",textAlign:"right"}}>{Math.max(0,tm-td).toLocaleString()}</td>
        <td style={{padding:"10px 12px",textAlign:"center"}}>{ct.toFixed(1)}%</td>
        <td style={{padding:"10px 12px",textAlign:"center"}}><span style={{background:sc.bg,color:sc.tx,padding:"3px 8px",borderRadius:10,fontSize:11}}>{sc.lb}</span></td>
      </tr></tfoot>
    </table></div>
  </div>);
}

const App=()=>{
  const [data,setData]=useState<DashData|null>(null);
  const [tab,setTab]=useState("res");
  useEffect(()=>{fetch("./data.json").then(r=>r.json()).then(setData);},[]);
  if(!data) return <div style={{display:"flex",alignItems:"center",justifyContent:"center",height:"100vh",fontSize:18,color:"#6c757d"}}>Cargando...</div>;
  const M=data.municipios;
  const td=M.reduce((x,m)=>x+m.TOTAL,0),tm=M.reduce((x,m)=>x+m.META_TOTAL,0),ct=tm>0?td/tm*100:0,sc=sem(ct);
  return(<div style={{minHeight:"100vh",background:"#fff",fontFamily:"Arial,sans-serif"}}>
    <div style={{background:"#fff",borderBottom:"3px solid #28a745",padding:"16px 24px",display:"flex",alignItems:"center",gap:16,boxShadow:"0 2px 8px rgba(0,0,0,0.08)"}}>
      <div style={{width:56,height:56,background:"linear-gradient(135deg,#f7971e,#e84393,#4facfe)",borderRadius:8,display:"flex",alignItems:"center",justifyContent:"center",fontSize:28}}>🦠</div>
      <div style={{flex:1}}>
        <div style={{fontSize:11,color:"#6c757d",textTransform:"uppercase",letterSpacing:1}}>Servicios de Salud de Durango</div>
        <h1 style={{margin:"2px 0",fontSize:20,fontWeight:700,color:"#212529"}}>Cobertura Sarampion SRP/SR</h1>
        <div style={{fontSize:13,color:"#6c757d"}}>CONAPO 2026 · Corte: {data.corte} · Semana {data.semana}</div>
      </div>
      <div style={{textAlign:"right",background:sc.bg,color:sc.tx,padding:"8px 16px",borderRadius:8}}>
        <div style={{fontSize:22,fontWeight:700}}>{ct.toFixed(1)}%</div>
        <div style={{fontSize:11}}>{sc.lb}</div>
      </div>
    </div>
    <div style={{background:"#f8f9fa",borderBottom:"1px solid #dee2e6",padding:"8px 24px",display:"flex",gap:8,flexWrap:"wrap",alignItems:"center"}}>
      <span style={{fontSize:12,color:"#6c757d"}}>Semaforo:</span>
      {[{bg:"#d4edda",tx:"#155724",lb:"✅ >=95% META"},{bg:"#c3e6cb",tx:"#155724",lb:"🟢 80-94%"},{bg:"#fff3cd",tx:"#856404",lb:"🟡 50-79%"},{bg:"#ffe5cc",tx:"#7d3c00",lb:"🟠 25-49%"},{bg:"#f8d7da",tx:"#721c24",lb:"🔴 <25%"}].map(s=>(
        <span key={s.lb} style={{background:s.bg,color:s.tx,padding:"3px 10px",borderRadius:12,fontSize:11,fontWeight:600}}>{s.lb}</span>
      ))}
    </div>
    <div style={{borderBottom:"2px solid #dee2e6",padding:"0 24px",background:"#fff",display:"flex",gap:4}}>
      {TABS.map(t=><button key={t.k} onClick={()=>setTab(t.k)} style={{padding:"12px 16px",border:"none",background:"none",cursor:"pointer",fontSize:13,fontWeight:tab===t.k?700:400,color:tab===t.k?"#28a745":"#6c757d",borderBottom:tab===t.k?"3px solid #28a745":"3px solid transparent",marginBottom:-2}}>{t.l}</button>)}
    </div>
    <div style={{padding:"20px 24px"}}>
      {tab==="res" && <div>
        <div style={{display:"grid",gridTemplateColumns:"repeat(auto-fit,minmax(150px,1fr))",gap:12,marginBottom:20}}>
          {[{l:"Universo",v:Math.round(tm).toLocaleString(),c:"#0d6efd"},{l:"Total Dosis",v:Math.round(td).toLocaleString(),c:"#28a745"},{l:"Pendientes",v:Math.max(0,tm-td).toLocaleString(),c:"#dc3545"},{l:"Cobertura",v:ct.toFixed(1)+"%",c:ct>=80?"#28a745":ct>=50?"#856404":"#dc3545"}].map(k=>(
            <div key={k.l} style={{background:"#f8f9fa",border:"1px solid #dee2e6",borderRadius:8,padding:"14px 16px",borderTop:`4px solid ${k.c}`}}>
              <div style={{color:"#6c757d",fontSize:12}}>{k.l}</div>
              <div style={{fontSize:22,fontWeight:700,color:k.c}}>{k.v}</div>
            </div>
          ))}
        </div>
        <div style={{overflowX:"auto"}}><table style={{width:"100%",borderCollapse:"collapse",fontSize:14}}>
          <thead><tr style={{background:"#343a40",color:"white"}}>{["Municipio","Meta","12M","18M","6A","Adultos","Total","Cobertura","Semaforo"].map(h=><th key={h} style={{padding:"10px 12px",textAlign:h==="Municipio"?"left":"center",whiteSpace:"nowrap"}}>{h}</th>)}</tr></thead>
          <tbody>{[...M].sort((a,b)=>a.COBERTURA-b.COBERTURA).map((m,i)=>{const sc=sem(m.COBERTURA);return(
            <tr key={m.MUNICIPIO} style={{background:i%2===0?"#fff":"#f8f9fa",borderBottom:"1px solid #dee2e6"}}>
              <td style={{padding:"8px 12px",fontWeight:500}}>{m.MUNICIPIO}</td>
              <td style={{padding:"8px 12px",textAlign:"right"}}>{Math.round(m.META_TOTAL).toLocaleString()}</td>
              <td style={{padding:"8px 12px",textAlign:"right"}}>{Math.round(m.DOSIS_12M).toLocaleString()}</td>
              <td style={{padding:"8px 12px",textAlign:"right"}}>{Math.round(m.DOSIS_18M).toLocaleString()}</td>
              <td style={{padding:"8px 12px",textAlign:"right"}}>{Math.round(m.DOSIS_6A).toLocaleString()}</td>
              <td style={{padding:"8px 12px",textAlign:"right"}}>{Math.round(m.DOSIS_10_49).toLocaleString()}</td>
              <td style={{padding:"8px 12px",textAlign:"right",fontWeight:700}}>{Math.round(m.TOTAL).toLocaleString()}</td>
              <td style={{padding:"8px 12px",textAlign:"center",fontWeight:700}}>{m.COBERTURA.toFixed(1)}%</td>
              <td style={{padding:"8px 12px",textAlign:"center"}}><span style={{background:sc.bg,color:sc.tx,padding:"3px 8px",borderRadius:10,fontSize:11,fontWeight:600}}>{sc.lb}</span></td>
            </tr>);})}</tbody>
        </table></div>
      </div>}
      {tab==="12m" && <Tabla muns={M} dk="DOSIS_12M" ck="COB_12M" pct={1.0}/>}
      {tab==="18m" && <Tabla muns={M} dk="DOSIS_18M" ck="COB_18M" pct={1.0}/>}
      {tab==="6a"  && <Tabla muns={M} dk="DOSIS_6A"  ck="COB_6A"  pct={0.5}/>}
      {tab==="adu" && <Tabla muns={M} dk="DOSIS_10_49" ck="COB_ADULT" pct={0.5}/>}
    </div>
    <div style={{textAlign:"center",padding:16,fontSize:11,color:"#adb5bd",borderTop:"1px solid #dee2e6"}}>Datos CeNSIA · Actualizacion automatica diaria · Durango Servicios de Salud</div>
  </div>);
};
export default App;
