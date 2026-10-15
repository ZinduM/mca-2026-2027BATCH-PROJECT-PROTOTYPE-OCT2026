import { useState } from 'react';
import {
  CheckCircle,
  XCircle,
  Terminal,
  Table2,
  Lightbulb,
  RotateCcw,
  Database,
  ChevronDown,
  ChevronUp,
} from 'lucide-react';

export default function QueryResult({ result, onRecommendedQuery }) {
  const [showSql, setShowSql] = useState(true);

  if (!result) return null;

  const {
    original_query,
    sql,
    execution_status,
    columns = [],
    data = [],
    row_count = 0,
    insight,
    recommendations = [],
    error,
  } = result;

  const isSuccess = execution_status === 'Success';

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }} className="animate-fade-in">
      {/* 1. User Question */}
      <div className="card" style={{ padding: '16px 20px', borderLeft: '4px solid var(--primary)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
          <span style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-muted)', letterSpacing: '0.06em' }}>
            Your Question
          </span>
        </div>
        <p style={{ fontWeight: 600, color: 'var(--text-primary)', fontSize: 16 }}>{original_query}</p>
      </div>

      {/* 2. Generated SQL with Collapsible Toggle */}
      {sql && (
        <div className="card" style={{ padding: '16px 20px' }}>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              marginBottom: showSql ? 10 : 0,
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <Terminal size={16} color="var(--teal)" />
              <span style={{ fontSize: 12, fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-muted)', letterSpacing: '0.06em' }}>
                Generated SQL
              </span>
            </div>

            <button
              type="button"
              onClick={() => setShowSql((prev) => !prev)}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: 6,
                background: '#f8fafc',
                border: '1px solid var(--border)',
                borderRadius: 'var(--radius)',
                padding: '4px 10px',
                fontSize: 12,
                fontWeight: 600,
                color: 'var(--text-secondary)',
                cursor: 'pointer',
              }}
            >
              <span>{showSql ? 'Hide Query' : 'Show Query'}</span>
              {showSql ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
            </button>
          </div>

          {/* Collapsible SQL Block */}
          {showSql && (
            <pre
              style={{
                margin: 0,
                padding: '12px 16px',
                background: '#0f172a',
                color: '#7dd3fc',
                borderRadius: 'var(--radius)',
                fontSize: 13,
                fontFamily: 'ui-monospace, Consolas, monospace',
                overflowX: 'auto',
                lineHeight: 1.6,
                whiteSpace: 'pre-wrap',
                wordBreak: 'break-word',
              }}
            >
              {sql}
            </pre>
          )}
        </div>
      )}

      {/* 3. Execution Status */}
      <div
        className="card"
        style={{
          padding: '14px 20px',
          borderLeft: `4px solid ${isSuccess ? 'var(--success)' : 'var(--error)'}`,
          background: isSuccess ? '#f0fdf4' : '#fef2f2',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          {isSuccess ? <CheckCircle size={20} color="var(--success)" /> : <XCircle size={20} color="var(--error)" />}
          <div>
            <p style={{ fontWeight: 700, color: isSuccess ? '#15803d' : '#dc2626' }}>
              {isSuccess ? 'Query Executed Successfully' : 'Query Failed'}
            </p>
            {isSuccess && (
              <p style={{ fontSize: 13, color: '#16a34a', marginTop: 2 }}>
                <Database size={12} style={{ marginRight: 4, verticalAlign: 'middle' }} />
                {row_count} row{row_count !== 1 ? 's' : ''} returned
              </p>
            )}
            {error && <p style={{ fontSize: 13, color: '#dc2626', marginTop: 2 }}>{error}</p>}
          </div>
        </div>
      </div>

      {/* 4. Result Table */}
      {isSuccess && columns.length > 0 && (
        <div className="card" style={{ padding: '16px 20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 }}>
            <Table2 size={16} color="var(--primary)" />
            <span style={{ fontSize: 12, fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-muted)', letterSpacing: '0.06em' }}>
              Results
            </span>
            <span style={{ marginLeft: 'auto', fontSize: 12, color: 'var(--text-muted)' }}>{row_count} records</span>
          </div>
          {data.length === 0 ? (
            <p style={{ color: 'var(--text-muted)', fontSize: 14, textAlign: 'center', padding: '20px 0' }}>No records found</p>
          ) : (
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    {columns.map((col) => (
                      <th key={col}>{col.replace(/_/g, ' ')}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {data.map((row, i) => (
                    <tr key={i}>
                      {columns.map((col) => (
                        <td key={col}>{row[col] ?? '—'}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* 5. AI Insight */}
      {insight && (
        <div
          className="card"
          style={{
            padding: '16px 20px',
            background: 'linear-gradient(135deg, #eff6ff, #f0fdf4)',
            borderLeft: '4px solid var(--teal)',
          }}
        >
          <div style={{ display: 'flex', gap: 12 }}>
            <div
              style={{
                width: 36,
                height: 36,
                borderRadius: '50%',
                flexShrink: 0,
                background: 'linear-gradient(135deg, var(--primary), var(--teal))',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <Lightbulb size={18} color="white" />
            </div>
            <div>
              <p style={{ fontWeight: 700, color: 'var(--primary-dark)', marginBottom: 4, fontSize: 13, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                AI Insight
              </p>
              <p style={{ color: 'var(--text-primary)', lineHeight: 1.6 }}>{insight}</p>
            </div>
          </div>
        </div>
      )}

      {/* 6. Recommended Queries */}
      {recommendations.length > 0 && (
        <div className="card" style={{ padding: '16px 20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 }}>
            <RotateCcw size={16} color="var(--primary)" />
            <span style={{ fontSize: 12, fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-muted)', letterSpacing: '0.06em' }}>
              Recommended Queries
            </span>
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {recommendations.map((rec, i) => (
              <button
                key={i}
                type="button"
                onClick={() => onRecommendedQuery && onRecommendedQuery(rec)}
                style={{
                  padding: '7px 14px',
                  borderRadius: 99,
                  border: '1.5px solid var(--border)',
                  background: 'white',
                  color: 'var(--primary)',
                  fontSize: 13,
                  fontWeight: 500,
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                }}
                onMouseEnter={(e) => {
                  e.target.style.background = 'var(--primary)';
                  e.target.style.color = 'white';
                  e.target.style.borderColor = 'var(--primary)';
                }}
                onMouseLeave={(e) => {
                  e.target.style.background = 'white';
                  e.target.style.color = 'var(--primary)';
                  e.target.style.borderColor = 'var(--border)';
                }}
              >
                {rec}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}