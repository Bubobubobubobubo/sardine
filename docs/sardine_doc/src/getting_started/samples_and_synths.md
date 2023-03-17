# Synths and samples

The sounds from **Sardine** are generated from the **SuperDirt** audio engine,
which runs in [SuperColider](https://supercollider.github.io/). **SuperDirt** 
comes with a standard sample set and a group of synthesizers. **SuperDirt** 
receives information about audio samples and synthesizers from a string (`'bd`,
`'cp'`, `'tech:2'`).

**SuperDirt** default samples:

    (Numbers show how many samples in each bank.)
    808 (6) 808bd (25) 808cy (25) 808hc (5) 808ht (5) 808lc (5) 808lt (5) 808mc (5)
    808mt (5) 808oh (5) 808sd (25) 909 (1) ab (12) ade (10) ades2 (9) ades3 (7)
    ades4 (6) alex (2) alphabet (26) amencutup (32) armora (7) arp (2) arpy (11)
    auto (11) baa (7) baa2 (7) bass (4) bass0 (3) bass1 (30) bass2 (5) bass3 (11)
    bassdm (24) bassfoo (3) battles (2) bd (24) bend (4) bev (2) bin (2) birds (10)
    birds3 (19) bleep (13) blip (2) blue (2) bottle (13) breaks125 (2) breaks152 (1)
    breaks157 (1) breaks165 (1) breath (1) bubble (8) can (14) casio (3) cb (1) cc (6)
    chin (4) circus (3) clak (2) click (4) clubkick (5) co (4) coins (1) control (2)
    cosmicg (15) cp (2) cr (6) crow (4) d (4) db (13) diphone (38) diphone2 (12) 
    dist (16) dork2 (4) dorkbot (2) dr (42) dr2 (6) dr55 (4) dr_few (8) drum (6)
    drumtraks (13) e (8) east (9) electro1 (13) em2 (6) erk (1) f (1) feel (7)
    feelfx (8) fest (1) fire (1) flick (17) fm (17) foo (27) future (17) gab (10)
    gabba (4) gabbaloud (4) gabbalouder (4) glasstap (3) glitch (8) glitch2 (8)
    gretsch (24) gtr (3) h (7) hand (17) hardcore (12) hardkick (6) haw (6) hc (6)
    hh (13) hh27 (13) hit (6) hmm (1) ho (6) hoover (6) house (8) ht (16) if (5)
    ifdrums (3) incoming (8) industrial (32) insect (3) invaders (18) jazz (8)
    jungbass (20) jungle (13) juno (12) jvbass (13) kicklinn (1) koy (2) kurt (7)
    latibro (8) led (1) less (4) lighter (33) linnhats (6) lt (16) made (7) made2 (1) 
    mash (2) mash2 (4) metal (10) miniyeah (4) monsterb (6) moog (7) mouth (15) 
    mp3 (4) msg (9) mt (16) mute (28) newnotes (15) noise (1) noise2 (8) notes (15)
    numbers (9) oc (4) odx (15) off (1) outdoor (6) pad (3) padlong (1) pebbles (1)
    perc (6) peri (15) pluck (17) popkick (10) print (11) proc (2) procshort (8)
    psr (30) rave (8) rave2 (4) ravemono (2) realclaps (4) reverbkick (1)
    rm (2) rs (1) sax (22) sd (2) seawolf (3) sequential (8) sf (18) sheffield (1)
    short (5) sid (12) sine (6) sitar (8) sn (52) space (18) speakspell (12)
    speech (7) speechless (10) speedupdown (9) stab (23) stomp (10) subroc3d (11)
    sugar (2) sundance (6) tabla (26) tabla2 (46) tablex (3) tacscan (22) tech (13)
    techno (7) tink (5) tok (4) toys (13) trump (11) ul (10) ulgab (5) uxay (3)
    v (6) voodoo (5) wind (10) wobble (1) world (3) xmas (1) yeah (31)

Each sample bank is a folder with individual sample files. A colon after the name designates the individual sample in that folder. Without a colon, SuperDirt will use the first file (`'bd'` = `'bd:0'`).

```python
Pa >> d('voodoo:0 voodoo:1 voodoo:2')
silence(Pa)
```
This pattern plays the first, second and third sample from the `voodoo` folder. The sample counter starts at **0** and wraps back to **0** when it reaches the last sample number, so higher numbers will work.

The same syntax is used for **SuperDirt** synthesizers:

```python
# Requires sc3_plugins
Pa >> d('supersaw superpiano')
Pb >> d('supersaw superpiano', n='60 62 63 67')
    
silence()
```
**Summary:**

-   You call synthesizers and samples using `"strings"`.
-   You call a specific sample by using the colon syntax  `bd:4`.
-   `"names"` can refer to a synth or a sample.
