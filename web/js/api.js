/*
NOTEPROOF-FILE
module:   web
owner:    erdener         second: aysu
story:    S1, S3, S4, S5, S6, S7
contract: 02#7 HTTP API (istemci tarafı)
depends:  register/app.py HTTP API (arda)
status:   wip
*/
/**
 * Kayıt servisine giden bütün fetch çağrıları buradadır (erdener tasarım notları).
 * Kayıt servisiyle (Arda) sözleşme: 02 bölüm 7. Alan adları camelCase ve oradaki gibi kalır.
 *
 * USE_MOCK açıkken her fonksiyon web/mock/ altındaki örnek yanıtları döndürür; gerçek API ile aynı
 * biçimde döner ve aynı ApiError'ları atar. Böylece Faz 2'de yalnızca config.js'teki anahtar değişir.
 */

import { API_BASE, USE_MOCK, MOCK_BASE, SESSION_STORAGE_KEY, MAX_UPLOAD_BYTES, ALLOWED_TYPES } from "./config.js";
import { findCourse, topicWithNarrower } from "./helpers.js";

/** API'nin hata biçimi: {"error": {"code", "message", "violations"}}. message bilerek tutulmaz. */
export class ApiError extends Error {
  constructor(status, code, violations = []) {
    super(code);
    this.status = status;
    this.code = code;
    this.violations = violations;
  }
}

// ---------------------------------------------------------------------------
// Oturum: takma ad ve token (K-007). Token yalnızca bir kez gösterilir; tarayıcıda saklanır.
// Tarayıcı depolaması bazı ortamlarda kapalı olabilir; o zaman oturum yalnızca sayfa açıkken yaşar.
// ---------------------------------------------------------------------------

let memorySession = null;

export function getSession() {
  try {
    const raw = window.localStorage.getItem(SESSION_STORAGE_KEY);
    return raw ? JSON.parse(raw) : memorySession;
  } catch {
    return memorySession;
  }
}

function saveSession(session) {
  memorySession = session;
  try {
    window.localStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(session));
  } catch {
    /* depolama kapalı: bellekteki kopya yeterli */
  }
}

export function clearSession() {
  memorySession = null;
  try {
    window.localStorage.removeItem(SESSION_STORAGE_KEY);
  } catch {
    /* depolama kapalı */
  }
}

// ---------------------------------------------------------------------------
// Gerçek API
// ---------------------------------------------------------------------------

async function request(path, { method = "GET", json, form, auth = false } = {}) {
  const headers = {};
  let body;
  if (json !== undefined) {
    headers["Content-Type"] = "application/json";
    body = JSON.stringify(json);
  } else if (form !== undefined) {
    body = form; // multipart/form-data sınırını tarayıcı kendisi yazar
  }
  if (auth) {
    const session = getSession();
    if (!session?.token) throw new ApiError(401, "unauthorized");
    headers["X-NoteProof-Token"] = session.token;
  }

  let response;
  try {
    response = await fetch(`${API_BASE}${path}`, { method, headers, body });
  } catch {
    throw new ApiError(0, "network");
  }

  let data = null;
  try {
    data = await response.json();
  } catch {
    /* gövdesiz ya da JSON olmayan yanıt */
  }
  if (!response.ok) {
    const err = data?.error ?? {};
    throw new ApiError(response.status, err.code ?? "unknown", err.violations ?? []);
  }
  return data;
}

// ---------------------------------------------------------------------------
// Sahte veri (web/mock/). Gerçek API ile aynı imza ve aynı hata kodları.
// ---------------------------------------------------------------------------

async function mockFile(name) {
  let response;
  try {
    response = await fetch(`${MOCK_BASE}/${name}`);
  } catch {
    throw new ApiError(0, "network");
  }
  if (!response.ok) throw new ApiError(0, "network");
  return response.json();
}

async function mockError(name, status) {
  const data = await mockFile(name);
  throw new ApiError(status, data.error.code, data.error.violations ?? []);
}

