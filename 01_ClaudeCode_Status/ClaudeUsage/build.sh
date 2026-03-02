#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC_DIR="$SCRIPT_DIR/ClaudeUsage"
BUILD_DIR="$SCRIPT_DIR/build"
APP_NAME="ClaudeUsage"
APP_BUNDLE="$BUILD_DIR/$APP_NAME.app"

echo "=== Building $APP_NAME ==="

# Clean previous build
rm -rf "$BUILD_DIR"
mkdir -p "$APP_BUNDLE/Contents/MacOS"
mkdir -p "$APP_BUNDLE/Contents/Resources"

# Compile Swift sources
echo "Compiling..."
swiftc \
    -o "$APP_BUNDLE/Contents/MacOS/$APP_NAME" \
    -target arm64-apple-macosx13.0 \
    -sdk "$(xcrun --show-sdk-path)" \
    -framework SwiftUI \
    -framework ServiceManagement \
    -O \
    "$SRC_DIR/Models.swift" \
    "$SRC_DIR/CredentialManager.swift" \
    "$SRC_DIR/UsageViewModel.swift" \
    "$SRC_DIR/UsagePopoverView.swift" \
    "$SRC_DIR/ClaudeUsageApp.swift"

# Copy Info.plist
cp "$SRC_DIR/Info.plist" "$APP_BUNDLE/Contents/Info.plist"

echo "=== Build complete ==="
echo "App: $APP_BUNDLE"
echo ""
echo "To run:  open \"$APP_BUNDLE\""
echo "To install: cp -r \"$APP_BUNDLE\" /Applications/"
