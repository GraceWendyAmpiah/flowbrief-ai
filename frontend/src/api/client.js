const BASE = import.meta.env.VITE_API_URL

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw Object.assign(
      new Error(err.error || `HTTP ${res.status}`),
      { code: err.code, status: res.status }
    )
  }
  return res.json()
}

export async function processDocument(formData) {
  const res = await fetch(`${BASE}/api/process`, {
    method: 'POST',
    body: formData,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw Object.assign(
      new Error(err.error || `HTTP ${res.status}`),
      { code: err.code, status: res.status }
    )
  }
  return res.json()
}

export const getCase = (id) =>
  request(`/api/cases/${id}`)

export const listCases = (params = {}) => {
  const qs = new URLSearchParams(
    Object.entries(params)
      .filter(([, v]) => v !== '' && v != null)
  ).toString()
  return request(`/api/cases${qs ? `?${qs}` : ''}`)
}

export const getDashboard = () =>
  request('/api/dashboard')
