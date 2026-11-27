/*
NOTEPROOF-FILE
module:   web
owner:    erdener         second: aysu
story:    S1, S3, S4, S6
contract: 02#7 POST /api/accounts, GET /api/vocabulary, POST /api/notes/preview, POST /api/notes
depends:  web/js/api.js
status:   wip
*/
/**
 * Yükleme sayfası (web/upload.html). Akış üç adımdır: dosya seçimi → öneriler ve onay → sonuç.
 *
 * Kurallar (01 bölüm 5, S3, S4):
 * - Onaya kadar hiçbir kayıt isteği gitmez; "Vazgeç" hiçbir istek göndermez.
 * - Konu yalnızca sözlük listesinden eklenir; serbest metinle konu yazılamaz.
 * - Kopya uyarısı hüküm değildir: metin "Olası kopya", bağlantı önceki notun kanıtıdır; skor gösterilmez.
 * Gerçek API'ye bağlanması ve S3/S4 kabul testleri ERD-4'tedir.
 */

import { ApiError, clearSession, confirmNote, createAccount, getSession, getVocabulary, previewNote } from "./api.js";
import { errorText, findCourse, formatDate, formatDateTime, labelFor, shortHash, topicTree } from "./helpers.js";

const $ = (id) => document.getElementById(id);
const VIEWS = ["account-view", "pick-view", "review-view", "done-view"];

let vocabulary = { courses: [] };
let preview = null; // son önizleme yanıtı
let topics = []; // yazarın şu an seçili konuları (yerel kimlikler)

function el(tag, attrs = {}, text) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
  if (text !== undefined) node.textContent = text;
  return node;
}

function show(viewId) {
  for (const id of VIEWS) $(id).hidden = id !== viewId;
}

function showError(err) {
  $("error").textContent = errorText(err instanceof ApiError ? err.code : "unknown");
  $("error").hidden = false;
}

function clearError() {
  $("error").hidden = true;
}

/** Proof bağlantısı: API "/api/notes/<hash>/proof" verir; kullanıcıyı proof sayfasına götürürüz. */
function proofPageUrl(noteHash) {
  return `proof.html?hash=${encodeURIComponent(noteHash)}`;
}

// ---------------------------------------------------------------------------
// Hesap
// ---------------------------------------------------------------------------

function startPick() {
  const session = getSession();
  if (!session?.token) {
    show("account-view");
    return;
  }
  $("current-pseudonym").textContent = `@${session.pseudonym}`;
  $("pick-status").textContent = "";
  $("file-input").value = "";
  show("pick-view");
}

async function onCreateAccount(event) {
  event.preventDefault();
  clearError();
  const pseudonym = $("pseudonym").value.trim();
  try {
    await createAccount(pseudonym);
    startPick();
  } catch (err) {
    showError(err);
  }
}

// ---------------------------------------------------------------------------
// 3a → 3b: önizleme (hiçbir şey kaydedilmez)
// ---------------------------------------------------------------------------

async function onFile(file) {
  if (!file) return;
  clearError();
  $("pick-status").textContent = "Dosya inceleniyor...";
  try {
    preview = await previewNote(file);
  } catch (err) {
    $("pick-status").textContent = "";
    if (err.code === "unauthorized") clearSession();
    showError(err);
    if (err.code === "unauthorized") startPick();
    return;
  }
  renderReview(file.name);
}

function renderCopyWarnings(warnings) {
  const box = $("copy-warnings");
  box.replaceChildren();
  for (const w of warnings) {
    const strip = el("div", { class: "copy-note" });
    strip.append(el("strong", {}, "! Olası kopya"), el("br"));
    strip.append(`@${w.earlierAuthor} · ${formatDate(w.earlierRegisteredAt)} `);
    strip.append(el("a", { href: proofPageUrl(w.earlierNoteHash) }, "Önceki notun kanıtı ›"));
    box.append(strip);
  }
}

function renderReview(fileName) {
  $("file-name").textContent = fileName;
  $("note-hash").textContent = shortHash(preview.noteHash);
  $("violations").hidden = true;
  $("checked").checked = false;
  $("save").disabled = true;

  const already = preview.alreadyRegistered;
  $("already").hidden = !already;
  $("confirm-form").hidden = Boolean(already);
  if (already) {
    $("already").replaceChildren(
      `Bu dosya ${formatDate(already.registeredAt)} tarihinde @${already.author} tarafından kaydedildi. `,
      el("a", { href: proofPageUrl(preview.noteHash) }, "Kanıtı gör"),
    );
    renderCopyWarnings([]);
    show("review-view");
    return;
  }

  renderCopyWarnings(preview.copyWarnings ?? []);
  const suggestion = preview.suggestion ?? { course: null, topics: [], summary: "" };
  $("title").value = fileName.replace(/\.[^.]+$/, "");
  fillCourses(suggestion.course);
  topics = [...suggestion.topics];
  renderTopics();
  $("summary").value = suggestion.summary;
  show("review-view");
}

