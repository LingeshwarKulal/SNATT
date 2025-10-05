'use client'

import { useState } from 'react'
import axios from 'axios'

export default function BackupPanel() {
  const [backupType, setBackupType] = useState('running')
  const [backing, setBacking] = useState(false)
  const [backupHistory, setBackupHistory] = useState([])

  const handleBackup = async () => {
    setBacking(true)
    try {
      const response = await axios.post('/api/backup/create', {
        backup_type: backupType
      })
      alert('Backup completed successfully!')
      // Refresh backup history
      loadBackupHistory()
    } catch (error) {
      console.error('Backup error:', error)
      alert('Failed to create backup: ' + error.message)
    } finally {
      setBacking(false)
    }
  }

  const loadBackupHistory = async () => {
    try {
      const response = await axios.get('/api/backup/history')
      setBackupHistory(response.data.backups || [])
    } catch (error) {
      console.error('Failed to load backup history:', error)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">💾 Configuration Backup</h2>
        <p className="text-gray-600">Backup device configurations</p>
      </div>

      {/* Backup Controls */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Configuration Type
            </label>
            <select
              value={backupType}
              onChange={(e) => setBackupType(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="running">Running Configuration</option>
              <option value="startup">Startup Configuration</option>
              <option value="both">Both Configurations</option>
            </select>
          </div>

          <button
            onClick={handleBackup}
            disabled={backing}
            className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {backing ? 'Creating Backup...' : 'Backup Now'}
          </button>
        </div>
      </div>

      {/* Backup History */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-gray-800">Backup History</h3>
          <button
            onClick={loadBackupHistory}
            className="px-4 py-2 text-sm bg-gray-200 hover:bg-gray-300 rounded-lg transition-colors"
          >
            Refresh
          </button>
        </div>

        {backupHistory.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Device</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {backupHistory.map((backup, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm text-gray-900">{backup.device_name}</td>
                    <td className="px-6 py-4 text-sm text-gray-900">{backup.type}</td>
                    <td className="px-6 py-4 text-sm text-gray-900">{backup.timestamp}</td>
                    <td className="px-6 py-4 text-sm">
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        backup.status === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
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
          <p className="text-gray-500 text-center py-4">No backup history available</p>
        )}
      </div>
    </div>
  )
}
