(function(){
  window.dataLayer = window.dataLayer || [];
  var allowedEvents = {
    asset_view:1, tool_start:1, tool_complete:1, copy_click:1, print_click:1,
    download_click:1, support_page_click:1, related_tool_click:1, directory_filter_use:1
  };
  var allowedParams = {
    asset_id:1, category:1, count:1, download_type:1, export_type:1, format:1, hub:1,
    language:1, output:1, page_path:1, page_title:1, page_type:1, step:1, type:1
  };
  function clean(value){
    if (value == null) return value;
    if (typeof value === 'number' || typeof value === 'boolean') return value;
    var s = String(value).slice(0, 120);
    if (/@|token|secret|password|key|address|query/i.test(s)) return '[filtered]';
    return s;
  }
  function forward(item){
    if (!item || !item.event || !allowedEvents[item.event] || typeof window.gtag !== 'function') return;
    var params = {};
    Object.keys(item).forEach(function(k){ if (k !== 'event' && allowedParams[k]) params[k] = clean(item[k]); });
    params.page_path = params.page_path || location.pathname;
    params.page_title = params.page_title || document.title;
    window.gtag('event', item.event, params);
  }
  var dl = window.dataLayer;
  if (dl && !dl.__freeUtilityBridgePatched) {
    dl.slice().forEach(forward);
    var originalPush = dl.push;
    dl.push = function(){
      for (var i=0;i<arguments.length;i++) forward(arguments[i]);
      return originalPush.apply(dl, arguments);
    };
    dl.__freeUtilityBridgePatched = true;
  }
})();
