from pathlib import Path
from typing import Union
from datetime import datetime
from collections import defaultdict
import pandas as pd
from loguru import logger
from .regex import *



def parse_line(line: str):
    row = {}

    # Timestamp
    tm = TS_RE.search(line)
    if not tm:
        return None  # skip unrecognized lines
    
    # Conversion to ISO dt (can be localized if you needed)
    row['timestamp_raw'] = tm.group('ts')
    row['timestamp_ns'] = datetime.strptime(tm.group('ts'), '%m-%d-%Y %H:%M:%S').timestamp() * 1e9

    # RAM / SWAP
    if m := RAM_RE.search(line):
        row['ram_used_mb'] = int(m.group('used'))
        row['ram_total_mb'] = int(m.group('total'))
        row['lfb_blocks']  = int(m.group('lfb_blocks'))
        row['lfb_block_mb']= int(m.group('lfb_mb'))

    if m := SWAP_RE.search(line):
        row['swap_used_mb']   = int(m.group('used'))
        row['swap_total_mb']  = int(m.group('total'))
        row['swap_cached_mb'] = int(m.group('cached'))
    
    # CPU block
    if m := CPU_RE.search(line):
        body = m.group('body')
        pairs = CPU_PAIR_RE.findall(body)
        for (i, pair) in enumerate(pairs):
            if pair[2]:
                v, f = None, None
            else:
                v = int(pair[0])
                f = int(pair[1])
            row[f'cpu{i}_pct'] = v
            row[f'cpu{i}_mhz'] = f
    
    # EMC / GR3D / VIC / APE
    if m := EMC_RE.search(line):
        row['emc_pct'] = int(m.group('pct'))
        row['emc_mhz'] = int(m.group('mhz'))

    if m := GR3D_RE.search(line):
        row['gr3d_pct'] = int(m.group('pct'))
        row['gr3d_mhz'] = int(m.group('mhz_plain') or m.group('mhz_bracket'))

    if m := VIC_RE.search(line):
        row['vic_mhz'] = int(m.group('mhz'))
    if m := APE_RE.search(line):
        row['ape_mhz'] = int(m.group('mhz'))
    
    # Temperatures (expand into columns)
    if pairs := TEMP_RE.findall(line):
        for pair in pairs:
            # Some sensors report -256C when unavailable; keep as None
            label = pair[0]
            temp = float(pair[1])
            row[f'temp_{label}_C'] = None if temp <= -200 else temp
    
    # Power rails (instant/avg)
    if pairs := PWR_RE.findall(line):
        for pair in pairs:
            rail = pair[0]
            row[f'{rail}_mw_now'] = int(pair[1])
            row[f'{rail}_mw_avg'] = int(pair[2])
    
    return row


def adjust_timestamp(dataframe: pd.DataFrame) -> pd.DataFrame:
    # 1) Sort by insertion order
    # df = df.sort_values('row_idx').reset_index(drop=True)

    # 3) Group by the *second* (integer seconds from epoch)
    second_key = dataframe['timestamp_ns']

    # Stable order within each second follows the current row order (after sort by row_idx)
    order_in_grp = second_key.groupby(second_key).cumcount()              # 0..n-1
    size_in_grp  = second_key.groupby(second_key).transform('size')       # n for each row

    # 4) Evenly space offsets within the 1-second window (strictly < 1e9 ns)
    #    This guarantees the adjusted timestamps never spill into the next second.
    offset_ns = (1_000_000_000 * order_in_grp) // size_in_grp

    # 5) Final adjusted timestamp at nanosecond resolution
    dataframe['timestamp_ns'] = dataframe['timestamp_ns'] + offset_ns

    return dataframe



def post_process_jetson_orin_nano(log_path: Union[str, Path]):
    log_path = Path(log_path).resolve()
    logger.debug(f'Processing power from {log_path}')

    rows = []
    with open(log_path) as f:
        row_idx = 0
        for line in f:
            line = line.strip()
            if not line:
                continue
            clean_row = parse_line(line)
            
            if clean_row:
                clean_row['row_idx'] = row_idx
                rows.append(clean_row)
                row_idx += 1

    if not rows:
        logger.info("No parsable lines found.")
        return
    
    # Normalize to DataFrame
    df = pd.DataFrame(rows).sort_values(['timestamp_ns','row_idx']).reset_index(drop=True)

    cols = ['timestamp_raw', 'timestamp_ns', 'row_idx']
    cols += sorted([c for c in df.columns if (c not in cols)])
    df = df[cols]

    # Adjust timestamp from seconds to nanoseconds
    df = adjust_timestamp(df)

    # Small summary preview
    try:
        summary = defaultdict(dict)
        if 'VDD_SOC_mw_now' in df.columns:
            summary['power']['VDD_SOC_mw_now_mean'] = float(df['VDD_SOC_mw_now'].mean())
            summary['power']['VDD_SOC_mw_now_max']  = int(df['VDD_SOC_mw_now'].max())
        if 'emc_pct' in df:
            summary['emc']['emc_pct_mean'] = float(df['emc_pct'].mean())
        if any(c.startswith('cpu0_pct') for c in df.columns):
            summary['cpu']['cpu0_pct_mean'] = float(df['cpu0_pct'].mean())

        # Compute sampling frequency as: N / (t_last - t_first)
        tcol = 'timestamp_ns'
        nb_samples = len(df)
        duration_s = (df[tcol].iloc[-1] - df[tcol].iloc[0]) / 1e9  # ns → s
        freq_Hz = nb_samples / duration_s if duration_s > 0 else float('nan')
        summary['sampling'] = {
            'nb_samples': int(nb_samples),
            'duration_s': float(duration_s),
            'freq_Hz': float(freq_Hz),
        }
        logger.info(f'Quick summary: {dict(summary)}')
    except Exception:
        pass

    return df
