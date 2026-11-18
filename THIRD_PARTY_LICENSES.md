# Third-party components and licences

This inventory was checked against the Orfeusz Gateway 1.10.74 source package
and its Gradle build configuration. It is not a substitute for checking the
resolved dependency graph of a future release.

## Runtime dependency

### usb-serial-for-android 3.8.1

- Project: https://github.com/mik3y/usb-serial-for-android
- Declared dependency: `com.github.mik3y:usb-serial-for-android:3.8.1`
- Licence: MIT
- Copyright notices: Google Inc. (2011–2013); Mike Wakerly (2013)

The MIT licence text:

```text
MIT License

Copyright (c) 2011-2013 Google Inc.
Copyright (c) 2013 Mike Wakerly

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Build tools and wrapper

The source package includes the Gradle Wrapper (Gradle 8.7). Gradle is
distributed under the Apache License 2.0. The Android Gradle Plugin declared
by the project (8.6.1) is also distributed under the Apache License 2.0.
These are build-time tools and are not bundled as application runtime
libraries by the declared app dependency configuration.

The full Apache License 2.0 text is included at [licenses/Apache-2.0.txt](licenses/Apache-2.0.txt).

## Android platform

The Android SDK and platform APIs are supplied by the Android development
environment. They are not third-party runtime libraries copied into this
repository by the declared app dependency configuration.

## Maintenance note

The list above is based on the dependencies explicitly declared in the
1.10.74 source package. Before each release, inspect the resolved dependency
graph and update this file if dependencies, versions, licences, or bundled
components change. Preserve upstream copyright and licence notices.
