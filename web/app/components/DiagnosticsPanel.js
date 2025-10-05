'use client'

import { useState } from 'react'
import axios from 'axios'

export default function DiagnosticsPanel() {
  const [devices, setDevices] = useState([])
  const [selectedWorkflow, setSelectedWorkflow] = useState('interface_health')
  const [running, setRunning] = useState(false)
  const [results, setResults] = useState([])

  const workflows = [
    { id: 'interface_health', name: 'Interface Health Check' },
    { id: 'cpu_memory', name: 'CPU & Memory Check' },
    { id: 'connectivity', name: 'Connectivity Check' },
    { id: 'log_analysis', name: 'Log Analysis' },
  ]

  const handleRunDiagnostics = async () => {
    setRunning(true)
    try {
      const response = await axios.post('/api/diagnostics/run', {
        workflow: selectedWorkflow
      })
      setResults(response.data.results || [])
    } catch (error) {
      console.error('Diagnostics error:', error)
      alert('Failed to run diagnostics: ' + error.message)
    } finally {
      setRunning(false)
    }
  }

  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'critical':
        return 'bg-red-100 text-red-800 border-red-300'
      case 'warning':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300'
      case 'info':
        return 'bg-blue-100 text-blue-800 border-blue-300'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300'
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">🩺 Diagnostics</h2>
        <p className="text-gray-600">Run diagnostic workflows on connected devices</p>
      </div>

      {/* Controls */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Diagnostic Workflow
            </label>
            <select
              value={selectedWorkflow}
              onChange={(e) => setSelectedWorkflow(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
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
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {running ? 'Running Diagnostics...' : 'Run Diagnostics'}
          </button>
        </div>
      </div>

      {/* Results */}
      {results.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-800">Diagnostic Results</h3>
          {results.map((result, index) => (
            <div
              key={index}
              className={`border rounded-lg p-4 ${getSeverityColor(result.severity)}`}
            >
              <div className="flex justify-between items-start mb-2">
                <h4 className="font-semibold">{result.device_name || result.device_ip}</h4>
                <span className="text-xs font-medium uppercase">{result.severity}</span>
              </div>
              <p className="text-sm mb-2">{result.message}</p>
              {result.details && (
                <div className="mt-2 text-xs bg-white bg-opacity-50 p-2 rounded">
                  <pre className="whitespace-pre-wrap">{result.details}</pre>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {running && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-center">
          <p className="text-blue-700">Running diagnostics... Please wait.</p>
        </div>
      )}
    </div>
  )
}
