/*
NOTEPROOF-FILE
module:   web
owner:    erdener         second: aysu
story:    S7
contract: 02#6 proof dosyası, 02#7 GET /api/notes/{hash}/proof
depends:  web/js/api.js
status:   wip
*/
/**
 * Proof sayfası (web/proof.html). Hesap gerekmez.
 *
 * Kanıt iki yoldan okunur: bağlantıdaki hash ile sunucudan (proof.html?hash=…) ya da kullanıcının
 * seçtiği yerel proof dosyasından. Sunucuya ulaşılamazsa sayfa yerel dosyaya yönlendirir; böylece
 * arşivin sunucusu kapalıyken de çalışır (S7).
 *
 * Bu iskelette kanıt dosyası okunur ve alanları gösterilir. Hash ve Merkle doğrulaması (verify.js)
 * ERD-2'de, ağaç çizimi ve zincir kontrolü (chain.js) ERD-3'te eklenir.
 */

import { getProof } from "./api.js";
import { errorText, formatDateTime, shortHash } from "./helpers.js";

const $ = (id) => document.getElementById(id);
const HEX64 = /^[0-9a-f]{64}$/;
const params = new URLSearchParams(location.search);
const linkHash = HEX64.test(params.get("hash") ?? "") ? params.get("hash") : null;

function showError(text) {
  $("error").textContent = text;
  $("error").hidden = false;
}

function selectSource(source) {
  $(source === "server" ? "source-server" : "source-local").checked = true;
  $("proof-file").disabled = source !== "local";
  $("proof-file-button").setAttribute("aria-disabled", String(source !== "local"));
}

/** Seçilen dosyanın adını düğmenin yanında gösterir (tarayıcının kendi metni dile göre değişir). */
function showFileName(inputId, labelId) {
  $(inputId).addEventListener("change", () => {
    $(labelId).textContent = $(inputId).files[0]?.name ?? "Dosya seçilmedi";
  });
}

/** Proof dosyasının 02 bölüm 6'daki biçime uyup uymadığına kaba bir bakış. Asıl kontrol verify.js'te. */
function looksLikeProof(proof) {
  return (
    proof &&
    HEX64.test(proof.noteHash ?? "") &&
    HEX64.test(proof.merkleRoot ?? "") &&
    Array.isArray(proof.merklePath) &&
    proof.merklePath.every((s) => (s.side === "left" || s.side === "right") && HEX64.test(s.sibling ?? ""))
  );
}

async function readLocalProof(file) {
  try {
    return JSON.parse(await file.text());
  } catch {
    return null;
  }
}

async function loadProof() {
  if ($("source-server").checked) {
    try {
      return await getProof(linkHash);
    } catch (err) {
      if (err.code === "network") {
        selectSource("local");
        showError("Sunucuya ulaşılamadı. Kanıt dosyan varsa bilgisayarından seç.");
      } else {
        showError(errorText(err.code));
      }
      return null;
    }
  }
  const file = $("proof-file").files[0];
  if (!file) {
    showError("Kanıt dosyasını seç.");
    return null;
  }
  return readLocalProof(file);
}

function renderProof(proof) {
  $("verdict").textContent = "Kanıt dosyası okundu. Dosyanın bu kanıtla doğrulanması bir sonraki sürümde eklenecek.";
  $("r-hash").textContent = shortHash(proof.noteHash);
  $("r-network").textContent = proof.network ?? "—";
  $("r-block").textContent = Number.isInteger(proof.blockHeight) ? `#${proof.blockHeight.toLocaleString("tr")}` : "—";
  $("r-time").textContent = formatDateTime(proof.blockTime);
  $("r-txid").textContent = shortHash(proof.txid ?? "");
  $("r-path").replaceChildren(
    ...proof.merklePath.map((step) => {
      const li = document.createElement("li");
      li.textContent = `${step.side === "left" ? "sol" : "sağ"} kardeş: ${shortHash(step.sibling)}`;
      return li;
    }),
  );
  $("r-root").textContent = shortHash(proof.merkleRoot);
  $("result").hidden = false;
}

async function onSubmit(event) {
  event.preventDefault();
  $("error").hidden = true;
  $("result").hidden = true;
  if (!$("note-file").files[0]) {
    showError("Not dosyasını seç.");
    return;
  }
  const proof = await loadProof();
  if (!proof) return;
  if (!looksLikeProof(proof)) {
    showError("Kanıt dosyası okunamadı. NoteProof'tan indirilen .json dosyasını seç.");
    return;
  }
  // ERD-2: verifyProof(fileBytes, proof) → {ok, reason}; Kanıtlandı / Değiştirilmiş rozeti.
  renderProof(proof);
}

function init() {
  if (linkHash) {
    $("server-hash").textContent = `(${shortHash(linkHash)})`;
    selectSource("server");
  } else {
    $("source-server").disabled = true;
    selectSource("local");
  }
  for (const radio of document.querySelectorAll('input[name="source"]')) {
    radio.addEventListener("change", () => selectSource(radio.value));
  }
  showFileName("note-file", "note-file-name");
  showFileName("proof-file", "proof-file-name");
  $("proof-form").addEventListener("submit", onSubmit);
}

init();
