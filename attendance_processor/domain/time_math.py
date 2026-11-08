"""פונקציות עזר לחישובים מתמטיים של שעות וזמנים בדומיין הנוכחות."""

from datetime import datetime, time
from typing import Optional


def parse_time(time_str: Optional[str]) -> Optional[time]:
    """ממיר מחרוזת שעה (למשל '08:00') לאובייקט time, או מחזיר None אם אינו תקין."""
    if not time_str or not isinstance(time_str, str):
        return None
    time_str = time_str.strip()
    for fmt in ("%H:%M", "%H:%M:%S"):
        try:
            return datetime.strptime(time_str, fmt).time()
        except ValueError:
            continue
    return None


def time_to_minutes(t: time) -> int:
    """ממיר אובייקט time לסך הדקות שעברו מתחילת היממה."""
    return t.hour * 60 + t.minute


def minutes_to_time_str(total_minutes: int) -> str:
    """ממיר סך דקות חזרה למחרוזת בפורמט 'HH:MM'."""
    total_minutes = max(0, total_minutes)
    hours = (total_minutes // 60) % 24
    minutes = total_minutes % 60
    return f"{hours:02d}:{minutes:02d}"


def shift_time_str(time_str: Optional[str], delta_minutes: int) -> Optional[str]:
    """מזיז מחרוזת שעה במספר דקות נתון ומחזיר מחרוזת מעודכנת."""
    t = parse_time(time_str)
    if not t:
        return time_str
    
    total_mins = time_to_minutes(t) + delta_minutes
    return minutes_to_time_str(total_mins)


def calculate_hours_difference(entry_str: Optional[str], exit_str: Optional[str], break_str: Optional[str] = None) -> str:
    """מחשב את הפרש השעות בין יציאה לכניסה, בניכוי הפסקה (אם קיימת), ומחזיר מחרוזת 'HH:MM'."""
    entry_t = parse_time(entry_str)
    exit_t = parse_time(exit_str)
    
    if not entry_t or not exit_t:
        return "00:00"
    
    entry_mins = time_to_minutes(entry_t)
    exit_mins = time_to_minutes(exit_t)
    
    if exit_mins < entry_mins:
        exit_mins += 24 * 60
        
    total_mins = exit_mins - entry_mins
    
    # ניכוי הפסקה אם קיימת
    if break_str:
        break_t = parse_time(break_str)
        if break_t:
            total_mins -= time_to_minutes(break_t)
                
    return minutes_to_time_str(total_mins)