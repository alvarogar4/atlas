/**
 * Image Cropping Utility
 *
 * Unified tool for cropping images with multiple modes:
 * - Aspect ratio: Center crop to specific ratio (16:9, 4:3, 1:1, etc.)
 * - Symmetric trim: Crop percentage from both top+bottom or left+right edges
 * - Individual edges: Crop percentage from any single edge independently
 *
 * IMPORTANT: --vertical and --horizontal crop from EACH side, not total.
 * Example: --vertical 10 removes 10% from top + 10% from bottom = 20% total height reduction
 *
 * Individual edge options can be combined with symmetric options.
 * Example: --vertical 5 --top 5 = 10% from top + 5% from bottom
 *
 * Usage:
 *   bun image:crop <input|directory> [options]
 *
 * Options:
 *   --ratio, -r      Aspect ratio to crop to (e.g., 16:9, 4:3, 1:1)
 *   --vertical, -v   Percentage to crop from top AND bottom (0-50)
 *   --horizontal, -h Percentage to crop from left AND right (0-50)
 *   --top, -t        Percentage to crop from top only (0-50)
 *   --bottom, -b     Percentage to crop from bottom only (0-50)
 *   --left, -l       Percentage to crop from left only (0-50)
 *   --right          Percentage to crop from right only (0-50)
 *   --output, -o     Output path (single file only)
 *
 * Examples:
 *   bun image:crop hero.png --ratio 16:9           # Center crop to 16:9
 *   bun image:crop hero.png -r 1:1                 # Center crop to square
 *   bun image:crop photo.png --vertical 10        # Remove 10% top + 10% bottom
 *   bun image:crop photo.png --horizontal 5       # Remove 5% left + 5% right
 *   bun image:crop photo.png --top 15             # Remove 15% from top only
 *   bun image:crop photo.png --bottom 10          # Remove 10% from bottom only
 *   bun image:crop photo.png --left 5 --right 10  # Remove 5% left + 10% right
 *   bun image:crop photo.png -v 10 -h 5           # Combine vertical + horizontal
 *   bun image:crop ./images --ratio 4:3           # Batch process directory
 *   bun image:crop hero.png -r 16:9 -o out.png    # Custom output path
 */

import sharp from "sharp";
import { parse, join } from "node:path";
import { readdir, stat } from "node:fs/promises";

interface CropOptions {
  inputPath: string;
  ratio?: string;
  vertical?: number;
  horizontal?: number;
  top?: number;
  bottom?: number;
  left?: number;
  right?: number;
  outputPath?: string;
}

interface CropResult {
  outputPath: string;
  originalWidth: number;
  originalHeight: number;
  croppedWidth: number;
  croppedHeight: number;
}

const SUPPORTED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp", ".gif"];

function isSupportedImage(filename: string): boolean {
  const ext = parse(filename).ext.toLowerCase();
  return SUPPORTED_EXTENSIONS.includes(ext);
}

/**
 * Parse aspect ratio string into width and height numbers
 */
function parseAspectRatio(ratio: string): { width: number; height: number } {
  const parts = ratio.split(":");
  if (parts.length !== 2) {
    throw new Error(
      `Invalid aspect ratio format: "${ratio}". Use format like "16:9" or "4:3"`
    );
  }

  const width = parseFloat(parts[0]);
  const height = parseFloat(parts[1]);

  if (isNaN(width) || isNaN(height) || width <= 0 || height <= 0) {
    throw new Error(
      `Invalid aspect ratio values: "${ratio}". Both values must be positive numbers`
    );
  }

  return { width, height };
}

/**
 * Calculate the largest centered crop area for a given aspect ratio
 */
