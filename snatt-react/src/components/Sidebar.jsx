import './Sidebar.css'

export default function Sidebar({ activePanel, setActivePanel }) {
  const menuItems = [
    { id: 'discovery', name: 'Discovery', icon: '🔍' },
    { id: 'diagnostics', name: 'Diagnostics', icon: '🩺' },
    { id: 'backup', name: 'Backup', icon: '💾' },
    { id: 'reports', name: 'Reports', icon: '📊' },
    { id: 'settings', name: 'Settings', icon: '⚙️' },
  ]

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h1 className="sidebar-title">SNATT</h1>
        <p className="sidebar-subtitle">Network Automation Tool</p>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <button
            key={item.id}
            onClick={() => setActivePanel(item.id)}
            className={`sidebar-item ${activePanel === item.id ? 'active' : ''}`}
          >
            <span className="sidebar-icon">{item.icon}</span>
            <span>{item.name}</span>
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">
        <p>Version 1.0.0</p>
        <p>Web Edition</p>
      </div>
    </div>
  )
}
