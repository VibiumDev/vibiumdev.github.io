// Surface picker state. Loaded blocking from <head> so the filter applies
// before first paint; kept out of the HTML to keep pages light.
window.VibiumSurface = (() => {
  const storageKey = 'vibium-surface';
  const surfaces = ['cli', 'mcp', 'javascript', 'python', 'java'];
  const read = () => {
    try {
      return localStorage.getItem(storageKey);
    } catch {
      return null;
    }
  };
  const apply = (surface) => {
    if (surfaces.includes(surface)) document.documentElement.dataset.surface = surface;
    else delete document.documentElement.dataset.surface;
  };
  const set = (surface) => {
    try {
      localStorage.setItem(storageKey, surfaces.includes(surface) ? surface : 'all');
    } catch {}
    apply(surface);
    updatePickers();
  };
  const updatePickers = () => {
    const current = document.documentElement.dataset.surface ?? 'all';
    document.querySelectorAll('vibium-surface-select select').forEach((select) => {
      select.value = current;
    });
  };
  const requested = new URLSearchParams(location.search).get('surface');
  const section = location.pathname.match(/\/docs\/libraries\/(javascript|python|java)(\/|$)/);
  if (requested === 'all' || surfaces.includes(requested)) set(requested);
  else if (section && read() === null) set(section[1]);
  else apply(read());
  return { set, updatePickers };
})();