function calculateCenteredCrop(
  imageWidth: number,
  imageHeight: number,
  targetAspectWidth: number,
  targetAspectHeight: number
): { left: number; top: number; width: number; height: number } {
  const targetRatio = targetAspectWidth / targetAspectHeight;
  const imageRatio = imageWidth / imageHeight;

  let cropWidth: number;
  let cropHeight: number;

  if (imageRatio > targetRatio) {
    // Image is wider than target ratio - crop width
    cropHeight = imageHeight;
    cropWidth = Math.round(imageHeight * targetRatio);
  } else {
    // Image is taller than target ratio - crop height
    cropWidth = imageWidth;
    cropHeight = Math.round(imageWidth / targetRatio);
  }

  // Center the crop
  const left = Math.round((imageWidth - cropWidth) / 2);
  const top = Math.round((imageHeight - cropHeight) / 2);

  return { left, top, width: cropWidth, height: cropHeight };
}

/**
 * Generate output filename based on crop mode
 */
function generateOutputPath(inputPath: string, ratio?: string): string {
  const parsed = parse(inputPath);

  if (ratio) {
    const ratioSuffix = ratio.replace(":", "x");
    return join(parsed.dir, `${parsed.name}-${ratioSuffix}${parsed.ext}`);
  }

  return join(parsed.dir, `${parsed.name}-cropped${parsed.ext}`);
}

/**
 * Crop an image to a specific aspect ratio, centered, as large as possible
 */
export async function cropToAspectRatio(
  inputPath: string,
  aspectRatio: string,
  outputPath?: string
): Promise<CropResult> {
  const { width: aspectWidth, height: aspectHeight } =
    parseAspectRatio(aspectRatio);

  const image = sharp(inputPath);
  const metadata = await image.metadata();

  if (!metadata.width || !metadata.height) {
    throw new Error(`Could not read image dimensions from: ${inputPath}`);
  }

  const { width: originalWidth, height: originalHeight } = metadata;

  const crop = calculateCenteredCrop(
    originalWidth,
    originalHeight,
    aspectWidth,
    aspectHeight
  );

  const finalOutputPath =
    outputPath || generateOutputPath(inputPath, aspectRatio);

  await image
    .extract({
      left: crop.left,
      top: crop.top,
      width: crop.width,
      height: crop.height,
    })
    .toFile(finalOutputPath);

  return {
    outputPath: finalOutputPath,
    originalWidth,
    originalHeight,
    croppedWidth: crop.width,
    croppedHeight: crop.height,
  };
}

/**
 * Crop a percentage from top and bottom of an image
 */
export async function cropVertical(
  inputPath: string,
  percentage: number,
  outputPath?: string
): Promise<CropResult> {
  if (percentage <= 0 || percentage >= 50) {
    throw new Error(
      `Invalid percentage: ${percentage}. Must be between 0 and 50 (exclusive)`
    );
  }

  const image = sharp(inputPath);
  const metadata = await image.metadata();

  if (!metadata.width || !metadata.height) {
    throw new Error(`Could not read image dimensions from: ${inputPath}`);
  }

  const { width: originalWidth, height: originalHeight } = metadata;

  const cropFromEachSide = Math.round(originalHeight * (percentage / 100));
  const top = cropFromEachSide;
  const newHeight = originalHeight - cropFromEachSide * 2;

  const finalOutputPath = outputPath || generateOutputPath(inputPath);

  await image
    .extract({
      left: 0,
      top: top,
      width: originalWidth,
      height: newHeight,
    })
    .toFile(finalOutputPath);

  return {
    outputPath: finalOutputPath,
    originalWidth,
    originalHeight,
    croppedWidth: originalWidth,
    croppedHeight: newHeight,
  };
}

/**
 * Crop a percentage from left and right of an image
 */
