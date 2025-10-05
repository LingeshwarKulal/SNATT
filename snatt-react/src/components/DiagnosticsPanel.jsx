import { useState } from 'react'

export default function DiagnosticsPanel() {
  const [selectedWorkflow, setSelectedWorkflow] = useState('interface_health')
  const [running, setRunning] = useState(false)
  const [results, setResults] = useState([])

  const workflows = [
    { id: 'interface_health', name: 'Interface Health Check' },
    { id: 'cpu_memory', name: 'CPU & Memory Check' },
    { id: 'connectivity', name: 'Connectivity Check' },
    { id: 'log_analysis', name: 'Log Analysis' },
  ]

  const handleRunDiagnostics = () => {
    setRunning(true)
    // Simulate diagnostics
    setTimeout(() => {
      const mockResults = [
        {
          device_name: 'Router-01',
          device_ip: '192.168.1.1',
          severity: 'info',
          message: 'All interfaces operational',
          details: 'GigabitEthernet0/0: UP\nGigabitEthernet0/1: UP'
        },
        {
          device_name: 'Switch-01',
          device_ip: '192.168.1.2',
          severity: 'warning',
          message: 'High CPU usage detected',
          details: 'CPU: 85%\nMemory: 60%'
        }
      ]
      setResults(mockResults)
      setRunning(false)
    }, 2000)
  }

  return (
    <div>
      {/* Header */}
      <div className="panel">
        <div className="panel-header">
          <h2 className="panel-title">🩺 Diagnostics</h2>
          <p className="panel-subtitle">Run diagnostic workflows on connected devices</p>
        </div>
      </div>

      {/* Controls */}
      <div className="panel">
        <div className="form-group">
          <label className="form-label">Select Diagnostic Workflow</label>
          <select
            value={selectedWorkflow}
            onChange={(e) => setSelectedWorkflow(e.target.value)}
            className="form-select"
          >
            {workflows.map((workflow) => (
              <option key={workflow.id} value={workflow.id}>
                {workflow.name}
              </option>
            ))}
          </select>
        </div>

        <button
          onClick={handleRunDiagnostics}
          disabled={running}
          className="btn btn-primary"
        >
          {running ? 'Running Diagnostics...' : 'Run Diagnostics'}
        </button>
      </div>

      {/* Results */}
      {results.length > 0 && (
        <div>
          <h3 style={{ marginBottom: '1rem', fontSize: '1.125rem', fontWeight: '600' }}>
            Diagnostic Results
          </h3>
          {results.map((result, index) => (
            <div key={index} className={`diagnostic-result ${result.severity}`}>
              <div className="diagnostic-result-header">
                <h4 className="diagnostic-result-title">
                  {result.device_name} ({result.device_ip})
                </h4>
                <span className="diagnostic-result-severity">{result.severity}</span>
              </div>
              <p className="diagnostic-result-message">{result.message}</p>
              {result.details && (
                <pre className="diagnostic-result-details">{result.details}</pre>
              )}
            </div>
          ))}
        </div>
      )}

      {running && (
        <div className="alert alert-info">
          <p>Running diagnostics... Please wait.</p>
        </div>
      )}
    </div>
  )
}
