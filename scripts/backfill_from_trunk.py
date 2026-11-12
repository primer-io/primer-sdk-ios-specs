#!/usr/bin/env python3
"""Copy every published version of the Primer pods from the CocoaPods Trunk CDN into this spec repo.

CocoaPods takes a pod from the first source in the Podfile that has it, so this repo must hold
the old versions too, or apps pinned to an old version stop resolving.
"""
import hashlib, json, pathlib, sys, time, urllib.request

PODS = [
    "PrimerSDK", "PrimerFoundation", "PrimerCore", "PrimerNetworking", "PrimerResources", "PrimerUI",
    "PrimerStepResolver", "PrimerBDCCore", "PrimerBDCEngine", "PrimerBDCUI",
    "Primer3DS", "PrimerKlarnaSDK", "PrimerIPay88MYSDK", "PrimerNolPaySDK", "PrimerStripeSDK",
]
CDN = "https://cdn.cocoapods.org"
ROOT = pathlib.Path(__file__).resolve().parent.parent

def get(url, attempts=4):
    request = urllib.request.Request(url, headers={"User-Agent": "primer-sdk-ios-specs-backfill"})
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read()
        except OSError:
            if attempt == attempts - 1:
                raise
            time.sleep(2 ** attempt)

def shard(pod):
    return list(hashlib.md5(pod.encode()).hexdigest()[:3])

def versions(pod):
    index = get(f"{CDN}/all_pods_versions_{'_'.join(shard(pod))}.txt").decode()
    for line in index.splitlines():
        name, *found = line.split("/")
        if name == pod:
            return found
    return []

def main():
    total = 0
    for pod in PODS:
        found = versions(pod)
        for version in found:
            target = ROOT / pod / version / f"{pod}.podspec.json"
            if target.exists():
                continue
            spec = get(f"{CDN}/Specs/{'/'.join(shard(pod))}/{pod}/{version}/{pod}.podspec.json")
            json.loads(spec)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(spec)
            total += 1
        print(f"{pod}: {len(found)} versions on Trunk", file=sys.stderr)
    print(f"{total} podspecs added", file=sys.stderr)

if __name__ == "__main__":
    main()