export async function cropHorizontal(
  inputPath: string,
  percentage: number,
  outputPath?: string
): Promise<CropResult> {
  if (percentage <= 0 || percentage >= 50) {
    throw new Error(
      `Invalid percentage: ${percentage}. Must be between 0 and 50 (exclusive)`
    );
  }

  const image = sharp(inputPath);
  const metadata = await image.metadata();

  if (!metadata.width || !metadata.height) {
    throw new Error(`Could not read image dimensions from: ${inputPath}`);
  }

  const { width: originalWidth, height: originalHeight } = metadata;

  const cropFromEachSide = Math.round(originalWidth * (percentage / 100));
  const left = cropFromEachSide;
  const newWidth = originalWidth - cropFromEachSide * 2;

  const finalOutputPath = outputPath || generateOutputPath(inputPath);

  await image
    .extract({
      left: left,
      top: 0,
      width: newWidth,
      height: originalHeight,
    })
    .toFile(finalOutputPath);

  return {
    outputPath: finalOutputPath,
    originalWidth,
    originalHeight,
    croppedWidth: newWidth,
    croppedHeight: originalHeight,
  };
}

/**
 * Crop a percentage from bottom only
 */
export async function cropBottom(
  inputPath: string,
  percentage: number,
  outputPath?: string
): Promise<CropResult> {
  if (percentage <= 0 || percentage >= 50) {
    throw new Error(
      `Invalid percentage: ${percentage}. Must be between 0 and 50 (exclusive)`
    );
  }

  const image = sharp(inputPath);
  const metadata = await image.metadata();

  if (!metadata.width || !metadata.height) {
    throw new Error(`Could not read image dimensions from: ${inputPath}`);
  }

  const { width: originalWidth, height: originalHeight } = metadata;

  const cropAmount = Math.round(originalHeight * (percentage / 100));
  const newHeight = originalHeight - cropAmount;

  const finalOutputPath = outputPath || generateOutputPath(inputPath);

  await image
    .extract({
      left: 0,
      top: 0,
      width: originalWidth,
      height: newHeight,
    })
    .toFile(finalOutputPath);

  return {
    outputPath: finalOutputPath,
    originalWidth,
    originalHeight,
    croppedWidth: originalWidth,
    croppedHeight: newHeight,
  };
}

/**
 * Crop a percentage from top only
 */
export async function cropTop(
  inputPath: string,
  percentage: number,
  outputPath?: string
): Promise<CropResult> {
  if (percentage <= 0 || percentage >= 50) {
    throw new Error(
      `Invalid percentage: ${percentage}. Must be between 0 and 50 (exclusive)`
    );
  }

  const image = sharp(inputPath);
  const metadata = await image.metadata();

  if (!metadata.width || !metadata.height) {
    throw new Error(`Could not read image dimensions from: ${inputPath}`);
  }

  const { width: originalWidth, height: originalHeight } = metadata;

  const cropAmount = Math.round(originalHeight * (percentage / 100));
  const newHeight = originalHeight - cropAmount;

  const finalOutputPath = outputPath || generateOutputPath(inputPath);

  await image
    .extract({
      left: 0,
      top: cropAmount,
      width: originalWidth,
      height: newHeight,
    })
    .toFile(finalOutputPath);

  return {
    outputPath: finalOutputPath,
    originalWidth,
    originalHeight,
    croppedWidth: originalWidth,
    croppedHeight: newHeight,
  };
}

/**
 * Crop a percentage from left only
 */
export async function cropLeft(
  inputPath: string,
  percentage: number,
  outputPath?: string
): Promise<CropResult> {
  if (percentage <= 0 || percentage >= 50) {
    throw new Error(
      `Invalid percentage: ${percentage}. Must be between 0 and 50 (exclusive)`
    );
  }

  const image = sharp(inputPath);
  const metadata = await image.metadata();

  if (!metadata.width || !metadata.height) {
    throw new Error(`Could not read image dimensions from: ${inputPath}`);
  }

  const { width: originalWidth, height: originalHeight } = metadata;

  const cropAmount = Math.round(originalWidth * (percentage / 100));
  const newWidth = originalWidth - cropAmount;

  const finalOutputPath = outputPath || generateOutputPath(inputPath);

  await image
    .extract({
      left: cropAmount,
      top: 0,
      width: newWidth,
      height: originalHeight,
    })
    .toFile(finalOutputPath);

  return {
    outputPath: finalOutputPath,
    originalWidth,
    originalHeight,
    croppedWidth: newWidth,
    croppedHeight: originalHeight,
  };
}

