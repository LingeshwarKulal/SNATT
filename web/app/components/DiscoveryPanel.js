'use client'

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
      const response = await axios.post('/api/discovery/scan', { ip_range: ipRange })
      setDevices(response.data.devices || [])
    } catch (error) {
      console.error('Scan error:', error)
      alert('Failed to scan network: ' + error.message)
    } finally {
      setScanning(false)
    }
  }

  const handleConnect = async () => {
    if (selectedDevices.length === 0) {
      alert('Please select devices to connect')
      return
    }
    
    try {
      const response = await axios.post('/api/discovery/connect', { 
        device_ids: selectedDevices 
      })
      alert('Connected to ' + response.data.connected + ' devices')
      // Refresh device list
      handleScan()
    } catch (error) {
      console.error('Connect error:', error)
      alert('Failed to connect: ' + error.message)
    }
  }

  const toggleDeviceSelection = (deviceId) => {
    setSelectedDevices(prev =>
      prev.includes(deviceId)
        ? prev.filter(id => id !== deviceId)
        : [...prev, deviceId]
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">🔍 Network Discovery</h2>
        <p className="text-gray-600">Scan your network to discover devices</p>
      </div>

      {/* Scan Controls */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              IP Range or Subnet
            </label>
            <input
              type="text"
              value={ipRange}
              onChange={(e) => setIpRange(e.target.value)}
              placeholder="e.g., 192.168.1.0/24 or 192.168.1.1-192.168.1.50"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div className="flex gap-3">
            <button
              onClick={handleScan}
              disabled={scanning || !ipRange}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              {scanning ? 'Scanning...' : 'Scan Network'}
            </button>
            
            <button
              onClick={handleConnect}
              disabled={selectedDevices.length === 0}
              className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              Connect Selected ({selectedDevices.length})
            </button>
          </div>
        </div>
      </div>

      {/* Devices Table */}
      {devices.length > 0 && (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  <input
                    type="checkbox"
                    onChange={(e) =>
                      setSelectedDevices(e.target.checked ? devices.map(d => d.id) : [])
                    }
                    className="rounded"
                  />
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">IP Address</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Hostname</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Vendor</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {devices.map((device) => (
                <tr key={device.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <input
                      type="checkbox"
                      checked={selectedDevices.includes(device.id)}
                      onChange={() => toggleDeviceSelection(device.id)}
                      className="rounded"
                    />
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">{device.ip_address}</td>
                  <td className="px-6 py-4 text-sm text-gray-900">{device.hostname || '-'}</td>
                  <td className="px-6 py-4 text-sm text-gray-900">{device.vendor || 'Unknown'}</td>
                  <td className="px-6 py-4 text-sm">
                    <span className={`px-2 py-1 rounded-full text-xs ${
                      device.status === 'connected' ? 'bg-green-100 text-green-800' :
                      device.status === 'reachable' ? 'bg-blue-100 text-blue-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {device.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {scanning && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-center">
          <p className="text-blue-700">Scanning network... This may take a few moments.</p>
        </div>
      )}
    </div>
  )
}
