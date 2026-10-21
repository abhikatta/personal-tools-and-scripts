"""Toggle external monitor between 1440p60 and 1080p120. Usage: res [1440|1080]"""

import sys
from gi.repository import Gio

TARGETS = {"1440": (2560, 1440, 60), "1080": (1920, 1080, 120)}
PERSISTENT = False  # True = GNOME remembers it after reboot

bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
proxy = Gio.DBusProxy.new_sync(
    bus,
    Gio.DBusProxyFlags.NONE,
    None,
    "org.gnome.Mutter.DisplayConfig",
    "/org/gnome/Mutter/DisplayConfig",
    "org.gnome.Mutter.DisplayConfig",
    None,
)

serial, monitors, logical, _ = proxy.call_sync(
    "GetCurrentState", None, Gio.DBusCallFlags.NONE, -1, None
).unpack()

modes_by_conn, current = {}, {}
for spec, modes, _p in monitors:
    conn = spec[0]
    modes_by_conn[conn] = modes
    current[conn] = next(m for m in modes if m[6].get("is-current"))

externals = [c for c in modes_by_conn if not c.startswith("eDP")]
if not externals:
    sys.exit("No external monitor detected.")
ext = externals[0]

if len(sys.argv) > 1 and sys.argv[1] in TARGETS:
    key = sys.argv[1]
else:
    key = "1080" if current[ext][2] == 1440 else "1440"

w, h, hz = TARGETS[key]
new_mode = next(
    (m for m in modes_by_conn[ext] if (m[1], m[2]) == (w, h) and abs(m[3] - hz) < 0.5),
    None,
)
if new_mode is None:
    sys.exit(f"Mode {w}x{h}@{hz} not offered on {ext}.")

chosen = dict(current)
chosen[ext] = new_mode

# Re-pack screens left to right so there are no gaps or overlaps after the size change
cfg, x_cursor = [], 0
for lx, ly, scale, transform, primary, mons, _p in sorted(logical, key=lambda l: l[0]):
    conn = mons[0][0]
    m = chosen[conn]
    cfg.append(
        (
            x_cursor,
            ly,
            scale,
            transform,
            primary,
            [(c[0], chosen[c[0]][0], {}) for c in mons],
        )
    )
    x_cursor += round(m[1] / scale)

from gi.repository import GLib

params = GLib.Variant(
    "(uua(iiduba(ssa{sv}))a{sv})", (serial, 2 if PERSISTENT else 1, cfg, {})
)
proxy.call_sync("ApplyMonitorsConfig", params, Gio.DBusCallFlags.NONE, -1, None)
print(f"{ext}: {w}x{h} @ {new_mode[3]:.2f}Hz")
