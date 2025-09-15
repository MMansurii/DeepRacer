import math

CFG = {
    # نگاه جلو
    "look_min": 3,
    "look_max": 6,

    # آستانه‌های انحنا (درجه)
    "deg_soft": 8.0,
    "deg_hard": 18.0,

    # بایاس داخل پیچ و صاف‌سازی چیکین
    "bias_soft": 1.06,
    "bias_hard": 1.25,
    "chicane_gain": 1.20,
    "straight_ref_deg": 5.0,   # فرمان کمتر از این → پاداش در چیکین

    # نگاشت سرعت هدف (هم‌راستا با اکشن‌ها: 1.1 / 2.3 / 3.6)
    "v_hi": 3.0,               # نزدیک مستقیم
    "v_lo": 1.8,               # پیچ تند
    "spd_bonus_cap": 1.20,

    # هدینگ/فرمان
    "steer_full_deg": 30.0,
    "heading_drop_deg": 45.0,

    # لِترال-G ملایم (سرعت^2 × انحنا)
    "lat_k": 0.015,            # ضریب مهار در پیچ اگر سرعت زیاد باشد

    # پیشرفت
    "prog_rate": 0.12,         # ≈ 100% در ~830 گام

    # کلیپ نهایی
    "r_min": 1e-3,
    "r_max": 3.0,
}

def _ang(ax, ay, bx, by):
    return math.degrees(math.atan2(by - ay, bx - ax))

def _diff(a, b):
    d = (a - b) % 360.0
    return d - 360.0 if d > 180.0 else d

def reward_function(params):
    if (not params.get("all_wheels_on_track", True)) or params.get("is_reversed", False):
        return CFG["r_min"]

    wp = params["waypoints"]
    i_prev, i_next = params["closest_waypoints"]
    N = len(wp)

    speed    = params["speed"]
    steer    = abs(params["steering_angle"])
    heading  = params["heading"]
    is_left  = params["is_left_of_center"]
    dist_c   = params["distance_from_center"]
    width    = params["track_width"]
    steps    = params["steps"]
    prog     = params["progress"]

    # جهت فعلی مسیر و خطای هدینگ
    x1, y1 = wp[i_prev]
    x2, y2 = wp[i_next]
    dir_now = _ang(x1, y1, x2, y2)
    h_err = abs(_diff(heading, dir_now))
    r_head = max(0.0, 1.0 - h_err / CFG["heading_drop_deg"])

    # نگاه جلو تطبیقی
    L = max(CFG["look_min"], min(CFG["look_max"], CFG["look_min"] + int(min(3, h_err // 10))))

    dirs = [dir_now]
    idx = i_next
    for _ in range(L):
        a = wp[idx]; b = wp[(idx + 1) % N]
        dirs.append(_ang(a[0], a[1], b[0], b[1]))
        idx = (idx + 1) % N

    signed_sum = 0.0
    ds = []
    for k in range(len(dirs) - 1):
        d = _diff(dirs[k + 1], dirs[k])
        ds.append(d); signed_sum += d

    mean_abs = sum(abs(d) for d in ds) / max(1, len(ds))
    turn_sign = 0 if abs(signed_sum) < 1e-6 else (1 if signed_sum > 0 else -1)  # +چپ، -راست
    is_turn  = mean_abs >= CFG["deg_soft"]
    is_hard  = mean_abs >= CFG["deg_hard"]
    is_chic  = (abs(signed_sum) < CFG["deg_soft"]) and (mean_abs >= CFG["deg_soft"])

    # لاین: داخل پیچ یا صاف‌سازی چیکین
    r_line = 1.0
    if is_chic:
        steer_rel = max(0.0, 1.0 - steer / CFG["straight_ref_deg"])
        r_line *= 1.0 + (CFG["chicane_gain"] - 1.0) * steer_rel
    elif is_turn and turn_sign != 0:
        gain = CFG["bias_hard"] if is_hard else CFG["bias_soft"]
        on_inside = (is_left and turn_sign > 0) or ((not is_left) and turn_sign < 0)
        # نرمال‌شده نسبت به نیم‌عرض
        dnorm = min(1.0, dist_c / (0.5 * width))
        if on_inside:
            r_line *= 1.0 + (gain - 1.0) * min(1.0, 0.5 + 0.5 * dnorm)
        else:
            r_line *= max(0.80, 1.0 - 0.3 * (0.5 + 0.5 * dnorm))

    # نگاشت سرعت هدف بر پایه انحنا (پیوسته)
    t = max(0.0, min(1.0, (mean_abs - CFG["deg_soft"]) / max(1.0, (CFG["deg_hard"] - CFG["deg_soft"]))))
    v_tgt = CFG["v_hi"] * (1.0 - t) + CFG["v_lo"] * t
    if is_chic:
        v_tgt = max(CFG["v_lo"], 0.85 * CFG["v_hi"])

    # مهار لِترال (سرعت^2 × انحناِ رادیانی)
    lat = (speed ** 2) * (abs(math.radians(mean_abs)))
    lat_pen = max(0.7, 1.0 - CFG["lat_k"] * lat)

    if speed >= v_tgt:
        r_spd = min(CFG["spd_bonus_cap"], 0.6 + (speed / max(1e-6, v_tgt)) * 0.4)
    else:
        r_spd = max(0.6, 1.0 - (v_tgt - speed) * 0.3)

    # نرمی فرمان
    r_steer = max(0.3, 1.0 - (steer / CFG["steer_full_deg"]))

    # پیشرفت پایدار
    exp_p = min(100.0, steps * CFG["prog_rate"])
    r_prog = 1.0 if prog >= exp_p else 0.8

    reward = 1.0
    for comp in (r_head, r_line, r_spd * lat_pen, r_steer, r_prog):
        reward *= comp

    return float(min(CFG["r_max"], max(CFG["r_min"], reward)))