async function mockSearch({ course, topic, q }) {
  const [{ results }, vocabulary] = await Promise.all([mockFile("search.json"), mockFile("vocabulary.json")]);
  let topicIds = null;
  if (topic) {
    const owner = findCourse(vocabulary, course) ?? vocabulary.courses.find((c) => c.topics.some((t) => t.id === topic));
    topicIds = owner ? topicWithNarrower(owner, topic) : new Set([topic]);
  }
  const needle = q ? q.toLocaleLowerCase("tr") : null;
  return {
    results: results.filter(
      (card) =>
        (!course || card.course === course) &&
        (!topicIds || card.topics.some((t) => topicIds.has(t))) &&
        (!needle || card.title.toLocaleLowerCase("tr").includes(needle)),
    ),
  };
}

// ---------------------------------------------------------------------------
// Sözleşme fonksiyonları (02 bölüm 7)
// ---------------------------------------------------------------------------

/** GET /api/vocabulary */
export async function getVocabulary() {
  return USE_MOCK ? mockFile("vocabulary.json") : request("/vocabulary");
}

/** GET /api/search?course=&topic=&q= → {"results": [not kartı]} */
export async function searchNotes({ course = "", topic = "", q = "" } = {}) {
  if (USE_MOCK) return mockSearch({ course, topic, q });
  const params = new URLSearchParams();
  if (course) params.set("course", course);
  if (topic) params.set("topic", topic);
  if (q) params.set("q", q);
  return request(`/search?${params}`);
}

/** GET /api/notes/{hash} → not kartı */
export async function getNote(noteHash) {
  if (!USE_MOCK) return request(`/notes/${encodeURIComponent(noteHash)}`);
  const { results } = await mockFile("search.json");
  const card = results.find((c) => c.noteHash === noteHash);
  if (!card) throw new ApiError(404, "not_found");
  return card;
}

/** GET /api/notes/{hash}/proof → proof dosyası (02 bölüm 6) ya da 404 proof_pending */
export async function getProof(noteHash) {
  if (!USE_MOCK) return request(`/notes/${encodeURIComponent(noteHash)}/proof`);
  const proof = await mockFile("proof.json");
  if (proof.noteHash !== noteHash) return mockError("error-proof-pending.json", 404);
  return proof;
}

/** POST /api/accounts {"pseudonym"} → {"account", "token"}; token tarayıcıda saklanır. */
export async function createAccount(pseudonym) {
  const data = USE_MOCK ? await mockFile("account.json") : await request("/accounts", { method: "POST", json: { pseudonym } });
  saveSession({ pseudonym, token: data.token });
  return data;
}

/**
 * POST /api/notes/preview (multipart, alan adı "file"). Hiçbir şey kaydedilmez (S3).
 * Sahte modda adı "kayitli" içeren dosya, "daha önce kaydedildi" yanıtını gösterir.
 */
export async function previewNote(file) {
  if (!USE_MOCK) {
    const form = new FormData();
    form.append("file", file);
    return request("/notes/preview", { method: "POST", form, auth: true });
  }
  if (!getSession()?.token) throw new ApiError(401, "unauthorized");
  if (!ALLOWED_TYPES.includes(file.type) && !/\.(md|txt)$/i.test(file.name)) throw new ApiError(400, "unsupported_type");
  if (file.size > MAX_UPLOAD_BYTES) throw new ApiError(400, "too_large");
  return mockFile(/kayitli/i.test(file.name) ? "preview-registered.json" : "preview.json");
}

/**
 * POST /api/notes: onay gövdesi {previewToken, title, course, topics, summary, confirmed: true}.
 * Kayıt isteği yalnızca buradan ve yalnızca yazar onay verince gider (S3).
 */
export async function confirmNote(body) {
  if (!USE_MOCK) return request("/notes", { method: "POST", json: body, auth: true });
  if (!getSession()?.token) throw new ApiError(401, "unauthorized");
  if (body.confirmed !== true) throw new ApiError(400, "not_confirmed");
  if (!body.course || body.topics.length === 0) return mockError("error-shape-violation.json", 422);
  return mockFile("note-created.json");
}