/**
 * Crop a percentage from right only
 */
export async function cropRight(
  inputPath: string,
  percentage: number,
  outputPath?: string
): Promise<CropResult> {
  if (percentage <= 0 || percentage >= 50) {
    throw new Error(
      `Invalid percentage: ${percentage}. Must be between 0 and 50 (exclusive)`
    );
  }

  const image = sharp(inputPath);
  const metadata = await image.metadata();

  if (!metadata.width || !metadata.height) {
    throw new Error(`Could not read image dimensions from: ${inputPath}`);
  }

  const { width: originalWidth, height: originalHeight } = metadata;

  const cropAmount = Math.round(originalWidth * (percentage / 100));
  const newWidth = originalWidth - cropAmount;

  const finalOutputPath = outputPath || generateOutputPath(inputPath);

  await image
    .extract({
      left: 0,
      top: 0,
      width: newWidth,
      height: originalHeight,
    })
    .toFile(finalOutputPath);

  return {
    outputPath: finalOutputPath,
    originalWidth,
    originalHeight,
    croppedWidth: newWidth,
    croppedHeight: originalHeight,
  };
}

/**
 * Combined crop: apply ratio first, then all edge crops in a single pass
 */
async function cropCombined(options: CropOptions): Promise<CropResult> {
  const {
    inputPath,
    ratio,
    vertical = 0,
    horizontal = 0,
    top = 0,
    bottom = 0,
    left = 0,
    right = 0,
    outputPath,
  } = options;

  // Get original dimensions
  const originalImage = sharp(inputPath);
  const originalMetadata = await originalImage.metadata();
  if (!originalMetadata.width || !originalMetadata.height) {
    throw new Error(`Could not read image dimensions from: ${inputPath}`);
  }
  const originalWidth = originalMetadata.width;
  const originalHeight = originalMetadata.height;

  // Determine final output path
  const finalOutputPath = outputPath || generateOutputPath(inputPath, ratio);

  // Check if we have any edge crops
  const hasEdgeCrops = vertical || horizontal || top || bottom || left || right;

  // Step 1: Ratio crop (if specified)
  let currentPath = inputPath;
  let tempFile: string | null = null;
  let currentWidth = originalWidth;
  let currentHeight = originalHeight;

  if (ratio) {
    if (hasEdgeCrops) {
      // Need temp file for ratio crop
      tempFile = generateOutputPath(inputPath, ratio) + ".temp";
      const result = await cropToAspectRatio(currentPath, ratio, tempFile);
      currentPath = tempFile;
      currentWidth = result.croppedWidth;
      currentHeight = result.croppedHeight;
    } else {
      // Ratio only, output directly
      const result = await cropToAspectRatio(currentPath, ratio, finalOutputPath);
      return {
        outputPath: finalOutputPath,
        originalWidth,
        originalHeight,
        croppedWidth: result.croppedWidth,
        croppedHeight: result.croppedHeight,
      };
    }
  }

  // Step 2: Apply all edge crops in a single pass
  if (hasEdgeCrops) {
    // Calculate total crop from each edge (individual + symmetric)
    const cropTopPercent = top + vertical;
    const cropBottomPercent = bottom + vertical;
    const cropLeftPercent = left + horizontal;
    const cropRightPercent = right + horizontal;

    // Calculate pixel offsets and dimensions
    const extractTop = Math.round(currentHeight * (cropTopPercent / 100));
    const extractLeft = Math.round(currentWidth * (cropLeftPercent / 100));
    const extractHeight =
      currentHeight -
      Math.round(currentHeight * (cropTopPercent / 100)) -
      Math.round(currentHeight * (cropBottomPercent / 100));
    const extractWidth =
      currentWidth -
      Math.round(currentWidth * (cropLeftPercent / 100)) -
      Math.round(currentWidth * (cropRightPercent / 100));

    if (extractWidth <= 0 || extractHeight <= 0) {
      if (tempFile) await cleanupTempFiles([tempFile]);
      throw new Error(
        `Invalid crop: combined percentages result in zero or negative dimensions`
      );
    }

    const image = sharp(currentPath);
    await image
      .extract({
        left: extractLeft,
        top: extractTop,
        width: extractWidth,
        height: extractHeight,
      })
      .toFile(finalOutputPath);

    // Clean up temp file
    if (tempFile) await cleanupTempFiles([tempFile]);

    return {
      outputPath: finalOutputPath,
      originalWidth,
      originalHeight,
      croppedWidth: extractWidth,
      croppedHeight: extractHeight,
    };
  }

  // No crops specified - shouldn't reach here but handle it
  throw new Error("No crop mode specified");
}

