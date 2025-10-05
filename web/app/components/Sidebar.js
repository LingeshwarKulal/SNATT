'use client'

export default function Sidebar({ activePanel, setActivePanel }) {
  const menuItems = [
    { id: 'discovery', name: 'Discovery', icon: '🔍' },
    { id: 'diagnostics', name: 'Diagnostics', icon: '🩺' },
    { id: 'backup', name: 'Backup', icon: '💾' },
    { id: 'reports', name: 'Reports', icon: '📊' },
    { id: 'settings', name: 'Settings', icon: '⚙️' },
  ]

  return (
    <div className="w-64 bg-gray-900 text-white flex flex-col">
      {/* Logo/Header */}
      <div className="p-6 border-b border-gray-700">
        <h1 className="text-2xl font-bold text-blue-400">SNATT</h1>
        <p className="text-sm text-gray-400">Network Automation Tool</p>
      </div>

      {/* Menu Items */}
      <nav className="flex-1 p-4">
        {menuItems.map((item) => (
          <button
            key={item.id}
            onClick={() => setActivePanel(item.id)}
            className={`w-full text-left px-4 py-3 rounded-lg mb-2 flex items-center gap-3 transition-colors ${
              activePanel === item.id
                ? 'bg-blue-600 text-white'
                : 'hover:bg-gray-800 text-gray-300'
            }`}
          >
            <span className="text-xl">{item.icon}</span>
            <span>{item.name}</span>
          </button>
        ))}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-gray-700 text-sm text-gray-400">
        <p>Version 1.0.0</p>
        <p>Web Edition</p>
      </div>
    </div>
  )
}
