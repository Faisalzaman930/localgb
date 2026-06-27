#!/usr/bin/env python3
"""Generate GB Guide favicons (no external deps): a Karakoram-peak mark — gold
range with a snow-capped summit on a dark rounded square. Renders supersampled
RGBA, downsamples for anti-aliasing, writes PNGs + a PNG-in-ICO.
Outputs: favicon.ico, favicon-48x48.png, favicon-96x96.png,
apple-touch-icon.png (180), icon-192.png, icon-512.png."""
import zlib, struct

INK   = (14, 17, 23)      # dark rounded-square background
GOLD  = (200, 144, 58)    # peaks
GOLDD = (139, 98, 26)     # base line
CREAM = (240, 232, 213)   # snow cap

# geometry in a 0..1 square (y down)
RANGE = [(0.09,0.78),(0.31,0.44),(0.42,0.56),(0.58,0.25),(0.70,0.45),(0.80,0.37),(0.91,0.78)]
CAP   = [(0.58,0.25),(0.515,0.40),(0.645,0.40)]     # snow cap on main summit
BASE_Y0, BASE_Y1 = 0.78, 0.82                       # baseline bar
CORNER = 0.22                                        # rounded-corner radius (fraction)

def in_poly(x, y, pts):
    n=len(pts); inside=False; j=n-1
    for i in range(n):
        xi,yi=pts[i]; xj,yj=pts[j]
        if ((yi>y)!=(yj>y)) and (x < (xj-xi)*(y-yi)/(yj-yi)+xi): inside=not inside
        j=i
    return inside

def in_rounded(x, y, r):
    if x<r and y<r:   return (x-r)**2+(y-r)**2 <= r*r
    if x>1-r and y<r: return (x-(1-r))**2+(y-r)**2 <= r*r
    if x<r and y>1-r: return (x-r)**2+(y-(1-r))**2 <= r*r
    if x>1-r and y>1-r: return (x-(1-r))**2+(y-(1-r))**2 <= r*r
    return True

def sample(u, v):
    """colour (r,g,b,a) at fractional coords u,v in 0..1."""
    if not in_rounded(u, v, CORNER): return (0,0,0,0)
    col = INK
    if BASE_Y0 <= v <= BASE_Y1 and 0.09 <= u <= 0.91: col = GOLDD
    if in_poly(u, v, RANGE): col = GOLD
    if in_poly(u, v, CAP):   col = CREAM
    return (col[0], col[1], col[2], 255)

def render(size, ss=4):
    W = size*ss
    # supersampled buffer
    buf = [[ (0,0,0,0) ]*W for _ in range(W)]
    for py in range(W):
        v = (py+0.5)/W
        row = buf[py]
        for px in range(W):
            row[px] = sample((px+0.5)/W, v)
    # downsample ss x ss (average, premultiplied-ish over transparent)
    out = bytearray()
    for y in range(size):
        out_row = bytearray([0])  # PNG filter byte 0
        for x in range(size):
            r=g=b=a=0
            for dy in range(ss):
                for dx in range(ss):
                    pr,pg,pb,pa = buf[y*ss+dy][x*ss+dx]
                    r+=pr*pa; g+=pg*pa; b+=pb*pa; a+=pa
            n=ss*ss
            if a>0:
                out_row += bytes((r//a, g//a, b//a, a//n))
            else:
                out_row += b"\x00\x00\x00\x00"
        out += out_row
    return bytes(out)

def png_bytes(size):
    raw = render(size)
    def chunk(typ, data):
        return struct.pack(">I", len(data)) + typ + data + struct.pack(">I", zlib.crc32(typ+data) & 0xffffffff)
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)  # 8-bit RGBA
    idat = zlib.compress(raw, 9)
    return sig + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")

def write(path, size):
    with open(path,"wb") as f: f.write(png_bytes(size))
    print("  wrote", path, f"({size}x{size})")

def write_ico(path, size=48):
    png = png_bytes(size)
    # ICONDIR + 1 entry, image stored as PNG
    hdr = struct.pack("<HHH", 0, 1, 1)
    entry = struct.pack("<BBBBHHII", size&0xFF, size&0xFF, 0, 0, 1, 32, len(png), 22)
    with open(path,"wb") as f: f.write(hdr+entry+png)
    print("  wrote", path, "(ICO)")

if __name__ == "__main__":
    print("Generating favicons…")
    write("favicon-48x48.png", 48)
    write("favicon-96x96.png", 96)
    write("apple-touch-icon.png", 180)
    write("icon-192.png", 192)
    write("icon-512.png", 512)
    write_ico("favicon.ico", 48)
    print("done.")
