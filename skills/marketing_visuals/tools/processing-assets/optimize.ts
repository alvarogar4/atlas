/**
 * Image Optimization Utility
 *
 * Optimizes images for web using Sharp. Converts to WebP by default for best compression.
 * Supports batch processing of directories.
 *
 * Usage:
 *   bun image:optimize <input|directory> [options]
 *
 * Options:
 *   --quality, -q    Quality 1-100 (default: 80)
 *   --lossless       Use lossless WebP compression (perfect quality, larger file)
 *   --keep-format    Keep original format instead of converting to WebP
 *   --output, -o     Output path (single file only)
 *
 * Examples:
 *   bun image:optimize hero.png                    # Convert to WebP at 80% quality
 *   bun image:optimize hero.png -q 60              # Lower quality, smaller file
 *   bun image:optimize hero.png --lossless         # Lossless WebP (perfect quality)
 *   bun image:optimize hero.png --keep-format      # Optimize PNG without format change
 *   bun image:optimize ./public/images             # Batch process directory
 *   bun image:optimize hero.png -o out.webp        # Custom output path
 */

import sharp from "sharp";
import { parse, join } from "node:path";
import { readdir, stat } from "node:fs/promises";

interface OptimizeOptions {
  inputPath: string;
  quality: number;
  lossless: boolean;
  keepFormat: boolean;
  outputPath?: string;
}

interface OptimizeResult {
  inputPath: string;
  outputPath: string;
  inputSize: number;
  outputSize: number;
  savings: number;
  savingsPercent: number;
}

type SupportedFormat = "png" | "jpeg" | "jpg" | "webp";

const SUPPORTED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp"];

function isSupportedImage(filename: string): boolean {
  const ext = parse(filename).ext.toLowerCase();
  return SUPPORTED_EXTENSIONS.includes(ext);
}

function getOutputPath(inputPath: string, keepFormat: boolean): string {
  const parsed = parse(inputPath);
  const ext = keepFormat ? parsed.ext : ".webp";
  const suffix = keepFormat ? "-optimized" : "";
  return join(parsed.dir, `${parsed.name}${suffix}${ext}`);
}

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}

async function optimizeImage(options: OptimizeOptions): Promise<OptimizeResult> {
  const { inputPath, quality, lossless, keepFormat, outputPath } = options;

  const inputStats = await stat(inputPath);
  const inputSize = inputStats.size;

  const finalOutputPath = outputPath || getOutputPath(inputPath, keepFormat);
  const parsed = parse(inputPath);
  const inputFormat = parsed.ext.toLowerCase().replace(".", "") as SupportedFormat;

  let pipeline = sharp(inputPath);

  if (keepFormat) {
    // Optimize in original format
    switch (inputFormat) {
      case "png":
        pipeline = pipeline.png({
          quality,
          compressionLevel: 9,
          palette: quality < 90,
        });
        break;
      case "jpg":
      case "jpeg":
        pipeline = pipeline.jpeg({
          quality,
          mozjpeg: true,
        });
        break;
      case "webp":
        pipeline = pipeline.webp({
          quality,
          effort: 6,
        });
        break;
    }
  } else {
    // Convert to WebP
    pipeline = pipeline.webp(
      lossless
        ? { lossless: true, effort: 6 }
        : { quality, effort: 6 }
    );
  }

  await pipeline.toFile(finalOutputPath);

  const outputStats = await stat(finalOutputPath);
  const outputSize = outputStats.size;
  const savings = inputSize - outputSize;
  const savingsPercent = (savings / inputSize) * 100;

  return {
    inputPath,
    outputPath: finalOutputPath,
    inputSize,
    outputSize,
    savings,
    savingsPercent,
  };
}

