import React, { useState, useEffect } from 'react';
import { LayoutDashboard } from 'lucide-react';
import './styles/dashboard.css';

interface MuniData {
  MUNICIPIO: string;
  META_TOTAL: number;
  TOTAL: number;
  DOSIS_12M: number;
  DOSIS_18M: number;
  DOSIS_6A: number;
  DOSIS_10_49: number;
  COB_12M: number;
  COB_18M: number;
  COB_6A: number;
  COB_ADULT: number;
  COBERTURA: number;
  SEMAFORO: string;
}

interface DashboardState {
  corte: string;
  semana: number;
  generado: string;
  municipios: MuniData[];
}

const App: React.FC = () => {
  const [data, setData] = useState<DashboardState | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('data.json')
      .then(res => res.json())
      .then(d => {
        setData(d as DashboardState);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching data:', err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="dashboard-container">
      <aside className="sidebar">
        <h2 style={{ fontSize: '0.8rem', color: 'var(--accent-gold)' }}>V4.0 SAFE - ESTÁTICO</h2>
        <nav style={{ marginTop: '2rem' }}>
          <div className="nav-item active"><LayoutDashboard size={18} /> Dashboard</div>
        </nav>
      </aside>

      <main className="main-content">
        <header className="header">
          <h1>COBERTURAS <span style={{ color: 'var(--accent-gold)' }}>SARAMPION</span></h1>
          <div style={{ color: '#aaa', fontSize: '0.9rem' }}>
            {data ? `Corte: ${data.corte} - Semana ${data.semana}` : 'Cargando...'}
          </div>
        </header>

        {loading ? (
          <div className="card" style={{ padding: '3rem', textAlign: 'center' }}>
            <h3>Cargando datos de campañas...</h3>
          </div>
        ) : !data ? (
          <div className="card" style={{ padding: '3rem', textAlign: 'center', color: 'red' }}>
            <h3>Error al cargar los datos</h3>
          </div>
        ) : (
          <div className="table-card">
            <div className="table-container large">
              <table className="excel-table">
                <thead>
                  <tr>
                    <th className="sticky-col">MUNICIPIO</th>
                    <th>META GLOBAL</th>
                    <th>DOSIS 12M</th>
                    <th>DOSIS 18M</th>
                    <th>DOSIS 6A</th>
                    <th>DOSIS ADULTOS</th>
                    <th>TOTAL APLICADO</th>
                    <th>COBERTURA %</th>
                    <th>SEMÁFORO</th>
                  </tr>
                </thead>
                <tbody>
                  {data.municipios.map((r, i) => (
                    <tr key={i}>
                      <td className="sticky-col">{r.MUNICIPIO}</td>
                      <td>{Math.round(r.META_TOTAL).toLocaleString()}</td>
                      <td>{Math.round(r.DOSIS_12M).toLocaleString()}</td>
                      <td>{Math.round(r.DOSIS_18M).toLocaleString()}</td>
                      <td>{Math.round(r.DOSIS_6A).toLocaleString()}</td>
                      <td>{Math.round(r.DOSIS_10_49).toLocaleString()}</td>
                      <td>{Math.round(r.TOTAL).toLocaleString()}</td>
                      <td>{typeof r.COBERTURA === 'number' ? r.COBERTURA.toFixed(1) : r.COBERTURA}%</td>
                      <td>{r.SEMAFORO}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default App;