async function cleanupTempFiles(files: string[]): Promise<void> {
  const { unlink } = await import("node:fs/promises");
  for (const file of files) {
    try {
      await unlink(file);
    } catch {
      // Ignore cleanup errors
    }
  }
}

/**
 * Process all images in a directory
 */
async function processDirectory(
  dirPath: string,
  options: Omit<CropOptions, "inputPath" | "outputPath">
): Promise<void> {
  const entries = await readdir(dirPath, { withFileTypes: true });

  const imageFiles = entries.filter(
    (entry) =>
      entry.isFile() &&
      isSupportedImage(entry.name) &&
      !entry.name.includes("-cropped") &&
      !entry.name.match(/-\d+x\d+\./)
  );

  if (imageFiles.length === 0) {
    console.log("No image files found in directory");
    return;
  }

  console.log(`Found ${imageFiles.length} images to process...\n`);

  for (const file of imageFiles) {
    const inputPath = join(dirPath, file.name);
    try {
      console.log(`Processing ${file.name}...`);
      const result = await cropCombined({ inputPath, ...options });
      console.log(
        `  ${result.originalWidth}x${result.originalHeight} -> ${result.croppedWidth}x${result.croppedHeight} (${parse(result.outputPath).base})`
      );
    } catch (error) {
      console.error(
        `  Error: ${error instanceof Error ? error.message : String(error)}`
      );
    }
  }

  console.log("\nDone!");
}

/**
 * Parse command line arguments
 */
function parseArgs(args: readonly string[]): {
  input?: string;
  ratio?: string;
  vertical?: number;
  horizontal?: number;
  top?: number;
  bottom?: number;
  left?: number;
  right?: number;
  output?: string;
} {
  let ratio: string | undefined;
  let vertical: number | undefined;
  let horizontal: number | undefined;
  let top: number | undefined;
  let bottom: number | undefined;
  let left: number | undefined;
  let right: number | undefined;
  let output: string | undefined;
  let input: string | undefined;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg === "-r" || arg === "--ratio") {
      ratio = args[++i];
    } else if (arg === "-v" || arg === "--vertical") {
      vertical = parseFloat(args[++i]);
    } else if (arg === "-h" || arg === "--horizontal") {
      horizontal = parseFloat(args[++i]);
    } else if (arg === "-t" || arg === "--top") {
      top = parseFloat(args[++i]);
    } else if (arg === "-b" || arg === "--bottom") {
      bottom = parseFloat(args[++i]);
    } else if (arg === "-l" || arg === "--left") {
      left = parseFloat(args[++i]);
    } else if (arg === "--right") {
      right = parseFloat(args[++i]);
    } else if (arg === "-o" || arg === "--output") {
      output = args[++i];
    } else if (!arg.startsWith("-")) {
      input = arg;
    }
  }

  return { input, ratio, vertical, horizontal, top, bottom, left, right, output };
}

