from generators.config import get_color_map
from math import sin, cos, pi, sqrt
from random import uniform, randint

color_map: dict[str, str] = get_color_map()

Number = int | float

Width, Height = Number, Number
Dimensions = tuple[Width, Height]

Point = tuple[Number, Number]

SortedElements = dict[str, Number]
MaxElements = int
ElementsInfo = tuple[SortedElements, MaxElements]


def _calculate_radius(desired_area: Number) -> Number:
    return sqrt(desired_area / pi)


def _generate_points(num_points: int, radius: Number, frame_offset: Number = 0) -> list[Point]:
    points = []
    angle_step = 2 * pi / num_points
    
    for i in range(num_points):
        angle = i * angle_step
        r = radius * uniform(0.7, 1.3)
        angle_offset = frame_offset + uniform(-0.2, 0.2)
        final_angle = angle + angle_offset
        
        x = r * cos(final_angle)
        y = r * sin(final_angle)
        points.append((x, y))
    
    return points


def _calculate_control_points(current: Point, next_point: Point) -> tuple[Point, Point]:
    mid_x = (current[0] + next_point[0]) / 2
    mid_y = (current[1] + next_point[1]) / 2
    
    dx = next_point[0] - current[0]
    dy = next_point[1] - current[1]
    length = sqrt(dx*dx + dy*dy)
    
    if length > 0:
        perp_x = -dy / length
        perp_y = dx / length
        offset = uniform(0.3, 0.6) * length
        
        cp1_x = mid_x + perp_x * offset * uniform(-1, 1)
        cp1_y = mid_y + perp_y * offset * uniform(-1, 1)
        cp2_x = mid_x + perp_x * offset * uniform(-1, 1)
        cp2_y = mid_y + perp_y * offset * uniform(-1, 1)
    else:
        cp1_x, cp1_y = current
        cp2_x, cp2_y = next_point
    
    return (cp1_x, cp1_y), (cp2_x, cp2_y)


def _build_path_from_points(points: list[Point]) -> str:
    num_points = len(points)
    path_parts = [f"M {points[0][0]:.0f},{points[0][1]:.0f}"]
    
    for i in range(num_points):
        current = points[i]
        next_point = points[(i + 1) % num_points]
        cp1, cp2 = _calculate_control_points(current, next_point)
        
        path_parts.append(
            f"C {cp1[0]:.0f},{cp1[1]:.0f} {cp2[0]:.0f},{cp2[1]:.0f} {next_point[0]:.0f},{next_point[1]:.0f}"
        )
    
    path_parts.append("Z")
    return "\n\t\t".join(path_parts)


def _calculate_keyframes(blob_area: Number, svg_area: Number, min_frames: int = 3, max_frames: int = 10) -> int:
    percentage = blob_area / svg_area
    frames = int(min_frames + (max_frames - min_frames) * percentage)
    return max(min_frames, min(frames, max_frames))

def generate_blob_path(svg_total_dimensions: Dimensions, desired_area: Number, num_keyframes: int | None = None) -> str:
    svg_x, svg_y = svg_total_dimensions
    svg_area = svg_x * svg_y
    
    if num_keyframes is None:
        num_keyframes = _calculate_keyframes(desired_area, svg_area)
    
    radius = _calculate_radius(desired_area)
    num_points = randint(5, 8)
    
    paths = []
    
    for frame in range(num_keyframes):
        if frame == num_keyframes - 1:
            paths.append(paths[0])
            continue
        
        frame_offset = frame * 0.3
        points = _generate_points(num_points, radius, frame_offset)
        path = _build_path_from_points(points)
        paths.append(path)
    
    return ";\n\n\t\t".join(paths)

class Background:
    def __init__(self, elements_info: ElementsInfo, dimensions: Dimensions, debug: bool = False):
        self.all_elements, self.max_elements = elements_info
        self.width, self.height = dimensions
        self.debug = debug

    def apple(self) -> str:
        header = f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
        foot = '</svg>'

        if not self.all_elements: 
            return f'{header}<rect width="100%" height="100%" fill="#0d1119" />{foot}'
        
        drift_max = 50
        blur = 20
        top_langs = list(self.all_elements.items())[:self.max_elements]

        svg_parts = [header]
        svg_parts.append(f'<defs><filter id="blobBlur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{blur}"/></filter></defs>')
        _percent = 100
        for i, (lang, percent) in enumerate(top_langs):
            color = color_map.get(lang, '#858585')
            if i == 0:
                svg_parts.append(f'<rect width="100%" height="100%" fill="{color}"/>')
            else:
                if i == 5:
                    lang = 'Others'
                    percent = _percent
                    color = color_map.get(lang, '#858585')
                
                if self.debug:
                    print(
                        f'{i}/{len(top_langs)}:\n'
                        f"{'Language:':4} {lang}' -> '{percent}%\n"
                        f"{'Others:':4}  -> {_percent}%\n"
                        )
                scale = percent / 100
                x = uniform(0, self.width * (1 - scale))
                y = uniform(0, self.height * (1 - scale))
                
                blob_area = self.width * self.height * scale
                
                shapes = generate_blob_path((self.width, self.height), blob_area, num_keyframes=3)
                
                tx1, ty1 = x, y
                tx2, ty2 = x + uniform(-drift_max, drift_max), y + uniform(-drift_max, drift_max)
                tx3, ty3 = x + uniform(-drift_max, drift_max), y + uniform(-drift_max, drift_max)
                locations = f"{tx1},{ty1};{tx2},{ty2};{tx3},{ty3};{tx1},{ty1}"
                
                morph_dur = uniform(15, 35)
                drift_dur = uniform(20, 40)
                
                if self.debug:
                    print(f'Blob for {lang} ({percent}%): area={blob_area:.0f}px²')
                msg = ''
                #msg = f'<!-- Blob for {lang} ({percent}%) -->\n'
                blob_morph = f'{msg}<animate attributeName="d" dur="{morph_dur}s" repeatCount="indefinite"\n\t\t\tvalues="{shapes}"/>'
                blob_drift = f'<animateTransform attributeName="transform" dur="{drift_dur}s" repeatCount="indefinite" type="translate"\n\t\t\tvalues="{locations}" />'
                blob = f'\t<path fill="{color}" filter="url(#blobBlur)">\n\t\t{blob_morph}\n\t\t{blob_drift}\n\t</path>'
                
                svg_parts.append(blob)
        
            _percent -= percent

        svg_parts.append(foot)
        return '\n'.join(svg_parts)

if __name__ == "__main__":
    l_info = (
        {
            'Python': 49.34090654349339,
            'TypeScript': 16.59815500752021,
            'C': 13.065351520854568,
            'Java': 12.917293350676298,
            'R': 5.501351552134462,
            'Shell': 1.5991846374008492,
            'PowerShell': 0.5995313229049639,
            'CSS': 0.20853263405390046,
            'JavaScript': 0.1332002200019289,
            'CMake': 0.029715900352680815,
            'Batchfile': 0.006777310606751766
            }, 6)
    
    dimensions = (500, 800)
    svg = Background(l_info, dimensions, False).apple()

    filename = f"img/test/apple.svg"
    
    with open(filename, "w", encoding='utf-8') as f: f.write(svg)