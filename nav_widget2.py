"""Shared navigation bar HTML inserted into every sub-app template."""

NAV_HTML = """\
<nav class="navbar navbar-expand-sm navbar-dark bg-dark px-3 py-1 mb-2" id="_mainNav" style="font-size:.875rem">
  <a class="navbar-brand fw-bold py-0" href="/">&#128202; FinAgent</a>
  <ul class="navbar-nav ms-3">
    <li class="nav-item"><a class="nav-link py-1" href="/kg">&#128376; Knowledge Graph</a></li>
    <li class="nav-item"><a class="nav-link py-1" href="/zsxq">&#128218; ZSXQ</a></li>
    <li class="nav-item"><a class="nav-link py-1" href="/sec">&#128196; US Reports</a></li>
    <li class="nav-item"><a class="nav-link py-1" href="/cn">&#127464;&#127475; CN Reports</a></li>
  </ul>
</nav>
<script>
document.querySelectorAll('#_mainNav .nav-link').forEach(function(a){
  if(window.location.pathname.startsWith(a.getAttribute('href'))) a.classList.add('active');
});
</script>"""

# JS snippet injected right after <body> in every template.
# Patches fetch() and EventSource() to prepend the blueprint URL prefix,
# so all existing absolute-path API calls ('/reports', '/download?...') work
# unchanged inside blueprints mounted at '/sec', '/cn', etc.
URL_PATCH_JS = """\
<script id="_urlPatch">
(function(){
  var b='{{ _base | default("") }}';
  if(!b) return;
  window._BASE=b;
  var _f=window.fetch;
  window.fetch=function(u,o){
    if(typeof u==='string'&&u.charAt(0)==='/') u=b+u;
    return _f.call(this,u,o);
  };
  var _E=window.EventSource;
  window.EventSource=function(u,c){
    if(u.charAt(0)==='/') u=b+u;
    return new _E(u,c);
  };
})();
</script>"""
