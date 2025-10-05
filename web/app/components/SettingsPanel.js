'use client'

import { useState } from 'react'
import axios from 'axios'

export default function SettingsPanel() {
  const [credentials, setCredentials] = useState([])
  const [showAddForm, setShowAddForm] = useState(false)
  const [newCredential, setNewCredential] = useState({
    name: '',
    username: '',
    password: '',
    enable_password: ''
  })

  const handleAddCredential = async () => {
    try {
      await axios.post('/api/settings/credentials', newCredential)
      alert('Credential added successfully!')
      setShowAddForm(false)
      setNewCredential({ name: '', username: '', password: '', enable_password: '' })
      loadCredentials()
    } catch (error) {
      console.error('Failed to add credential:', error)
      alert('Failed to add credential: ' + error.message)
    }
  }

  const loadCredentials = async () => {
    try {
      const response = await axios.get('/api/settings/credentials')
      setCredentials(response.data.credentials || [])
    } catch (error) {
      console.error('Failed to load credentials:', error)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">⚙️ Settings</h2>
        <p className="text-gray-600">Configure application settings and credentials</p>
      </div>

      {/* Credentials Section */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-gray-800">Device Credentials</h3>
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            {showAddForm ? 'Cancel' : '+ Add Credential'}
          </button>
        </div>

        {/* Add Credential Form */}
        {showAddForm && (
          <div className="mb-6 p-4 bg-gray-50 rounded-lg space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Credential Name
              </label>
              <input
                type="text"
                value={newCredential.name}
                onChange={(e) => setNewCredential({ ...newCredential, name: e.target.value })}
                placeholder="e.g., cisco_lab"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Username
              </label>
              <input
                type="text"
                value={newCredential.username}
                onChange={(e) => setNewCredential({ ...newCredential, username: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <input
                type="password"
                value={newCredential.password}
                onChange={(e) => setNewCredential({ ...newCredential, password: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Enable Password (Optional)
              </label>
              <input
                type="password"
                value={newCredential.enable_password}
                onChange={(e) => setNewCredential({ ...newCredential, enable_password: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <button
              onClick={handleAddCredential}
              className="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            >
              Save Credential
            </button>
          </div>
        )}

        {/* Credentials List */}
        <div className="space-y-2">
          <button
            onClick={loadCredentials}
            className="text-sm text-blue-600 hover:text-blue-700"
          >
            Load Credentials
          </button>
          
          {credentials.length > 0 ? (
            <div className="space-y-2">
              {credentials.map((cred, index) => (
                <div key={index} className="p-3 bg-gray-50 rounded-lg flex justify-between items-center">
                  <div>
                    <p className="font-medium">{cred.name}</p>
                    <p className="text-sm text-gray-600">Username: {cred.username}</p>
                  </div>
                  <span className="text-xs text-green-600">✓ Saved</span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-sm">No credentials saved yet</p>
          )}
        </div>
      </div>

      {/* General Settings */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">General Settings</h3>
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <div>
              <p className="font-medium">Auto-refresh</p>
              <p className="text-sm text-gray-600">Automatically refresh device status</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" className="sr-only peer" />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>

          <div className="flex justify-between items-center">
            <div>
              <p className="font-medium">Dark Mode</p>
              <p className="text-sm text-gray-600">Enable dark theme</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" className="sr-only peer" />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>
        </div>
      </div>
    </div>
  )
}
