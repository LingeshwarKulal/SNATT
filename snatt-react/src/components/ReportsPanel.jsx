import { useState } from 'react'

export default function ReportsPanel() {
  const [reportType, setReportType] = useState('health')
  const [format, setFormat] = useState('xlsx')
  const [generating, setGenerating] = useState(false)

  const handleGenerateReport = () => {
    setGenerating(true)
    setTimeout(() => {
      alert(`${reportType} report generated in ${format} format!`)
      setGenerating(false)
    }, 2000)
  }

  return (
    <div>
      {/* Header */}
      <div className="panel">
        <div className="panel-header">
          <h2 className="panel-title">📊 Reports</h2>
          <p className="panel-subtitle">Generate comprehensive network reports</p>
        </div>
      </div>

      {/* Report Generation */}
      <div className="panel">
        <div className="form-group">
          <label className="form-label">Report Type</label>
          <select
            value={reportType}
            onChange={(e) => setReportType(e.target.value)}
            className="form-select"
          >
            <option value="health">Network Health Report</option>
            <option value="backup">Backup Status Report</option>
            <option value="diagnostics">Diagnostics Report</option>
            <option value="inventory">Device Inventory</option>
          </select>
        </div>

        <div className="form-group">
          <label className="form-label">Export Format</label>
          <select
            value={format}
            onChange={(e) => setFormat(e.target.value)}
            className="form-select"
          >
            <option value="xlsx">Excel (.xlsx)</option>
            <option value="pdf">PDF (.pdf)</option>
            <option value="csv">CSV (.csv)</option>
          </select>
        </div>

        <button
          onClick={handleGenerateReport}
          disabled={generating}
          className="btn btn-primary"
        >
          {generating ? 'Generating Report...' : 'Generate Report'}
        </button>
      </div>

      {/* Info Box */}
      <div className="alert alert-info">
        <h3 style={{ fontWeight: '600', marginBottom: '0.5rem' }}>Report Types:</h3>
        <ul style={{ marginLeft: '1.5rem', fontSize: '0.875rem' }}>
          <li><strong>Network Health:</strong> Overall device status and health metrics</li>
          <li><strong>Backup Status:</strong> Configuration backup history and status</li>
          <li><strong>Diagnostics:</strong> Detailed diagnostic results and issues</li>
          <li><strong>Device Inventory:</strong> Complete device list with details</li>
        </ul>
      </div>
    </div>
  )
}
