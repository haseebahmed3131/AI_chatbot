import { useState } from 'react'
import axios from 'axios'
import './Chatbot.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function Chatbot({ onNewTrace }) {
  const [message, setMessage] = useState('')
  const [conversation, setConversation] = useState([])
  const [loading, setLoading] = useState(false)

  const handleSend = async () => {
    if (!message.trim() || loading) return

    const userMessage = message.trim()
    setMessage('')
    setLoading(true)

    // Add user message to conversation
    setConversation(prev => [...prev, { role: 'user', content: userMessage }])

    try {
      const response = await axios.post(`${API_URL}/chat`, {
        message: userMessage
      })

      // Add bot response to conversation
      setConversation(prev => [...prev, { 
        role: 'bot', 
        content: response.data.bot_response,
        category: response.data.category
      }])

      // Notify parent that a new trace was created
      if (onNewTrace) {
        onNewTrace()
      }
    } catch (error) {
      console.error('Chat error:', error)
      setConversation(prev => [...prev, { 
        role: 'bot', 
        content: 'Sorry, I encountered an error. Please try again.',
        error: true
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="chatbot">
      <div className="chatbot-header">
        <h2>💬 BillFlow Support Chat</h2>
        <p>Ask me anything about billing, refunds, account access, or cancellations</p>
      </div>

      <div className="chatbot-messages">
        {conversation.length === 0 && (
          <div className="chatbot-welcome">
            <h3>Welcome to BillFlow Support! 👋</h3>
            <p>How can I help you today?</p>
            <div className="chatbot-suggestions">
              <button onClick={() => setMessage("Why was I charged twice?")}>
                Why was I charged twice?
              </button>
              <button onClick={() => setMessage("I can't log into my account")}>
                I can't log into my account
              </button>
              <button onClick={() => setMessage("How do I cancel my subscription?")}>
                How do I cancel my subscription?
              </button>
            </div>
          </div>
        )}

        {conversation.map((msg, idx) => (
          <div key={idx} className={`message message-${msg.role}`}>
            <div className="message-avatar">
              {msg.role === 'user' ? '👤' : '🤖'}
            </div>
            <div className="message-content">
              <div className="message-text">{msg.content}</div>
              {msg.category && (
                <div className="message-meta">
                  <span className={`category-badge ${msg.category.toLowerCase().replace(' ', '-')}`}>
                    {msg.category}
                  </span>
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="message message-bot">
            <div className="message-avatar">🤖</div>
            <div className="message-content">
              <div className="message-loading">
                <span></span><span></span><span></span>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="chatbot-input">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message..."
          rows="2"
          disabled={loading}
        />
        <button onClick={handleSend} disabled={!message.trim() || loading}>
          {loading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  )
}

export default Chatbot
