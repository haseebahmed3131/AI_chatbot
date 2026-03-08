import { useState } from 'react'
import Chatbot from './components/Chatbot'
import Dashboard from './components/Dashboard'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [refreshTrigger, setRefreshTrigger] = useState(0)

  const handleNewTrace = () => {
    setRefreshTrigger(prev => prev + 1)
    setActiveTab('dashboard')
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🔍 SupportLens</h1>
        <p>Customer Support Chatbot Observability Platform</p>
      </header>

      <nav className="app-nav">
        <button 
          className={activeTab === 'dashboard' ? 'active' : ''}
          onClick={() => setActiveTab('dashboard')}
        >
          Dashboard
        </button>
        <button 
          className={activeTab === 'chatbot' ? 'active' : ''}
          onClick={() => setActiveTab('chatbot')}
        >
          Chatbot
        </button>
      </nav>

      <main className="app-main">
        {activeTab === 'dashboard' && <Dashboard refreshTrigger={refreshTrigger} />}
        {activeTab === 'chatbot' && <Chatbot onNewTrace={handleNewTrace} />}
      </main>
    </div>
  )
}

export default App
