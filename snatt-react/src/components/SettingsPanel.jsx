import { useState } from 'react'

export default function SettingsPanel() {
  const [showAddForm, setShowAddForm] = useState(false)
  const [newCredential, setNewCredential] = useState({
    name: '',
    username: '',
    password: '',
    enable_password: ''
  })
  const [credentials, setCredentials] = useState([
    { name: 'cisco_lab', username: 'admin' },
    { name: 'switch_access', username: 'netadmin' },
  ])

  const handleAddCredential = () => {
    if (!newCredential.name || !newCredential.username || !newCredential.password) {
      alert('Please fill in all required fields')
      return
    }
    
    setCredentials([...credentials, { name: newCredential.name, username: newCredential.username }])
    setNewCredential({ name: '', username: '', password: '', enable_password: '' })
    setShowAddForm(false)
    alert('Credential added successfully!')
  }

  return (
    <div>
      {/* Header */}
      <div className="panel">
        <div className="panel-header">
          <h2 className="panel-title">⚙️ Settings</h2>
          <p className="panel-subtitle">Configure application settings and credentials</p>
        </div>
      </div>

      {/* Credentials Section */}
      <div className="panel">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <h3 style={{ fontSize: '1.125rem', fontWeight: '600' }}>Device Credentials</h3>
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="btn btn-primary"
          >
            {showAddForm ? 'Cancel' : '+ Add Credential'}
          </button>
        </div>

        {/* Add Credential Form */}
        {showAddForm && (
          <div style={{ marginBottom: '1.5rem', padding: '1rem', backgroundColor: '#f9fafb', borderRadius: '0.5rem' }}>
            <div className="form-group">
              <label className="form-label">Credential Name</label>
              <input
                type="text"
                value={newCredential.name}
                onChange={(e) => setNewCredential({ ...newCredential, name: e.target.value })}
                placeholder="e.g., cisco_lab"
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Username</label>
              <input
                type="text"
                value={newCredential.username}
                onChange={(e) => setNewCredential({ ...newCredential, username: e.target.value })}
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Password</label>
              <input
                type="password"
                value={newCredential.password}
                onChange={(e) => setNewCredential({ ...newCredential, password: e.target.value })}
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Enable Password (Optional)</label>
              <input
                type="password"
                value={newCredential.enable_password}
                onChange={(e) => setNewCredential({ ...newCredential, enable_password: e.target.value })}
                className="form-input"
              />
            </div>

            <button
              onClick={handleAddCredential}
              className="btn btn-success"
              style={{ width: '100%' }}
            >
              Save Credential
            </button>
          </div>
        )}

        {/* Credentials List */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          {credentials.length > 0 ? (
            credentials.map((cred, index) => (
              <div key={index} style={{ padding: '0.75rem', backgroundColor: '#f9fafb', borderRadius: '0.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <p style={{ fontWeight: '500' }}>{cred.name}</p>
                  <p style={{ fontSize: '0.875rem', color: '#6b7280' }}>Username: {cred.username}</p>
                </div>
                <span style={{ fontSize: '0.75rem', color: '#10b981' }}>✓ Saved</span>
              </div>
            ))
          ) : (
            <p style={{ color: '#6b7280', fontSize: '0.875rem' }}>No credentials saved yet</p>
          )}
        </div>
      </div>

      {/* General Settings */}
      <div className="panel">
        <h3 style={{ fontSize: '1.125rem', fontWeight: '600', marginBottom: '1rem' }}>General Settings</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <p style={{ fontWeight: '500' }}>Auto-refresh</p>
              <p style={{ fontSize: '0.875rem', color: '#6b7280' }}>Automatically refresh device status</p>
            </div>
            <input type="checkbox" />
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <p style={{ fontWeight: '500' }}>Dark Mode</p>
              <p style={{ fontSize: '0.875rem', color: '#6b7280' }}>Enable dark theme</p>
            </div>
            <input type="checkbox" />
          </div>
        </div>
      </div>
    </div>
  )
}
