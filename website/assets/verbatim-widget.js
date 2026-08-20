/* Verbatim AI chatbot widget — configuration for the ChemCorp demo site.
 *
 * HAND-MAINTAINED FILE. gen_website.py creates it once if missing and never
 * overwrites it, so your credentials survive every rebuild. To get a fresh
 * copy of this template, delete the file and re-run gen_website.py.
 *
 * Docs: https://verbatim-ai.gitbook.io/docs
 */
(function () {
  // --- Fill these in ------------------------------------------------------
  // Token needs 4 scopes: session:read, session:create, post:read, post:create
  var ACCESS_TOKEN = "YOUR_ACCESS_TOKEN";
  var CORPUS_IDS   = ["YOUR_CORPUS_ID"];   // at least one corpus id
  // ------------------------------------------------------------------------

  // French browsers ("fr", "fr-CA", …) get the French widget; everyone else English.
  function browserLang() {
    var tag = (navigator.languages && navigator.languages[0]) || navigator.language || "";
    return String(tag).toLowerCase().split("-")[0] === "fr" ? "fr" : "en";
  }

  // Per-language branding, picked by browserLang() at mount time.
  var COPY = {
    en: {
      title: "ChemCorp Assistant",
      greeting: "Hi! Ask me anything about the ChemCorp corpus — invoices, product data " +
                "sheets, purchase orders, meeting minutes and strategy documents.",
      chatPrompts: [
        "What is the total including VAT on invoice FC-2024-00187?",
        "What is the CAS number of acetone and its auto-ignition temperature?",
        "Which supplier received the highest-value purchase order?",
        "What are the 2024–2030 green-chemistry objectives?"
      ]
    },
    fr: {
      title: "Assistant ChemCorp",
      greeting: "Bonjour ! Posez-moi toutes vos questions sur le corpus ChemCorp — factures, " +
                "fiches produits, bons de commande, comptes rendus de réunion et documents " +
                "stratégiques.",
      chatPrompts: [
        "Quel est le total TTC de la facture FC-2024-00187 ?",
        "Quel est le numéro CAS de l'acétone et sa température d'auto-inflammation ?",
        "Quel fournisseur a reçu le bon de commande le plus élevé ?",
        "Quels sont les objectifs de chimie verte 2024–2030 ?"
      ]
    }
  };

  if (typeof ChatbotWidget === "undefined") {
    console.warn("[chemcorp] Verbatim widget bundle did not load — skipping mount.");
    return;
  }
  if (!ACCESS_TOKEN || ACCESS_TOKEN === "YOUR_ACCESS_TOKEN" ||
      !CORPUS_IDS.length || CORPUS_IDS[0] === "YOUR_CORPUS_ID") {
    console.info("[chemcorp] Verbatim widget not configured yet — set ACCESS_TOKEN " +
                 "and CORPUS_IDS in website/assets/verbatim-widget.js.");
    return;
  }

  var lang = browserLang();
  var copy = COPY[lang];

  ChatbotWidget.mountChatbotWidget("#verbatim-chatbot", {
    // Connection
    // apiBaseUrl: "https://staging-api.verbatim-ai.com",  // staging; default is production
    accessToken: ACCESS_TOKEN,
    corpusIds: CORPUS_IDS,
    lang: lang,

    // Content
    title: copy.title,
    greeting: copy.greeting,
    greetingOutside: true,
    chatPrompts: copy.chatPrompts,

    // Appearance — tracks the site accent (--accent #1c5cab, --series-1 #2a78d6)
    theme: {
      preset: "boring",
      tokens: {
        headerBackground: "linear-gradient(90deg, #1c5cab, #2a78d6)",
        openButtonBackground: "#1c5cab",
        openButtonColor: "#ffffff",
        badgeBackground: "#8a4b12"
      }
    }
  });
})();
