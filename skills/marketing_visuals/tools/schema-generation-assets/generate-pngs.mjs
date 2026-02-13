import { chromium } from "playwright";
import { join, resolve } from "path";
import { readdir } from "fs/promises";

// Target directory passed as argument, or current working directory
const targetDir = resolve(process.argv[2] || process.cwd());

async function generatePNGs() {
  console.log(`Target directory: ${targetDir}`);

  const browser = await chromium.launch();

  const files = await readdir(targetDir);
  const htmlFiles = files.filter(
    (f) => f.endsWith(".html") && !f.startsWith("_"),
  );

  if (htmlFiles.length === 0) {
    console.log("No HTML files found to convert.");
    await browser.close();
    return;
  }

  console.log(`Found ${htmlFiles.length} HTML file(s) to convert...`);

  for (const htmlFile of htmlFiles) {
    const htmlPath = join(targetDir, htmlFile);
    const pngPath = htmlPath.replace(".html", ".png");

    console.log(`Converting: ${htmlFile}`);

    // First, load page to get body dimensions
    const tempContext = await browser.newContext({
      viewport: { width: 1920, height: 1200 },
    });
    const tempPage = await tempContext.newPage();
    await tempPage.goto(`file://${htmlPath}`);

    const dimensions = await tempPage.evaluate(() => {
      const body = document.body;
      const style = window.getComputedStyle(body);
      return {
        width: parseInt(style.width) || body.offsetWidth,
        height: parseInt(style.height) || body.offsetHeight,
      };
    });
    await tempPage.close();
    await tempContext.close();

    console.log(`  Dimensions: ${dimensions.width}x${dimensions.height}`);

    // Now create context with correct viewport
    const context = await browser.newContext({
      viewport: { width: dimensions.width, height: dimensions.height },
      deviceScaleFactor: 2, // 2x for retina quality
    });
    const page = await context.newPage();
    await page.goto(`file://${htmlPath}`);
    await page.waitForTimeout(500); // Wait for any animations/fonts to settle

    await page.screenshot({
      path: pngPath,
      type: "png",
    });

    await page.close();
    await context.close();
    console.log(`  → ${htmlFile.replace(".html", ".png")}`);
  }

  await browser.close();
  console.log("\nDone! Generated PNGs:");
  htmlFiles.forEach((f) => console.log(`  - ${f.replace(".html", ".png")}`));
}

generatePNGs().catch(console.error);
