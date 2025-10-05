'use client'

import { useState } from 'react'
import Sidebar from './components/Sidebar'
import DiscoveryPanel from './components/DiscoveryPanel'
import DiagnosticsPanel from './components/DiagnosticsPanel'
import BackupPanel from './components/BackupPanel'
import ReportsPanel from './components/ReportsPanel'
import SettingsPanel from './components/SettingsPanel'

export default function Home() {
  const [activePanel, setActivePanel] = useState('discovery')

  const renderPanel = () => {
    switch (activePanel) {
      case 'discovery':
        return <DiscoveryPanel />
      case 'diagnostics':
        return <DiagnosticsPanel />
      case 'backup':
        return <BackupPanel />
      case 'reports':
        return <ReportsPanel />
      case 'settings':
        return <SettingsPanel />
      default:
        return <DiscoveryPanel />
    }
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar activePanel={activePanel} setActivePanel={setActivePanel} />
      <main className="flex-1 overflow-auto">
        <div className="container mx-auto p-6">
          {renderPanel()}
        </div>
      </main>
    </div>
  )
}
