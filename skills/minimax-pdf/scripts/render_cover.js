#!/usr/bin/env node
/**
 * render_cover.js — Render cover.html → cover.pdf via Playwright.
 *
 * Usage:
 *   node render_cover.js --input cover.html --out cover.pdf
 *   node render_cover.js --input cover.html --out cover.pdf --wait 1200
 *
 * Exit codes: 0 success, 1 bad args, 2 dependency missing, 3 render error
 */

const path = require("path");
const fs   = require("fs");

function usage() {
  console.error("Usage: node render_cover.js --input <file.html> --out <file.pdf> [--wait <ms>]");
  process.exit(1);
}

// ── Arg parsing ────────────────────────────────────────────────────────────────
const args = process.argv.slice(2);
let inputFile = null, outFile = null, waitMs = 800;

for (let i = 0; i < args.length; i++) {
  if (args[i] === "--input" && args[i + 1]) { inputFile = args[++i]; }
  else if (args[i] === "--out"   && args[i + 1]) { outFile   = args[++i]; }
  else if (args[i] === "--wait"  && args[i + 1]) { waitMs    = parseInt(args[++i], 10); }
}

if (!inputFile || !outFile) usage();
if (!fs.existsSync(inputFile)) {
  console.error(JSON.stringify({ status: "error", error: `File not found: ${inputFile}` }));
  process.exit(1);
}

// ── Playwright loader (safe for plugin distribution) ──────────────────────────
function loadPlaywright() {
  try { return require("playwright"); } catch (_) {}
  console.error(JSON.stringify({
    status: "error",
    error: "playwright not found",
    hint: "Install Playwright in the host environment before using minimax-pdf"
  }));
  process.exit(2);
}

function findBrowserExecutable() {
  const candidates = [
    process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE,
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
  ].filter(Boolean);

  for (const candidate of candidates) {
    try {
      fs.accessSync(candidate, fs.constants.X_OK);
      return candidate;
    } catch (_) {}
  }
  return null;
}

// ── Main ───────────────────────────────────────────────────────────────────────
(async () => {
  const { chromium } = loadPlaywright();
  const executablePath = findBrowserExecutable();

  let browser;
  try {
    browser = executablePath
      ? await chromium.launch({ executablePath })
      : await chromium.launch();
  } catch (e) {
    console.error(JSON.stringify({
      status: "error",
      error: "Chromium could not be launched",
      hint: "Install a supported browser or set PLAYWRIGHT_CHROMIUM_EXECUTABLE in the host environment"
    }));
    process.exit(2);
  }

  try {
    const page = await browser.newPage();
    const fileUrl = "file://" + path.resolve(inputFile);
    await page.goto(fileUrl);
    await page.waitForTimeout(waitMs);   // let CSS + any JS settle

    await page.pdf({
      path:            outFile,
      width:           "794px",
      height:          "1123px",
      printBackground: true,
    });

    await browser.close();

    // Basic sanity: output file must exist and be > 5 KB
    const stat = fs.statSync(outFile);
    if (stat.size < 5000) {
      console.error(JSON.stringify({
        status: "error",
        error: "Output PDF is suspiciously small — cover may be blank",
        hint:  "Check cover.html for render errors"
      }));
      process.exit(3);
    }

    console.log(JSON.stringify({
      status: "ok",
      out:    outFile,
      size_kb: Math.round(stat.size / 1024),
    }));

  } catch (e) {
    if (browser) await browser.close().catch(() => {});
    console.error(JSON.stringify({ status: "error", error: String(e) }));
    process.exit(3);
  }
})();
