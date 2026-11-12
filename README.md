# primer-sdk-ios-specs

CocoaPods specs for the Primer iOS SDK and its wrapper SDKs. CocoaPods Trunk accepts no new versions from 2 December 2026, so new Primer versions are published here.

For native iOS apps, Swift Package Manager is the recommended way to install the Primer iOS SDK. This repo is for React Native apps, and for a limited time for native apps that still use CocoaPods.

## Use it

Add these two lines at the top of your Podfile, in this order:

```ruby
source 'https://github.com/primer-io/primer-sdk-ios-specs.git'
source 'https://cdn.cocoapods.org/'
```

Keep both lines. CocoaPods takes a pod from the first source that has it, so this repo must come first. Your other pods still come from the CocoaPods CDN, and once a Podfile has a `source` line, CocoaPods no longer adds the CDN by itself.

## What is in it

Every published version of these pods:

- `PrimerSDK` and its module pods (`PrimerFoundation`, `PrimerCore`, `PrimerNetworking`, `PrimerResources`, `PrimerUI`, `PrimerStepResolver`, `PrimerBDCCore`, `PrimerBDCEngine`, `PrimerBDCUI`)
- `Primer3DS`, `PrimerKlarnaSDK`, `PrimerIPay88MYSDK`, `PrimerNolPaySDK`, `PrimerStripeSDK`

Versions released before 2 December 2026 were copied from Trunk with `scripts/backfill_from_trunk.py`.

## Publishing

The release jobs of primer-sdk-ios and the wrapper repos push here with `pod repo push primer-sdk-ios-specs --use-json`. They get write access through the `SPEC_REPO_TOKEN` CI variable. Do not edit published specs by hand.
