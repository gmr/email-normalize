Release History
===============

3.0.0
-----
- FIXED: Multi-segment TLD normalization using tldextract library
- FIXED: Fastmail subdomain parsing for domains like .co.uk, .com.au

2.0.0
-----
- FIXED: Remove period stripping from Yahoo domain normalization
- ADDED: googlemail.com support and consistent host lowercasing
- CHANGED: Make Normalizer no longer a singleton
- FIXED: Handle domains with no MX records

1.0.2
-----
- FIXED: Documentation and distribution improvements
- CHANGED: Modernized test infrastructure and Python version support
- REMOVED: Python 3.5 and 3.6 support

1.0.0
-----
- Initial stable release with modernized codebase
- ADDED: Optional DNS resolution and timeout handling
- FIXED: Python 2/3 compatibility issues