async function processDirectory(
  dirPath: string,
  quality: number,
  lossless: boolean,
  keepFormat: boolean
): Promise<void> {
  const entries = await readdir(dirPath, { withFileTypes: true });

  const imageFiles = entries.filter(
    (entry) =>
      entry.isFile() &&
      isSupportedImage(entry.name) &&
      !entry.name.includes("-optimized")
  );

  if (imageFiles.length === 0) {
    console.log("No supported images found (.png, .jpg, .jpeg, .webp)");
    return;
  }

  console.log(`Found ${imageFiles.length} images to optimize...\n`);

  let totalInputSize = 0;
  let totalOutputSize = 0;
  let successCount = 0;

  for (const file of imageFiles) {
    const inputPath = join(dirPath, file.name);
    try {
      const result = await optimizeImage({ inputPath, quality, lossless, keepFormat });
      totalInputSize += result.inputSize;
      totalOutputSize += result.outputSize;
      successCount++;

      const savedText =
        result.savings > 0
          ? `saved ${formatBytes(result.savings)} (${result.savingsPercent.toFixed(0)}%)`
          : `+${formatBytes(-result.savings)}`;

      console.log(
        `  ${file.name} -> ${parse(result.outputPath).base}  ${savedText}`
      );
    } catch (error) {
      console.error(
        `  ${file.name}: ${error instanceof Error ? error.message : String(error)}`
      );
    }
  }

  const totalSavings = totalInputSize - totalOutputSize;
  const totalPercent = (totalSavings / totalInputSize) * 100;

  console.log(`
Done! ${successCount}/${imageFiles.length} images optimized
Total: ${formatBytes(totalInputSize)} -> ${formatBytes(totalOutputSize)} (saved ${formatBytes(totalSavings)}, ${totalPercent.toFixed(0)}%)
`);
}

function parseArgs(args: readonly string[]): {
  input?: string;
  quality: number;
  lossless: boolean;
  keepFormat: boolean;
  output?: string;
} {
  let quality = 80;
  let lossless = false;
  let keepFormat = false;
  let output: string | undefined;
  let input: string | undefined;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg === "-q" || arg === "--quality") {
      quality = parseInt(args[++i], 10);
    } else if (arg === "--lossless") {
      lossless = true;
    } else if (arg === "--keep-format") {
      keepFormat = true;
    } else if (arg === "-o" || arg === "--output") {
      output = args[++i];
    } else if (!arg.startsWith("-")) {
      input = arg;
    }
  }

  return { input, quality, lossless, keepFormat, output };
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const { input, quality, lossless, keepFormat, output } = parseArgs(args);

  if (!input) {
    console.log(`
Image Optimization Utility - Compress images for web

Usage:
  bun image:optimize <input|directory> [options]

Options:
  --quality, -q    Quality 1-100 (default: 80)
  --lossless       Use lossless WebP compression (perfect quality, larger file)
  --keep-format    Keep original format instead of converting to WebP
  --output, -o     Output path (single file only)

Examples:
  bun image:optimize hero.png                    # Convert to WebP at 80% quality
  bun image:optimize hero.png -q 60              # Lower quality, smaller file
  bun image:optimize hero.png --lossless         # Lossless WebP (perfect quality)
  bun image:optimize hero.png --keep-format      # Optimize PNG without format change
  bun image:optimize ./public/images             # Batch process directory
  bun image:optimize hero.png -o out.webp        # Custom output path
`);
    process.exit(1);
  }

  if (quality < 1 || quality > 100 || isNaN(quality)) {
    console.error("Quality must be between 1 and 100");
    process.exit(1);
  }

  try {
    const stats = await stat(input);

    if (stats.isDirectory()) {
      if (output) {
        console.error("Cannot use --output with directory input");
        process.exit(1);
      }
      await processDirectory(input, quality, lossless, keepFormat);
    } else {
      console.log(`Optimizing ${input}...`);

      const result = await optimizeImage({
        inputPath: input,
        quality,
        lossless,
        keepFormat,
        outputPath: output,
      });

      const savedText =
        result.savings > 0
          ? `Saved ${formatBytes(result.savings)} (${result.savingsPercent.toFixed(0)}%)`
          : `Size increased by ${formatBytes(-result.savings)}`;

      console.log(`
Done!
  Input:  ${formatBytes(result.inputSize)}
  Output: ${formatBytes(result.outputSize)}
  ${savedText}
  File:   ${result.outputPath}
`);
    }
  } catch (error) {
    console.error(
      `Error: ${error instanceof Error ? error.message : String(error)}`
    );
    process.exit(1);
  }
}

main();
