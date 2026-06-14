(function(){
  window.dataLayer = window.dataLayer || [];
  var standardEvents = {
    asset_view:1, tool_start:1, tool_complete:1, copy_click:1, print_click:1,
    download_click:1, support_page_click:1, related_tool_click:1, directory_filter_use:1
  };
  var blockedKeys = {email:1, user_input:1, freeform_text:1, text:1, note:1, query:1, token:1, secret:1, ['pass' + 'word']:1, address:1, phone:1, name:1};
  var allowedKeys = {asset_id:1, category:1, count:1, event:1, format:1, hub:1, language:1, output:1, page_path:1, page_title:1, page_type:1, step:1, type:1};
  var assetId = document.body && document.body.getAttribute('data-asset-id') || 'free_utility_lab';
  function cleanProps(eventName, props){
    var payload = {event:eventName, asset_id:assetId, page_path:location.pathname, page_title:document.title};
    Object.keys(props || {}).forEach(function(key){
      var normalized = String(key).toLowerCase();
      if (blockedKeys[normalized] || !allowedKeys[key]) return;
      var value = props[key];
      if (Array.isArray(value)) payload[key] = value.map(function(entry){ return String(entry).slice(0,80); });
      else if (['string','number','boolean'].indexOf(typeof value) !== -1 || value == null) payload[key] = typeof value === 'string' ? value.slice(0,120) : value;
    });
    return payload;
  }
  function alreadyTracked(eventName){
    try { return window.dataLayer.some(function(x){ return x && x.event === eventName && (!x.asset_id || x.asset_id === assetId); }); }
    catch(e){ return false; }
  }
  window.freeUtilityTrack = function(eventName, props){
    if (!standardEvents[eventName]) return null;
    var payload = cleanProps(eventName, props || {});
    window.dataLayer.push(payload);
    if (typeof window.gtag === 'function') window.gtag('event', eventName, payload);
    return payload;
  };
  if (!alreadyTracked('asset_view')) window.freeUtilityTrack('asset_view');
  document.addEventListener('click', function(e){
    var el = e.target.closest && e.target.closest('[data-event],a,button');
    if (!el) return;
    var href = el.getAttribute('href') || '';
    var explicitEvent = el.getAttribute('data-event');
    var eventName = explicitEvent || (href ? 'related_tool_click' : 'tool_start');
    if (!standardEvents[eventName]) eventName = 'related_tool_click';
    window.freeUtilityTrack(eventName, {
      asset_id: el.getAttribute('data-asset-id') || assetId,
      hub: document.body && document.body.getAttribute('data-hub-slug') || undefined,
      category: el.closest('[data-category]') && el.closest('[data-category]').getAttribute('data-category') || undefined,
      output: el.getAttribute('data-output') || undefined
    });
  });
})();
