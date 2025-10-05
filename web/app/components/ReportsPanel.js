'use client'

import { useState } from 'react'
import axios from 'axios'

export default function ReportsPanel() {
  const [reportType, setReportType] = useState('health')
  const [format, setFormat] = useState('xlsx')
  const [generating, setGenerating] = useState(false)

  const handleGenerateReport = async () => {
    setGenerating(true)
    try {
      const response = await axios.post('/api/reports/generate', {
        report_type: reportType,
        format: format
      }, {
        responseType: 'blob'
      })

      // Download the file
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `snatt_report_${Date.now()}.${format}`)
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (error) {
      console.error('Report generation error:', error)
      alert('Failed to generate report: ' + error.message)
    } finally {
      setGenerating(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">📊 Reports</h2>
        <p className="text-gray-600">Generate comprehensive network reports</p>
      </div>

      {/* Report Generation */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Report Type
            </label>
            <select
              value={reportType}
              onChange={(e) => setReportType(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="health">Network Health Report</option>
              <option value="backup">Backup Status Report</option>
              <option value="diagnostics">Diagnostics Report</option>
              <option value="inventory">Device Inventory</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Export Format
            </label>
            <select
              value={format}
              onChange={(e) => setFormat(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="xlsx">Excel (.xlsx)</option>
              <option value="pdf">PDF (.pdf)</option>
              <option value="csv">CSV (.csv)</option>
            </select>
          </div>

          <button
            onClick={handleGenerateReport}
            disabled={generating}
            className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {generating ? 'Generating Report...' : 'Generate Report'}
          </button>
        </div>
      </div>

      {/* Info Box */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="font-semibold text-blue-900 mb-2">Report Types:</h3>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• <strong>Network Health:</strong> Overall device status and health metrics</li>
          <li>• <strong>Backup Status:</strong> Configuration backup history and status</li>
          <li>• <strong>Diagnostics:</strong> Detailed diagnostic results and issues</li>
          <li>• <strong>Device Inventory:</strong> Complete device list with details</li>
        </ul>
      </div>
    </div>
  )
}
