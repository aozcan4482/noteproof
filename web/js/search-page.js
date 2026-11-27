/*
NOTEPROOF-FILE
module:   web
owner:    erdener         second: aysu
story:    S5, S6
contract: 02#7 GET /api/vocabulary, GET /api/search, GET /api/notes/{hash}
depends:  web/js/api.js
status:   wip
*/
/**
 * Arama sayfası (web/index.html): ders ve konu süzgeçleri, not kartları, kart ayrıntısı.
 * Ayrıntı aynı sayfada ayrı bir görünümdür; adres "#not/<hash>" olur, geri tuşu listeye döner.
 * Yazar olarak yalnızca takma ad gösterilir; kopya için metin her zaman "Olası kopya"dır.
 */

import { getVocabulary, searchNotes, getNote } from "./api.js";
import {
  badgeText,
  errorText,
  findCourse,
  formatDate,
  formatDateTime,
  labelFor,
  shortHash,
  topicTree,
} from "./helpers.js";

const $ = (id) => document.getElementById(id);
let vocabulary = { courses: [] };

function el(tag, attrs = {}, text) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
  if (text !== undefined) node.textContent = text;
  return node;
}

function badge(proofStatus) {
  return el("span", { class: `badge ${proofStatus === "proven" ? "proven" : "pending"}` }, badgeText(proofStatus));
}

/** "Olası kopya" satırı: hüküm vermez, önceki notun proof sayfasına bağlanır. */
function copyNote(possibleCopyOf) {
  const box = el("div", { class: "copy-note" });
  box.append("! Olası kopya → ");
  box.append(el("a", { href: `proof.html?hash=${encodeURIComponent(possibleCopyOf)}` }, "önceki notun kanıtı"));
  return box;
}

function courseLine(card) {
  const topics = card.topics.map((t) => labelFor(vocabulary, t)).join(", ");
  return `${labelFor(vocabulary, card.course)} · ${topics}`;
}

// ---------------------------------------------------------------------------
// Süzgeçler
// ---------------------------------------------------------------------------

function fillCourses() {
  const select = $("course");
  for (const course of vocabulary.courses) select.append(el("option", { value: course.id }, course.labelTr));
}

function fillTopics() {
  const select = $("topic");
  select.replaceChildren(el("option", { value: "" }, "Bütün konular"));
  const course = findCourse(vocabulary, $("course").value);
  select.disabled = !course;
  if (!course) return;
  for (const item of topicTree(course)) {
    // Alt konular girintiyle gösterilir; girinti için bölünmez boşluk kullanılır.
    select.append(el("option", { value: item.id }, `${"   ".repeat(item.depth)}${item.label}`));
  }
}

// ---------------------------------------------------------------------------
// Sonuç listesi
// ---------------------------------------------------------------------------

function renderResults(results) {
  const list = $("results");
  list.replaceChildren();
  $("result-count").textContent = results.length ? `${results.length} not bulundu` : "";
  $("empty").hidden = results.length > 0;

  for (const card of results) {
    const item = el("li", { class: "card" });
    const link = el("a", { class: "card-link", href: `#not/${card.noteHash}` });
    link.append(
      el("p", { class: "card-title" }, card.title),
      el("p", { class: "meta" }, courseLine(card)),
      el("p", { class: "meta" }, `@${card.author} · ${formatDate(card.registeredAt)}`),
      badge(card.proofStatus),
    );
    item.append(link);
    if (card.possibleCopyOf) item.append(copyNote(card.possibleCopyOf));
    list.append(item);
  }
}

async function runSearch() {
  $("search-error").hidden = true;
  try {
    const { results } = await searchNotes({ course: $("course").value, topic: $("topic").value, q: $("q").value.trim() });
    renderResults(results);
  } catch (err) {
    renderResults([]);
    $("empty").hidden = true;
    $("search-error").textContent = errorText(err.code);
    $("search-error").hidden = false;
  }
}

// ---------------------------------------------------------------------------
// Ayrıntı görünümü
// ---------------------------------------------------------------------------

async function showDetail(noteHash) {
  $("search-view").hidden = true;
  $("detail-view").hidden = false;
  $("detail").hidden = true;
  $("detail-error").hidden = true;
  $("d-copy-status").textContent = "";

  let card;
  try {
    card = await getNote(noteHash);
  } catch (err) {
    $("detail-error").textContent = errorText(err.code);
    $("detail-error").hidden = false;
    return;
  }

  $("d-title").textContent = card.title;
  $("d-course").textContent = labelFor(vocabulary, card.course);
  $("d-topics").replaceChildren(...card.topics.map((t) => el("li", { class: "chip static" }, labelFor(vocabulary, t))));
  $("d-summary").textContent = card.summary;
  $("d-author").textContent = `@${card.author}`;
  $("d-registered").textContent = formatDateTime(card.registeredAt);

  const proven = card.proofStatus === "proven";
  $("d-badge").replaceWith(Object.assign(badge(card.proofStatus), { id: "d-badge" }));
  $("d-proof-text").textContent = proven
    ? "Bu dosya Bitcoin'e damgalandı. Kanıtı hesap açmadan kontrol edebilirsin."
    : "Kayıt alındı. Kanıt, günlük zaman damgasından (23:00) sonra hazır olur.";
  $("d-proof-link").hidden = !proven;
  $("d-proof-link").href = `proof.html?hash=${encodeURIComponent(card.noteHash)}`;

  const copy = $("d-copy");
  copy.hidden = !card.possibleCopyOf;
  if (card.possibleCopyOf) copy.replaceChildren(...copyNote(card.possibleCopyOf).childNodes);

  $("d-hash").textContent = shortHash(card.noteHash);
  $("d-copy-hash").onclick = async () => {
    try {
      await navigator.clipboard.writeText(card.noteHash);
      $("d-copy-status").textContent = "Hash kopyalandı.";
    } catch {
      $("d-copy-status").textContent = card.noteHash;
    }
  };
  $("detail").hidden = false;
}

function showList() {
  $("detail-view").hidden = true;
  $("search-view").hidden = false;
}

function route() {
  const match = location.hash.match(/^#not\/([0-9a-f]{64})$/);
  if (match) showDetail(match[1]);
  else showList();
}

// ---------------------------------------------------------------------------
// Başlangıç
// ---------------------------------------------------------------------------

async function init() {
  try {
    vocabulary = await getVocabulary();
  } catch (err) {
    $("search-error").textContent = errorText(err.code);
    $("search-error").hidden = false;
  }
  fillCourses();
  $("course").addEventListener("change", fillTopics);
  $("search-form").addEventListener("submit", (event) => {
    event.preventDefault();
    runSearch();
  });
  $("reset-filters").addEventListener("click", () => {
    $("search-form").reset();
    fillTopics();
    runSearch();
  });
  window.addEventListener("hashchange", route);
  route();
  runSearch();
}

init();
