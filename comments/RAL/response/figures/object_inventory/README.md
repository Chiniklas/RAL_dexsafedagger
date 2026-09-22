# Provisional 22-object selection

This is a visually identified candidate set from the asset library. The first six entries are the objects reported in the main paper. Yellow panels in the [master contact sheet](selected_objects_contact_sheet.png) mark those six objects.

The explicit-name assets are straightforward to identify. Several paper objects are stored under opaque asset IDs, so the mappings marked **medium** should be visually checked before they are used as final paper labels.

| # | Object name | Asset ID | Status | Confidence | Three-view snapshot |
|---:|---|---|---|---|---|
| 1 | WindCart | `1m0lvpzs` | Main paper, seen | Medium | [PNG](selected/01_windcart_1m0lvpzs.png) |
| 2 | Boot | `2kp2e9k7` | Main paper, seen | High | [PNG](selected/02_boot_2kp2e9k7.png) |
| 3 | ToolBox | `2oiqpnts` | Main paper, seen | High | [PNG](selected/03_toolbox_2oiqpnts.png) |
| 4 | Cow | `z73ltdbb` | Main paper, seen | Medium | [PNG](selected/04_cow_z73ltdbb.png) |
| 5 | Plane | `1nbuaiv2` | Main paper, OOD | High | [PNG](selected/05_plane_1nbuaiv2.png) |
| 6 | Shoe | `1wdf56lx` | Main paper, OOD | Medium | [PNG](selected/06_shoe_1wdf56lx.png) |
| 7 | Horse | `horse` | Additional candidate | High | [PNG](selected/07_horse_horse.png) |
| 8 | Teapot | `teapot` | Additional candidate | High | [PNG](selected/08_teapot_teapot.png) |
| 9 | Sphinx | `sphinx` | Additional candidate | High | [PNG](selected/09_sphinx_sphinx.png) |
| 10 | Dragon | `xyzrgb_dragon` | Additional candidate | High | [PNG](selected/10_dragon_xyzrgb_dragon.png) |
| 11 | Homer bust | `homer` | Additional candidate | High | [PNG](selected/11_homer_bust_homer.png) |
| 12 | Ogre | `ogre` | Additional candidate | High | [PNG](selected/12_ogre_ogre.png) |
| 13 | Cheburashka | `cheburashka` | Additional candidate | High | [PNG](selected/13_cheburashka_cheburashka.png) |
| 14 | Lucy statue | `lucy` | Additional candidate | High | [PNG](selected/14_lucy_statue_lucy.png) |
| 15 | Beethoven bust | `beeth` | Additional candidate | High | [PNG](selected/15_beethoven_bust_beeth.png) |
| 16 | Igea bust | `igea` | Additional candidate | High | [PNG](selected/16_igea_bust_igea.png) |
| 17 | Dog pair | `Hundepaar` | Additional candidate | High | [PNG](selected/17_dog_pair_Hundepaar.png) |
| 18 | Spot dog | `spot` | Additional candidate | Medium | [PNG](selected/18_spot_dog_spot.png) |
| 19 | Monkey head | `suzanne` | Additional candidate | High | [PNG](selected/19_suzanne_monkey_head_suzanne.png) |
| 20 | Blub character | `blub_triangulated` | Additional candidate | Medium | [PNG](selected/20_blub_character_blub_triangulated.png) |
| 21 | Statue | `happy` | Additional candidate | Medium | [PNG](selected/21_happy_character_happy.png) |
| 22 | Dinosaur | `lh0nc4xq` | Additional candidate | Medium | [PNG](selected/22_dinosaur_lh0nc4xq.png) |

The [TSV manifest](selected_objects.tsv) contains the same information in machine-readable form. The six files in [`contact_sheets/`](contact_sheets/) cover the complete subset of the asset library for which renderable point clouds were found. These images are geometry-verification renders from the stored 1,000-point point clouds, rather than camera captures from Isaac Sim.
