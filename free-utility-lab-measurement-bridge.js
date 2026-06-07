(function(){
  window.dataLayer = window.dataLayer || [];
  var allowedEvents = {
    asset_view:1, calculator_start:1, calculator_complete:1, generator_start:1, generator_complete:1,
    download_click:1, print_click:1, result_copy:1, cta_click:1, support_page_click:1,
    buy_click:1, tool_add:1, language_change:1, checklist_toggle:1, habit_toggle:1, month_change:1,
    link_click:1, button_click:1
  };
  var allowedParams = {
    asset_id:1, asset_type:1, asset_slug:1, page_path:1, page_title:1, button:1, target:1, section:1,
    download_type:1, export_type:1, language:1, currency:1, count:1, item_count:1, tool_count:1,
    plan_count:1, total_monthly:1, monthly_bucket:1, score:1, score_bucket:1, link_url:1, link_text:1
  };
  function clean(value){
    if (value == null) return value;
    if (typeof value === 'number' || typeof value === 'boolean') return value;
    var s = String(value).slice(0, 160);
    if (/@|token|secret|password|key|address/i.test(s)) return '[filtered]';
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
