/**
 * Image Polish Utility
 *
 * Enhances images with brightness, contrast, saturation, and sharpening adjustments.
 * All adjustments use multipliers where 1.0 = no change.
 *
 * Usage:
 *   bun polish <input|directory> [options]
 *
 * Options:
 *   --brightness, -b    Brightness multiplier (0.5-2.0, default: 1.0)
 *   --contrast, -c      Contrast multiplier (0.5-2.0, default: 1.0)
 *   --saturation, -s    Saturation multiplier (0.0-2.0, default: 1.0)
 *   --sharpen           Apply sharpening (sigma value 0.5-5.0, default: off)
 *   --auto              Auto-enhance: normalize contrast + light sharpen
 *   --output, -o        Output path (single file only)
 *
 * Examples:
 *   bun polish photo.png --brightness 1.1           # Slightly brighter
 *   bun polish photo.png --contrast 1.2             # More contrast
 *   bun polish photo.png --saturation 1.3           # More vibrant
 *   bun polish photo.png --sharpen 1.5              # Sharpen with sigma 1.5
 *   bun polish photo.png --auto                     # Auto-enhance
 *   bun polish photo.png -b 1.1 -c 1.15 --sharpen 1 # Combine adjustments
 *   bun polish ./images --auto                      # Batch process directory
 */

import sharp from "sharp";
import { parse, join } from "node:path";
import { readdir, stat } from "node:fs/promises";

interface PolishOptions {
  inputPath: string;
  brightness?: number;
  contrast?: number;
  saturation?: number;
  sharpen?: number;
  auto?: boolean;
  outputPath?: string;
}

interface PolishResult {
  inputPath: string;
  outputPath: string;
  adjustments: string[];
}

const SUPPORTED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp"];

function isSupportedImage(filename: string): boolean {
  const ext = parse(filename).ext.toLowerCase();
  return SUPPORTED_EXTENSIONS.includes(ext);
}

function getOutputPath(inputPath: string): string {
  const parsed = parse(inputPath);
  return join(parsed.dir, `${parsed.name}-polished${parsed.ext}`);
}

/**
 * Apply polish adjustments to an image
 */
async function polishImage(options: PolishOptions): Promise<PolishResult> {
  const {
    inputPath,
    brightness = 1.0,
    contrast = 1.0,
    saturation = 1.0,
    sharpen,
    auto,
    outputPath,
  } = options;

  const finalOutputPath = outputPath || getOutputPath(inputPath);
  const adjustments: string[] = [];

  let pipeline = sharp(inputPath);

  if (auto) {
    // Auto-enhance: normalize contrast and apply light sharpening
    pipeline = pipeline.normalize().sharpen({ sigma: 1.0 });
    adjustments.push("auto-enhance (normalize + sharpen)");
  } else {
    // Apply brightness and saturation via modulate
    if (brightness !== 1.0 || saturation !== 1.0) {
      pipeline = pipeline.modulate({
        brightness: brightness,
        saturation: saturation,
      });
      if (brightness !== 1.0) adjustments.push(`brightness: ${brightness}x`);
      if (saturation !== 1.0) adjustments.push(`saturation: ${saturation}x`);
    }

    // Apply contrast via linear transform
    // contrast multiplier: values > 1 increase contrast, < 1 decrease
    if (contrast !== 1.0) {
      // Linear transform: output = input * a + b
      // For contrast: a = contrast, b = 128 * (1 - contrast) to keep midpoint stable
      const offset = 128 * (1 - contrast);
      pipeline = pipeline.linear(contrast, offset);
      adjustments.push(`contrast: ${contrast}x`);
    }

    // Apply sharpening
    if (sharpen && sharpen > 0) {
      pipeline = pipeline.sharpen({ sigma: sharpen });
      adjustments.push(`sharpen: sigma ${sharpen}`);
    }
  }

  await pipeline.toFile(finalOutputPath);

  return {
    inputPath,
    outputPath: finalOutputPath,
    adjustments,
  };
}

/**
 * Process all images in a directory
 */
async function processDirectory(
  dirPath: string,
  options: Omit<PolishOptions, "inputPath" | "outputPath">
): Promise<void> {
  const entries = await readdir(dirPath, { withFileTypes: true });

  const imageFiles = entries.filter(
    (entry) =>
      entry.isFile() &&
      isSupportedImage(entry.name) &&
      !entry.name.includes("-polished")
  );

  if (imageFiles.length === 0) {
    console.log("No supported images found (.png, .jpg, .jpeg, .webp)");
    return;
  }

  console.log(`Found ${imageFiles.length} images to process...\n`);

  let successCount = 0;

  for (const file of imageFiles) {
    const inputPath = join(dirPath, file.name);
    try {
      const result = await polishImage({ inputPath, ...options });
      console.log(`  ${file.name} -> ${parse(result.outputPath).base}`);
      if (result.adjustments.length > 0) {
        console.log(`    ${result.adjustments.join(", ")}`);
      }
      successCount++;
    } catch (error) {
      console.error(
        `  ${file.name}: ${error instanceof Error ? error.message : String(error)}`
      );
    }
  }

  console.log(`\nDone! ${successCount}/${imageFiles.length} images processed.`);
}

