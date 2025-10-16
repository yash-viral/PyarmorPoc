import React, { useState } from 'react'

// Default to backend at 127.0.0.1:8000. You can override by setting VITE_API in .env (e.g. VITE_API=http://127.0.0.1:8000)
const API_ORIGIN = (import.meta.env.VITE_API) ? String(import.meta.env.VITE_API) : 'http://127.0.0.1:8000'
const API_BASE = `${API_ORIGIN.replace(/\/$/, '')}/api/licenses`

const PLANS = {
  1: { name: 'starter', rate_limit: 2, max_agents: 2, color: '#4CAF50' },
  2: { name: 'growth', rate_limit: 5, max_agents: 3, color: '#2196F3' },
  3: { name: 'pro', rate_limit: 15, max_agents: 4, color: '#FF9800' },
  4: { name: 'enterprise', rate_limit: 50, max_agents: 4, color: '#9C27B0' }
}

const AGENTS = ['agent1', 'agent2', 'agent3', 'agent4']

export default function App(){
  const [userId, setUserId] = useState(1)
  const [planId, setPlanId] = useState(1)
  const [selectedAgents, setSelectedAgents] = useState(['agent1', 'agent2'])
  const [duration, setDuration] = useState(10)
  const [issueResult, setIssueResult] = useState(null)


  const [lastLicense, setLastLicense] = useState(null)
  const [licenseMeta, setLicenseMeta] = useState(null)

  async function issueLicense(e){
    e && e.preventDefault()
    setIssueResult('Issuing...')
    // include both numeric plan_id and string plan to satisfy different backend schemas
    const plan = PLANS[Number(planId)]
    const payload = {
      user_id: Number(userId),
      plan_id: Number(planId),
      plan: plan.name,
      agents: selectedAgents,
      duration_days: Number(duration),
      machine_id: null
    }
    try{
      const res = await fetch(API_BASE + '/', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(payload)
      })

      const ct = res.headers.get('content-type') || ''
      let data = null
      let text = null
      try{
        if(ct.includes('application/json')){
          data = await res.json()
        } else {
          text = await res.text()
          if(text){
            try{ data = JSON.parse(text) }catch(e){ /* keep text as fallback */ }
          }
        }
      }catch(err){
        setIssueResult({ error: 'Invalid JSON response: ' + err.message })
        return
      }

      if(!res.ok){
        let detail = data?.detail ?? data?.error ?? text ?? JSON.stringify(data)
        // if server returned an empty string as error, provide a fallback
        const finalError = (detail && String(detail).trim()) ? detail : `HTTP ${res.status} ${res.statusText}`
        setIssueResult({ error: finalError })
        return
      }

      const licenseData = data?.license_data ?? data ?? (text || null)
      setLastLicense(licenseData)
      // capture metadata if response contains it
      if(data && (data.license_key || data.plan_name || data.user_email || data.expires_at)){
        setLicenseMeta({
          license_key: data.license_key,
          plan_name: data.plan_name,
          user_email: data.user_email,
          expires_at: data.expires_at
        })
      }
      setIssueResult({ success: licenseData })
    }catch(err){
      setIssueResult({ error: err.message })
    }
  }



  function testAgent(agentName){
    setAgentResult(`Testing ${agentName}...`)
    // Simulate agent response
    setTimeout(() => {
      setAgentResult({ success: `Hello I am ${agentName}` })
    }, 500)
  }

  function downloadLicense(){
    if(!licenseMeta?.license_key) return alert('No license key available')
    // Download PyArmor license file
    const downloadUrl = `${API_BASE}/download/${licenseMeta.license_key}`
    const a = document.createElement('a')
    a.href = downloadUrl
    a.download = `${licenseMeta.license_key}.lic`
    document.body.appendChild(a)
    a.click()
    a.remove()
  }
  


  const handleAgentToggle = (agent) => {
    const plan = PLANS[planId]
    if (selectedAgents.includes(agent)) {
      setSelectedAgents(selectedAgents.filter(a => a !== agent))
    } else if (selectedAgents.length < plan.max_agents) {
      setSelectedAgents([...selectedAgents, agent])
    }
  }

  return (
    <div className="container">
      <h1>🔐 PyArmor Subscription Server</h1>
      
      <div className="card">
        <h2>Select Your Plan</h2>
        <div className="plans-grid">
          {Object.entries(PLANS).map(([id, plan]) => (
            <div 
              key={id} 
              className={`plan-card ${planId == id ? 'selected' : ''}`}
              onClick={() => setPlanId(Number(id))}
              style={{borderColor: plan.color}}
            >
              <h3 style={{color: plan.color}}>{plan.name.toUpperCase()}</h3>
              <div className="plan-details">
                <div>Rate: {plan.rate_limit}/min</div>
                <div>Max Agents: {plan.max_agents}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="card">
        <h2>Configure License</h2>
        <form onSubmit={issueLicense}>
          <div className="form-group">
            <label>Select Agents (Max {PLANS[planId].max_agents}):</label>
            <div className="agents-grid">
              {AGENTS.map(agent => (
                <label key={agent} className="agent-checkbox">
                  <input
                    type="checkbox"
                    checked={selectedAgents.includes(agent)}
                    onChange={() => handleAgentToggle(agent)}
                    disabled={!selectedAgents.includes(agent) && selectedAgents.length >= PLANS[planId].max_agents}
                  />
                  {agent}
                </label>
              ))}
            </div>
          </div>
          
          <div className="form-group">
            <label>Duration: 
              <select value={duration} onChange={e=>setDuration(e.target.value)}>
                <option value="0.0014">2 minutes (testing)</option>
                <option value="1">1 day</option>
                <option value="7">7 days</option>
                <option value="10">10 days</option>
                <option value="30">30 days</option>
                <option value="90">90 days</option>
                <option value="365">365 days</option>
              </select>
            </label>
          </div>
          
          <div className="actions">
            <button type="submit" disabled={selectedAgents.length === 0}>Generate License</button>
          </div>
        </form>
        <ResultBox value={issueResult} />
        {licenseMeta && (
          <div style={{marginTop:12}}>
            <strong>License key:</strong> <code>{licenseMeta.license_key}</code>
            <button onClick={() => navigator.clipboard.writeText(licenseMeta.license_key)}>Copy Key</button><br />
            <strong>Plan:</strong> {licenseMeta.plan_name} &nbsp; <strong>User:</strong> {licenseMeta.user_email}<br />
            <strong>Expires:</strong> {licenseMeta.expires_at}<br/>

            <div style={{marginTop: '10px'}}>
              <button onClick={downloadLicense}>Download License File</button>
            </div>
          </div>
        )}
      </div>




      <footer>API: <code>{API_BASE}</code></footer>
    </div>
  )
}

function ResultBox({value}){
  if(value === null) return null
  if(typeof value === 'string') return <div className="result">{value}</div>
  if(value.error) return <pre className="result error">Error: {typeof value.error === 'string' ? value.error : JSON.stringify(value.error)}</pre>
  return <pre className="result">{JSON.stringify(value.success || value, null, 2)}</pre>
}
