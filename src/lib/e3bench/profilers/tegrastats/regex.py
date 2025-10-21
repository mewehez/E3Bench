import re


# --------- Regex patterns (robust to small format variations) ----------
TS_RE        = re.compile(r'^(?P<ts>\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2})\b')
RAM_RE       = re.compile(r'RAM (?P<used>\d+)/(?P<total>\d+)MB \(lfb (?P<lfb_blocks>\d+)x(?P<lfb_mb>\d+)MB\)')
SWAP_RE      = re.compile(r'SWAP (?P<used>\d+)/(?P<total>\d+)MB \(cached (?P<cached>\d+)MB\)')
CPU_RE       = re.compile(r'CPU \[(?P<body>[^\]]+)\]')
EMC_RE       = re.compile(r'EMC_FREQ (?P<pct>\d+)%@(?P<mhz>\d+)')
#GR3D_RE      = re.compile(r'GR3D_FREQ (?P<pct>\d+)%@(?P<rest>\S+)')  # e.g. @305 or @[305,0]
VIC_RE       = re.compile(r'VIC_FREQ (?P<mhz>\d+)')
APE_RE       = re.compile(r'APE (?P<mhz>\d+)')
TEMP_RE      = re.compile(r'\b(?P<temp_name>[a-zA-Z0-9]+)@(?P<temp_c>-?\d+(?:\.\d+)?)C\b') # temp_name
PWR_RE       = re.compile(r'\b(?P<rail>[A-Z0-9_]+) (?P<now_mw>\d+)mW/(?P<avg_mw>\d+)mW\b') # vdd_name

GR3D_RE = re.compile(
    r"""
    GR3D_FREQ
    \s+
    (?P<pct>\d+)%
    @
    (?:                      # non-capturing group for the frequency part
        \[                   # case like [305,0]
           (?P<mhz_bracket>\d+)      # capture the first number inside brackets
           (?:,[^\]]*)?       # ignore the rest
        \]
      | (?P<mhz_plain>\d+)    # OR plain number like 305
    )
    """, re.X
)

# re.X is for ignoring white space and comments while compiling the regex
CPU_PAIR_RE = re.compile(
    r"""\s*
        (?:
        (?P<pct>\d+)%@(?P<mhz>\d+)    # e.g. 33%@1497
        | (?P<off>off)                  # or the token 'off'
        )
        \s*(?:,|$)                        # followed by comma or end
    """, re.X
)

__all__ = [
    "TS_RE",
    "RAM_RE",
    "SWAP_RE",
    "CPU_RE",
    "CPU_PAIR_RE",
    "EMC_RE",
    "GR3D_RE",
    "VIC_RE",
    "APE_RE",
    "TEMP_RE",
    "PWR_RE",
]