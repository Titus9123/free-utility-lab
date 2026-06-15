(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.FreeUtilityLabActions = factory();
  }
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const STANDARD_MEASUREMENT_EVENTS = Object.freeze([
    'asset_view',
    'tool_start',
    'tool_complete',
    'copy_click',
    'print_click',
    'download_click',
    'support_page_click',
    'related_tool_click',
    'directory_filter_use'
  ]);

  const LEGACY_EVENT_ALIASES = Object.freeze({
    ['calculator' + '_start']: 'tool_start',
    ['calculator' + '_complete']: 'tool_complete',
    ['generator' + '_start']: 'tool_start',
    ['generator' + '_complete']: 'tool_complete',
    ['result' + '_copy']: 'copy_click',
    ['marketplace' + '_tool_click']: 'related_tool_click',
    ['cta' + '_click']: 'related_tool_click',
    ['calculator' + '_click']: 'related_tool_click'
  });

  const BLOCKED_TRACKING_KEYS = new Set([
    'address', 'client' + '_secret', 'connection_string', 'email', 'freeform_text',
    'full_name', 'name', 'note', 'password', 'phone', 'query', 'refresh' + '_token',
    'secret', 'text', 'token', 'user_input'
  ]);

  const SAFE_TRACKING_KEYS = new Set([
    'asset_id', 'category', 'event', 'format', 'formats', 'hub', 'id', 'language',
    'output', 'outputs', 'page_type', 'status', 'step', 'tool_id', 'type', 'value',
    'amount', 'count', 'index', 'priority'
  ]);

  function csvEscape(value) {
    if (value == null) {
      return '';
    }
    const text = String(value);
    if (/[",\r\n]/.test(text)) {
      return '"' + text.replace(/"/g, '""') + '"';
    }
    return text;
  }

  function tableToCsv(rows) {
    return (rows || [])
      .map(function (row) { return (row || []).map(csvEscape).join(','); })
      .join('\r\n');
  }

  function downloadText(filename, text, mimeType) {
    if (typeof document === 'undefined') {
      return { filename, text, mimeType: mimeType || 'text/plain' };
    }
    const blob = new Blob([text], { type: mimeType || 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
    return true;
  }

  function copyText(text) {
    if (typeof navigator !== 'undefined' && navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(String(text));
    }
    if (typeof document !== 'undefined') {
      const textarea = document.createElement('textarea');
      textarea.value = String(text);
      textarea.setAttribute('readonly', '');
      textarea.style.position = 'fixed';
      textarea.style.left = '-9999px';
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      textarea.remove();
      return Promise.resolve();
    }
    return Promise.resolve(String(text));
  }

  function createPrintSectionMarkup(id, innerHtml) {
    return '<section class="ful-print-section" data-print-section="' + String(id).replace(/"/g, '&quot;') + '">' + innerHtml + '</section>';
  }

  function printSection(id) {
    if (typeof document === 'undefined' || typeof window === 'undefined') {
      return false;
    }
    const safeId = String(id || '');
    const escaped = typeof CSS !== 'undefined' && CSS.escape ? CSS.escape(safeId) : safeId.replace(/"/g, '\\"');
    const target = document.getElementById(safeId) || document.querySelector('section[data-print-section="' + escaped + '"], [data-print-section="' + escaped + '"]:not(button)');
    if (!target) {
      return false;
    }
    document.body.setAttribute('data-ful-print-target', safeId);
    window.print();
    document.body.removeAttribute('data-ful-print-target');
    return true;
  }

  function initDomActions() {
    if (typeof document === 'undefined') {
      return false;
    }
    document.addEventListener('click', function (event) {
      const copyButton = event.target.closest('[data-copy-target]');
      if (copyButton) {
        const target = document.querySelector(copyButton.getAttribute('data-copy-target'));
        copyText(target ? target.innerText : '').then(function () {
          trackSafe('copy_click', { output: 'template' });
        });
        return;
      }
      const csvButton = event.target.closest('[data-csv-target]');
      if (csvButton) {
        const table = document.querySelector(csvButton.getAttribute('data-csv-target'));
        if (table) {
          const rows = Array.from(table.querySelectorAll('tr')).map(function (row) {
            return Array.from(row.querySelectorAll('th,td')).map(function (cell) { return cell.innerText.trim(); });
          });
          downloadText(csvButton.getAttribute('data-filename') || 'free-utility-lab-template.csv', tableToCsv(rows), 'text/csv;charset=utf-8');
          trackSafe('download_click', { output: 'csv' });
        }
        return;
      }
      const printButton = event.target.closest('button[data-print-section]');
      if (printButton) {
        printSection(printButton.getAttribute('data-print-section'));
        trackSafe('print_click', { output: 'template' });
      }
    });
    return true;
  }

  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initDomActions, { once: true });
    } else {
      initDomActions();
    }
  }

  function filterMarketplaceItems(items, filters) {
    filters = filters || {};
    return (items || []).filter(function (item) {
      if (filters.category && item.category !== filters.category) {
        return false;
      }
      if (filters.format && !(item.formats || []).includes(filters.format)) {
        return false;
      }
      if (filters.output && !(item.outputs || []).includes(filters.output)) {
        return false;
      }
      if (filters.userType && !(item.user_types || []).includes(filters.userType)) {
        return false;
      }
      return true;
    });
  }

  function normalizeMeasurementEvent(eventName) {
    const normalized = String(eventName || '').trim();
    return LEGACY_EVENT_ALIASES[normalized] || normalized;
  }

  function sanitizeTrackingPayload(payload) {
    const safe = {};
    Object.entries(payload || {}).forEach(function ([key, value]) {
      const normalized = String(key).toLowerCase();
      if (BLOCKED_TRACKING_KEYS.has(normalized) || !SAFE_TRACKING_KEYS.has(key)) {
        return;
      }
      if (key === 'event') {
        const eventName = normalizeMeasurementEvent(value);
        if (!STANDARD_MEASUREMENT_EVENTS.includes(eventName)) {
          return;
        }
        safe[key] = eventName;
        return;
      }
      if (Array.isArray(value)) {
        safe[key] = value.map(function (entry) { return String(entry).slice(0, 80); });
      } else if (['string', 'number', 'boolean'].includes(typeof value) || value == null) {
        safe[key] = typeof value === 'string' ? value.slice(0, 120) : value;
      }
    });
    return safe;
  }

  function trackSafe(eventName, payload) {
    const standardEventName = normalizeMeasurementEvent(eventName);
    const sanitized = sanitizeTrackingPayload(Object.assign({}, payload || {}, { event: standardEventName }));
    if (!sanitized.event) {
      return sanitized;
    }
    if (typeof window !== 'undefined' && typeof window.freeUtilityTrack === 'function') {
      window.freeUtilityTrack(standardEventName, sanitized);
    } else if (typeof window !== 'undefined' && typeof window.gtag === 'function') {
      window.gtag('event', standardEventName, sanitized);
    }
    return sanitized;
  }

  return {
    STANDARD_MEASUREMENT_EVENTS,
    copyText,
    createPrintSectionMarkup,
    csvEscape,
    downloadText,
    filterMarketplaceItems,
    normalizeMeasurementEvent,
    printSection,
    sanitizeTrackingPayload,
    tableToCsv,
    trackSafe,
    trackSafeEvent: trackSafe
  };
});
