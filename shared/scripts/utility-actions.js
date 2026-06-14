(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.FreeUtilityLabActions = factory();
  }
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const BLOCKED_TRACKING_KEYS = new Set([
    'address', 'client' + '_secret', 'connection_string', 'email', 'freeform_text',
    'full_name', 'name', 'note', 'password', 'phone', 'refresh' + '_token', 'secret',
    'text', 'token', 'user_input'
  ]);

  const SAFE_TRACKING_KEYS = new Set([
    'asset_id', 'category', 'event', 'format', 'formats', 'id', 'language',
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
    const target = document.querySelector('[data-print-section="' + CSS.escape(id) + '"]');
    if (!target) {
      return false;
    }
    document.body.setAttribute('data-ful-print-target', id);
    window.print();
    document.body.removeAttribute('data-ful-print-target');
    return true;
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

  function sanitizeTrackingPayload(payload) {
    const safe = {};
    Object.entries(payload || {}).forEach(function ([key, value]) {
      const normalized = String(key).toLowerCase();
      if (BLOCKED_TRACKING_KEYS.has(normalized) || !SAFE_TRACKING_KEYS.has(key)) {
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
    const sanitized = sanitizeTrackingPayload(Object.assign({}, payload || {}, { event: eventName }));
    if (typeof window !== 'undefined' && typeof window.freeUtilityLabTrack === 'function') {
      window.freeUtilityLabTrack(eventName, sanitized);
    } else if (typeof window !== 'undefined' && typeof window.gtag === 'function') {
      window.gtag('event', eventName, sanitized);
    }
    return sanitized;
  }

  return {
    copyText,
    createPrintSectionMarkup,
    csvEscape,
    downloadText,
    filterMarketplaceItems,
    printSection,
    sanitizeTrackingPayload,
    tableToCsv,
    trackSafe
  };
});
