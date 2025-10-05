import { useState } from 'react'
import './App.css'
import Sidebar from './components/Sidebar'
import DiscoveryPanel from './components/DiscoveryPanel'
import DiagnosticsPanel from './components/DiagnosticsPanel'
import BackupPanel from './components/BackupPanel'
import ReportsPanel from './components/ReportsPanel'
import SettingsPanel from './components/SettingsPanel'

function App() {
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
    <div className="app-container">
      <Sidebar activePanel={activePanel} setActivePanel={setActivePanel} />
      <main className="main-content">
        <div className="content-wrapper">
          {renderPanel()}
        </div>
      </main>
    </div>
  )
}

export default App
