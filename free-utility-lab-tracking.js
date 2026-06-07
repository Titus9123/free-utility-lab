(function(){
  window.dataLayer = window.dataLayer || [];
  var assetId = document.body && document.body.getAttribute('data-asset-id') || 'free_utility_lab';
  function alreadyTracked(eventName){
    try { return window.dataLayer.some(function(x){ return x && x.event === eventName && (!x.asset_id || x.asset_id === assetId); }); }
    catch(e){ return false; }
  }
  window.freeUtilityTrack = function(eventName, props){
    var payload = Object.assign({
      event: eventName,
      asset_id: assetId,
      page_path: location.pathname,
      page_title: document.title
    }, props || {});
    window.dataLayer.push(payload);
    if (typeof window.gtag === 'function') window.gtag('event', eventName, payload);
  };
  if (!alreadyTracked('asset_view')) window.freeUtilityTrack('asset_view');
  document.addEventListener('click', function(e){
    var el = e.target.closest && e.target.closest('[data-event],a,button');
    if (!el) return;
    var href = el.getAttribute('href') || '';
    var eventName = el.getAttribute('data-event') || (href ? 'link_click' : 'button_click');
    window.freeUtilityTrack(eventName, {
      link_url: href,
      link_text: (el.innerText || el.getAttribute('aria-label') || '').trim().slice(0, 120)
    });
  });
})();
