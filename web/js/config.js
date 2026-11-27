/*
NOTEPROOF-FILE
module:   web
owner:    erdener         second: aysu
story:    S1, S3, S4, S5, S6, S7
contract: 02#7 HTTP API (taban yol)
depends:  -
status:   wip
*/
/**
 * Arayüzün bütün adresleri ve anahtarları burada durur (03 bölüm 6).
 * Başka hiçbir dosyada adres yazılmaz; ağ çağrıları api.js ve chain.js'tedir.
 */

/** Kayıt servisinin (Arda, register/app.py) taban yolu. Sayfalar aynı sunucudan açılır. */
export const API_BASE = "/api";

/**
 * Sahte veri anahtarı. true iken api.js gerçek API yerine web/mock/*.json dosyalarını okur.
 * Kayıt servisi main'e girene kadar (ARD-3, ARD-4) açık kalır; Faz 2 entegrasyonunda false yapılır.
 */
export const USE_MOCK = true;

/** Sahte yanıtların klasörü; sayfalara göre göreli. */
export const MOCK_BASE = "./mock";

/**
 * Public signet API'sinin adresi (proof sayfasının zincir kontrolü, ERD-3).
 * NP-DECISION(K-008): hangi servisin kullanılacağı ve CORS izni henüz açık.
 * NP-TODO(burak): K-008 kararıyla doğrulanmış public signet API adresi.
 */
export const SIGNET_API_BASE = null;

/**
 * İşlemi tarayıcıda açan public signet gezgininin adresi; sonuna txid eklenir.
 * NP-TODO(burak): K-008 kararıyla birlikte gelecek.
 */
export const SIGNET_EXPLORER_TX_URL = null;

/** En büyük dosya boyutu (K-006). Sunucu da denetler; burada yalnızca erken uyarı içindir. */
export const MAX_UPLOAD_BYTES = 10 * 1024 * 1024;

/** Kabul edilen dosya türleri (K-006). */
export const ALLOWED_TYPES = ["application/pdf", "image/jpeg", "image/png", "text/plain", "text/markdown"];

/** Takma ad ve token'ın tarayıcıda saklandığı anahtar (K-007). */
export const SESSION_STORAGE_KEY = "noteproof.session";
