import { useState, useEffect } from 'react'
import axios from 'axios'
import './Dashboard.css'

const API_URL = 'http://localhost:8000'

const CATEGORIES = ['Billing', 'Refund', 'Account Access', 'Cancellation', 'General Inquiry']

function Dashboard({ refreshTrigger }) {
  const [analytics, setAnalytics] = useState(null)
  const [traces, setTraces] = useState([])
  const [selectedCategory, setSelectedCategory] = useState(null)
  const [expandedTrace, setExpandedTrace] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
  }, [refreshTrigger, selectedCategory])

  const fetchData = async () => {
    setLoading(true)
    try {
      const [analyticsRes, tracesRes] = await Promise.all([
        axios.get(`${API_URL}/analytics`),
        axios.get(`${API_URL}/traces${selectedCategory ? `?category=${selectedCategory}` : ''}`)
      ])
      setAnalytics(analyticsRes.data)
      setTraces(tracesRes.data)
    } catch (error) {
      console.error('Error fetching data:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp)
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const truncate = (text, maxLength = 80) => {
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
  }

  if (loading && !analytics) {
    return <div className="dashboard-loading">Loading dashboard...</div>
  }

  return (
    <div className="dashboard">
      {/* Analytics Section */}
      <div className="analytics-section">
        <h2>📊 Analytics Overview</h2>
        
        <div className="analytics-cards">
          <div className="analytics-card primary">
            <div className="card-value">{analytics?.total_traces || 0}</div>
            <div className="card-label">Total Traces</div>
          </div>
          
          <div className="analytics-card">
            <div className="card-value">{analytics?.average_response_time?.toFixed(0) || 0}ms</div>
            <div className="card-label">Avg Response Time</div>
          </div>
        </div>

        <div className="category-breakdown">
          <h3>Category Breakdown</h3>
          <div className="category-cards">
            {CATEGORIES.map(category => {
              const data = analytics?.category_breakdown?.[category] || { count: 0, percentage: 0 }
              return (
                <div 
                  key={category} 
                  className={`category-card ${category.toLowerCase().replace(' ', '-')}`}
                >
                  <div className="category-name">{category}</div>
                  <div className="category-count">{data.count}</div>
                  <div className="category-percentage">{data.percentage}%</div>
                </div>
              )
            })}
          </div>
        </div>
      </div>

      {/* Traces Section */}
      <div className="traces-section">
        <div className="traces-header">
          <h2>📝 Conversation Traces</h2>
          <div className="traces-filters">
            <button 
              className={!selectedCategory ? 'active' : ''}
              onClick={() => setSelectedCategory(null)}
            >
              All
            </button>
            {CATEGORIES.map(category => (
              <button
                key={category}
                className={selectedCategory === category ? 'active' : ''}
                onClick={() => setSelectedCategory(category)}
              >
                {category}
              </button>
            ))}
          </div>
        </div>

        <div className="traces-table">
          {traces.length === 0 ? (
            <div className="traces-empty">
              No traces found. Try the chatbot to create some!
            </div>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>User Message</th>
                  <th>Bot Response</th>
                  <th>Category</th>
                  <th>Response Time</th>
                </tr>
              </thead>
              <tbody>
                {traces.map(trace => (
                  <>
                    <tr 
                      key={trace.id}
                      onClick={() => setExpandedTrace(expandedTrace === trace.id ? null : trace.id)}
                      className={expandedTrace === trace.id ? 'expanded' : ''}
                    >
                      <td className="timestamp">{formatTimestamp(trace.timestamp)}</td>
                      <td className="message">{truncate(trace.user_message)}</td>
                      <td className="message">{truncate(trace.bot_response)}</td>
                      <td>
                        <span className={`category-badge ${trace.category.toLowerCase().replace(' ', '-')}`}>
                          {trace.category}
                        </span>
                      </td>
                      <td className="response-time">{trace.response_time_ms}ms</td>
                    </tr>
                    {expandedTrace === trace.id && (
                      <tr className="trace-detail">
                        <td colSpan="5">
                          <div className="trace-detail-content">
                            <div className="trace-detail-section">
                              <strong>User Message:</strong>
                              <p>{trace.user_message}</p>
                            </div>
                            <div className="trace-detail-section">
                              <strong>Bot Response:</strong>
                              <p>{trace.bot_response}</p>
                            </div>
                          </div>
                        </td>
                      </tr>
                    )}
                  </>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  )
}

export default Dashboard
