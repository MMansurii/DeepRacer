import math

CFG = {
    "look_min": 3,
    "look_max": 6,
    "deg_soft": 10.0,
    "deg_hard": 20.0,
    "deg_sharp": 35.0,
    "corner_cut_threshold": 30.0,  
    "edge_bonus_sharp": 1.40,
    "safe_margin": 0.04,
    "v_straight": 4.0,
    "v_turn": 2.4,
    "v_sharp": 1.2,
    "spd_bonus": 1.35,
    "steer_full_deg": 30.0,
    "heading_tolerance": 35.0,
    "prog_rate": 0.14,
    "off_track_penalty": 0.001,
    "r_min": 1e-3,
    "r_max": 3.5,
}

def _ang(ax, ay, bx, by):
    return math.degrees(math.atan2(by - ay, bx - ax))

def _diff(a, b):
    d = (a - b) % 360.0
    return d - 360.0 if d > 180.0 else d

def reward_function(params):
    if not params.get("all_wheels_on_track", True) or params.get("is_reversed", False):
        return CFG["off_track_penalty"]
    
    wp = params["waypoints"]
    i_prev, i_next = params["closest_waypoints"]
    N = len(wp)
    
    speed = params["speed"]
    steer = abs(params["steering_angle"])
    heading = params["heading"]
    is_left = params["is_left_of_center"]
    dist_c = params["distance_from_center"]
    width = params["track_width"]
    steps = params["steps"]
    prog = params["progress"]
    
    x1, y1 = wp[i_prev]
    x2, y2 = wp[i_next]
    dir_now = _ang(x1, y1, x2, y2)
    h_err = abs(_diff(heading, dir_now))
    
    look = min(CFG["look_max"], CFG["look_min"] + int(speed))
    
    dirs = [dir_now]
    idx = i_next
    for _ in range(look):
        a = wp[idx]
        b = wp[(idx + 1) % N]
        dirs.append(_ang(a[0], a[1], b[0], b[1]))
        idx = (idx + 1) % N
    
    deltas = []
    for k in range(len(dirs) - 1):
        deltas.append(_diff(dirs[k + 1], dirs[k]))
    
    signed_sum = sum(deltas)
    mean_abs = sum(abs(d) for d in deltas) / max(1, len(deltas))
    max_curve = max(abs(d) for d in deltas) if deltas else 0
    
    is_sharp = max_curve >= CFG["deg_sharp"] or mean_abs >= 30.0
    is_turn = mean_abs >= CFG["deg_soft"]
    turn_sign = 0 if abs(signed_sum) < 1e-6 else (1 if signed_sum > 0 else -1)
    
    r_head = max(0.4, 1.0 - h_err / CFG["heading_tolerance"])
    if is_sharp:
        r_head = max(0.6, r_head)
    
    r_line = 1.0
    half_width = 0.5 * width
    safe_edge = half_width * (1.0 - CFG["safe_margin"])
    
    if is_sharp and mean_abs >= CFG["corner_cut_threshold"]:
        on_inside = (is_left and turn_sign > 0) or ((not is_left) and turn_sign < 0)
        
        if on_inside:
            if dist_c > safe_edge * 0.8:
                r_line = CFG["edge_bonus_sharp"]
            elif dist_c > safe_edge * 0.5:
                r_line = 1.20
            else:
                r_line = 1.0
        else:
            if dist_c > half_width * 0.6:
                r_line = 1.15
            else:
                r_line = 0.85
    
    elif is_turn:
        on_inside = (is_left and turn_sign > 0) or ((not is_left) and turn_sign < 0)
        if on_inside:
            r_line = 1.0 + 0.15 * (dist_c / half_width)
        else:
            r_line = max(0.9, 1.0 - 0.1 * (1.0 - dist_c / half_width))
    
    else:
        center_factor = 1.0 - (dist_c / half_width) * 0.2
        r_line = center_factor
    
    if is_sharp:
        v_target = CFG["v_sharp"]
        if speed <= 1.5:
            r_spd = 1.0
        else:
            r_spd = 0.3
            
    elif is_turn:
        v_target = CFG["v_turn"]
        if speed >= v_target * 0.8:
            r_spd = 1.0 + (speed / v_target - 0.8) * 0.3
        else:
            r_spd = 0.5 + 0.5 * (speed / (v_target * 0.8))
            
    else:
        v_target = CFG["v_straight"]
        if speed >= 3.6:
            r_spd = CFG["spd_bonus"]
        elif speed >= 3.0:
            r_spd = 1.0
        else:
            r_spd = 0.3
    
    if is_sharp:
        r_steer = 1.0
    else:
        r_steer = max(0.5, 1.0 - 0.5 * (steer / CFG["steer_full_deg"]))
    
    exp_p = min(100.0, steps * CFG["prog_rate"])
    if prog >= exp_p:
        r_prog = 1.2
    elif prog >= exp_p * 0.85:
        r_prog = 0.9
    else:
        r_prog = 0.6
    
    reward = r_head * r_line * r_spd * r_steer * r_prog
    
    if not is_turn and speed >= 3.6:
        reward *= 1.15
    
    if is_sharp and on_inside and dist_c > safe_edge * 0.7 and speed <= 1.5:
        reward *= 1.10
    
    return float(min(CFG["r_max"], max(CFG["r_min"], reward)))