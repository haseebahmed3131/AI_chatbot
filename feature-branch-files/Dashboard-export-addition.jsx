# Add this to frontend/src/components/Dashboard.jsx

// Add this function inside the Dashboard component, after fetchData:

const handleExport = () => {
  const url = `${API_URL}/traces/export${selectedCategory ? `?category=${selectedCategory}` : ''}`
  window.open(url, '_blank')
}

// Update the traces-header div to include the export button:

<div className="traces-header">
  <div className="traces-header-top">
    <h2>📝 Conversation Traces</h2>
    <button className="export-button" onClick={handleExport}>
      📥 Export CSV
    </button>
  </div>
  <div className="traces-filters">
    {/* existing filter buttons */}
  </div>
</div>
