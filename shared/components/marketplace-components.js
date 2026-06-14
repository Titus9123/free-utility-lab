(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.FreeUtilityLabComponents = factory();
  }
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const OUTPUT_LABELS = {
    copy: 'Copy',
    csv: 'CSV',
    print: 'Print',
    download: 'Download',
    checklist: 'Checklist',
    external_link: 'External link',
    free: 'Free',
    no_signup: 'No signup'
  };

  function escapeHtml(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function pathFromPublicUrl(publicUrl, basePath) {
    const fallbackBasePath = basePath || '/free-utility-lab/';
    try {
      const url = new URL(publicUrl);
      return url.pathname;
    } catch (error) {
      if (!publicUrl) {
        return fallbackBasePath;
      }
      if (String(publicUrl).startsWith('/')) {
        return publicUrl;
      }
      return fallbackBasePath.replace(/\/$/, '') + '/' + String(publicUrl).replace(/^\//, '');
    }
  }

  function outputLabel(output) {
    return OUTPUT_LABELS[output] || String(output).replace(/[_-]+/g, ' ').replace(/\b\w/g, function (letter) {
      return letter.toUpperCase();
    });
  }

  function renderBadgeList(items) {
    return (items || [])
      .filter(Boolean)
      .map(function (item) {
        return '<span class="ful-badge">' + escapeHtml(outputLabel(item)) + '</span>';
      })
      .join('');
  }

  function renderToolCard(asset, options) {
    options = options || {};
    const outputs = Array.isArray(asset.outputs) ? asset.outputs : [];
    const formats = Array.isArray(asset.formats) ? asset.formats : [];
    const userTypes = Array.isArray(asset.user_types) ? asset.user_types : [];
    const badges = ['free', 'no_signup'].concat(outputs);
    const href = pathFromPublicUrl(asset.public_url, options.basePath);
    const assetId = asset.tracking_asset_id || asset.id;

    return [
      '<article class="ful-tool-card" data-asset-id="' + escapeHtml(asset.id) + '" data-category="' + escapeHtml(asset.category) + '">',
      '  <div class="ful-card-topline">' + escapeHtml(asset.category || 'tool') + '</div>',
      '  <h3>' + escapeHtml(asset.name) + '</h3>',
      '  <p>' + escapeHtml(asset.intent || '') + '</p>',
      '  <div class="ful-badges" aria-label="Tool outputs">' + renderBadgeList(badges) + '</div>',
      '  <p class="ful-card-meta">Formats: ' + escapeHtml(formats.join(', ')) + '</p>',
      '  <p class="ful-card-meta">Useful for: ' + escapeHtml(userTypes.join(', ')) + '</p>',
      '  <a class="ful-primary-cta" href="' + escapeHtml(href) + '" data-event="marketplace_tool_click" data-asset-id="' + escapeHtml(assetId) + '">Open free tool</a>',
      '</article>'
    ].join('\n');
  }

  function renderRelatedTools(assets, relatedIds, options) {
    const wanted = new Set(relatedIds || []);
    return (assets || [])
      .filter(function (asset) { return wanted.has(asset.id); })
      .map(function (asset) { return renderToolCard(asset, options); })
      .join('\n');
  }

  function renderBreadcrumb(items) {
    return '<nav class="ful-breadcrumb" aria-label="Breadcrumb">' +
      (items || []).map(function (item, index) {
        const label = escapeHtml(item.label || item.name || 'Page');
        const href = item.href ? escapeHtml(item.href) : '';
        if (!href || index === items.length - 1) {
          return '<span aria-current="page">' + label + '</span>';
        }
        return '<a href="' + href + '">' + label + '</a>';
      }).join('<span class="ful-breadcrumb-separator">/</span>') +
      '</nav>';
  }

  function renderFaq(items) {
    return '<section class="ful-faq">' + (items || []).map(function (item) {
      return '<details><summary>' + escapeHtml(item.question) + '</summary><p>' + escapeHtml(item.answer) + '</p></details>';
    }).join('\n') + '</section>';
  }

  return {
    escapeHtml,
    renderBadgeList,
    renderToolCard,
    renderRelatedTools,
    renderBreadcrumb,
    renderFaq,
    pathFromPublicUrl
  };
});
