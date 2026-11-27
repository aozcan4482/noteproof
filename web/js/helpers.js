/*
NOTEPROOF-FILE
module:   web
owner:    erdener         second: aysu
story:    S5, S6, S7
contract: -
depends:  -
status:   wip
*/
/**
 * Sayfaların ortak yardımcıları: tarih ve hash biçimi, sözlükten konu ağacı, hata metinleri.
 * Ağa çıkmaz ve DOM'a dokunmaz; bu yüzden node --test ile doğrudan test edilir (tests/web/).
 */

const MONTHS_TR = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"];

/**
 * Zaman alanlarını (registeredAt, blockTime; ISO 8601, UTC) yerel saate çevirir.
 * Taslaktaki biçim: "24 Kas 2026, 14:05". timeZone verilmezse tarayıcının saat dilimi kullanılır.
 */
function dateParts(iso, timeZone) {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return null;
  const fmt = new Intl.DateTimeFormat("en-GB", {
    timeZone,
    year: "numeric",
    month: "numeric",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hourCycle: "h23",
  });
  const parts = Object.fromEntries(fmt.formatToParts(date).map((p) => [p.type, p.value]));
  return {
    day: String(Number(parts.day)),
    month: MONTHS_TR[Number(parts.month) - 1],
    year: parts.year,
    time: `${parts.hour}:${parts.minute}`,
  };
}

export function formatDate(iso, timeZone) {
  const p = dateParts(iso, timeZone);
  return p ? `${p.day} ${p.month} ${p.year}` : "—";
}

export function formatDateTime(iso, timeZone) {
  const p = dateParts(iso, timeZone);
  return p ? `${p.day} ${p.month} ${p.year}, ${p.time}` : "—";
}

/** Uzun hash'i ekranda "3f9a...c21e" biçiminde kısaltır; tamamı Kopyala ile alınır. */
export function shortHash(hex) {
  if (typeof hex !== "string" || hex.length <= 12) return hex ?? "";
  return `${hex.slice(0, 4)}...${hex.slice(-4)}`;
}

/** Sözlükteki bir dersi kimliğiyle bulur (GET /api/vocabulary yanıtı). */
export function findCourse(vocabulary, courseId) {
  return vocabulary.courses.find((c) => c.id === courseId) ?? null;
}

/**
 * Kimliğin ekranda gösterilecek Türkçe etiketi. Ekranda kimlik (Topic_FeeRate) değil etiket görünür.
 * Sözlükte yoksa kimliğin kendisi döner; böylece eksik veri sessizce kaybolmaz.
 */
export function labelFor(vocabulary, conceptId) {
  for (const course of vocabulary.courses) {
    if (course.id === conceptId) return course.labelTr;
    const topic = course.topics.find((t) => t.id === conceptId);
    if (topic) return topic.labelTr;
  }
  return conceptId;
}

/**
 * Dersin konularını ağaç sırasıyla ve derinlikleriyle döndürür (konu seçimindeki girinti için).
 * Üst kavram `broader` alanından okunur; dersin doğrudan konularının `broader` değeri dersin kimliğidir.
 */
export function topicTree(course) {
  const children = new Map();
  for (const topic of course.topics) {
    const parent = course.topics.some((t) => t.id === topic.broader) ? topic.broader : course.id;
    if (!children.has(parent)) children.set(parent, []);
    children.get(parent).push(topic);
  }
  const out = [];
  const walk = (parentId, depth) => {
    for (const topic of children.get(parentId) ?? []) {
      out.push({ id: topic.id, label: topic.labelTr, depth });
      walk(topic.id, depth + 1);
    }
  };
  walk(course.id, 0);
  return out;
}

/** Konunun kendisi ve bütün alt konuları (skos:narrower* ile aynı anlam). */
export function topicWithNarrower(course, topicId) {
  const ids = new Set([topicId]);
  let grew = true;
  while (grew) {
    grew = false;
    for (const topic of course.topics) {
      if (ids.has(topic.broader) && !ids.has(topic.id)) {
        ids.add(topic.id);
        grew = true;
      }
    }
  }
  return ids;
}

/**
 * API hata kodundan (error.code) kullanıcıya gösterilecek Türkçe metin.
 * API'nin `message` alanı ekrana basılmaz (erdener tasarım notları).
 */
const ERROR_TEXTS = {
  unsupported_type: "Bu dosya türü desteklenmiyor. PDF, JPEG, PNG ya da metin dosyası yükle.",
  too_large: "Dosya 10 MB'tan büyük.",
  not_confirmed: "Kaydetmeden önce etiketleri kontrol ettiğini işaretle.",
  unauthorized: "Oturumun bulunamadı. Takma adınla yeniden hesap oluştur.",
  not_found: "Bu not bulunamadı.",
  proof_pending: "Bu notun kanıtı henüz hazır değil.",
  preview_expired: "Önizlemenin süresi doldu. Dosyayı yeniden yükle.",
  shape_violation: "Etiketler kurallara uymuyor. Konuyu listeden seç.",
  network: "Sunucuya ulaşılamadı. Biraz sonra yeniden dene.",
};

export function errorText(code) {
  return ERROR_TEXTS[code] ?? "Beklenmeyen bir hata oldu. Biraz sonra yeniden dene.";
}

/** Proof durumunun rozet metni (02 bölüm 3). */
export function badgeText(proofStatus) {
  if (proofStatus === "proven") return "Kanıtlandı";
  if (proofStatus === "pending") return "Beklemede";
  return "Değiştirilmiş";
}