// ---------------------------------------------------------------------------
// Ders ve konu seçimi: yalnızca sözlükten
// ---------------------------------------------------------------------------

function fillCourses(selected) {
  const select = $("course");
  select.replaceChildren(el("option", { value: "" }, "Ders seç"));
  for (const course of vocabulary.courses) select.append(el("option", { value: course.id }, course.labelTr));
  select.value = selected && findCourse(vocabulary, selected) ? selected : "";
}

function renderTopics() {
  const list = $("topics");
  list.replaceChildren();
  for (const id of topics) {
    const chip = el("li", { class: "chip" }, labelFor(vocabulary, id));
    const remove = el("button", { type: "button", "aria-label": `${labelFor(vocabulary, id)} konusunu çıkar` }, "×");
    remove.addEventListener("click", () => {
      topics = topics.filter((t) => t !== id);
      renderTopics();
    });
    chip.append(remove);
    list.append(chip);
  }

  const add = $("add-topic");
  add.replaceChildren(el("option", { value: "" }, "+ Listeden konu ekle"));
  const course = findCourse(vocabulary, $("course").value);
  add.disabled = !course;
  if (!course) return;
  for (const item of topicTree(course)) {
    if (topics.includes(item.id)) continue;
    add.append(el("option", { value: item.id }, `${"   ".repeat(item.depth)}${item.label}`));
  }
}

function onCourseChange() {
  // Ders değişince önceki dersin konuları geçersiz olur; yalnızca yeni dersin konuları kalır.
  const course = findCourse(vocabulary, $("course").value);
  const valid = new Set(course ? course.topics.map((t) => t.id) : []);
  topics = topics.filter((t) => valid.has(t));
  renderTopics();
}

function onAddTopic() {
  const id = $("add-topic").value;
  if (id && !topics.includes(id)) topics.push(id);
  renderTopics();
}

// ---------------------------------------------------------------------------
// 3b → 3c: onay (tek kayıt isteği burada)
// ---------------------------------------------------------------------------

function showViolations(violations) {
  const box = $("violations");
  const list = el("ul");
  for (const v of violations) list.append(el("li", {}, v.message));
  box.replaceChildren(el("span", {}, "Konuyu listeden seç."), list);
  box.hidden = false;
  if (violations.some((v) => v.path === "np:topic")) $("add-topic").classList.add("field-invalid");
  if (violations.some((v) => v.path === "np:course")) $("course").classList.add("field-invalid");
  box.scrollIntoView({ behavior: "smooth", block: "start" });
}

async function onConfirm(event) {
  event.preventDefault();
  clearError();
  $("violations").hidden = true;
  $("add-topic").classList.remove("field-invalid");
  $("course").classList.remove("field-invalid");

  const body = {
    previewToken: preview.previewToken,
    title: $("title").value.trim(),
    course: $("course").value,
    topics: [...topics],
    summary: $("summary").value.trim(),
    confirmed: $("checked").checked,
  };
  try {
    const created = await confirmNote(body);
    $("done-hash").textContent = shortHash(created.noteHash);
    $("done-registered").textContent = formatDateTime(created.registeredAt);
    $("done-view-note").href = `index.html#not/${created.noteHash}`;
    $("done-copy").onclick = () => navigator.clipboard?.writeText(created.noteHash);
    show("done-view");
  } catch (err) {
    if (err.code === "shape_violation") showViolations(err.violations);
    else showError(err);
  }
}

function onCancel() {
  // Vazgeç: hiçbir istek gönderilmez, önizleme unutulur.
  preview = null;
  topics = [];
  clearError();
  startPick();
}

// ---------------------------------------------------------------------------
// Başlangıç
// ---------------------------------------------------------------------------

function setupDropzone() {
  const zone = $("dropzone");
  zone.addEventListener("dragover", (event) => {
    event.preventDefault();
    zone.classList.add("dragover");
  });
  zone.addEventListener("dragleave", () => zone.classList.remove("dragover"));
  zone.addEventListener("drop", (event) => {
    event.preventDefault();
    zone.classList.remove("dragover");
    onFile(event.dataTransfer.files[0]);
  });
  $("file-input").addEventListener("change", (event) => onFile(event.target.files[0]));
}

async function init() {
  try {
    vocabulary = await getVocabulary();
  } catch (err) {
    showError(err);
  }
  $("account-form").addEventListener("submit", onCreateAccount);
  $("change-account").addEventListener("click", () => {
    clearSession();
    startPick();
  });
  setupDropzone();
  $("course").addEventListener("change", onCourseChange);
  $("add-topic").addEventListener("change", onAddTopic);
  $("checked").addEventListener("change", () => {
    $("save").disabled = !$("checked").checked;
  });
  $("confirm-form").addEventListener("submit", onConfirm);
  $("cancel").addEventListener("click", onCancel);
  $("new-note").addEventListener("click", onCancel);
  startPick();
}

init();
