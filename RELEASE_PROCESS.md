# Orfeusz Gateway – Release publishing process

This checklist describes the repository's current release asset convention and the automated stable-download alias.

## Before publishing

1. Build the Android application from the intended source revision.
2. Verify the Gradle `versionName` and `versionCode`; synchronize the in-app version display, README files and release notes.
3. Install the APK on a test device and verify startup, Zello launch/connection status, USB–UART detection, radio receive, PTT/transmit and stop behaviour.
4. Confirm that the release tag uses `MAJOR.MINOR.PATCH` format, for example `1.10.63`.
5. Name the versioned APK exactly `Orfeusz.Gateway_v<TAG>.apk`, for example `Orfeusz.Gateway_v1.10.63.apk`.
6. Prepare the matching release notes. Do not publish an unbuilt, untested or placeholder APK.

## Source archive and GPL compliance

Starting with version 1.10.75, releases are made under GPL-3.0-only. For every
GPL-3.0-only release, prepare a matching source archive named
`Orfeusz.Gateway_Source_v<TAG>.zip`. The archive must contain the complete
Corresponding Source needed to build and modify that APK, including at minimum:

- the Android project source and Gradle wrapper;
- the root `LICENSE` file with the complete GPL-3.0-only text;
- `NOTICE`, `COPYRIGHT.md`, and `THIRD_PARTY_LICENSES.md`;
- the project documentation and any scripts needed to build the application.

Do not rely only on GitHub's automatically generated repository source archive:
the Android project is supplied as a versioned source ZIP release asset and the
release build workflow builds from that archive.

## Publish the GitHub Release

1. Create a GitHub Release using the version tag.
2. Attach the matching source archive `Orfeusz.Gateway_Source_v<TAG>.zip`.
3. Attach the versioned APK and release notes.
4. Publish the release only after confirming both the source archive and APK
   assets are present, correctly named, and correspond to the same source revision.
5. Keep the source archive available alongside the binary for GPL recipients.

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

If the workflow fails after the release is published, inspect the failed Actions run and correct the missing or incorrectly named asset. Then open **Actions → Maintain latest APK download → Run workflow**, enter the exact release tag (for example `1.10.63`), and run it.

## Final verification

- Confirm the workflow completed successfully.
- Open the release and verify that the versioned APK, stable alias and SHA-256 checksum are attached.
- Download the stable URL and compare its size or SHA-256 value with the versioned release APK.
- Confirm the release is not marked as a prerelease.

## Important

The stable URL is an alias to the latest published stable GitHub Release; it does not mean that GitHub Pages or the application itself has been rebuilt. A release must contain the correctly named versioned APK before the workflow can publish the alias.
