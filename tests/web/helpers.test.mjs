/*
NOTEPROOF-FILE
module:   tests/web
owner:    erdener         second: burak
story:    S5, S7
contract: -
depends:  web/js/helpers.js
status:   wip
*/
// Arayüz yardımcılarının testleri: tarih ve hash biçimi, konu ağacı ve alt konular (S5), hata metinleri.
// Çalıştırma (repo kökünde): node --test tests/web/

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

import {
  badgeText,
  errorText,
  findCourse,
  formatDate,
  formatDateTime,
  labelFor,
  shortHash,
  topicTree,
  topicWithNarrower,
} from "../../web/js/helpers.js";

const vocabulary = JSON.parse(readFileSync(new URL("../../web/mock/vocabulary.json", import.meta.url), "utf8"));
const course = findCourse(vocabulary, "Course_SEN0401");

test("tarih taslaktaki biçimde ve yerel saatte gösterilir", () => {
  assert.equal(formatDateTime("2026-11-24T11:05:00+00:00", "Europe/Istanbul"), "24 Kas 2026, 14:05");
  assert.equal(formatDate("2026-01-03T22:30:00+00:00", "Europe/Istanbul"), "4 Oca 2026");
  assert.equal(formatDate("geçersiz"), "—");
});

test("hash ilk 4 ve son 4 karakterle kısaltılır", () => {
  assert.equal(shortHash("3f9a" + "0".repeat(56) + "c21e"), "3f9a...c21e");
});

test("ekranda kimlik değil Türkçe etiket görünür", () => {
  assert.equal(labelFor(vocabulary, "Topic_FeeRate"), "Ücret oranı");
  assert.equal(labelFor(vocabulary, "Course_SEN0401"), "SEN 401 Blockchain");
  assert.equal(labelFor(vocabulary, "Topic_Unknown"), "Topic_Unknown");
});

test("konu ağacı alt konuları üst konunun altında ve girintili sıralar", () => {
  const tree = topicTree(course);
  const ids = tree.map((t) => t.id);
  assert.ok(ids.indexOf("Topic_Transactions") < ids.indexOf("Topic_TransactionFees"));
  assert.ok(ids.indexOf("Topic_TransactionFees") < ids.indexOf("Topic_FeeRate"));
  assert.equal(tree.find((t) => t.id === "Topic_FeeRate").depth, 2);
  assert.equal(tree.length, course.topics.length);
});

test("s5 konu araması alt konuları da kapsar (skos:narrower*)", () => {
  const ids = topicWithNarrower(course, "Topic_Transactions");
  assert.deepEqual([...ids].sort(), ["Topic_FeeRate", "Topic_TransactionFees", "Topic_Transactions"]);
  assert.deepEqual([...topicWithNarrower(course, "Topic_FeeRate")], ["Topic_FeeRate"]);
});

test("hata metinleri koda göre Türkçe; bilinmeyen kod için genel metin", () => {
  assert.equal(errorText("too_large"), "Dosya 10 MB'tan büyük.");
  assert.match(errorText("başka_bir_kod"), /Beklenmeyen bir hata/);
});

test("rozet metinleri 02 bölüm 3'teki gibi", () => {
  assert.equal(badgeText("pending"), "Beklemede");
  assert.equal(badgeText("proven"), "Kanıtlandı");
});
