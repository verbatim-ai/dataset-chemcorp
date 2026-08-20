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

  ChatbotWidget.mountChatbotWidget("#verbatim-chatbot", {
    // Connection
    // apiBaseUrl: "https://staging-api.verbatim-ai.com",  // staging; default is production
    accessToken: ACCESS_TOKEN,
    corpusIds: CORPUS_IDS,
    lang: "en",

    // Content
    title: "ChemCorp Assistant",
    greeting: "Hi! Ask me anything about the ChemCorp corpus — invoices, product data " +
              "sheets, purchase orders, meeting minutes and strategy documents.",
    greetingOutside: true,
    chatPrompts: [
      "What is the total including VAT on invoice FC-2024-00187?",
      "What is the CAS number of acetone and its auto-ignition temperature?",
      "Which supplier received the highest-value purchase order?",
      "What are the 2024–2030 green-chemistry objectives?"
    ],

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
