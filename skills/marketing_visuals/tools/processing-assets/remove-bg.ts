/**
 * Background Removal Utility
 *
 * Removes background from images using AI-powered detection.
 * Outputs PNG format with transparency.
 *
 * NOTE: First run downloads AI models (~30MB) which may take time.
 * Subsequent runs are faster but still computationally intensive.
 *
 * Usage:
 *   bun image:remove-bg <input|directory> [output]
 *
 * Arguments:
 *   input   Path to input image or directory of images
 *   output  Optional output path (single file only, defaults to input_nobg.png)
 *
 * Examples:
 *   bun image:remove-bg photo.png                    # Single file
 *   bun image:remove-bg photo.png transparent.png    # Custom output
 *   bun image:remove-bg ./portraits                  # Batch process directory
 */

import { removeBackground, type Config } from "@imgly/background-removal-node";
import { writeFile, readdir, stat } from "node:fs/promises";
import { parse, join, dirname, resolve } from "node:path";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const distPath = dirname(require.resolve("@imgly/background-removal-node"));

const config: Config = {
  publicPath: `file://${distPath}/`,
};

const SUPPORTED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp"];

function isSupportedImage(filename: string): boolean {
  const ext = parse(filename).ext.toLowerCase();
  return SUPPORTED_EXTENSIONS.includes(ext);
}

/**
 * Remove background from a single image
 */
export async function removeBg(
  inputPath: string,
  outputPath?: string
): Promise<string> {
  const parsed = parse(inputPath);
  const output = outputPath ?? join(parsed.dir, `${parsed.name}_nobg.png`);

  // Resolve to absolute path and use file:// URL for local files
  const absolutePath = resolve(inputPath);
  const inputUrl = `file://${absolutePath}`;

  const resultBlob = await removeBackground(inputUrl, config);

  const arrayBuffer = await resultBlob.arrayBuffer();
  await writeFile(output, new Uint8Array(arrayBuffer));

  return output;
}

/**
 * Process all images in a directory
 */
async function processDirectory(dirPath: string): Promise<void> {
  const entries = await readdir(dirPath, { withFileTypes: true });

  const imageFiles = entries.filter(
    (entry) =>
      entry.isFile() &&
      isSupportedImage(entry.name) &&
      !entry.name.includes("_nobg")
  );

  if (imageFiles.length === 0) {
    console.log("No supported images found (.png, .jpg, .jpeg, .webp)");
    return;
  }

  console.log(`Found ${imageFiles.length} images to process...\n`);
  console.log("Note: Background removal is computationally intensive.\n");

  let successCount = 0;

  for (let i = 0; i < imageFiles.length; i++) {
    const file = imageFiles[i];
    const inputPath = join(dirPath, file.name);
    const progress = `[${i + 1}/${imageFiles.length}]`;

    try {
      console.log(`${progress} Processing ${file.name}...`);
      const outputPath = await removeBg(inputPath);
      console.log(`  -> ${parse(outputPath).base}`);
      successCount++;
    } catch (error) {
      console.error(
        `  Error: ${error instanceof Error ? error.message : String(error)}`
      );
    }
  }

  console.log(`\nDone! ${successCount}/${imageFiles.length} images processed.`);
}

function printHelp(): void {
  console.log(`
Background Removal Utility - Remove backgrounds using AI

Usage:
  bun image:remove-bg <input|directory> [output]

Arguments:
  input   Path to input image or directory of images
  output  Optional output path (single file only, defaults to input_nobg.png)

Note: First run downloads AI models (~30MB) which may take time.
Subsequent runs are faster but still computationally intensive.

Examples:
  bun image:remove-bg photo.png                    # Single file
  bun image:remove-bg photo.png transparent.png    # Custom output
  bun image:remove-bg ./portraits                  # Batch process directory
`);
}

async function main(): Promise<void> {
  const [inputPath, outputPath] = process.argv.slice(2);

  if (!inputPath) {
    printHelp();
    process.exit(1);
  }

  try {
    const stats = await stat(inputPath);

    if (stats.isDirectory()) {
      if (outputPath) {
        console.error("Error: Cannot use output path with directory input");
        process.exit(1);
      }
      await processDirectory(inputPath);
    } else {
      console.log("Processing (this may take a moment on first run)...");
      const result = await removeBg(inputPath, outputPath);
      console.log(`Saved: ${result}`);
    }
  } catch (error) {
    console.error(
      `Error: ${error instanceof Error ? error.message : String(error)}`
    );
    process.exit(1);
  }
}

main();