function printHelp(): void {
  console.log(`
Image Cropping Utility - Multiple crop modes

Usage:
  bun image:crop <input|directory> [options]

Options:
  --ratio, -r      Aspect ratio to crop to (e.g., 16:9, 4:3, 1:1)
  --vertical, -v   Percentage to crop from top AND bottom (0-50)
  --horizontal, -h Percentage to crop from left AND right (0-50)
  --top, -t        Percentage to crop from top only (0-50)
  --bottom, -b     Percentage to crop from bottom only (0-50)
  --left, -l       Percentage to crop from left only (0-50)
  --right          Percentage to crop from right only (0-50)
  --output, -o     Output path (single file only)

Note: --vertical and --horizontal crop from EACH side, not total.
Example: --vertical 10 removes 10% top + 10% bottom = 20% total
         --top 10 removes 10% from top only
         Options can be combined: --vertical 5 --top 5 = 10% top + 5% bottom

Examples:
  bun image:crop hero.png --ratio 16:9           # Center crop to 16:9
  bun image:crop hero.png -r 1:1                 # Center crop to square
  bun image:crop photo.png --vertical 10         # Remove 10% top + 10% bottom
  bun image:crop photo.png --horizontal 5        # Remove 5% left + 5% right
  bun image:crop photo.png --top 15              # Remove 15% from top only
  bun image:crop photo.png --bottom 10           # Remove 10% from bottom only
  bun image:crop photo.png --left 5 --right 10   # Remove 5% left + 10% right
  bun image:crop photo.png -v 10 -h 5            # Combine vertical + horizontal
  bun image:crop ./images --ratio 4:3            # Batch process directory
  bun image:crop hero.png -r 16:9 -o out.png     # Custom output path
`);
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const { input, ratio, vertical, horizontal, top, bottom, left, right, output } =
    parseArgs(args);

  if (!input) {
    printHelp();
    process.exit(1);
  }

  // Validate that at least one crop mode is specified
  if (!ratio && !vertical && !horizontal && !top && !bottom && !left && !right) {
    console.error(
      "Error: At least one crop mode required (--ratio, --vertical, --horizontal, --top, --bottom, --left, or --right)"
    );
    printHelp();
    process.exit(1);
  }

  // Validate percentage values
  const validatePercent = (name: string, value: number | undefined) => {
    if (value !== undefined && (isNaN(value) || value <= 0 || value >= 50)) {
      console.error(`Error: ${name} must be a number between 0 and 50 (exclusive)`);
      process.exit(1);
    }
  };

  validatePercent("--vertical", vertical);
  validatePercent("--horizontal", horizontal);
  validatePercent("--top", top);
  validatePercent("--bottom", bottom);
  validatePercent("--left", left);
  validatePercent("--right", right);

  try {
    const stats = await stat(input);

    if (stats.isDirectory()) {
      if (output) {
        console.error("Error: Cannot use --output with directory input");
        process.exit(1);
      }
      await processDirectory(input, { ratio, vertical, horizontal, top, bottom, left, right });
    } else {
      const modeDesc = [
        ratio && `ratio ${ratio}`,
        vertical && `vertical ${vertical}%`,
        horizontal && `horizontal ${horizontal}%`,
        top && `top ${top}%`,
        bottom && `bottom ${bottom}%`,
        left && `left ${left}%`,
        right && `right ${right}%`,
      ]
        .filter(Boolean)
        .join(", ");

      console.log(`Cropping ${input} (${modeDesc})...`);

      const result = await cropCombined({
        inputPath: input,
        ratio,
        vertical,
        horizontal,
        top,
        bottom,
        left,
        right,
        outputPath: output,
      });

      console.log(`
Cropped successfully!
  Original: ${result.originalWidth}x${result.originalHeight}
  Cropped:  ${result.croppedWidth}x${result.croppedHeight}
  Output:   ${result.outputPath}
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
