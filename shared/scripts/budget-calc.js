/* budget-calc.js — shared budget calculation utilities
   Namespace: window.BudgetCalc
   Used by: budgetreset, movebudget and any finance asset */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) { module.exports = factory(); }
  else { root.BudgetCalc = factory(); }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  function n(v) { return Math.max(0, Number(v) || 0); }

  function money(v, symbol) {
    return (symbol || '$') + Math.round(Math.abs(v)).toLocaleString('en-US');
  }

  /** 50/30/20 analysis: returns {needs, wants, savings, labels, status} */
  function analyze5030(income, needs, wants, savings) {
    if (!income) return null;
    var needsPct = Math.round(needs / income * 100);
    var wantsPct = Math.round(wants / income * 100);
    var savingsPct = Math.round(savings / income * 100);
    var status = 'ok';
    if (needsPct > 60) status = 'warning';
    if (needsPct > 70) status = 'danger';
    return {
      needs: needsPct, wants: wantsPct, savings: savingsPct,
      labels: { needs: needsPct + '% needs', wants: wantsPct + '% wants', savings: savingsPct + '% savings' },
      status: status
    };
  }

  /** Debt payoff estimate in months (snowball or avalanche) */
  function payoffMonths(debts, extra, method) {
    var items = debts.map(function (d) { return Object.assign({}, d); }).filter(function (d) { return d.balance > 0; });
    if (!items.length) return 0;
    var months = 0; var max = 600;
    while (items.some(function (d) { return d.balance > 1; }) && months < max) {
      if (method === 'avalanche') items.sort(function (a, b) { return b.apr - a.apr; });
      else items.sort(function (a, b) { return a.balance - b.balance; });
      var first = true;
      items.forEach(function (d) {
        if (d.balance <= 0) return;
        d.balance += d.balance * (d.apr / 100 / 12);
        var p = d.payment + (first ? (extra || 0) : 0);
        d.balance -= Math.max(0, p);
        if (d.balance < 0) d.balance = 0;
        first = false;
      });
      months++;
    }
    return months >= max ? max : months;
  }

  /** Budget health: 'healthy' | 'tight' | 'over' */
  function budgetHealth(net, income) {
    if (!income) return 'neutral';
    if (net >= income * 0.1) return 'healthy';
    if (net >= 0) return 'tight';
    return 'over';
  }

  /** Simple localStorage helpers with namespace prefix */
  function lsGet(ns, key) {
    try { return localStorage.getItem(ns + key); } catch (e) { return null; }
  }
  function lsSet(ns, key, val) {
    try { localStorage.setItem(ns + key, val); } catch (e) {}
  }
  function lsGetObj(ns, key) {
    try { var v = localStorage.getItem(ns + key); return v ? JSON.parse(v) : null; } catch (e) { return null; }
  }
  function lsSetObj(ns, key, obj) {
    try { localStorage.setItem(ns + key, JSON.stringify(obj)); } catch (e) {}
  }

  /** CSV escaping */
  function csvEscape(v) { return '"' + String(v).replace(/"/g, '""') + '"'; }

  return {
    n: n,
    money: money,
    analyze5030: analyze5030,
    payoffMonths: payoffMonths,
    budgetHealth: budgetHealth,
    lsGet: lsGet,
    lsSet: lsSet,
    lsGetObj: lsGetObj,
    lsSetObj: lsSetObj,
    csvEscape: csvEscape
  };
});
