import { useState } from 'react'
import axios from 'axios'

export default function DiscoveryPanel() {
  const [ipRange, setIpRange] = useState('')
  const [scanning, setScanning] = useState(false)
  const [devices, setDevices] = useState([])
  const [selectedDevices, setSelectedDevices] = useState([])

  const handleScan = async () => {
    setScanning(true)
    try {
      // Simulate API call - replace with real endpoint
      setTimeout(() => {
        const mockDevices = [
          { id: '1', ip_address: '192.168.1.1', hostname: 'Router-01', vendor: 'Cisco', status: 'reachable' },
          { id: '2', ip_address: '192.168.1.2', hostname: 'Switch-01', vendor: 'Cisco', status: 'reachable' },
          { id: '3', ip_address: '192.168.1.3', hostname: 'Switch-02', vendor: 'Arista', status: 'reachable' },
        ]
        setDevices(mockDevices)
        setScanning(false)
      }, 2000)
    } catch (error) {
      console.error('Scan error:', error)
      alert('Failed to scan network: ' + error.message)
      setScanning(false)
    }
  }

  const handleConnect = () => {
    if (selectedDevices.length === 0) {
      alert('Please select devices to connect')
      return
    }
    
    // Update device status to connected
    setDevices(devices.map(device =>
      selectedDevices.includes(device.id)
        ? { ...device, status: 'connected' }
        : device
    ))
    alert(`Connected to ${selectedDevices.length} device(s)`)
  }

  const toggleDeviceSelection = (deviceId) => {
    setSelectedDevices(prev =>
      prev.includes(deviceId)
        ? prev.filter(id => id !== deviceId)
        : [...prev, deviceId]
    )
  }

  const toggleAllDevices = (e) => {
    setSelectedDevices(e.target.checked ? devices.map(d => d.id) : [])
  }

  return (
    <div>
      {/* Header */}
      <div className="panel">
        <div className="panel-header">
          <h2 className="panel-title">🔍 Network Discovery</h2>
          <p className="panel-subtitle">Scan your network to discover devices</p>
        </div>
      </div>

      {/* Scan Controls */}
      <div className="panel">
        <div className="form-group">
          <label className="form-label">IP Range or Subnet</label>
          <input
            type="text"
            value={ipRange}
            onChange={(e) => setIpRange(e.target.value)}
            placeholder="e.g., 192.168.1.0/24 or 192.168.1.1-192.168.1.50"
            className="form-input"
          />
        </div>

        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <button
            onClick={handleScan}
            disabled={scanning || !ipRange}
            className="btn btn-primary"
          >
            {scanning ? 'Scanning...' : 'Scan Network'}
          </button>
          
          <button
            onClick={handleConnect}
            disabled={selectedDevices.length === 0}
            className="btn btn-success"
          >
            Connect Selected ({selectedDevices.length})
          </button>
        </div>
      </div>

      {/* Devices Table */}
      {devices.length > 0 && (
        <div className="panel">
          <h3 style={{ marginBottom: '1rem', fontSize: '1.125rem', fontWeight: '600' }}>
            Discovered Devices
          </h3>
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th style={{ width: '50px' }}>
                    <input
                      type="checkbox"
                      onChange={toggleAllDevices}
                      checked={selectedDevices.length === devices.length && devices.length > 0}
                    />
                  </th>
                  <th>IP Address</th>
                  <th>Hostname</th>
                  <th>Vendor</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {devices.map((device) => (
                  <tr key={device.id}>
                    <td>
                      <input
                        type="checkbox"
                        checked={selectedDevices.includes(device.id)}
                        onChange={() => toggleDeviceSelection(device.id)}
                      />
                    </td>
                    <td>{device.ip_address}</td>
                    <td>{device.hostname || '-'}</td>
                    <td>{device.vendor || 'Unknown'}</td>
                    <td>
                      <span className={`badge ${
                        device.status === 'connected' ? 'badge-success' :
                        device.status === 'reachable' ? 'badge-info' :
                        'badge-gray'
                      }`}>
                        {device.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {scanning && (
        <div className="alert alert-info">
          <p>Scanning network... This may take a few moments.</p>
        </div>
      )}
    </div>
  )
}
