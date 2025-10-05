import { useState } from 'react'

export default function BackupPanel() {
  const [backupType, setBackupType] = useState('running')
  const [backing, setBacking] = useState(false)
  const [backupHistory, setBackupHistory] = useState([
    { device_name: 'Router-01', type: 'running', timestamp: '2025-10-05 20:00', status: 'success' },
    { device_name: 'Switch-01', type: 'startup', timestamp: '2025-10-05 19:30', status: 'success' },
  ])

  const handleBackup = () => {
    setBacking(true)
    setTimeout(() => {
      alert('Backup completed successfully!')
      // Add new backup to history
      const newBackup = {
        device_name: 'Router-01',
        type: backupType,
        timestamp: new Date().toLocaleString(),
        status: 'success'
      }
      setBackupHistory([newBackup, ...backupHistory])
      setBacking(false)
    }, 2000)
  }

  return (
    <div>
      {/* Header */}
      <div className="panel">
        <div className="panel-header">
          <h2 className="panel-title">💾 Configuration Backup</h2>
          <p className="panel-subtitle">Backup device configurations</p>
        </div>
      </div>

      {/* Backup Controls */}
      <div className="panel">
        <div className="form-group">
          <label className="form-label">Configuration Type</label>
          <select
            value={backupType}
            onChange={(e) => setBackupType(e.target.value)}
            className="form-select"
          >
            <option value="running">Running Configuration</option>
            <option value="startup">Startup Configuration</option>
            <option value="both">Both Configurations</option>
          </select>
        </div>

        <button
          onClick={handleBackup}
          disabled={backing}
          className="btn btn-success"
        >
          {backing ? 'Creating Backup...' : 'Backup Now'}
        </button>
      </div>

      {/* Backup History */}
      <div className="panel">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <h3 style={{ fontSize: '1.125rem', fontWeight: '600' }}>Backup History</h3>
          <button className="btn btn-secondary">Refresh</button>
        </div>

        {backupHistory.length > 0 ? (
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Device</th>
                  <th>Type</th>
                  <th>Date</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {backupHistory.map((backup, index) => (
                  <tr key={index}>
                    <td>{backup.device_name}</td>
                    <td>{backup.type}</td>
                    <td>{backup.timestamp}</td>
                    <td>
                      <span className={`badge ${
                        backup.status === 'success' ? 'badge-success' : 'badge-danger'
                      }`}>
                        {backup.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p style={{ color: '#6b7280', textAlign: 'center', padding: '1rem' }}>
            No backup history available
          </p>
        )}
      </div>
    </div>
  )
}
