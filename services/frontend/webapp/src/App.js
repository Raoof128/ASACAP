import { useEffect, useState } from 'react';
import './App.css';

const API_BASE = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

function App() {
  const [assets, setAssets] = useState([]);
  const [score, setScore] = useState(null);
  const [templates, setTemplates] = useState([]);
  const [incidentForm, setIncidentForm] = useState({
    title: '',
    description: '',
    severity: 'Medium',
    asset_id: '',
  });
  const [incidentResponse, setIncidentResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loadingIncident, setLoadingIncident] = useState(false);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [assetRes, scoreRes, templateRes] = await Promise.all([
          fetch(`${API_BASE}/assets`),
          fetch(`${API_BASE}/compliance/score`),
          fetch(`${API_BASE}/cirmp/templates`),
        ]);
        setAssets(await assetRes.json());
        setScore(await scoreRes.json());
        setTemplates(await templateRes.json());
      } catch (err) {
        setError('Unable to reach backend API. Ensure FastAPI is running.');
      }
    };
    loadData();
  }, []);

  const handleIncidentChange = (event) => {
    const { name, value } = event.target;
    setIncidentForm((current) => ({ ...current, [name]: value }));
  };

  const submitIncident = async (event) => {
    event.preventDefault();
    setLoadingIncident(true);
    setError(null);
    try {
      const created = await fetch(`${API_BASE}/incidents`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: incidentForm.title,
          description: incidentForm.description,
          severity: incidentForm.severity,
          asset_id: incidentForm.asset_id || null,
          evidence_bundle: ['screenshot.pdf'],
        }),
      }).then((res) => res.json());
      const report = await fetch(`${API_BASE}/incidents/${created.id}/report`, {
        method: 'POST',
      }).then((res) => res.json());
      setIncidentResponse(report);
      setIncidentForm({ title: '', description: '', severity: 'Medium', asset_id: '' });
    } catch (err) {
      setError('Incident workflow failed. Check API logs.');
    } finally {
      setLoadingIncident(false);
    }
  };

  return (
    <div className="App">
      <header>
        <h1>SOCI Compliance Control Room</h1>
        <p>Automate CIRMP, ACSC reporting, and IEC 62443 monitoring from one pane of glass.</p>
      </header>

      {error && <div className="alert">{error}</div>}

      <section className="grid">
        <article>
          <h2>Compliance score</h2>
          {score ? (
            <>
              <p className="score">{score.score}%</p>
              <p className="muted">Open issues: {score.open_issues}</p>
            </>
          ) : (
            <p className="muted">Loading...</p>
          )}
        </article>
        <article>
          <h2>Templates generated</h2>
          <p className="score">{templates.length}</p>
          <p className="muted">All-hazards coverage with IEC 62443 mapping.</p>
        </article>
        <article>
          <h2>Assets tracked</h2>
          <p className="score">{assets.length}</p>
          <p className="muted">Across energy, communications, finance, and more.</p>
        </article>
      </section>

      <section>
        <h2>Asset inventory</h2>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Sector</th>
              <th>Category</th>
              <th>Type</th>
              <th>Criticality</th>
            </tr>
          </thead>
          <tbody>
            {assets.map((asset) => (
              <tr key={asset.id}>
                <td>{asset.name}</td>
                <td>{asset.sector}</td>
                <td>{asset.category}</td>
                <td>{asset.asset_type}</td>
                <td>{asset.criticality}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section>
        <h2>CIRMP templates</h2>
        <div className="template-grid">
          {templates.map((template) => (
            <article key={template.id}>
              <h3>{template.asset_type}</h3>
              <p className="muted">Sector: {template.sector}</p>
              <ul>
                {template.controls.slice(0, 3).map((control) => (
                  <li key={control}>{control}</li>
                ))}
              </ul>
              <p className="muted">Review every {template.review_cadence_days} days</p>
            </article>
          ))}
        </div>
      </section>

      <section>
        <h2>Incident reporting</h2>
        <form onSubmit={submitIncident}>
          <label htmlFor="title">Title</label>
          <input id="title" name="title" value={incidentForm.title} onChange={handleIncidentChange} required />

          <label htmlFor="description">Description</label>
          <textarea id="description" name="description" value={incidentForm.description} onChange={handleIncidentChange} required />

          <label htmlFor="severity">Severity</label>
          <select id="severity" name="severity" value={incidentForm.severity} onChange={handleIncidentChange}>
            <option value="Critical">Critical</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>

          <label htmlFor="asset_id">Asset ID (optional)</label>
          <input id="asset_id" name="asset_id" value={incidentForm.asset_id} onChange={handleIncidentChange} placeholder="Paste asset UUID" />

          <button type="submit" disabled={loadingIncident}>
            {loadingIncident ? 'Submitting…' : 'Submit incident to ACSC mock'}
          </button>
        </form>
        {incidentResponse && (
          <pre aria-live="polite">{JSON.stringify(incidentResponse, null, 2)}</pre>
        )}
      </section>
    </div>
  );
}

export default App;
