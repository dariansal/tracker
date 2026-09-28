// A small stand-in for the claude.ai artifact runtime, for local testing only (see dev_server.py).
// Implements just what tracker.html uses: use("db") with doc/collection get, set, delete,
// onSnapshot (backed by localStorage key "mock-db"), and use("sample") with no image support
// whose json() calls fail as if Claude were unreachable (so the built-in fallbacks run).
(() => {
  const KEY = "mock-db";
  const load = () => { try { return JSON.parse(localStorage.getItem(KEY) || "{}"); } catch { return {}; } };
  const save = s => localStorage.setItem(KEY, JSON.stringify(s));
  const listeners = new Set();
  const notify = () => setTimeout(() => listeners.forEach(fn => fn()), 0);
  const docSnap = (path, s) => ({ id: path.split("/").pop(), exists: path in s, data: () => s[path], metadata: {} });
  const docRef = path => ({
    get: async () => docSnap(path, load()),
    set: async data => { const s = load(); s[path] = JSON.parse(JSON.stringify(data)); save(s); notify(); },
    delete: async () => { const s = load(); delete s[path]; save(s); notify(); },
    onSnapshot: (next) => { const fn = () => next(docSnap(path, load())); listeners.add(fn); fn(); return () => listeners.delete(fn); },
  });
  const colRef = name => ({
    doc: id => docRef(name + "/" + id),
    onSnapshot: (next) => {
      const fn = () => {
        const s = load(), docs = Object.keys(s).filter(k => k.startsWith(name + "/") && !k.slice(name.length + 1).includes("/"))
          .map(k => docSnap(k, s));
        next({ docs, size: docs.length, empty: !docs.length, docChanges: () => [], metadata: { fromCache: false, hasPendingWrites: false } });
      };
      listeners.add(fn); fn(); return () => listeners.delete(fn);
    },
  });
  const db = { doc: docRef, collection: colRef };
  const sample = {
    limits: async () => ({}),   // no image support, like the owner's phone
    json: async () => { const e = new Error("mock: Claude unavailable"); e.code = "unavailable"; throw e; },
  };
  window.claude = { use: async name => (name === "db" ? db : name === "sample" ? sample : null) };
  console.log("[mock-claude] claude.ai runtime stand-in active");
})();
