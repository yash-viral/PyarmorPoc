import React, { useState, useEffect } from 'react'

const API_BASE = 'http://127.0.0.1:8001'

export default function App() {
  const [licenseFile, setLicenseFile] = useState(null)
  const [licenseStatus, setLicenseStatus] = useState(null)
  const [availableAgents, setAvailableAgents] = useState([])
  const [selectedAgent, setSelectedAgent] = useState('')
  const [messages, setMessages] = useState([])
  const [currentMessage, setCurrentMessage] = useState('')
  const [status, setStatus] = useState(null)
  const [rateLimitInfo, setRateLimitInfo] = useState(null)

  const validateLicense = async () => {
    if (!licenseFile) {
      setStatus({ type: 'error', message: 'Please select a license file' })
      return
    }
    
    try {
      const formData = new FormData()
      formData.append('file', licenseFile)
      
      const response = await fetch(`${API_BASE}/upload-license`, {
        method: 'POST',
        body: formData
      })
      
      if (response.ok) {
        const result = await response.json()
        setLicenseStatus(result.license)
        setStatus({ type: 'success', message: 'License validated successfully!' })
        loadAvailableAgents()
      } else {
        const error = await response.json()
        setStatus({ type: 'error', message: error.detail })
      }
    } catch (error) {
      setStatus({ type: 'error', message: 'Failed to validate license file' })
    }
  }
  
  const checkExistingLicense = async () => {
    try {
      const response = await fetch(`${API_BASE}/validate-license-file`, {
        method: 'POST'
      })
      
      if (response.ok) {
        const result = await response.json()
        setLicenseStatus(result.license)
        setStatus({ type: 'success', message: 'Existing license file validated!' })
        loadAvailableAgents()
      } else {
        setStatus({ type: 'error', message: 'No valid license file found' })
      }
    } catch (error) {
      setStatus({ type: 'error', message: 'Failed to check existing license' })
    }
  }

  const loadAvailableAgents = async () => {
    try {
      const response = await fetch(`${API_BASE}/available-agents`)
      const result = await response.json()
      setAvailableAgents(result.agents)
      if (result.agents.length > 0) {
        setSelectedAgent(result.agents[0])
      }
    } catch (error) {
      console.error('Failed to load agents:', error)
    }
  }

  const sendMessage = async () => {
    if (!currentMessage.trim() || !selectedAgent) return

    const userMessage = { type: 'user', content: currentMessage }
    setMessages(prev => [...prev, userMessage])
    const messageToSend = currentMessage
    setCurrentMessage('')

    try {
      const response = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ agent: selectedAgent, message: messageToSend })
      })
      
      const result = await response.json()
      
      if (response.ok) {
        const agentMessage = { type: 'agent', content: result.response }
        setMessages(prev => [...prev, agentMessage])
        
        // Update rate limit info
        if (result.rate_limit_info) {
          setRateLimitInfo(result.rate_limit_info)
        }
      } else {
        setStatus({ type: 'error', message: result.detail })
        
        // Show specific error messages in chat
        if (result.detail.includes('expired')) {
          const errorMessage = { type: 'agent', content: `🚫 LICENSE EXPIRED: ${result.detail} Please upload a new license file.` }
          setMessages(prev => [...prev, errorMessage])
          // Clear license status to force re-upload
          setLicenseStatus(null)
        } else if (result.detail.includes('rate limit')) {
          const errorMessage = { type: 'agent', content: `⚠️ ${result.detail}` }
          setMessages(prev => [...prev, errorMessage])
        } else {
          const errorMessage = { type: 'agent', content: `❌ ${result.detail}` }
          setMessages(prev => [...prev, errorMessage])
        }
      }
    } catch (error) {
      setStatus({ type: 'error', message: 'Failed to send message' })
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage()
    }
  }

  return (
    <div className="container">
      <div className="header">
        <h1>🤖 PyArmor Protected AI Agent Chat</h1>
        <p>Upload your license file to access AI agents</p>
      </div>
      
      {licenseStatus && (
        <div className="license-info">
          <h3>📋 License Status</h3>
          <div className="license-details">
            <span className={`plan-badge plan-${licenseStatus.plan}`}>{licenseStatus.plan.toUpperCase()}</span>
            <span>Rate Limit: {licenseStatus.rate_limit}/min</span>
            <span>Agents: {licenseStatus.agents.length}</span>
            <span>Expires: {new Date(licenseStatus.expires_at).toLocaleDateString()}</span>
          </div>
        </div>
      )}

      <div className="license-section">
        <h3>Upload License File</h3>
        
        <input
          type="file"
          accept=".lic"
          onChange={(e) => setLicenseFile(e.target.files[0])}
          className="license-file-input"
        />
        
        <div className="license-buttons">
          <button className="btn btn-primary" onClick={validateLicense}>
            Upload & Validate License
          </button>
          <button className="btn btn-secondary" onClick={checkExistingLicense}>
            Check Existing License
          </button>
        </div>

        {status && (
          <div className={`status ${status.type}`}>
            {status.message}
          </div>
        )}

        {licenseStatus && (
          <div className="status success">
            <strong>License Valid!</strong><br/>
            Plan: {licenseStatus.plan}<br/>
            Agents: {licenseStatus.agents.join(', ')}<br/>
            Rate Limit: {licenseStatus.rate_limit}/min<br/>
            Expires: {new Date(licenseStatus.expires_at).toLocaleString()}
          </div>
        )}
      </div>

      {licenseStatus && (
        <div className="chat-section">
          <div className="agent-section">
            <h3>Select Agent (Licensed: {licenseStatus.agents.join(', ')})</h3>
            <div className="agents-grid">
              {['agent1', 'agent2', 'agent3', 'agent4'].map(agent => {
                const isLicensed = licenseStatus.agents.includes(agent)
                return (
                  <button
                    key={agent}
                    className={`agent-btn ${selectedAgent === agent ? 'selected' : ''} ${!isLicensed ? 'disabled' : ''}`}
                    onClick={() => isLicensed && setSelectedAgent(agent)}
                    disabled={!isLicensed}
                  >
                    {agent} {!isLicensed && '🔒'}
                  </button>
                )
              })}
            </div>
          </div>

          <div className="chat-header">
            <h3>Chat with {selectedAgent}</h3>
            {rateLimitInfo && (
              <div className="rate-limit-info">
                Requests: {rateLimitInfo.count}/{licenseStatus.rate_limit} per minute
              </div>
            )}
          </div>
          
          <div className="chat-messages">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.type}-message`}>
                <strong>{msg.type === 'user' ? 'You' : selectedAgent}:</strong> {msg.content}
              </div>
            ))}
          </div>

          <div className="chat-input">
            <input
              type="text"
              placeholder="Type your message..."
              value={currentMessage}
              onChange={(e) => setCurrentMessage(e.target.value)}
              onKeyPress={handleKeyPress}
            />
            <button className="btn btn-success" onClick={sendMessage}>
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  )
}