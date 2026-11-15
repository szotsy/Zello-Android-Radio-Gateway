# Orfeusz Gateway – Release publishing process

This checklist describes the repository's current release asset convention and the automated stable-download alias.

## Before publishing

1. Build the Android application from the intended source revision.
2. Verify the Gradle `versionName` and `versionCode`; synchronize the in-app version display, README files and release notes.
3. Install the APK on a test device and verify startup, Zello launch/connection status, FTDI detection, radio receive, PTT/transmit and stop behaviour.
4. Confirm that the release tag uses `MAJOR.MINOR.PATCH` format, for example `1.10.62`.
5. Name the versioned APK exactly `Orfeusz.Gateway_v<TAG>.apk`, for example `Orfeusz.Gateway_v1.10.62.apk`.
6. Prepare the matching release notes. Do not publish an unbuilt, untested or placeholder APK.

## Publish the GitHub Release

1. Create a GitHub Release using the version tag.
2. Attach the versioned APK and release notes.
3. Publish the release only after confirming the APK asset is present and correct.

## Automated stable download

The `.github/workflows/latest-apk-alias.yml` workflow runs when a release is published. For stable releases it:

- downloads the versioned APK asset;
- checks that the file exists and is not empty;
- calculates a SHA-256 checksum;
- creates `Orfeusz.Gateway.apk` as a byte-for-byte copy;
- verifies the copy and checksum;
- uploads both `Orfeusz.Gateway.apk` and `Orfeusz.Gateway.apk.sha256` to the release.

The permanent direct download URL is:

`https://github.com/szotsy/Zello-Android-Radio-Gateway/releases/latest/download/Orfeusz.Gateway.apk`

Prereleases are intentionally excluded from automatic stable-alias updates.

## Recovery / manual run

If the workflow fails after the release is published, inspect the failed Actions run and correct the missing or incorrectly named asset. Then open **Actions → Maintain latest APK download → Run workflow**, enter the exact release tag (for example `1.10.62`), and run it.

## Final verification

- Confirm the workflow completed successfully.
- Open the release and verify that the versioned APK, stable alias and SHA-256 checksum are attached.
- Download the stable URL and compare its size or SHA-256 value with the versioned release APK.
- Confirm the release is not marked as a prerelease.

## Important

The stable URL is an alias to the latest published stable GitHub Release; it does not mean that GitHub Pages or the application itself has been rebuilt. A release must contain the correctly named versioned APK before the workflow can publish the alias.
