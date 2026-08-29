"""Shared navigation bar HTML inserted into every sub-app template."""

NAV_HTML = """\
<nav class="navbar navbar-expand navbar-dark bg-dark px-3 py-1 mb-2" id="_mainNav" style="font-size:.875rem">
  <a class="navbar-brand fw-bold py-0" href="/">&#128202; FinAgent</a>
  <ul class="navbar-nav ms-3">
    <li class="nav-item"><a class="nav-link py-1" href="/zep">&#128376; Knowledge Graph</a></li>
    <li class="nav-item"><a class="nav-link py-1" href="/zsxq">&#128218; ZSXQ</a></li>
    <li class="nav-item"><a class="nav-link py-1" href="/zsxq/research-lens">&#128269; Research Lens</a></li>
    <li class="nav-item"><a class="nav-link py-1" href="/manual-report">&#128206; Manual Report</a></li>
    <li class="nav-item"><a class="nav-link py-1" href="/claude-reports">&#128209; Claude Reports</a></li>
    <li class="nav-item"><a class="nav-link py-1" href="/comments">&#128172; Comments</a></li>
    <li class="nav-item"><a class="nav-link py-1" href="/indicators">&#128200; Indicators</a></li>
    <li class="nav-item"><a class="nav-link py-1" href="/pe">&#128181; P/E</a></li>
    <li class="nav-item"><a class="nav-link py-1" href="/pt">&#127919; Price Target</a></li>
    <li class="nav-item"><a class="nav-link py-1" href="/obsidian">&#128204; Obsidian</a></li>
  </ul>
</nav>
<script>
(function(){
  var path = window.location.pathname;
  var links = Array.from(document.querySelectorAll('#_mainNav .nav-link'));
  var best = null;
  links.forEach(function(a){
    var href = a.getAttribute('href');
    if(path === href || (href !== '/' && path.startsWith(href + '/'))) {
      if(!best || href.length > best.getAttribute('href').length) best = a;
    }
  });
  if(best) best.classList.add('active');
})();
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
