# Claude

<iframe width="700" height="500" src="https://www.youtube.com/embed/F4HdBTVKRWg" title="Claude v0.0.0 Live-Coding Demo" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

[Claude](https://github.com/mugulmd/Claude/) is a tool for synchronizing visuals with audio in a live-coding context.

It comes as a Sardine extension, and allows you to control an OpenGL shader from Sardine.

```python
@swim
def arpy(p=.25, i=0):
    build_up = '[1:100,.2]'
    D('(neu arpy:rand*20 2|5 8)', i=i,
        lpf=f'100+{build_up}*50',
        room=1, size=f'.5+{build_up}*(.4/100)'
    )
    again(arpy, p=.25, i=i+1)

@swim
def stomp(p=.5, i=0):
    D('(eu stomp:(6|4|1) 5 8)', i=i)
    Claude('cellsize', '.3 .2 .1 .', i=i, d=4)
    D('. stomp:3', i=i, d=4, speed='[1 .5]!!2')
    Claude('noiseamp', '0 0 .02 0', i=i, d=2)
    again(stomp, p=.5, i=i+1)

@swim
def slowmvt(p=2, i=0):
    Claude('mvt', ['.1 (-.1) 0', '0 rand*.2'], i=i)
    Claude('gap', '2 3|4', dt='i', i=i, d=3)
    again(slowmvt, p=2, i=i+1)
```

```
#version 330

uniform vec2 resolution;
uniform float time;

uniform float cellsize = .5;
uniform float pixsize = .01;
uniform float noiseamp = .0;
uniform int gap = 2;
uniform vec2 mvt = vec2(0.1, 0.0);

out vec3 frag_color;

float noise(float x) {
    return fract(sin(x) * 43758.5453123);
}

ivec2 pixelate(vec2 uv, float size) {
    return ivec2(floor(uv / size));
}

vec2 cell_point(ivec2 cell) {
    float rand = noise(dot(cell, ivec2(12, 45)));
    float phase = rand * 100;
    float speed = 1 + rand;
    float angle = speed * time + phase;
    return (vec2(cos(angle), sin(angle)) + 1.0) * .5;
}

void main() {
    // Retrieve, normalize and unsqueeze fragment coordinates
    vec2 uv = gl_FragCoord.xy / resolution;
    uv = 2.0 * uv - 1.0;
    uv.x *= resolution.x / resolution.y;

    uv += mvt * time;

    ivec2 pix = pixelate(uv, pixsize);
    uv = pix * pixsize;
    float disp = 2*noise(pix.y) - 1;
    uv += disp * noiseamp;

    ivec2 coords = pixelate(uv, cellsize);

    // Compute Voronoi cell
    float dist_min = 1000.;
    ivec2 cell_min = coords;
    for (int dx = -1; dx <= 1; dx++) {
        for (int dy = -1; dy <= 1; dy++) {
            ivec2 cell = coords + ivec2(dx, dy);
            vec2 pos = (cell_point(cell) + vec2(cell)) * cellsize;
            float dist = distance(uv, pos);
            if (dist < dist_min) {
                dist_min = dist;
                cell_min = cell;
            }
        }
    }

    // Output color based on cell coordinates
    if (cell_min.x % gap == 0) {
        frag_color = vec3(1.0, 0.7, 0.9);
    } else {
        frag_color = vec3(0.0, 0.4, 0.6);
    }
}
```
