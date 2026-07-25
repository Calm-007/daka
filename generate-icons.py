import struct, zlib, math, os

def create_png(width, height, pixels):
    """pixels is list of (r,g,b,a) tuples, row by row"""
    def chunk(ctype, data):
        c = ctype + data
        crc = struct.pack('>I', zlib.crc32(c) & 0xffffffff)
        return struct.pack('>I', len(data)) + c + crc

    sig = b'\x89PNG\r\n\x1a\n'
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    ihdr = chunk(b'IHDR', ihdr_data)

    raw = b''
    for row in pixels:
        raw += b'\x00'
        for r, g, b, a in row:
            raw += struct.pack('BBBB', r, g, b, a)

    compressed = zlib.compress(raw)
    idat = chunk(b'IDAT', compressed)
    iend = chunk(b'IEND', b'')
    return sig + ihdr + idat + iend

def draw_icon(size):
    """Draw indigo circle + white checkmark"""
    cx = size / 2.0
    cy = size / 2.0
    radius = size * 0.46  # bigger circle

    pixels = []
    for y in range(size):
        row = []
        for x in range(size):
            dx = x - cx + 0.5
            dy = y - cy + 0.5
            dist = math.sqrt(dx*dx + dy*dy)

            if dist <= radius - 1.5:
                # Inside circle - check if checkmark
                # Checkmark: (0.28, 0.50) -> (0.42, 0.64) -> (0.70, 0.36)
                # Transform to pixel coords
                x_norm = (x + 0.5) / size
                y_norm = (y + 0.5) / size

                # Checkmark line 1: (0.28, 0.50) to (0.42, 0.64)
                # Checkmark line 2: (0.42, 0.64) to (0.70, 0.36)
                stroke_w = 0.09

                on_checkmark = False
                # Line 1
                on_checkmark = on_checkmark or point_near_segment(
                    x_norm, y_norm, 0.28, 0.50, 0.42, 0.64, stroke_w)
                # Line 2
                on_checkmark = on_checkmark or point_near_segment(
                    x_norm, y_norm, 0.42, 0.64, 0.70, 0.36, stroke_w)

                if on_checkmark:
                    row.append((255, 255, 255, 255))
                else:
                    row.append((79, 70, 229, 255))  # indigo
            elif dist <= radius + 1.0:
                # Anti-alias edge
                alpha = max(0, min(255, int(255 * (radius + 1.0 - dist))))
                row.append((79, 70, 229, alpha))
            else:
                row.append((0, 0, 0, 0))
        pixels.append(row)
    return pixels

def point_near_segment(px, py, x1, y1, x2, y2, width):
    """Check if point is near a line segment"""
    dx = x2 - x1
    dy = y2 - y1
    seg_len_sq = dx*dx + dy*dy
    if seg_len_sq < 1e-9:
        return math.sqrt((px-x1)**2 + (py-y1)**2) <= width/2

    t = max(0, min(1, ((px-x1)*dx + (py-y1)*dy) / seg_len_sq))
    proj_x = x1 + t * dx
    proj_y = y1 + t * dy
    return math.sqrt((px-proj_x)**2 + (py-proj_y)**2) <= width/2

# Generate icons
os.chdir(os.path.dirname(os.path.abspath(__file__)))

for size in [192, 512]:
    pixels = draw_icon(size)
    png_data = create_png(size, size, pixels)
    filename = f'icon-{size}.png'
    with open(filename, 'wb') as f:
        f.write(png_data)
    print(f'Created {filename} ({len(png_data)} bytes)')

print('Done!')