function parseArgs(args: readonly string[]): {
  input?: string;
  brightness: number;
  contrast: number;
  saturation: number;
  sharpen?: number;
  auto: boolean;
  output?: string;
} {
  let brightness = 1.0;
  let contrast = 1.0;
  let saturation = 1.0;
  let sharpen: number | undefined;
  let auto = false;
  let output: string | undefined;
  let input: string | undefined;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg === "-b" || arg === "--brightness") {
      brightness = parseFloat(args[++i]);
    } else if (arg === "-c" || arg === "--contrast") {
      contrast = parseFloat(args[++i]);
    } else if (arg === "-s" || arg === "--saturation") {
      saturation = parseFloat(args[++i]);
    } else if (arg === "--sharpen") {
      sharpen = parseFloat(args[++i]);
    } else if (arg === "--auto") {
      auto = true;
    } else if (arg === "-o" || arg === "--output") {
      output = args[++i];
    } else if (!arg.startsWith("-")) {
      input = arg;
    }
  }

  return { input, brightness, contrast, saturation, sharpen, auto, output };
}

function printHelp(): void {
  console.log(`
Image Polish Utility - Enhance brightness, contrast, saturation, sharpness

Usage:
  bun polish <input|directory> [options]

Options:
  --brightness, -b    Brightness multiplier (0.5-2.0, default: 1.0)
  --contrast, -c      Contrast multiplier (0.5-2.0, default: 1.0)
  --saturation, -s    Saturation multiplier (0.0-2.0, default: 1.0)
  --sharpen           Apply sharpening (sigma 0.5-5.0, default: off)
  --auto              Auto-enhance: normalize contrast + light sharpen
  --output, -o        Output path (single file only)

Multiplier reference:
  0.5  = 50% (darker/less)
  1.0  = no change
  1.5  = 150% (brighter/more)
  2.0  = 200% (max recommended)

Examples:
  bun polish photo.png --brightness 1.1           # Slightly brighter
  bun polish photo.png --contrast 1.2             # More contrast
  bun polish photo.png --saturation 1.3           # More vibrant
  bun polish photo.png --sharpen 1.5              # Sharpen
  bun polish photo.png --auto                     # Auto-enhance
  bun polish photo.png -b 1.1 -c 1.15 --sharpen 1 # Combine adjustments
  bun polish ./images --auto                      # Batch process
`);
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const { input, brightness, contrast, saturation, sharpen, auto, output } =
    parseArgs(args);

  if (!input) {
    printHelp();
    process.exit(1);
  }

  // Validate ranges
  const validateRange = (
    name: string,
    value: number,
    min: number,
    max: number
  ) => {
    if (isNaN(value) || value < min || value > max) {
      console.error(`Error: ${name} must be between ${min} and ${max}`);
      process.exit(1);
    }
  };

  if (!auto) {
    validateRange("brightness", brightness, 0.5, 2.0);
    validateRange("contrast", contrast, 0.5, 2.0);
    validateRange("saturation", saturation, 0.0, 2.0);
    if (sharpen !== undefined) {
      validateRange("sharpen", sharpen, 0.5, 5.0);
    }
  }

  // Check if any adjustments specified
  const hasAdjustments =
    auto ||
    brightness !== 1.0 ||
    contrast !== 1.0 ||
    saturation !== 1.0 ||
    sharpen !== undefined;

  if (!hasAdjustments) {
    console.error("Error: No adjustments specified. Use --auto or specify options.");
    printHelp();
    process.exit(1);
  }

  try {
    const stats = await stat(input);

    if (stats.isDirectory()) {
      if (output) {
        console.error("Error: Cannot use --output with directory input");
        process.exit(1);
      }
      await processDirectory(input, { brightness, contrast, saturation, sharpen, auto });
    } else {
      const adjustmentDesc = auto
        ? "auto-enhance"
        : [
            brightness !== 1.0 && `brightness ${brightness}x`,
            contrast !== 1.0 && `contrast ${contrast}x`,
            saturation !== 1.0 && `saturation ${saturation}x`,
            sharpen && `sharpen σ${sharpen}`,
          ]
            .filter(Boolean)
            .join(", ");

      console.log(`Polishing ${input} (${adjustmentDesc})...`);

      const result = await polishImage({
        inputPath: input,
        brightness,
        contrast,
        saturation,
        sharpen,
        auto,
        outputPath: output,
      });

      console.log(`
Done!
  Applied: ${result.adjustments.join(", ")}
  Output:  ${result.outputPath}
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
