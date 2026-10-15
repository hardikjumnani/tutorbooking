import React, { useEffect, useState } from 'react'
import { createRoot } from 'react-dom/client'
import './styles.css'

const API = '/api'
const STATUSES = ['BOOKED', 'CONFIRMED', 'CANCELLED', 'DONE']

// Turn an ISO time string into something easy to read.
function formatTime(value) {
  if (!value) return ''
  const d = new Date(value)
  if (isNaN(d)) return value
  return d.toLocaleString([], {
    dateStyle: 'medium',
    timeStyle: 'short',
  })
}

function App() {
  const [appointments, setAppointments] = useState([])
  const [stats, setStats] = useState({ total: 0, booked: 0, confirmed: 0, cancelled: 0, done: 0 })
  const [filter, setFilter] = useState('ALL')
  const [showForm, setShowForm] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  // Load appointments and the summary counts from the backend.
  const load = async () => {
    try {
      setError('')
      const [list, summary] = await Promise.all([
        fetch(`${API}/appointments`),
        fetch(`${API}/appointments/stats`),
      ])
      if (!list.ok || !summary.ok) throw new Error('Backend not reachable')
      setAppointments(await list.json())
      setStats(await summary.json())
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const visible = filter === 'ALL'
    ? appointments
    : appointments.filter((a) => a.status === filter)

  // Create a new appointment from the form fields.
  const createAppointment = async (e) => {
    e.preventDefault()
    const f = new FormData(e.currentTarget)
    const payload = {
      student_name: f.get('student_name'),
      tutor: f.get('tutor'),
      subject: f.get('subject'),
      class_time: f.get('class_time'),
      notes: f.get('notes') || '',
      status: 'BOOKED',
    }
    const res = await fetch(`${API}/appointments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
    if (res.ok) {
      e.currentTarget.reset()
      setShowForm(false)
      load()
    } else {
      setError('Could not create the appointment')
    }
  }

  const changeStatus = async (appt, status) => {
    await fetch(`${API}/appointments/${appt.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status }),
    })
    load()
  }

  const remove = async (appt) => {
    await fetch(`${API}/appointments/${appt.id}`, { method: 'DELETE' })
    load()
  }

  return (
    <div className="page">
      <header className="topbar">
        <div className="brand">
          <span className="brand-mark">TS</span>
          <div>
            <b>TutorSlot</b>
            <small>Tutoring appointment booking</small>
          </div>
        </div>
        <button className="primary" onClick={() => setShowForm(true)}>＋ Book appointment</button>
      </header>

      <main className="content">
        <div className="intro">
          <h1>Appointments</h1>
          <p className="muted">Book and track tutoring sessions in one place.</p>
        </div>

        {error && (
          <div className="alert">⚠ {error}. Start the backend, then refresh the page.</div>
        )}

        <section className="stats">
          <Stat label="Total" value={stats.total} />
          <Stat label="Booked" value={stats.booked} tone="booked" />
          <Stat label="Confirmed" value={stats.confirmed} tone="confirmed" />
          <Stat label="Done" value={stats.done} tone="done" />
        </section>

        <section className="panel">
          <div className="panel-head">
            <h2>All sessions</h2>
            <div className="filters">
              {['ALL', ...STATUSES].map((s) => (
                <button
                  key={s}
                  className={filter === s ? 'chip selected' : 'chip'}
                  onClick={() => setFilter(s)}
                >
                  {s === 'ALL' ? 'All' : s.charAt(0) + s.slice(1).toLowerCase()}
                </button>
              ))}
            </div>
          </div>

          {loading ? (
            <div className="empty">Loading…</div>
          ) : (
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Student</th>
                    <th>Tutor</th>
                    <th>Subject</th>
                    <th>Class time</th>
                    <th>Status</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  {visible.map((a) => (
                    <tr key={a.id}>
                      <td><b>{a.student_name}</b></td>
                      <td>{a.tutor}</td>
                      <td>{a.subject}</td>
                      <td>{formatTime(a.class_time)}</td>
                      <td>
                        <span className={`status ${a.status.toLowerCase()}`}>
                          {a.status.charAt(0) + a.status.slice(1).toLowerCase()}
                        </span>
                      </td>
                      <td className="row-actions">
                        <select
                          value={a.status}
                          onChange={(e) => changeStatus(a, e.target.value)}
                          title="Change status"
                        >
                          {STATUSES.map((s) => (
                            <option key={s} value={s}>{s}</option>
                          ))}
                        </select>
                        <button className="link-danger" onClick={() => remove(a)} title="Delete">
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {!visible.length && <div className="empty">No appointments here yet.</div>}
            </div>
          )}
        </section>
      </main>

      {showForm && (
        <div className="modal-backdrop" onClick={() => setShowForm(false)}>
          <form className="modal" onSubmit={createAppointment} onClick={(e) => e.stopPropagation()}>
            <div className="modal-head">
              <h2>Book appointment</h2>
              <button type="button" className="close" onClick={() => setShowForm(false)}>×</button>
            </div>
            <label>Student name
              <input name="student_name" required placeholder="e.g. Aarav Sharma" />
            </label>
            <label>Tutor
              <input name="tutor" required placeholder="e.g. Ms. Rao" />
            </label>
            <label>Subject
              <input name="subject" required placeholder="e.g. Mathematics" />
            </label>
            <label>Class time
              <input name="class_time" type="datetime-local" required />
            </label>
            <label>Notes
              <textarea name="notes" placeholder="Anything the tutor should know (optional)" />
            </label>
            <button className="primary full" type="submit">Book</button>
          </form>
        </div>
      )}
    </div>
  )
}

function Stat({ label, value, tone }) {
  return (
    <div className="stat">
      <small>{label}</small>
      <strong className={tone ? `tone-${tone}` : ''}>{value}</strong>
    </div>
  )
}

createRoot(document.getElementById('root')).render(<App />)
