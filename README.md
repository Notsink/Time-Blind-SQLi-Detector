# Time-Blind SQLi Detector

Time-Blind SQLi Detector is a single-file, zero-dependency Python utility that exposes time-based blind SQL injection flaws through simple HTTP timing tests.
It targets penetration testers, red-teamers, and developers who need a quick, visual confirmation without installing heavy scanners.

# Features

| Feature               | Detail                                                    |
| --------------------- | --------------------------------------------------------- |
| **Single file**       | `sqli_detector.py` – copy anywhere, run instantly.        |
| **Zero dependencies** | Uses only the Python 3 standard library.                  |
| **Dark GUI**          | Consistent dark theme matching modern pentest toolchains. |
| **Real-time log**     | Color-coded output: red for vulnerable, green for clean.  |
| **Adjustable delay**  | Spin-box from 3 s to 15 s to match network jitter.        |
| **Cross-platform**    | Runs on Windows, macOS, and Linux without changes.        |

# How it works

  1.  Sends two GET requests to the same endpoint/parameter.
  2.  First request measures baseline response time.
  3.  Second request appends AND SLEEP(n) (configurable).
  4.  If the delta ≥ delay – 0.5 s, the parameter is marked vulnerable.

# Target use cases

Spot-checking individual parameters during manual testing.

Quick triage of suspected endpoints before deeper scans.

Teaching/CTF environments to demonstrate blind SQLi without complex setups.

# Security notes

Only read-only requests are issued; no data is altered.
Designed for authorized testing; users must ensure proper permissions.

# Contributing

Pull requests for small UI tweaks or additional payload formats are welcome.
For bugs, open an issue with target type, payload, and observed delta.

# Acknowledgments

Inspired by classic timing techniques and modern dark-themed security tools.

# How to Tell If a Site Is Vulnerable

 1. Run the Detector
  Enter the full URL (e.g. https://shop.example.com/product.php?id=7) and the parameter you suspect (id).

 2. Watch the Result Line

    Red line (🔴 VULNERABLE: +X.Xs) – the second request (with SLEEP) took at least delay – 0.5 s longer than the baseline.

    Green line (✅ Safe: delta +X.Xs) – the difference is smaller or even negative.

    Gray/negative delta – the test is inconclusive; the server may ignore the injected clause or return cached data.

 3.  Confirm Manually
    Change the injected clause to a different delay (sleep(8) instead of sleep(5)). If the delta shifts by the same amount, the injection is confirmed.

 4. Double-Check Network Jitter
    If the site is very slow or inconsistent, raise the delay in the GUI (e.g. 8–10 s) and retest.
